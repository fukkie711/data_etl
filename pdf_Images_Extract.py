# pip install PyMuPDF
import fitz
import sys
import shutil
import os
from pathlib import Path
import logging

ipt = ""
opt = ""

# for test
# ipt = "C:/tmp/pdf_images_extract/ipt"
# opt = "C:/tmp/pdf_images_extract/opt"

ipt = sys.argv[1]
opt = sys.argv[2]

p = Path(ipt)
pdf_path = p.glob('**/*.pdf')

# try:
for i in pdf_path:
    dirname = opt + "/" + i.stem
    # 2020-0514 added "if" for avoiding existing dirs and files
    if not os.path.exists(dirname):
        print(dirname)
        os.mkdir(dirname)
        doc = fitz.open(i)
        os.chdir(dirname)
        for j in range(len(doc)):
            for img in doc.getPageImageList(j):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG("p%s-%s.png" % (j, xref))
                    print("   p%s-%s.png" % (j, xref))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG("p%s-%s.png" % (j, xref))
                    print("   p%s-%s.png" % (j, xref))
                    pix1 = None
                pix = None
# except:
#     import traceback
#     traceback.print_exc()
#     fh = logging.FileHandler('c:/logs/loggingtest.log') #ファイル名を設定
#     logger.addHandler(fh)
#     sh = logging.StreamHandler()
#     logger.addHandler(sh)


    # f.write(e.args)
    # f.close
    # pass
    # raise
