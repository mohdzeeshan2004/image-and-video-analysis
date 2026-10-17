from moderation.policy_engine import evaluate_events


def test_no_matching_events_is_not_claimed_safe():
    result = evaluate_events([], {"policy_id": "test", "country": "IN", "status": "test", "rules": []})
    assert result["decision"] == "eligible_for_approval"
    assert "does not prove" in result["summary"]


def test_matching_event_requires_review():
    policy = {
        "policy_id": "test",
        "country": "IN",
        "status": "test",
        "rules": [{"category": "potential_physical_violence", "action": "human_review", "enabled": True}],
    }
    events = [{"category": "potential_physical_violence", "start_time": 1.0}]
    result = evaluate_events(events, policy)
    assert result["decision"] == "human_review"
    assert result["requires_human_review"] is True
