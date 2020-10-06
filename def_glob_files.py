import sys
import shutil
import os
from pathlib import Path

# for test(Windows)
ipt = "C:/tmp/ipt"
opt = "C:/tmp/opt"

# for test(Mac)
ipt = ""
opt = ""

# for honnbann
# ipt = sys.argv[1]
# opt = sys.argv[2]

ipt = Path(ipt)

ipt_pdf_path = ipt.glob('**/*.pdf')

# try:
for i in ipt_pdf_path:
    dirname = opt + "/" + i.stem