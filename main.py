import sys

import click

from xmldtd.utils import validate


@click.group()
def main():
    """
    Main function of the program.
    """


@main.command()
@click.argument("xml_file")
@click.argument("dtd_file")
def validate_xml_dtd(xml_file, dtd_file):
    """
    Validate an XML file against a DTD file.
    """
    if validate(xml_file, dtd_file):
        print("Valid !")
    else:
        print("Not valid !")


if __name__ == "__main__":
    main()
