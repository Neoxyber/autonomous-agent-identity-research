import ast
import copy
import dataclasses
import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from _support import EXAMPLE_PATH, REQUEST, SENSITIVE_VALUES
from aaid import audit, authorization, composition, verification
from aaid.audit import ERROR, prepare_audit_event

ALLOW = verification.ALLOW
DENY = verification.DENY
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

MALFORMED_SCALAR_CASES = [
    pytest.param(123, None, id="integer-event-type"),
    pytest.param({"a": 1}, None, id="mapping-event-type"),
    pytest.param("x", 123, id="integer-occurred-at"),
    pytest.param("x", {"t": 1}, id="mapping-occurred-at"),
    pytest.param(object(), object(), id="object-values"),
]

MALFORMED_COMPOSITION_CASES = [
    pytest.param(None, id="none"),
    pytest.param("x", id="string"),
    pytest.param(123, id="integer"),
    pytest.param(object(), id="object"),
    pytest.param(
        AuthorizationDecision(ALLOW, "authorization"),
        id="authorization-decision",
    ),
    pytest.param(
        VerificationResult(valid=False, decision=DENY, reason="verification"),
        id="verification-result",
    ),
]

MALFORMED_PASSPORT_REQUEST_CASES = [
    pytest.param(None, None, id="none"),
    pytest.param("x", "y", id="strings"),
    pytest.param(123, 456, id="integers"),
    pytest.param({}, {}, id="empty-mappings"),
    pytest.param(object(), object(), id="objects"),
]


def make_verification_result(decision=DENY, *, valid=None):
    valid = (decision == ALLOW) if valid is None else valid
    return VerificationResult(valid=valid, decision=decision, reason="verification")


def make_authorization_decision(decision=ALLOW):
    return AuthorizationDecision(decision, "authorization")


def make_composed_decision(decision=DENY, reason="composed"):
    return ComposedDecision(decision, reason)


def load_example_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from iter_strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from iter_strings(value)


def audit_event_text(event):
    return "\n".join(iter_strings(dataclasses.asdict(event)))


def make_test_audit_event(**overrides):
    kwargs = {
        "passport": {},
        "request": {},
        "verification": None,
        "authorization": None,
        "composition": make_composed_decision(DENY),
        "event_type": "x",
    }
    kwargs.update(overrides)
    return prepare_audit_event(**kwargs)


def test_safe_fields_included_with_correct_values():
    passport = load_example_passport()
    event = make_test_audit_event(
        passport=passport,
        request=REQUEST,
        verification=make_verification_result(DENY),
        authorization=make_authorization_decision(ALLOW),
        composition=make_composed_decision(DENY, "composed reason"),
        event_type="action_decision",
        occurred_at="2026-06-03T00:00:00Z",
    )
    assert (event.event_type, event.occurred_at) == (
        "action_decision",
        "2026-06-03T00:00:00Z",
    )
    assert (event.decision, event.decision_reason) == (DENY, "composed reason")
    assert (event.verification_decision, event.authorization_decision) == (
        DENY,
        ALLOW,
    )
    assert (event.requested_action, event.resource_scope) == (
        "summarize_public_text",
        "demo.public_text",
    )
    assert event.passport_id == passport["passport_id"]
    assert event.agent_id == passport["agent_id"]
    assert event.operator_id == passport["operator"]["operator_id"]
    assert event.issuer_id == passport["issuer_id"]
    assert (event.lifecycle_status, event.risk_class) == ("active", "standard")
    assert event.policy_id == passport["permissions"]["policy_id"]
    assert event.audit_stream_id == passport["audit"]["audit_stream_id"]
    assert event.revocation_reference == passport["revocation"]["status_reference"]


def test_occurred_at_injected_or_none():
    assert (
        make_test_audit_event(occurred_at="2026-06-03T12:00:00Z").occurred_at
        == "2026-06-03T12:00:00Z"
    )
    assert make_test_audit_event().occurred_at is None


@pytest.mark.parametrize("event_type, occurred_at", MALFORMED_SCALAR_CASES)
def test_malformed_scalar_inputs_do_not_raise(event_type, occurred_at):
    event = make_test_audit_event(event_type=event_type, occurred_at=occurred_at)
    assert event.event_type is None or isinstance(event.event_type, str)
    assert event.occurred_at is None or isinstance(event.occurred_at, str)


@pytest.mark.parametrize("bad_composition", MALFORMED_COMPOSITION_CASES)
def test_malformed_composition_records_error(bad_composition):
    assert make_test_audit_event(composition=bad_composition).decision == ERROR


@pytest.mark.parametrize("passport, request_arg", MALFORMED_PASSPORT_REQUEST_CASES)
def test_malformed_passport_request_record_none(passport, request_arg):
    event = make_test_audit_event(passport=passport, request=request_arg)
    assert event.passport_id is None
    assert event.agent_id is None
    assert event.operator_id is None
    assert event.requested_action is None
    assert event.resource_scope is None
    assert event.decision == DENY


def test_inputs_not_mutated():
    passport = load_example_passport()
    request = dict(REQUEST)
    verification_result = make_verification_result(DENY)
    authorization_decision = make_authorization_decision(ALLOW)
    composed_decision = make_composed_decision(DENY)

    snapshots = copy.deepcopy(
        (
            passport,
            request,
            verification_result,
            authorization_decision,
            composed_decision,
        )
    )
    make_test_audit_event(
        passport=passport,
        request=request,
        verification=verification_result,
        authorization=authorization_decision,
        composition=composed_decision,
    )

    assert (
        passport,
        request,
        verification_result,
        authorization_decision,
        composed_decision,
    ) == snapshots


def test_audit_event_is_frozen():
    event = make_test_audit_event()
    with pytest.raises(dataclasses.FrozenInstanceError):
        event.decision = ALLOW


def test_no_sensitive_value_leak():
    text = audit_event_text(
        make_test_audit_event(passport=load_example_passport(), request=REQUEST)
    )
    for sensitive in SENSITIVE_VALUES:
        assert sensitive not in text


def test_extra_request_fields_not_copied():
    request = {
        "action": "a",
        "resource_scope": "s",
        "secret_token": "TOPSECRET",
        "payload": {"x": "SECRETV"},
    }
    event = make_test_audit_event(request=request)
    text = audit_event_text(event)
    assert "TOPSECRET" not in text
    assert "SECRETV" not in text
    assert (event.requested_action, event.resource_scope) == ("a", "s")


def test_no_permission_lists_copied():
    text = audit_event_text(
        make_test_audit_event(passport=load_example_passport(), request=REQUEST)
    )
    assert "access_secrets" not in text
    assert "send_external_summary" not in text
    assert "demo.secret_store" not in text


def test_error_is_audit_only():
    assert ERROR == "ERROR"
    for module in (verification, authorization, composition):
        assert ERROR not in module._DECISIONS
        assert not hasattr(module, "ERROR")


FORBIDDEN_IMPORTS = {
    "azure",
    "boto3",
    "cosign",
    "cryptography",
    "fulcio",
    "google",
    "hashlib",
    "hmac",
    "http",
    "httpx",
    "jcs",
    "logging",
    "passport_verifier",
    "pickle",
    "requests",
    "rekor",
    "rfc8785",
    "secrets",
    "shelve",
    "sigstore",
    "socket",
    "sqlite3",
    "ssl",
    "subprocess",
    "urllib",
}
FORBIDDEN_ENGINES = (
    "authorize_action",
    "compose_decision",
    "passport_verifier",
    "verify_passport_envelope",
)
FORBIDDEN_SINKS = (
    ".hexdigest",
    ".write(",
    "chain(",
    "hashlib",
    "logging",
    "open(",
    "pickle",
    "previous_event",
    "print(",
    "requests",
    "sha256",
    "sign(",
    "socket",
    "sqlite",
    "subprocess",
)


def test_no_forbidden_imports_or_engines():
    source = Path(audit.__file__).read_text(encoding="utf-8")
    imported = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.update(alias.name.split("."))
        elif isinstance(node, ast.ImportFrom):
            imported.update((node.module or "").split("."))
    assert not (imported & FORBIDDEN_IMPORTS), imported & FORBIDDEN_IMPORTS
    for engine in FORBIDDEN_ENGINES:
        assert engine not in source


def test_no_io_sinks_in_source():
    source = Path(audit.__file__).read_text(encoding="utf-8")
    for snippet in FORBIDDEN_SINKS:
        assert snippet not in source, snippet
