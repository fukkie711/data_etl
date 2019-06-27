# this is for extracting parameters from xml tags
#coding:utf-8

import os
import xml.etree.ElementTree as ET

src = "/Users/k-fukuzawa/Dropbox/tmp/input"
fname = "/Users/k-fukuzawa/Dropbox/tmp/output/2017216881.xml"

with open(fname, "r") as file:
    str = file.read()

root = ET.fromstring(str)

child = root[0]
for child in root:
    print(child.tag, child.attrib)
