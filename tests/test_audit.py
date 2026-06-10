import ast
import copy
import dataclasses
import json
from collections.abc import Mapping
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

from aaid import audit, authorization, composition, verification
from aaid.audit import ERROR, prepare_audit_event

ALLOW, DENY = verification.ALLOW, verification.DENY
VerificationResult = verification.VerificationResult
AuthorizationDecision = authorization.AuthorizationDecision
ComposedDecision = composition.ComposedDecision

from _support import EXAMPLE_PATH, REQUEST, SENSITIVE_VALUES


def verif(decision=DENY, *, valid=None):
    valid = (decision == ALLOW) if valid is None else valid
    return VerificationResult(valid=valid, decision=decision, reason="verification")


def authz(decision=ALLOW):
    return AuthorizationDecision(decision, "authorization")


def comp(decision=DENY, reason="composed"):
    return ComposedDecision(decision, reason)


def load_passport():
    with EXAMPLE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)["passport"]


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, Mapping):
        for value in obj.values():
            yield from strings(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            yield from strings(value)


def event_text(event):
    return "\n".join(strings(dataclasses.asdict(event)))


def build(**overrides):
    kwargs = dict(
        passport={},
        request={},
        verification=None,
        authorization=None,
        composition=comp(DENY),
        event_type="x",
    )
    kwargs.update(overrides)
    return prepare_audit_event(**kwargs)


def test_safe_fields_included_with_correct_values():
    passport = load_passport()
    event = build(
        passport=passport,
        request=REQUEST,
        verification=verif(DENY),
        authorization=authz(ALLOW),
        composition=comp(DENY, "composed reason"),
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
        build(occurred_at="2026-06-03T12:00:00Z").occurred_at
        == "2026-06-03T12:00:00Z"
    )
    assert build().occurred_at is None


@pytest.mark.parametrize(
    "event_type, occurred_at",
    [
        (123, None),
        ({"a": 1}, None),
        ("x", 123),
        ("x", {"t": 1}),
        (object(), object()),
    ],
)
def test_malformed_scalar_inputs_do_not_raise(event_type, occurred_at):
    event = build(event_type=event_type, occurred_at=occurred_at)
    assert event.event_type is None or isinstance(event.event_type, str)
    assert event.occurred_at is None or isinstance(event.occurred_at, str)


@pytest.mark.parametrize("bad", [None, "x", 123, object(), authz(ALLOW), verif(DENY)])
def test_malformed_composition_records_error(bad):
    assert build(composition=bad).decision == ERROR


@pytest.mark.parametrize(
    "passport, request_arg",
    [
        (None, None),
        ("x", "y"),
        (123, 456),
        ({}, {}),
        (object(), object()),
    ],
)
def test_malformed_passport_request_record_none(passport, request_arg):
    event = build(passport=passport, request=request_arg)
    assert event.passport_id is None
    assert event.agent_id is None
    assert event.operator_id is None
    assert event.requested_action is None
    assert event.resource_scope is None
    assert event.decision == DENY


def test_inputs_not_mutated():
    passport, request = load_passport(), dict(REQUEST)
    v, a, c = verif(DENY), authz(ALLOW), comp(DENY)
    snapshots = copy.deepcopy((passport, request, v, a, c))
    build(
        passport=passport,
        request=request,
        verification=v,
        authorization=a,
        composition=c,
    )
    assert (passport, request, v, a, c) == snapshots


def test_audit_event_is_frozen():
    event = build()
    with pytest.raises(dataclasses.FrozenInstanceError):
        event.decision = ALLOW


def test_no_sensitive_value_leak():
    text = event_text(build(passport=load_passport(), request=REQUEST))
    for sensitive in SENSITIVE_VALUES:
        assert sensitive not in text


def test_extra_request_fields_not_copied():
    request = {
        "action": "a",
        "resource_scope": "s",
        "secret_token": "TOPSECRET",
        "payload": {"x": "SECRETV"},
    }
    event = build(request=request)
    text = event_text(event)
    assert "TOPSECRET" not in text
    assert "SECRETV" not in text
    assert (event.requested_action, event.resource_scope) == ("a", "s")


def test_no_permission_lists_copied():
    text = event_text(build(passport=load_passport(), request=REQUEST))
    assert "access_secrets" not in text
    assert "send_external_summary" not in text
    assert "demo.secret_store" not in text


def test_error_is_audit_only():
    assert ERROR == "ERROR"
    for module in (verification, authorization, composition):
        assert ERROR not in module._DECISIONS
        assert not hasattr(module, "ERROR")


FORBIDDEN_IMPORTS = {
    "hashlib", "hmac", "secrets", "cryptography", "ssl", "socket", "urllib",
    "http", "requests", "httpx", "subprocess", "sqlite3", "shelve", "pickle",
    "logging", "rfc8785", "jcs", "sigstore", "cosign", "rekor", "fulcio",
    "boto3", "google", "azure", "passport_verifier",
}
FORBIDDEN_ENGINES = (
    "verify_passport_envelope",
    "authorize_action",
    "compose_decision",
    "passport_verifier",
)
FORBIDDEN_SINKS = (
    "open(", ".write(", "print(", "logging", "socket", "requests", "httpx",
    "subprocess", "hashlib", ".hexdigest", "sha256", "sqlite", "pickle",
    "previous_event", "chain(", "sign(",
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
