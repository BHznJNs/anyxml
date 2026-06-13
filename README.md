# AnyXml

A minimal reimplementation of `ET.tostring` that supports unescaped "raw" text content.

The standard library's `ET.tostring` always XML-escapes the `text`/`tail` content of elements (e.g. `<`, `&`), which makes it impossible to inject pre-built, already-valid XML fragments (or other raw strings) during serialization.
This class provides :meth:`tostring`, which behaves similarly to `ET.tostring` but additionally supports:

- Strings wrapped in :class:`RawText` are emitted verbatim during serialization, without any escaping; regular `str` text is still escaped according to XML rules.
- Comment nodes (`ET.Comment`) and processing instruction nodes (`ET.ProcessingInstruction`) are rendered as `<!--...-->` and `<?...?>` respectively.
- Elements with no text and no children are rendered as self-closing tags (`<tag/>`).

## Example

```
>>> el = ET.Element("p")
>>> el.text = AnyXml.RawText("<b>bold</b>")
>>> AnyXml.tostring(el)
'<p><b>bold</b></p>'
```
