import fdfgen


def test_identifier_with_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('/Off')
    assert result == expected_identifier


def test_identifier_without_slash():
    expected_identifier = b'/Off'
    result = fdfgen.FDFIdentifier('Off')
    assert result == expected_identifier


test_identifier_without_slash()
test_identifier_with_slash()
print "hello"
