import subprocess
import xmltodict
import os
import sys
import logging
import stat

from iepy.utils import DIRS, unzip_from_url


logger = logging.getLogger(__name__)
_FOLDER = "stanford-corenlp-full-2014-08-27"
DOWNLOAD_URL = "http://nlp.stanford.edu/software/" + _FOLDER + ".zip"
COMMAND_PATH = os.path.join(DIRS.user_data_dir, _FOLDER, "corenlp.sh")


def get_analizer(_singleton=[]):
    # intentionally using a mutable default, so it's loaded only once
    if not _singleton:
        logger.info("Loading StanfordCoreNLP...")
        _singleton.append(StanfordCoreNLP())
    return _singleton[0]


class StanfordCoreNLP:
    CORENLP_CMD = "-outputFormat xml -threads 4"
    PROMPT = b"\nNLP> "

    def __init__(self, tokenize_with_whitespace=False):
        cmd = self.CORENLP_CMD
        if tokenize_with_whitespace:
            cmd += " -tokenize.whitespace=true"
        self.corenlp_cmd = [COMMAND_PATH] + cmd.split()
        self.proc = subprocess.Popen(
            self.corenlp_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self.output = self.iter_output_segments()
        self.receive()  # Wait until the prompt is ready

    def iter_output_segments(self):
        while True:
            buf = b""
            while self.PROMPT not in buf:
                buf += self.proc.stdout.read1(1024)

                if self.proc.poll() == 1:
                    logger.error("Error running '{}'".format(" ".join(self.corenlp_cmd)))
                    logger.error("Output was: '{}'".format(buf))
                    sys.exit(1)

            segment, _, buf = buf.partition(self.PROMPT)
            yield segment.decode("utf8")

    def receive(self):
        return next(self.output)

    def send(self, data):
        data = data.replace("\n", " ") + "\n"
        self.proc.stdin.write(data.encode("utf8"))
        self.proc.stdin.flush()

    def analize(self, text):
        self.send(text)
        text = self.receive()
        i = text.index("<?xml version")
        text = text[i:]
        return xmltodict.parse(text)["root"]["document"]


def download():
    base = os.path.dirname(COMMAND_PATH)
    if os.path.isfile(COMMAND_PATH):
        print("Stanford CoreNLP is already downloaded at {}.".format(base))
        return
    print("Downloading Stanford CoreNLP...")

    unzip_from_url(DOWNLOAD_URL, DIRS.user_data_dir)

    for directory in os.listdir(DIRS.user_data_dir):
        if directory.startswith("stanford-corenlp-full"):
            stanford_directory = os.path.join(DIRS.user_data_dir, directory)
            if os.path.isdir(stanford_directory):
                corenlp = os.path.join(stanford_directory, "corenlp.sh")
                st = os.stat(corenlp)
                os.chmod(corenlp, st.st_mode | stat.S_IEXEC)
                break
