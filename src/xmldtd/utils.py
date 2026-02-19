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
