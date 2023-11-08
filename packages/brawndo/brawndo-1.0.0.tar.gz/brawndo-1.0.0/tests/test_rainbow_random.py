from brawndo.brawndo import rainbow_random
import pytest

texts = [
    "The quick brown fox jumps over the lazy dog.",
    "'as..[poavesf[  8a7*.f\"]",
    "!@#$%^&*()-=_+",
]
rndseeds = [
    4292285838037326215,
    6551146165133617474,
    -5650950641291792112
]

desireds = [
    "T,black\nh,light_yellow\ne,light_magenta\n ,white\nq,cyan\nu,light_red\ni,light_blue\nc,light_grey\nk,light_cyan\n ,black\nb,light_grey\nr,light_magenta\no,yellow\nw,cyan\nn,light_green\n ,light_grey\nf,light_magenta\no,yellow\nx,light_blue\n ,green\nj,cyan\nu,white\nm,green\np,light_grey\ns,light_cyan\n ,green\no,blue\nv,white\ne,light_cyan\nr,light_blue\n ,light_magenta\nt,yellow\nh,magenta\ne,dark_grey\n ,light_cyan\nl,light_grey\na,light_magenta\nz,blue\ny,black\n ,green\nd,red\no,light_grey\ng,black\n.,light_blue\n",
    "',black\na,black\ns,light_cyan\n.,light_yellow\n.,light_blue\n[,dark_grey\np,black\no,light_yellow\na,green\nv,light_yellow\ne,magenta\ns,black\nf,green\n[,light_blue\n ,light_yellow\n ,blue\n8,dark_grey\na,light_red\n7,cyan\n*,cyan\n.,magenta\nf,light_green\n\",light_green\n],yellow\n",
    "!,light_red\n@,light_blue\n#,light_blue\n$,yellow\n%,black\n^,light_blue\n&,light_green\n*,yellow\n(,green\n),light_grey\n-,yellow\n=,light_grey\n_,light_magenta\n+,light_grey\n",
]

# Zip all together
params = zip(texts, rndseeds, desireds)


@pytest.mark.parametrize("text,rndseed,desired", params)
def test_rainbow_random(text, rndseed, desired):
    test_vector = rainbow_random(text, rndseed, testing=True)
    assert test_vector == desired
