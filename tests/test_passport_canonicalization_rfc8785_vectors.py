"""External RFC 8785/JCS known-answer and boundary tests.

These tests record current canonicalization observations against selected
RFC 8785/JCS examples and edge cases.

They do not present the current helper as a complete RFC 8785/JCS
implementation. Broader I-JSON, duplicate-key, UTF-16 sorting,
number-serialization, and payload-domain questions remain research work.
"""

import pytest

from aaid.canonicalization import canonicalize_passport_payload

RFC8785_SECTION_3_2_3_EXPECTED = (
    b'{"literals":[null,true,false],'
    b'"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],'
    b'"string":"\xe2\x82\xac$\\u000f\\nA\'B\\"\\\\\\\\\\"/"}'
)

PYTHON_CODE_POINT_ORDER_OUTPUT = (
    b'{"\xee\x80\x80":"bmp-private-use",'
    b'"\xf0\x90\x80\x80":"non-bmp"}'
)

JCS_UTF16_ORDER_OUTPUT = (
    b'{"\xf0\x90\x80\x80":"non-bmp",'
    b'"\xee\x80\x80":"bmp-private-use"}'
)

JCS_1E16_EXPECTED_OUTPUT = b'{"n":10000000000000000}'
PYTHON_1E16_OUTPUT = b'{"n":1e+16}'


def test_rfc8785_section_3_2_3_sample_object_known_answer() -> None:
    """Match the RFC 8785 sample object canonical form.

    This vector covers recursive object sorting, compact JSON, array order,
    booleans, null, selected number serialization, non-ASCII string output, and
    control-character escaping.

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

    assert canonicalize_passport_payload(sample) == RFC8785_SECTION_3_2_3_EXPECTED


@pytest.mark.parametrize(
    "non_finite_value",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive-infinity"),
        pytest.param(float("-inf"), id="negative-infinity"),
    ],
)
def test_canonicalize_rejects_non_finite_numbers(
    non_finite_value: float,
) -> None:
    """Reject non-finite numbers so canonicalization fails closed.

    Python's json module emits ``NaN``, ``Infinity``, and ``-Infinity`` tokens
    by default. Those tokens are not valid JSON and are not RFC 8785/JCS
    conformant. The helper rejects them rather than producing signing input that
    a conformant verifier cannot parse.
    """

    with pytest.raises(ValueError):
        canonicalize_passport_payload({"value": non_finite_value})


def test_current_helper_records_utf16_key_ordering_boundary() -> None:
    """Record a JCS key-ordering boundary for non-BMP object names.

    JCS sorts object member names by UTF-16 code units. Python sort_keys=True
    sorts strings by code point. Those orders can diverge for non-BMP keys.

    For U+E000 and U+10000:
    - Python code-point order places U+E000 first.
    - JCS UTF-16 code-unit order places U+10000 first.

    This test records the current helper behavior and the JCS expected order for
    one edge case. It does not change canonicalization behavior.
    """

    data = {
        chr(0xE000): "bmp-private-use",
        chr(0x10000): "non-bmp",
    }

    current_output = canonicalize_passport_payload(data)

    assert current_output != JCS_UTF16_ORDER_OUTPUT
    assert current_output == PYTHON_CODE_POINT_ORDER_OUTPUT


def test_current_helper_records_number_serialization_boundary() -> None:
    """Record a JCS number-serialization boundary for a large float.

    JCS serializes numbers with the ECMAScript Number::toString algorithm.
    Python json.dumps serializes floats with repr(), which switches to
    exponential notation earlier. The value 1e16 is exactly representable as an
    IEEE-754 double, so both forms carry the same digits while the notation
    differs.

    This test records the current helper behavior and the JCS expected form for
    one edge case. It does not change canonicalization behavior.
    """

    current_output = canonicalize_passport_payload({"n": 1e16})

    assert current_output != JCS_1E16_EXPECTED_OUTPUT
    assert current_output == PYTHON_1E16_OUTPUT
