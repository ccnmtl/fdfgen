import fdfgen


def test_identifier_with_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('/Off').value
    assert result == expected_identifier


def test_identifier_without_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('Off').value
    assert result == expected_identifier


def test_identifier_with_special_chars():
    expected_identifier = b'/with#20#28several#29#20special#2Fchars'
    result = fdfgen.FDFIdentifier('with (several) special/chars').value
    assert result == expected_identifier