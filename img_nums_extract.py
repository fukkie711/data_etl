# This is for extracting number of images in each directories(=ident numbers of each patents)
import sys
import glob
import os
from pathlib import Path

# for test
ipt = ""
opt = ""

# ipt = sys.argv[1]
# opt = sys.argv[2]

# for test(Windows)
# ipt = "C:/tmp/ipt"
# opt = "C:/tmp/opt"

# for test(Mac)
ipt = "/Users/k-fukuzawa/Dropbox/tmp/03input"
opt = "/Users/k-fukuzawa/Dropbox/tmp/03output"

# for honnbann
# ipt = sys.argv[1]
# opt = sys.argv[2]

ipt = Path(ipt)
# ipt_path = ipt.glob("**/*.png")
ipt_path = ipt.glob("**")
# ipt_path = glob.iglob(ipt, "**/*.png")

for i in ipt_path:
    print(i.stem)
    os.getcwd()
    files = os.listdir(i)  
    count = len(files)  
    print(count)  
