from brawndo.brawndo import rainbow_deterministic
import pytest

texts = [
    "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
    "The quick brown fox jumps over the lazy dog.",
    "The five boxing wizards jump quickly.",
]
shifts = [0, 1, 2]
desireds = [
    "!,black\n\",red\n#,green\n$,yellow\n%,blue\n&,magenta\n',cyan\n(,white\n),light_grey\n*,dark_grey\n+,light_red\n,,light_green\n-,light_yellow\n.,light_blue\n/,light_magenta\n0,light_cyan\n1,black\n2,red\n3,green\n4,yellow\n5,blue\n6,magenta\n7,cyan\n8,white\n9,light_grey\n:,dark_grey\n;,light_red\n<,light_green\n=,light_yellow\n>,light_blue\n?,light_magenta\n@,light_cyan\nA,black\nB,red\nC,green\nD,yellow\nE,blue\nF,magenta\nG,cyan\nH,white\nI,light_grey\nJ,dark_grey\nK,light_red\nL,light_green\nM,light_yellow\nN,light_blue\nO,light_magenta\nP,light_cyan\nQ,black\nR,red\nS,green\nT,yellow\nU,blue\nV,magenta\nW,cyan\nX,white\nY,light_grey\nZ,dark_grey\n[,light_red\n\\,light_green\n],light_yellow\n^,light_blue\n_,light_magenta\n`,light_cyan\na,black\nb,red\nc,green\nd,yellow\ne,blue\nf,magenta\ng,cyan\nh,white\ni,light_grey\nj,dark_grey\nk,light_red\nl,light_green\nm,light_yellow\nn,light_blue\no,light_magenta\np,light_cyan\nq,black\nr,red\ns,green\nt,yellow\nu,blue\nv,magenta\nw,cyan\nx,white\ny,light_grey\nz,dark_grey\n{,light_red\n|,light_green\n},light_yellow\n~,light_blue\n",
    "T,blue\nh,light_grey\ne,magenta\n ,none\nq,red\nu,magenta\ni,dark_grey\nc,yellow\nk,light_green\n ,none\nb,green\nr,green\no,light_cyan\nw,white\nn,light_magenta\n ,none\nf,cyan\no,light_cyan\nx,light_grey\n ,none\nj,light_red\nu,magenta\nm,light_blue\np,black\ns,yellow\n ,none\no,light_cyan\nv,cyan\ne,magenta\nr,green\n ,none\nt,blue\nh,light_grey\ne,magenta\n ,none\nl,light_yellow\na,red\nz,light_red\ny,dark_grey\n ,none\nd,blue\no,light_cyan\ng,white\n.,light_magenta\n",
    "T,magenta\nh,dark_grey\ne,cyan\n ,none\nf,white\ni,light_red\nv,white\ne,cyan\n ,none\nb,yellow\no,black\nx,dark_grey\ni,light_red\nn,light_cyan\ng,light_grey\n ,none\nw,light_grey\ni,light_red\nz,light_green\na,green\nr,yellow\nd,magenta\ns,blue\n ,none\nj,light_green\nu,cyan\nm,light_magenta\np,red\n ,none\nq,green\nu,cyan\ni,light_red\nc,blue\nk,light_yellow\nl,light_blue\ny,light_red\n.,light_cyan\n",
]

# Zip all together
params = zip(texts, shifts, desireds)


@pytest.mark.parametrize("text,shift,desired", params)
def test_rainbow_deterministic(text, shift, desired):
    test_vector = rainbow_deterministic(text, shift, testing=True)
    assert test_vector == desired
