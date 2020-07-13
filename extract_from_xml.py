# this is for extracting parameters from xml tags
#coding:utf-8

import os
import xml.etree.ElementTree as ET
import lxml import etree

src = "/Users/k-fukuzawa/Dropbox/tmp/input"

fname = "/Users/k-fukuzawa/Dropbox/tmp/output/2017216881.xml"

with open(fname, "r") as file:
    str = file.read()

root = ET.fromstring(str)

print("---------------")
for child in root:
    print(child.tag, child.attrib)
print("---------------")
for child in root.findall('.//publication-reference/document-id/country'):
    print(child.text)
print("---------------")
child_country = root.findtext('.//publication-reference/document-id/country')
print(child_country)
child_applicant1_num = root.findtext('.//parties/jp:applicants-agents-article/jp:applicants-agents[@sequence="1"]/applicant[@sequence="1"]/addressbook[@lang="ja"]/registered-number', namespaces={'jp':'http://www.jpo.go.jp'})
print(child_applicant1_num)
child1 = root.findtext('.//technical-field/p[@num="0001"]')
print(child1)
child2 = root.findtext('.//background-art/p[@num="0002"]')
print(child2)
#child3 = root.findtext('.//patent-literature/p[@num="0003"]/patcit/text')
#child3 = root.findtext('*//patent-literature/p[@num="0003"]/patcit/text')
child3 = root.findtext('*//patent-literature/p[@num="0003"]/patcit')
print(child3)

parser = ET.XMLPullParser()


child5 = root.findtext('.//tech-solution/p[@num="0005"]')
#print(child5)
child6 = root.findtext('.//tech-solution/p[@num="0006"]')
#print(child6)
