"""Goal management — create, list, update hierarchical goals."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


VALID_LEVELS = ["company", "team", "agent", "task"]
VALID_STATUSES = ["planned", "active", "achieved", "cancelled"]


def list_goals(client: PaperclipClient, company_id: str) -> list[dict[str, Any]]:
    """List all goals in a company."""
    resp = client.get(f"/companies/{company_id}/goals")
    if isinstance(resp, list):
        return resp
    return resp.get("goals", resp.get("data", []))


def get_goal(client: PaperclipClient, goal_id: str) -> dict[str, Any]:
    """Get goal details."""
    return client.get(f"/goals/{goal_id}")


def create_goal(
    client: PaperclipClient,
    company_id: str,
    title: str,
    description: str = "",
    level: str = "task",
    status: str = "planned",
    parent_id: str = "",
    owner_agent_id: str = "",
) -> dict[str, Any]:
    """Create a new goal."""
    body: dict[str, Any] = {"title": title, "level": level, "status": status}
    if description:
        body["description"] = description
    if parent_id:
        body["parentId"] = parent_id
    if owner_agent_id:
        body["ownerAgentId"] = owner_agent_id
    return client.post(f"/companies/{company_id}/goals", body)


def update_goal(
    client: PaperclipClient,
    goal_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update goal fields."""
    return client.patch(f"/goals/{goal_id}", kwargs)
