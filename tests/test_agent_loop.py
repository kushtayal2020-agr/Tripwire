from tripwire.agent_loop import parse_action


def test_parse_action_with_prose_and_json():
    assert parse_action('Here is the action: {"tool":"fetch_page","args":{"url":"demo"}}') == {
        "tool": "fetch_page",
        "args": {"url": "demo"},
    }


def test_parse_action_skips_invalid_json_before_valid_action():
    assert parse_action('Example: {not json}. Actual action: {"final":"done"}') == {
        "final": "done",
    }


def test_parse_action_returns_text_when_no_object_is_found():
    assert parse_action("The answer is 42.") == {"final": "The answer is 42."}
