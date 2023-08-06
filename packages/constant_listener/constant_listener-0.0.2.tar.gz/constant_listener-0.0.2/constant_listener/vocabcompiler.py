import os
import sys

import g2p


def text2lm(in_filename, out_filename):
    """Wrapper around the language model compilation tools"""
    def text2idngram(in_filename, out_filename):
        cmd = "text2idngram -vocab %s < %s -idngram temp.idngram" % (out_filename,
                                                                     in_filename)
        os.system(cmd)

    def idngram2lm(in_filename, out_filename):
        cmd = "idngram2lm -idngram temp.idngram -vocab %s -arpa %s" % (
            in_filename, out_filename)
        os.system(cmd)

    text2idngram(in_filename, in_filename)
    idngram2lm(in_filename, out_filename)


def compile(sentences, dictionary, languagemodel, words):

    # create the dictionary
    pronounced = g2p.translateWords(words)
    zipped = zip(words, pronounced)
    lines = ["%s %s" % (x, y) for x, y in zipped]

    with open(dictionary, "w") as f:
        f.write("\n".join(lines) + "\n")

    # create the language model
    with open(sentences, "w") as f:
        f.write("\n".join(words) + "\n")
        f.write("<s> \n </s> \n")
        f.close()

    # make language model
    text2lm(sentences, languagemodel)
