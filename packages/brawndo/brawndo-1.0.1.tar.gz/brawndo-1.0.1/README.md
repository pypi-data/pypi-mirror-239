# Brawndo
[![build](https://github.com/software-students-fall2023/3-python-package-exercise-team-not-sure/actions/workflows/python-app.yml/badge.svg)](https://github.com/software-students-fall2023/3-python-package-exercise-team-not-sure/actions/workflows/python-app.yml)

![It's Got Electrolytes!](https://github.com/software-students-fall2023/3-python-package-exercise-team-not-sure/blob/main/images/cover.png?raw=true)

### Makes your terminal text chaotic. It's got what plants crave!

See on [PyPI](https://pypi.org/project/brawndo/)

## Install
`pip install brawndo`

## Modifying

First, set up the environment:  
`cd .../3-python-package-exercise-team-not-sure`

![](https://github.com/software-students-fall2023/3-python-package-exercise-team-not-sure/blob/main/images/not_sure.jpg?raw=true)

Enter the pipenv:  
`pipenv shell`

Build (in project root):
`python -m build`


Modify `pyproject.toml` to whatever you want.

You can then use `twine upload dist/*` to upload to PyPI.

## Functions

Import with `from brawndo.brawndo import *`.

`rainbow_deterministic(text: str, shift: int, testing=False) -> Optional[str]`

- Prints out colors for each character in your `text`, making the same characters the same color.
- When run with the same `shift`, it stays the same each time! Change it to preference.
- Specify `testing=True` to get an additional output string (for testing).

`word_deterministic(text: str, shift: int, testing=False) -> Optional[str]`

- Prints out colors for each word in your `text`, making the same words the same color.
- When run with the same `shift`, it stays the same each time! Change it to preference.
- Specify `testing=True` to get an additional output string (for testing).

`rainbow_random(text: str, rndseed=None, testing=False) -> Optional[str]`

- By default, randomizes colors for each character.
- You can get a reproducible color order if you specify the same random seed!
- Specify `testing=True` to get an additional output string (for testing).

`def word_random(text: str, operate_on_sentences: bool, rndseed=None, testing=False) -> None`

- By default, randomizes color for each word (or entire sentence, if you specify `operate_on_sentences=True`).
- You can get a reproducible color order if you specify the same random seed!
- Specify `testing=True` to get an additional output string (for testing).

## Team Members

[Michael Lin \<mal9608@nyu.edu\>](https://github.com/freerainboxbox)

[Seolin Jung \<sj3182@nyu.edu\>](https://github.com/seolinjung)

[Marwan AbdElhameed \<mwa7459@nyu.edu\>](https://github.com/MarwanWalid2)

[Pavly Halim \<poh2005@nyu.edu\>](https://github.com/pavlyhalim)