"""Tests for finding untranslated prose.
"""
import unittest
import xml.sax
import StringIO
import i18ndude.untranslated


def find_untranslated(input):
    out = StringIO.StringIO()
    parser = xml.sax.make_parser(['expat'])
    handler = i18ndude.untranslated.VerboseHandler(parser, out)
    parser.setContentHandler(handler)
    parser.parse(StringIO.StringIO(input))
    return out.getvalue()


class TestUntranslated(unittest.TestCase):

    def test_untranslated_content(self):
        result_with_errors = find_untranslated('<div><p>foo</p></div>')
        self.assertIn(
            'i18n:translate missing for this:\n"""\nfoo\n"""',
            result_with_errors)
        self.assertIn(
            '(0 warnings, 1 errors)',
            result_with_errors)

    def test_untranslated(self):
        # When adding the i18n:translate marker, no errors are found:
        result_without_errors = find_untranslated(
            '<div><p i18n:translate="">foo</p></div>')
        self.assertNotIn(
            'i18n:translate missing',
            result_without_errors)
        self.assertIn('(0 warnings, 0 errors)', result_without_errors)

    def test_ignore_untranslated_with_marker(self):
        # Adding the i18n:ignore marker will skip untranslated strings.
        result_with_marker = find_untranslated(
            '<div><p i18n:ignore="">foo</p></div>')
        self.assertIn('(0 warnings, 0 errors)', result_with_marker)

    def test_ignore_untranslated_attribute(self):
        result_without_attributes = find_untranslated(
            '<div><a title="bar" i18n:translate="">spam</a></div>')
        self.assertIn(
            'title attribute of <a> lacks i18n:attributes',
            result_without_attributes)
        self.assertIn('(0 warnings, 1 errors)', result_without_attributes)

        result_with_ignore_attributes = find_untranslated(
            '''<div><a title="bar"
                i18n:ignore-attributes="title"
                i18n:translate=""
                >spam</a></div>''')
        self.assertIn('(0 warnings, 0 errors)', result_with_ignore_attributes)

    def test_ignore_untranslated_attribute_complain_about_other_attrs(self):
        result_without_attributes = find_untranslated(
            '''<div><img title="bar" alt="qux"
            i18n:ignore-attributes="title"/></div>''')
        self.assertIn(
            'alt attribute of <img> lacks i18n:attributes',
            result_without_attributes)
        self.assertIn('(0 warnings, 1 errors)', result_without_attributes)
