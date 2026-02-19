import os
import sys
import warnings

from lxml import etree


def validate(xml_path: str, dtd_path: str) -> bool:
    try:
        dtd = etree.DTD(open(dtd_path))
    except etree.DTDParseError as e:
        print(
            "DTD Parse Error : ",
            e.error_log[0].message,
            " at line ",
            e.error_log[0].line,
        )
        return False
    try:
        xml_doc = etree.parse(xml_path)
    except etree.XMLSyntaxError as e:
        print("XML Syntax Error : ", e)
        return False
    result = dtd.validate(xml_doc)
    if not result:
        print(dtd.error_log[0])
    return result


def main():
    if len(sys.argv) != 3:
        print("Usage: %s document.xml schema.dtd" % (sys.argv[0]))
        exit(0)
    xml_path = str((sys.argv[1]))
    dtd_path = str((sys.argv[2]))
    if validate(xml_path, dtd_path):
        print("Valid !")
    else:
        print("Not valid !")


if __name__ == "__main__":
    main()


# python3 validator.py xmldoc.xml dtddoc.dtd
# python3 validator.py xmldoc2.xml dtddoc2.dtd
# python3 validator.py xmldoc3.xml dtddoc2.dtd