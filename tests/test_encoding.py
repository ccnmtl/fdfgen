from __future__ import unicode_literals

import fdfgen


def test_string_with_unbalanced_paren():
    s = 'a) 1st item'
    e = b'\xfe\xff\x00a\x00\\)\x00 \x001\x00s\x00t\x00 \x00i\x00t\x00e\x00m'
    assert fdfgen.smart_encode_str(s) == e
