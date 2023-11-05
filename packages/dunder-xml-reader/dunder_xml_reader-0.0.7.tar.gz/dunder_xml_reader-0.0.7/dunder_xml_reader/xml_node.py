"""The dunder_xml_reader.xml_node module"""
from typing import Union

from dunder_xml_reader.xml_node_list import XmlNodeList


class XmlNode:
    """
    Using Python's built-in ElementTree package can be involved, especially when you
    are simply trying to just read data out of a CXML order for mapping.  The purpose
    of this class is to simply quick extraction of data out of a CXML order.  It is
    a dynamic class that exposes child-nodes as Python class attributes.  See the
    GitHub repo's README.md for examples on how to use.
    """

    def __init__(self, node, parent_node=None, raw_text: str = None, namespaces=None):
        """
        Constructor.
        :param node: A Python ElementTree (root) node to wrap
        :param parent_node: If this is not the root, this the parent ElementTree node
        :param raw_text:  Raw XML text string if you want to keep a copy
        """
        self.raw_text = raw_text
        self.node = node
        self.namespaces = namespaces if namespaces is not None else {}
        self.case_insensitive_props = dict((k.lower(), k) for k in self.node.attrib)
        self.parent_node = parent_node

    def text(self) -> str:
        """Get the node's text (the string between the XML tags)."""
        return '' if self.node.text is None else self.node.text

    def tag(self) -> str:
        """Get the XML element tag from the node."""
        return self._fixtag(self.node.tag)

    def first(self, default=None):
        """Seamless interop with XmlNodeList"""
        return XmlNodeList([self]).first(default)

    def last(self, default=None):
        """Seamless interop with XmlNodeList"""
        return XmlNodeList([self]).last(default)

    def filter(self, func: callable):
        """Seamless interop with XmlNodeList"""
        return XmlNodeList([self]).filter(func)

    def map(self, func: callable):
        """Seamless interop with XmlNodeList"""
        return XmlNodeList([self]).map(func)

    def get(self, item: str, default: str = None) -> str:
        """Get the given property from the node."""
        case_sensitive_item = self.case_insensitive_props.get(item.lower(), item)
        return self.node.attrib.get(case_sensitive_item, default)

    def __getitem__(self, item: Union[int, str]):
        if isinstance(item, int):
            if item == 0:
                return self
            raise IndexError('list index out of range')
        else:
            case_sensitive_item = self.case_insensitive_props.get(item.lower(), item)
            return self.node.attrib[case_sensitive_item]

    def __contains__(self, item: str):
        case_sensitive_item = self.case_insensitive_props.get(item.lower(), item)
        return case_sensitive_item in self.node.attrib

    def __getattr__(self, attribute: str):
        nodes = [n for n in self.node if self._fixtag(n.tag).lower() == attribute.lower()]
        if len(nodes) == 1:
            return XmlNode(node=nodes[0], parent_node=self.node, namespaces=self.namespaces)
        if len(nodes) > 1:
            return XmlNodeList([XmlNode(node=n, parent_node=self.node,
                                        namespaces=self.namespaces) for n in nodes])
        raise AttributeError(f"'{self.node.tag}' object has no attribute '{attribute}'")

    def __len__(self):
        return 1

    def __repr__(self):
        return f"XmlNode: {self.tag()}"

    def __dir__(self):
        return [self._fixtag(n.tag) for n in self.node]

    def _fixtag(self, tag):
        for ns_tag in self.namespaces:
            full_tag = f"{{{ns_tag}}}"
            if tag.startswith(full_tag):
                prefix = self._ns_prefix(ns_tag)
                return tag.replace(full_tag, prefix)
        return tag

    def _ns_prefix(self, ns):
        if isinstance(self.namespaces, set):
            return ''
        else:
            if self.namespaces[ns]:
                return f"{self.namespaces[ns]}_"
            else:
                return ''
