"""Regression test for the trace case in docs/trace_case.md (FM-03 ticket_trust, claim C-002).

On seeded_regression the agent believes the ticket's "5 days late" over the DB, so a model_override
event appears and a refund is written for a claim that must be denied. On fixed neither happens.
Run: python -m pytest -q -m student -o addopts= -k lab9_trace_case
"""
import json
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.student


def _trial(shape: str, claim_id: str, seed: int) -> dict:
    from lab9 import variants
    from lab9.eval import SPEC, load_spec, load_world, make_task

    variants.register()
    spec = load_spec(SPEC)
    world, claims = load_world(spec)
    labels = json.loads(Path(spec["labels"]).read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="lab9-trace-", ignore_cleanup_errors=True) as tmp:
        return make_task(shape, world, claims, labels, Path(tmp))({"claim_id": claim_id, "seed": seed}), labels[claim_id]


def _ctx(output: dict, label: dict):
    from types import SimpleNamespace

    return SimpleNamespace(output=output, expected_output=label)


def test_ticket_trust_is_caught_on_seeded_regression():
    from lab9.graders import DbFactKept, RefundAmountCorrect

    out, label = _trial("seeded_regression", "C-002", 11)
    assert any(e.get("kind") == "model_override" for e in out["events"])
    assert DbFactKept().evaluate(_ctx(out, label)).value is False
    assert RefundAmountCorrect().evaluate(_ctx(out, label)).value is False


def test_ticket_trust_is_absent_on_fixed():
    from lab9.graders import DbFactKept, RefundAmountCorrect

    out, label = _trial("fixed", "C-002", 11)
    assert DbFactKept().evaluate(_ctx(out, label)).value is True
    assert RefundAmountCorrect().evaluate(_ctx(out, label)).value is True


def test_misreport_is_caught_on_c008():
    """FM-08 seen on seeded_regression C-008@11: reply says 35.000đ, the ledger holds 20.000đ."""
    from lab9.graders import ReplyMatchesLedger

    bad, label = _trial("seeded_regression", "C-008", 11)
    good, _ = _trial("fixed", "C-008", 11)
    assert ReplyMatchesLedger().evaluate(_ctx(bad, label)).value is False
    assert ReplyMatchesLedger().evaluate(_ctx(good, label)).value is True
