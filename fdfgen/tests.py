import fdfgen
from unittest import TestCase

class Tests(TestCase):

    def test_string_with_unbalanced_paren(self):
        s = 'a) 1st item'
        e = '\xfe\xff\x00a\x00\\)\x00 \x001\x00s\x00t\x00 \x00i\x00t\x00e\x00m'
        self.assertEqual(fdfgen.smart_encode_str(s), e)
