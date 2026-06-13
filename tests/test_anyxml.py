import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from anyxml import AnyXml


def test_raw_text_is_not_escaped():
    el = ET.Element("p")
    el.text = AnyXml.RawText("<b>bold</b>")

    assert AnyXml.tostring(el) == "<p><b>bold</b></p>"


def test_plain_text_is_escaped():
    el = ET.Element("p")
    el.text = "a < b & c"

    assert AnyXml.tostring(el) == "<p>a &lt; b &amp; c</p>"


def test_attributes_are_serialized_and_escaped():
    el = ET.Element("item", {"title": 'a "quote" & more', "kind": "x"})

    assert AnyXml.tostring(el) == '<item title=\'a "quote" &amp; more\' kind="x"/>'


def test_comment_node_is_serialized():
    comment = ET.Comment("hello")

    assert AnyXml.tostring(comment) == "<!--hello-->"


def test_processing_instruction_is_serialized():
    pi = ET.ProcessingInstruction("xml-stylesheet", 'type="text/xsl" href="style.xsl"')

    assert AnyXml.tostring(pi) == '<?xml-stylesheet type="text/xsl" href="style.xsl"?>'


def test_empty_element_is_self_closing():
    el = ET.Element("empty")

    assert AnyXml.tostring(el) == "<empty/>"


def test_children_and_tail_are_serialized_in_order():
    root = ET.Element("root")
    root.text = "start <"

    child = ET.SubElement(root, "child")
    child.text = AnyXml.RawText("<b>x</b>")
    child.tail = " & end"

    assert AnyXml.tostring(root) == "<root>start &lt;<child><b>x</b></child> &amp; end</root>"


def test_comment_and_processing_instruction_as_children():
    root = ET.Element("root")
    root.append(ET.Comment("note"))
    root.append(ET.ProcessingInstruction("pi", "value"))

    assert AnyXml.tostring(root) == "<root><!--note--><?pi value?></root>"
