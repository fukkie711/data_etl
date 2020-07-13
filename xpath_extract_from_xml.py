from lxml import etree
root = etree.XML

src = "/Users/k-fukuzawa/Dropbox/tmp/input"
fname = "/Users/k-fukuzawa/Dropbox/tmp/output/2017216881.xml"

tree = etree.parse(fname)
root = tree.getroot()
print(root.tag)
