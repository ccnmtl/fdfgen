import fdfgen


def test_key_encoding():
    expected_field_name = b'T(\xfe\xff\x00f\x00o\x00o)'  # T(foo) where foo is UTF-16 coded
    result = fdfgen.forge_fdf(fdf_data_strings=[('foo', 'bar')])
    assert expected_field_name in result
