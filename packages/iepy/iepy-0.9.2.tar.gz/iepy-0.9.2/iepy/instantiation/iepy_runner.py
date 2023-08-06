"""
Run IEPY active-learning extractor

Usage:
    iepy_runner.py [options] <relation_name>
    iepy_runner.py -h | --help | --version

Options:
  --classifier=<classifier_path>     Load an already trained classifier
  --no-questions                     Won't generate questions to answer and will try to predict as is. Should be used with --classifier
  -h --help                          Show this screen
  --tune-for=<tune-for>              Predictions tuning. Options are high-prec or high-recall [default: high-prec]
  --extractor-config=<config.json>   Sets the extractor config
  --version                          Version number
"""

import os
import json
import logging
from docopt import docopt
from sys import exit

import iepy
INSTANCE_PATH = iepy.setup(__file__)

from iepy.extraction.active_learning_core import ActiveLearningCore, HIPREC, HIREC
from iepy.data.db import CandidateEvidenceManager
from iepy.data.models import Relation
from iepy.extraction.terminal import TerminalAdministration
from iepy.data import output


def print_all_relations():
    print("All available relations:")
    for relation in Relation.objects.all():
        print("  {}".format(relation))


def load_labeled_evidences(relation, evidences):
    CEM = CandidateEvidenceManager  # shorcut
    return CEM.labels_for(relation, evidences, CEM.conflict_resolution_newest_wins)


def run_from_command_line():
    opts = docopt(__doc__, version=iepy.__version__)
    relation = opts['<relation_name>']
    classifier_path = opts.get('--classifier')

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.getLogger("featureforge").setLevel(logging.WARN)

    if opts['--tune-for'] == 'high-prec':
        tuning_mode = HIPREC
    elif opts['--tune-for'] == 'high-recall':
        tuning_mode = HIREC
    else:
        print ('Invalid tuning mode')
        print (__doc__)
        exit(1)

    try:
        relation = Relation.objects.get(name=relation)
    except Relation.DoesNotExist:
        print("Relation {!r} non existent".format(relation))
        print_all_relations()
        exit(1)

    candidates = CandidateEvidenceManager.candidates_for_relation(relation)
    labeled_evidences = load_labeled_evidences(relation, candidates)

    if classifier_path:
        try:
            loaded_classifier = output.load_classifier(classifier_path)
        except ValueError:
            print("Error: unable to load classifier, invalid file")
            exit(1)

        iextractor = ActiveLearningCore(
            relation, labeled_evidences, performance_tradeoff=tuning_mode,
            classifier=loaded_classifier
        )
        was_ever_trained = True
    else:
        config_filepath = opts.get("--extractor-config")
        if not config_filepath:
            config_filepath = os.path.join(INSTANCE_PATH, "extractor_config.json")

        if not os.path.exists(config_filepath):
            print("Error: extractor config does not exists, please create the "
                  "file extractor_config.json or use the --extractor-config")
            exit(1)

        with open(config_filepath) as filehandler:
            try:
                extractor_config = json.load(filehandler)
            except Exception as error:
                print("Error: unable to load extractor config: {}".format(error))
                exit(1)

        iextractor = ActiveLearningCore(
            relation, labeled_evidences, extractor_config,
            performance_tradeoff=tuning_mode
        )
        iextractor.start()
        was_ever_trained = False


    if not opts.get("--no-questions", False):
        questions_loop(iextractor, relation, was_ever_trained)

    # Predict and store output
    predictions = iextractor.predict()
    if predictions:
        output.dump_output_loop(predictions)
        output.dump_classifier_loop(iextractor)


def questions_loop(iextractor, relation, was_ever_trained):
    STOP = u'STOP'
    term = TerminalAdministration(
        relation,
        extra_options=[(STOP, u'Stop execution')]
    )
    while iextractor.questions:
        questions = list(iextractor.questions)  # copying the list
        term.update_candidate_evidences_to_label(questions)
        result = term()
        i = 0
        for c, label_value in load_labeled_evidences(relation, questions).items():
            if label_value is not None:
                iextractor.add_answer(c, label_value)
                i += 1
        print ('Added %s new human labels to the extractor core' % i)
        iextractor.process()
        was_ever_trained = True
        if result == STOP:
            break

    if not was_ever_trained:
        # It's needed to run some process before asking for predictions
        iextractor.process()


if __name__ == u'__main__':
    run_from_command_line()
