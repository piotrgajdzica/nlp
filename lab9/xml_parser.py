import xml.etree.ElementTree as ET



def tokens(file):
    ET.parse('2000_696.txt.ccl')
    tree = ET.parse('2000_696.txt.ccl')
    root = tree.getroot()
    root.tag
    for child in root:
        print(child)


if __name__ == '__main__':
    pass