import argparse
from xml.dom.minidom import parse


def getId(xml_file):
    dom = parse(xml_file)
    print(dom.hasChildNodes())

    for n in dom.getElementsByTagName("address"):
        if n.hasAttribute("name"):
            print(n.getAttribute("id"))


def getPhone(xml_file):
    dom = parse(xml_file)

    tag_name = "phone"
    if dom.getElementsByTagName(tag_name):
        for n in dom.getElementsByTagName(tag_name):
            print(n.firstChild.data)
    else:
        print(f"No {tag_name} element found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml", type=str, help="Path to the XML file")
    args = parser.parse_args()

    print("IDs:")
    getId(args.xml)

    print("\n")

    print("Phone numbers:")
    getPhone(args.xml)
