from dunder_xml_reader import extract_namespaces


def test_extract_namespaces():
    # Given
    xml = """
        <section xmlns="http://www.ibm.com/events" xmlns:bk="urn:loc.gov:books" xmlns:pi="urn:personalInformation"
                 xmlns:isbn='urn:ISBN:0-395-36341-6'>
            <title>Book-Signing Event</title>
            <signing>
                <bk:author pi:title="Mr" pi:name="Jim Ross"/>
                <book bk:title="Writing COBOL for Fun and Profit" isbn:number="0426070806"/>
                <comment xmlns=''>What a great issue!</comment>
            </signing>
        </section>
    """

    # When
    result = extract_namespaces(xml)

    # Then
    assert result == {
        (None, 'http://www.ibm.com/events'),
        ('bk', 'urn:loc.gov:books'),
        ('pi', 'urn:personalInformation'),
        ('isbn', 'urn:ISBN:0-395-36341-6')
    }
