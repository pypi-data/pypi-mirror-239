from __future__ import annotations
import unicodedata

import pytest

from vina2vi.util import (
    Vietnamese,
    uncased_vina_normalizer,
)

@pytest.mark.parametrize("s,expected", [
    (unicodedata.normalize("NFD", Vietnamese.ambiguous_chars[char]),
     char * len(Vietnamese.ambiguous_chars[char]))
    for char in "aeiouy"
])
def test_vina_normalizers_no_need_NFC(s, expected):
    assert uncased_vina_normalizer.normalize_str(s) == expected



