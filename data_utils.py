from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

# Special vocabulary symbols - we always put them at the start.
_PAD = b"<pad>"
_GO = b"<go>"
_EOS = b"<eos>"
_START_VOCAB = [_PAD, _GO, _EOS]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2

IGNORED_WORDS = ["[noise]", "[laughter]", "[vocalized-noise]", "uh", "um", "eh", "mm", "hm", \
        "ah", "huh", "ha", "er", "oof", "hee", "ach", "eee", "ew"]

def get_relevant_words(char_str):
    char_str = char_str.replace("<sp>", " ")
    words = char_str.split()
    rel_words = []
    for word in words:
        if word in IGNORED_WORDS:
            continue
        elif len(word) > 0 and word[-1] == "-":
            ## Partial word
            continue
        else:
            rel_words.append(word)

    return words, rel_words

def initialize_vocabulary(vocabulary_path):
    """Initialize vocabulary from file.

    We assume the vocabulary is stored one-item-per-line, so a file:
    dog
    cat
    will result in a vocabulary {"dog": 0, "cat": 1}, and this function will
    also return the reversed-vocabulary ["dog", "cat"].

    Args:
    vocabulary_path: path to the file containing the vocabulary.

    Returns:
    a pair: the vocabulary (a dictionary mapping string to integers), and
    the reversed vocabulary (a list, which reverses the vocabulary mapping).

    Raises:
    ValueError: if the provided vocabulary_path does not exist.
    """
    if tf.gfile.Exists(vocabulary_path):
        rev_vocab = []
        with tf.gfile.GFile(vocabulary_path, mode="rb") as f:
            rev_vocab.extend(f.readlines())
            rev_vocab = [line.strip() for line in rev_vocab]
            vocab = dict([(x, y) for (y, x) in enumerate(rev_vocab)])
        return vocab, rev_vocab
    else:
        raise ValueError("Vocabulary file %s not found.", vocabulary_path)
