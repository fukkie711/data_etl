# pip install PyMuPDF
import fitz
import sys
import shutil
import os
from pathlib import Path
import logging
import datetime

ipt = ""
opt = ""
logdir = "/Users/k-fukuzawa/Dropbox/tmp/log/"

dt_now = datetime.datetime.now()

# for test (Windows)
# ipt = "C:/tmp/pdf_images_extract/ipt"
# opt = "C:/tmp/pdf_images_extract/opt"

# for test (Mac)
ipt = "/Users/k-fukuzawa/Dropbox/tmp/02input"
opt = "/Users/k-fukuzawa/Dropbox/tmp/02output"

# determine input directory, output directory, logfile directory (option) from command line arguments
# ipt = sys.argv[1]
# opt = sys.argv[2]
# logdfile = sys.argv[3] + "test.log"
logdir = logdir + "test.log"

# ログの出力名を設定
logger = logging.getLogger(__name__)
logger.setLevel(10)

# ログの出力形式の設定
fmt = "%(asctime)s %(levelname)s %(name)s %(pathname)s :%(message)s"
# fmt = "%(asctime)s %(levelname)s %(name)s %(pathname)s"
logging.basicConfig(filename=logdir, format=fmt)

# # ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)

# ログのファイル出力先を設定
fh = logging.FileHandler(logdir)
logger.addHandler(fh)

p = Path(ipt)
pdf_path = p.glob('**/*.pdf')

try:
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
except (RuntimeError) as e:
    logger.exception('RuntimeError: %s %s', e, dt_now)
else:
    # logger.log(10, 'Done')
    # logger.info('Done %s', dt_now)
    logger.info('Done')
    # logger.info()
    # print('Done (No error).')
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