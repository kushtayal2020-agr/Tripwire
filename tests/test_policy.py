from tripwire.policy import Policy


def test_blocks_risky_when_tainted(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert not p.check("send_email", {"to": "a@b.com"}, tainted=True).allowed


def test_allows_risky_when_clean(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert p.check("send_email", {"to": "a@b.com"}, tainted=False).allowed


def test_allows_safe_tool(tmp_path):
    p = Policy("block", log_path=str(tmp_path / "log.txt"))
    assert p.check("fetch_page", {}, tainted=True).allowed
