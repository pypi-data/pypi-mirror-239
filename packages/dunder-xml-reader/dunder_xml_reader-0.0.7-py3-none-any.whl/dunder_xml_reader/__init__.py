"""
Python object representations of XML trees.

This package provides a number of classes and functions for easily parsing and
reading XML documents.

Example usage:

    >>> import dunder_xml_reader
    >>> with open('order_cxml.xml') as infile:
    ...     raw_text = infile.read()
    >>> xml_doc = dunder_xml_reader.parse_xml(raw_text)
    >>> print(xml_doc.Header.From.Credential[0].text())
    05062019
    >>>

This package also includes a SafeReference class that makes writing code that
checks for missing nodes in an XML tree less tedious.

    >>> import dunder_xml_reader
    >>> with open('order_cxml.xml') as infile:
    ...     raw_text = infile.read()
    >>> xml_doc = dunder_xml_reader.parse_xml(raw_text)
    >>> print(xml_doc.Header.MissingNode.Credential[0].text())
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "./dunder_xml_reader/xml_node.py", line 56, in __getattr__
        raise AttributeError(f"'{self.node.tag}' object has no attribute '{attribute}'")
    AttributeError: 'Header' object has no attribute 'MissingNode'
    >>>
    >>> safe_order = xml_doc.safe_reference(xml_doc, 'n/a')
    >>> print(safe_order.Header.MissingNode.Credential[0].text())
    n/a
    >>>

"""
import re
import xml.etree.ElementTree

from dunder_xml_reader.safe_reference import SafeReference
from dunder_xml_reader.xml_node import XmlNode


def parse_xml(raw_text: str, namespaces=None) -> XmlNode:
    """
    Parse raw_text as XML and return a XmlNode instance of the root.
    :param raw_text: string holding valid XML
    :param namespaces: dict of namespaces
    :return: XmlNode instance pointing to root of XML
    """
    node = xml.etree.ElementTree.fromstring(raw_text)

    return XmlNode(node=node, parent_node=None, raw_text=raw_text, namespaces=namespaces)


def safe_reference(object, default='', wrap_methods=True) -> SafeReference:
    """
    Wrap object graph in a SafeReference instance.
    :param object: The object to wrap
    :param default: What should be returned instead of throwing Exception
    :param wrap_methods: Should calls to methods return a SafeReference or the actual result?
    :return: SafeReference instance
    """
    return SafeReference(object, default, wrap_methods)


def extract_namespaces(xml: str) -> set:
    namespaces = set()
    pattern = r'xmlns(:[a-zA-Z0-9-]+)?=("|\')([^("|\')]+)("|\')'
    matches = re.findall(pattern, xml)
    for match in matches:
        prefix, _, uri, _ = match
        prefix = prefix.replace(':', '')
        prefix = None if not prefix else prefix
        namespaces.add((prefix, uri))
    return namespaces
