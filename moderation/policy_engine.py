from __future__ import annotations

from pathlib import Path
import yaml

POLICY_DIR = Path(__file__).resolve().parents[1] / "config" / "policies"


def load_policy(country: str) -> dict:
    filename = {
        "IN": "india_demo_v1.yaml",
        "US": "us_demo_v1.yaml",
        "BD": "bd_demo_v1.yaml",
        "CUSTOM": "custom_demo_v1.yaml",
    }.get(country, "india_demo_v1.yaml")
    with (POLICY_DIR / filename).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_events(events: list[dict], policy: dict) -> dict:
    """
    Demonstration rule engine. It deliberately does not classify every detected object
    or transcript as harmful. Real rules must be validated and tied to authoritative sources.
    """
    configured = policy.get("rules", [])
    active_categories = {
        rule.get("category")
        for rule in configured
        if rule.get("enabled", True)
    }
    relevant = [e for e in events if e.get("category") in active_categories]

    if any(e.get("category") == "uncertain" for e in relevant):
        decision = "hold_for_review"
        summary = "Evidence is uncertain; review before publication."
    elif relevant:
        decision = "human_review"
        summary = f"{len(relevant)} event(s) match configured review categories."
    else:
        decision = "eligible_for_approval"
        summary = (
            "No configured policy category was triggered by this baseline. "
            "This does not prove the video is safe or legally compliant."
        )

    return {
        "decision": decision,
        "summary": summary,
        "policy_id": policy.get("policy_id"),
        "country": policy.get("country"),
        "policy_status": policy.get("status", "unknown"),
        "matched_event_count": len(relevant),
        "matched_events": relevant,
        "requires_human_review": decision != "eligible_for_approval",
    }
