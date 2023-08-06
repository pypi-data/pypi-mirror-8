from collections import defaultdict
from itertools import chain, groupby
import logging

from iepy.preprocess import corenlp
from iepy.preprocess.pipeline import BasePreProcessStepRunner, PreProcessSteps
from iepy.preprocess.ner.base import FoundEntity
from iepy.data.models import Entity, EntityOccurrence


logger = logging.getLogger(__name__)


class StanfordPreprocess(BasePreProcessStepRunner):
    def lemmatization_only(self, document):
        """ Run only the lemmatization """

        # Lemmatization was added after the first so we need to support
        # that a document has all the steps done but lemmatization

        analysis = corenlp.get_analizer().analize(document.text)
        sentences = analysis_to_sentences(analysis)
        tokens = get_tokens(sentences)
        if document.tokens != tokens:
            raise ValueError(
                "Document changed since last tokenization, "
                "can't add lemmas to it"
            )

        # Lemmatization
        document.set_lemmatization_result(get_lemmas(sentences))
        document.save()

    def __call__(self, document):
        steps = [
            PreProcessSteps.tokenization,
            PreProcessSteps.sentencer,
            PreProcessSteps.tagging,
            PreProcessSteps.ner,
            PreProcessSteps.lemmatization,
        ]
        if not self.override:
            if all(document.was_preprocess_step_done(step) for step in steps):
                return

            old_steps = steps[:-1]  # all but lemmatization
            old_steps_done = all(document.was_preprocess_step_done(step) for step in old_steps)
            lemmatization_done = document.was_preprocess_step_done(PreProcessSteps.lemmatization)
            if old_steps_done and not lemmatization_done:
                self.lemmatization_only(document)
                return

        if not self.override and document.was_preprocess_step_done(PreProcessSteps.tokenization):
            raise NotImplementedError("Running with mixed preprocess steps not supported, must be 100% StanfordMultiStepRunner")

        analysis = corenlp.get_analizer().analize(document.text)
        sentences = analysis_to_sentences(analysis)

        # Tokenization
        tokens = get_tokens(sentences)
        offsets = get_token_offsets(sentences)
        document.set_tokenization_result(list(zip(offsets, tokens)))

        # Lemmatization
        document.set_lemmatization_result(get_lemmas(sentences))

        # "Sentencing" (splitting in sentences)
        document.set_sentencer_result(get_sentence_boundaries(sentences))

        # POS tagging
        document.set_tagging_result(get_pos(sentences))

        # NER
        xs = [FoundEntity(key="{} {} {} {}".format(document.human_identifier, kind, i, j),
                          kind_name=kind,
                          alias=" ".join(tokens[i:j]),
                          offset=i,
                          offset_end=j)
              for i, j, kind in get_entity_occurrences(sentences)]
        document.set_ner_result(xs)

        # Save progress so far, next step doesn't modify `document`
        document.save()

        # Coreference resolution
        for coref in get_coreferences(analysis):
            try:
                apply_coreferences(document, coref)
            except CoreferenceError as e:
                logger.warning(e)


def _dictpath(d, *args):
    x = d
    for key in args:
        try:
            x = x[key]
        except KeyError:
            return []
    if not isinstance(x, list):
        x = [x]
    return x


def analysis_to_sentences(analysis):
    result = []
    sentences = _dictpath(analysis, "sentences", "sentence")
    for sentence in sentences:
        xs = []
        tokens = _dictpath(sentence, "tokens", "token")
        for t in tokens:
            xs.append(t)
        result.append(xs)
    return result


def get_tokens(sentences):
    return [x["word"] for x in chain.from_iterable(sentences)]


def get_lemmas(sentences):
    return [x["lemma"] for x in chain.from_iterable(sentences)]


def get_token_offsets(sentences):
    return [int(x["CharacterOffsetBegin"]) for x in chain.from_iterable(sentences)]


def get_pos(sentences):
    return [x["POS"] for x in chain.from_iterable(sentences)]


def get_sentence_boundaries(sentences):
    """
    Returns a list with the offsets in tokens where each sentence starts, in
    order. The list contains one extra element at the end containing the total
    number of tokens.
    """
    ys = [0]
    for x in sentences:
        y = ys[-1] + len(x)
        ys.append(y)
    return ys


def get_entity_occurrences(sentences):
    """
    Returns a list of tuples (i, j, kind) such that `i` is the start
    offset of an entity occurrence, `j` is the end offset and `kind` is the
    entity kind of the entity.
    """
    found_entities = []
    offset = 0
    for words in sentences:
        for kind, group in groupby(enumerate(words), key=lambda x: x[1]["NER"]):
            if kind == "O":
                continue
            ix = [i for i, word in group]
            i = ix[0] + offset
            j = ix[-1] + 1 + offset
            found_entities.append((i, j, kind))
        offset += len(words)
    return found_entities


def get_coreferences(analysis):
    """
    Returns a list of lists of tuples (i, j, k) such that `i` is the start
    offset of a reference, `j` is the end offset and `k` is the index of the
    head word within the reference.
    All offsets are in tokens and relative to the start of the document.
    All references within the same list refer to the same entity.
    All references in different lists refer to different entities.
    """
    sentences = analysis_to_sentences(analysis)
    sentence_offsets = get_sentence_boundaries(sentences)
    coreferences = []
    for mention in _dictpath(analysis, "coreference", "coreference"):
        occurrences = []
        representative = 0
        for r, occurrence in enumerate(_dictpath(mention, "mention")):
            if "@representative" in occurrence:
                representative = r
            sentence = int(occurrence["sentence"]) - 1
            offset = sentence_offsets[sentence]
            i = int(occurrence["start"]) - 1 + offset
            j = int(occurrence["end"]) - 1 + offset
            k = int(occurrence["head"]) - 1 + offset
            occurrences.append((i, j, k))
        # Occurrences' representative goes in the first position
        k = representative
        occurrences[0], occurrences[k] = occurrences[0], occurrences[k]
        coreferences.append(occurrences)
    return coreferences


def apply_coreferences(document, coreferences):
    """
    Makes all entity ocurrences named in `coreference` have the same
    entity.
    It uses coreference information to merge entity ocurrence's
    entities into a single entity.
    `correferences` is a list of tuples (i, j, head) where:
     - `i` is the offset in tokens where the occurrence starts.
     - `j` is the offset in tokens where the occurrence ends.
     - `head` is the index in tokens of the head of the occurrence (the "most
        important word").

    Every entity occurrence in `coreference` might already exist or not in
    `document`. If no occurrence exists in `document` then nothing is done.
    If at least one ocurrence exists in `document` then all other ocurrences
    named in `coreference` are automatically created.

    This function can raise CofererenceError in case a merge is attempted on
    entities of different kinds.
    """
    # For each token index make a list of the occurrences there
    occurrences = defaultdict(list)
    for occurrence in document.entity_occurrences.all():
        for i in range(occurrence.offset, occurrence.offset_end):
            occurrences[i].append(occurrence)

    entities = []  # Existing entities referenced by correferences
    missing = []  # References that have no entity occurrence yet
    for i, j, head in coreferences:
        if occurrences[head]:
            entities.extend(x.entity for x in occurrences[head])
        else:
            missing.append((i, j, head))

    if not entities:
        return
    if len(set(e.kind for e in entities)) != 1:
        raise CoreferenceError("Cannot merge entities of different kinds {!r}".format(set(e.kind for e in entities)))

    # Select canonical name for the entity
    i, j, _ = coreferences[0]
    name = " ".join(document.tokens[i:j])
    # Select canonical entity, every occurrence will point to this entity
    try:
        canonical = Entity.objects.get(key=name)
    except Entity.DoesNotExist:
        canonical = entities[0]

    # Each missing coreference needs to be created into an occurrence now
    for i, j, head in missing:
        if j - i >= 5:  # If the entity is a long phrase then just keep one token
            i = head
            j = head + 1
        EntityOccurrence.objects.get_or_create(
            document=document,
            entity=canonical,
            offset=i,
            offset_end=j,
            alias=" ".join(document.tokens[i:j]))

    # Finally, the merging 'per se', where all things are entity ocurrences
    for entity in set(x for x in entities if x != canonical):
        for occurrence in EntityOccurrence.objects.filter(entity=entity):
            occurrence.entity = canonical
            occurrence.save()


class CoreferenceError(Exception):
    pass
