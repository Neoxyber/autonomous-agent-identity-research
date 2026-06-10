"""External RFC 8785/JCS known-answer tests.

These tests begin the external canonicalization conformance work.

They do not claim that the current helper is a complete RFC 8785/JCS
implementation. They only pin behaviour where the current helper is expected to
match an RFC 8785 known-answer example. Broader I-JSON, duplicate-key,
UTF-16 sorting, and number-serialization boundary tests remain future work.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

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


@pytest.mark.parametrize("non_finite", [float("nan"), float("inf"), float("-inf")])
def test_canonicalize_rejects_non_finite_numbers(non_finite):
    """Reject non-finite numbers so canonicalization fails closed.

    Python's json module emits ``NaN``, ``Infinity``, and ``-Infinity`` tokens
    by default, which are not valid JSON and not RFC 8785/JCS conformant. The
    helper must reject them rather than produce signing input that no conformant
    verifier can parse.
    """

    with pytest.raises(ValueError):
        canonicalize_passport_payload({"value": non_finite})


def test_current_helper_documents_utf16_key_ordering_boundary():
    """Document a JCS key-ordering boundary for non-BMP object names.

    JCS sorts object member names by UTF-16 code units. Python sort_keys=True
    sorts strings by code point. Those orders can diverge for non-BMP keys.

    For U+E000 (a BMP code point) and U+10000 (a non-BMP code point encoded in
    UTF-16 as the surrogate pair D800 DC00):
    - Python code-point order places U+E000 first, because 0xE000 < 0x10000.
    - JCS UTF-16 code-unit order places U+10000 first, because its leading code
      unit D800 sorts before E000.

    This test records the current helper's behaviour and the JCS expected order
    for one edge case. It does not claim JCS compatibility and does not change
    canonicalization behaviour.
    """

    data = {
        chr(0xE000): "bmp-private-use",  # U+E000, a BMP private-use code point
        chr(0x10000): "non-bmp",  # U+10000, non-BMP (UTF-16 surrogate pair D800 DC00)
    }

    current_output = canonicalize_passport_payload(data)
    jcs_utf16_order_output = (
        b'{"\xf0\x90\x80\x80":"non-bmp",'
        b'"\xee\x80\x80":"bmp-private-use"}'
    )

    # The current helper does not match JCS UTF-16 ordering for this edge case.
    assert current_output != jcs_utf16_order_output
    # The current helper sorts by Python code point: the BMP key comes first.
    assert current_output == (
        b'{"\xee\x80\x80":"bmp-private-use",'
        b'"\xf0\x90\x80\x80":"non-bmp"}'
    )


def test_current_helper_documents_number_serialization_boundary():
    """Document a JCS number-serialization boundary for a large integer-valued float.

    JCS (RFC 8785) serializes numbers with the ECMAScript Number::toString
    algorithm, which writes a finite value below 1e21 in positional form. Python
    json.dumps serializes floats with repr(), which switches to exponential
    notation at 1e16. The value 1e16 is exactly representable as an IEEE-754
    double, so both produce the same digits; only the notation differs.

    The float 1e16 is used deliberately: the integer 10000000000000000 would be
    emitted as positional digits by Python too and would hide the boundary, while
    JCS treats every JSON number as a double.

    This test records the current helper's behaviour and the JCS expected form for
    one edge case. It does not claim JCS compatibility and does not change
    canonicalization behaviour.
    """

    current_output = canonicalize_passport_payload({"n": 1e16})
    jcs_expected_output = b'{"n":10000000000000000}'

    # The current helper does not match JCS number serialization for this edge case.
    assert current_output != jcs_expected_output
    # The current helper emits exponential notation via Python float repr.
    assert current_output == b'{"n":1e+16}'
