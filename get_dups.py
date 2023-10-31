import glob
import os
import io
from pathlib import PurePath 

try:
    os.remove('everything.txt')
except OSError:
    pass
dir = "covers"
my_dictionary = {}
for filename in glob.iglob(f"{dir}/*", recursive=False):    
    stem = PurePath(filename).stem
    if stem in my_dictionary:
        print("BOUM!")
        print(stem, filename)
        print(stem, my_dictionary[stem])
    my_dictionary[stem] = filename
print(f"{len(my_dictionary)} images in directory '{dir}'")