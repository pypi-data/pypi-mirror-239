"""Unit tests for the dunder_xml_reader.xml_node module"""

import pytest

from dunder_xml_reader import parse_xml
from dunder_xml_reader.xml_node_list import XmlNodeList


def test_initialization(sample_xml_text):
    # Given
    raw_text = sample_xml_text

    # When
    result = parse_xml(raw_text)

    # Then
    assert result.raw_text is raw_text
    assert result.tag() == 'cXML'


def test_get_item_as_dict(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc['payloadID']

    # Then
    assert result == '1233444-2001@premier.workchairs.com'


def test_get_item_as_dict_case_insensitive(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc['PaYlOaDiD']

    # Then
    assert result == '1233444-2001@premier.workchairs.com'


def test_get_item_as_dict_unavailable(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    with pytest.raises(KeyError) as exc_info:
        _ = xml_doc['not-there']

    # Then
    assert exc_info.value.args[0] == 'not-there'


def test_get_item_as_dict_function(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc.get('timestamp')

    # Then
    assert result == '2000-10-12T18:41:29-08:00'


def test_get_item_as_dict_function_with_default(sample_xml_text):
    # Give
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc.get('x-version', 'stuff')

    # Then
    assert result == 'stuff'


def test_contains_as_dict_found(sample_xml_text):
    # Give
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = 'timestamp' in xml_doc

    # Then
    assert result


def test_contains_as_dict_found_case_insensitive(sample_xml_text):
    # Give
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = 'tImEsTaMp' in xml_doc

    # Then
    assert result


def test_contains_as_dict_not_found(sample_xml_text):
    # Give
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = 'version' in xml_doc

    # Then
    assert not result


def test_attribute(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc.Header.To

    # Then
    assert result.tag() == 'To'


def test_attribute_case_insensitive(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc.header.to

    # Then
    assert result.tag() == 'To'


def test_attribute_unavailable(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    with pytest.raises(AttributeError) as exc_info:
        _ = xml_doc.not_there

    # Then
    assert exc_info.value.args[0] == "'cXML' object has no attribute 'not_there'"


def test_hasattr_with_available_attribute(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = hasattr(xml_doc.Header, 'From')

    # Then
    assert result


def test_hasattr_with_unavailable_attribute(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = hasattr(xml_doc.Header, 'Xfrom')

    # Then
    assert not result


def test_get_item_as_list(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = xml_doc.Header.Sender.UserAgent[0]

    # Then
    assert result.tag() == 'UserAgent'


def test_get_item_as_list_out_of_bounds_root(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    with pytest.raises(IndexError) as exc_info:
        _ = xml_doc.Header.Sender.UserAgent[1]

    # Then
    assert exc_info.value.args[0] == "list index out of range"


def test_len(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = len(xml_doc)

    # Then
    assert result == 1


def test_first(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)
    node = xml_doc.Header

    # When
    result = node.first()

    # Then
    assert result is node


def test_filter_match(sample_xml_text):
    # Given
    item = parse_xml(sample_xml_text).Header.From.Credential

    # When
    result = item.filter(lambda n: n['domain'] == 'DUNS')

    # Then
    assert result[0] is item


def test_filter_no_match(sample_xml_text):
    # Given
    item = parse_xml(sample_xml_text).Header.From.Credential

    # When
    result = item.filter(lambda n: n['domain'] == 'SNUD')

    # Then
    assert len(result) == 0


def test_map(sample_xml_text):
    # Given
    item = parse_xml(sample_xml_text).Header.From.Credential

    # When
    result = item.map(lambda n: n['domain'])

    # Then
    assert result == ['DUNS']


def test_repr(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = str(xml_doc.Header.From.Credential[0])

    # Then
    assert result == 'XmlNode: Credential'


def test_repr_non_xml_node_entries(sample_xml_text):
    # Given
    sut = XmlNodeList([1, 2, 3])

    # When
    result = str(sut)

    # Then
    assert result == '[1, 2, 3]'


def test_dir_shows_attributes(sample_xml_text):
    # Given
    xml_doc = parse_xml(sample_xml_text)

    # When
    result = dir(xml_doc.Header)

    # Then
    assert set(result) == {'From', 'To', 'Sender'}


def test_map(sample_xml_text):
    # Given
    credentials = parse_xml(sample_xml_text).Header.To.Credential

    # When
    result = credentials.map(lambda n: n.Identity.text())

    # Then
    assert result == ['bigadmin@marketplace.org', 'admin@acme.com']


def test_returns_blank_if_empty_element(sample_xml_text):
    # Given
    conf_header = parse_xml(sample_xml_text).Request.ConfirmationRequest.ConfirmationHeader

    # When
    result = conf_header.Notes.text()

    # Then
    assert result == ''


def test_with_namespaces(sample_soap_text):
    # Given
    raw_text = sample_soap_text

    # When
    result = parse_xml(raw_text, namespaces={
        'http://schemas.xmlsoap.org/soap/envelope/': 'soap',
        'http://insurance.com/webservices/ReceiveClaim.job': 'claim'
    })

    # Then
    assert result.raw_text is raw_text
    assert result.tag() == 'soap_Envelope'
    assert dir(result.soap_Body) == ['claim_ReceiveClaimResponse']
    assert hasattr(result.soap_Body, 'claim_ReceiveClaimResponse')
    assert result.soap_Body.claim_ReceiveClaimResponse.claim_ClaimResponse.claim_status.text() == 'S'


def test_with_blanked_namespaces(sample_soap_text):
    # Given
    raw_text = sample_soap_text

    # When
    result = parse_xml(raw_text, namespaces={
        'http://schemas.xmlsoap.org/soap/envelope/',
        'http://insurance.com/webservices/ReceiveClaim.job'
    })

    # Then
    assert result.raw_text is raw_text
    assert result.tag() == 'Envelope'
    assert dir(result.Body) == ['ReceiveClaimResponse']
    assert hasattr(result.Body, 'ReceiveClaimResponse')
    assert result.Body.ReceiveClaimResponse.ClaimResponse.status.text() == 'S'


def test_with_some_blanked_namespaces(sample_soap_text):
    # Given
    raw_text = sample_soap_text

    # When
    result = parse_xml(raw_text, namespaces={
        'http://schemas.xmlsoap.org/soap/envelope/': 'soap',
        'http://insurance.com/webservices/ReceiveClaim.job': None
    })

    # Then
    assert result.raw_text is raw_text
    assert result.tag() == 'soap_Envelope'
    assert dir(result.soap_Body) == ['ReceiveClaimResponse']
    assert hasattr(result.soap_Body, 'ReceiveClaimResponse')
    assert result.soap_Body.ReceiveClaimResponse.ClaimResponse.status.text() == 'S'
