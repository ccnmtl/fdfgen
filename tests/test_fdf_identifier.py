import fdfgen


def test_identifier_with_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('/Off').value
    assert result == expected_identifier


def test_identifier_without_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('Off').value
    assert result == expected_identifier
