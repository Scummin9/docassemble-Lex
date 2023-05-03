import sys
from multiprocessing import Pool
from .gvision import confuto_terminum
if __name__ == '__main__':
    pages = list(sys.argv[1:])
    ins = pages[::2]
    outs = pages[1::2]
    with Pool() as p:
      tfiles = list(p.starmap(confuto_terminum, zip(ins, outs)))