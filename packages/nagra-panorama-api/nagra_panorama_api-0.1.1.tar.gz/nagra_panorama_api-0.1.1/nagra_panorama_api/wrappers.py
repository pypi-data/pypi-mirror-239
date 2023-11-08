import addict
import xmltodict
from lxml import etree


class Dict(addict.Dict):

    def __init__(self, xml=None):
        if isinstance(xml, etree._Element):
            xml = etree.tostring(xml)
        if isinstance(xml, str):
            if not xml:
                xml = '<entry/>'
            xml = xmltodict.parse(xml)
        return super().__init__(xml)

    def dumps(self):
        return xmltodict.unparse(self, full_document=False)

    def element(self):
        return etree.fromstring(self.dumps())
