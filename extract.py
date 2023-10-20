"""
This file contains functions to extract words and frequencies from subtitle xml files
"""

import os.path
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

def extract(filename):
    """ Wrapper to detect file extension and extract """
    _, ext = os.path.splitext(filename)
    if ext == ".xml":
        yield from extract_xml(filename)
    elif ext == ".vtt":
        yield from extract_vtt(filename)
    else:
        raise Exception("Invalid file extension")

if __name__ == '__main__':
    filename = "./data/rhghr10.xml"
    for x in extract_xml(filename):
        print("Got " + x)
