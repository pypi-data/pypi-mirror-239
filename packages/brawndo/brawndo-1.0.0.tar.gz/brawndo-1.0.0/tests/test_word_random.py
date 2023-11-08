from brawndo.brawndo import word_random
import pytest

texts = [
    "The be to of and",
    "a in that have I",
    "it for not on with.",
    "The sun sets in the west. Autumn leaves are falling down. Night has come; it's time to rest.",
    "Can you believe she said that?! What on earth is happening here?! Are you kidding me right now?!",
    'Yes, I will be there before noon. The cat, though small, was a fierce hunter. He said, "Wait, I need to tell you something important."',
]
modes = [
    False,
    False,
    False,
    True,
    True,
    True,
]
rndseeds = [
    -4285599787418930330,
    -1711087449568291972,
    -8519561080946256753,
    1149577398128511356,
    6494851809922682231,
    -6732001643952364904,
]
desireds = [
    "The,white\nbe,cyan\nto,dark_grey\nof,magenta\nand,magenta\n",
    "a,green\nin,light_green\nthat,red\nhave,light_red\nI,blue\n",
    "it,light_cyan\nfor,light_blue\nnot,dark_grey\non,light_cyan\nwith.,light_green\n",
    "The sun sets in the west.,magenta\nAutumn leaves are falling down.,magenta\nNight has come; it's time to rest.,red\n",
    "Can you believe she said that?!,light_magenta\nWhat on earth is happening here?!,yellow\nAre you kidding me right now?,blue\n!,light_blue\n",
    "Yes, I will be there before noon.,light_cyan\nThe cat, though small, was a fierce hunter.,black\nHe said, \"Wait, I need to tell you something important.\",dark_grey\n",
]

# Zip all together
params = zip(texts, modes, rndseeds, desireds)


@pytest.mark.parametrize("text,mode,rndseed,desired", params)
def test_word_random(text, mode, rndseed, desired):
    test_vector = word_random(text, mode, rndseed, testing=True)
    assert test_vector == desired
