from tripwire.policy import Policy


def test_rejects_invalid_mode():
    try:
        Policy("allow")
    except ValueError as exc:
        assert str(exc) == "mode must be 'block' or 'confirm'"
    else:
        raise AssertionError("invalid policy mode should raise ValueError")


def test_blocks_risky_when_tainted(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert not p.check("send_email", {"to": "a@b.com"}, tainted=True).allowed


def test_allows_risky_when_clean(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert p.check("send_email", {"to": "a@b.com"}, tainted=False).allowed


def test_allows_safe_tool(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert p.check("fetch_page", {}, tainted=True).allowed


def test_blocks_application_specific_risky_tool(tmp_path):
    p = Policy(
        "block",
        log_path=str(tmp_path / "log.txt"),
        extra_risky_tools={"publish_release"},
    )
    decision = p.check("publish_release", {"version": "1.2.3"}, tainted=True)
    assert not decision.allowed
    assert "publish_release" in decision.reason


def test_confirm_mode_accepts_whitespace_and_uppercase_yes(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.input", lambda _: " Y ")
    p = Policy("confirm", log_path=str(tmp_path / "log.txt"))

    assert p.check("send_email", {}, tainted=True).allowed


def test_confirm_mode_denies_unless_user_explicitly_confirms(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.input", lambda _: "")
    p = Policy("confirm", log_path=str(tmp_path / "log.txt"))

    decision = p.check("send_email", {}, tainted=True)

    assert not decision.allowed
    assert "user denied" in decision.reason
