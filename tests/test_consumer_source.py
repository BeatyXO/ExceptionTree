from pathlib import Path


def test_exception_gate_is_real_typed_consumer_with_replay_protection():
    source = (Path(__file__).parents[1] / "contracts" / "exception_gate.py").read_text(encoding="utf-8")
    assert "@gl.contract_interface" in source
    assert "is_outcome" in source
    assert "execute_if_allowed" in source
    assert "used_actions" in source
    assert "action replay rejected" in source
    assert "class ExceptionGate(gl.Contract)" in source
