"""
This file contains functions to extract words and frequencies from subtitle xml files
"""

import xml.etree.ElementTree as ET
import webvtt

def extract_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    # TODO add namespaces
    ns = {'':'http://www.w3.org/ns/ttml'}
    for p in root.find('body',ns).find('div',ns).findall('p',ns):
        yield p.text

def extract_vtt(filename):
    for caption in webvtt.read(filename):
        yield caption.text

if __name__ == '__main__':
    filename = "./data/rhghr10.xml"
    for x in extract_xml(filename):
        print("Got " + x)
