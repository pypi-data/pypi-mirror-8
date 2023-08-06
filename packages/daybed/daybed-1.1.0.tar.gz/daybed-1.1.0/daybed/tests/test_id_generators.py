try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase  # flake8: noqa

import six
from mock import patch

from daybed.backends.id_generators import KoremutakeGenerator


class KoremutakeGeneratorTest(TestCase):

    def setUp(self):
        self.generator = KoremutakeGenerator()

    def test_it_defaults_the_max_bytes_to_4(self):
        self.assertEquals(self.generator.max_bytes, 4)

    @patch('koremutake.encode')
    def test_it_doesnt_reuse_a_name_twice(self, encode):
        encode.side_effect = ['existing-value', 'new-value']
        created = ['existing-value']
        def _exists(key):
            return key in created

        self.assertEquals(self.generator(key_exist=_exists), 'new-value')

    def test_it_returns_a_string_with_a_max_size(self):
        uid = self.generator()
        self.assertTrue(len(uid) <= 24)
        self.assertIsInstance(uid, six.text_type)
