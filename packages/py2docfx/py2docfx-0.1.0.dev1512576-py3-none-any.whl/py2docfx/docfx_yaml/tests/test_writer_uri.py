import pytest
from sphinx.testing import restructuredtext
from sphinx.io import SphinxStandaloneReader
from sphinx import addnodes

from py2docfx.docfx_yaml.utils import transform_node
from py2docfx.docfx_yaml.tests.utils.test_utils import prepare_app_envs,prepare_refered_objects,load_rst_transform_to_doctree

@pytest.mark.sphinx('dummy', testroot='writer-uri')
def test_http_link_in_summary_expect_same_link(app):
    # Test data definition
    objectToGenXml = 'code_with_uri.SampleClass'
    objectToGenXmlType = 'class'        

    # Arrange
    prepare_app_envs(app, objectToGenXml)
    doctree = load_rst_transform_to_doctree(app, objectToGenXmlType, objectToGenXml)
    
    # Act
    node = doctree[1][1][0]
    result = transform_node(app, doctree)

    # Assert
    # Shouldn't see something like [title]((link))
    expected = ("class code_with_uri.SampleClass\n\n\n   "
    "Some summary with link https://www.microsoft.com\n\n   "
    "dummy_param()\n\n\n      "
    "This is a content issue link [microsoft](https://www.microsoft.com)\n      "
    "We should not generate nested parenthesis causing docs validation warnings\n")

    assert(result == expected)
    