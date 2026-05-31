"""External RFC 8785/JCS known-answer tests.

These tests begin the external canonicalization conformance work.

They do not claim that the current helper is a complete RFC 8785/JCS
implementation. They only pin behaviour where the current helper is expected to
match an RFC 8785 known-answer example. Broader I-JSON, duplicate-key,
UTF-16 sorting, and number-serialization boundary tests remain future work.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aaid.canonicalization import canonicalize_passport_payload


def test_rfc8785_section_3_2_3_sample_object_known_answer():
    """Match the RFC 8785 sample object canonical form.

    This vector covers recursive object sorting, compact JSON, array order
    preservation, booleans, null, selected number serialization, non-ASCII
    string output, and control-character escaping.

    Passing this vector does not establish full RFC 8785/JCS conformance.
    """

    sample = {
        "numbers": [
            333333333.33333329,
            1e30,
            4.50,
            2e-3,
            0.000000000000000000000000001,
        ],
        "string": "\u20ac$\u000f\nA'B\"\\\\\"/",
        "literals": [None, True, False],
    }

    expected = (
        b'{"literals":[null,true,false],'
        b'"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],'
        b'"string":"\xe2\x82\xac$\\u000f\\nA\'B\\"\\\\\\\\\\"/"}'
    )

    assert canonicalize_passport_payload(sample) == expected
