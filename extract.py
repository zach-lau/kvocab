"""
This file contains functions to extract words and frequencies from subtitle xml files
"""

import xml.etree.ElementTree as ET

if __name__ == '__main__':
    filename = "./data/rhghr10.xml"
    tree = ET.parse(filename)
    root = tree.getroot()
    # TODO add namespaces
    ns = '{http://www.w3.org/ns/ttml}'
    for p in root.find(ns+'body').find(ns+'div').findall(ns+'p'):
        print(p.text)
