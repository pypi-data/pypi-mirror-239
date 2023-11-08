from brawndo.brawndo import word_deterministic
import pytest

texts = [
    "The be to of and",
    "a in that have I",
    "it for not on with.",
]
shifts = [0, 1, 2]
desireds = [
    "The,light_magenta\nbe,magenta\nto,red\nof,yellow\nand,black\n",
    "a,red\nin,cyan\nthat,light_magenta\nhave,red\nI,dark_grey\n",
    "it,light_blue\nfor,cyan\nnot,black\non,light_blue\nwith.,white\n",
]

# Zip all together
params = zip(texts, shifts, desireds)


@pytest.mark.parametrize("text,shift,desired", params)
def test_word_deterministic(text, shift, desired):
    test_vector = word_deterministic(text, shift, testing=True)
    assert test_vector == desired
