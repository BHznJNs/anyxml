import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr


class AnyXml:
    """A minimal reimplementation of `ET.tostring` that supports unescaped "raw" text content.

    The standard library's `ET.tostring` always XML-escapes the `text`/`tail` content of elements (e.g. `<`, `&`), which makes it impossible to inject pre-built, already-valid XML fragments (or other raw strings) during serialization.
    This class provides :meth:`tostring`, which behaves similarly to `ET.tostring` but additionally supports:

    - Strings wrapped in :class:`RawText` are emitted verbatim during serialization, without any escaping; regular `str` text is still escaped according to XML rules.
    - Comment nodes (`ET.Comment`) and processing instruction nodes (`ET.ProcessingInstruction`) are rendered as `<!--...-->` and `<?...?>` respectively.
    - Elements with no text and no children are rendered as self-closing tags (`<tag/>`).

    Examples:
        >>> el = ET.Element("p")
        >>> el.text = AnyXml.RawText("<b>bold</b>")
        >>> AnyXml.tostring(el)
        '<p><b>bold</b></p>'
    """

    class RawText(str): pass

    @staticmethod
    def _text(s: str) -> str:
        if isinstance(s, AnyXml.RawText): return s
        return escape(s)

    @staticmethod
    def _comment(el: ET.Element) -> str:
        assert el.tag is ET.Comment
        return f"<!--{el.text or ''}-->"

    @staticmethod
    def _processing_instruction(el: ET.Element) -> str:
        assert el.tag is ET.ProcessingInstruction
        return f"<?{el.text or ''}?>"

    @staticmethod
    def tostring(el: ET.Element) -> str:
        if el.tag is ET.Comment: return AnyXml._comment(el)
        if el.tag is ET.ProcessingInstruction: return AnyXml._processing_instruction(el)

        attrs = "".join(f" {k}={quoteattr(str(v))}" for k, v in el.attrib.items())

        children_xml = []
        for child in el:
            children_xml.append(AnyXml.tostring(child))
            if child.tail:
                children_xml.append(AnyXml._text(child.tail))

        if el.text is None and len(children_xml) == 0:
            return f"<{el.tag}{attrs}/>"

        inner_text = AnyXml._text(el.text) if el.text is not None else ""
        body = inner_text + "".join(children_xml)
        return f"<{el.tag}{attrs}>{body}</{el.tag}>"
