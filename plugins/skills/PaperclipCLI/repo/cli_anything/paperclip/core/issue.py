"""Issue/task management — create, list, update, checkout, comment."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


VALID_STATUSES = [
    "backlog", "todo", "in_progress", "in_review", "done", "blocked", "cancelled",
]

VALID_PRIORITIES = ["critical", "high", "medium", "low"]


def list_issues(
    client: PaperclipClient,
    company_id: str,
    status: str = "",
    assignee_agent_id: str = "",
    project_id: str = "",
    priority: str = "",
    limit: int = 50,
) -> list[dict[str, Any]]:
    """List issues in a company with optional filters."""
    params: dict[str, Any] = {"limit": limit}
    if status:
        params["status"] = status
    if assignee_agent_id:
        params["assigneeAgentId"] = assignee_agent_id
    if project_id:
        params["projectId"] = project_id
    if priority:
        params["priority"] = priority
    resp = client.get(f"/companies/{company_id}/issues", params)
    if isinstance(resp, list):
        return resp
    return resp.get("issues", resp.get("data", []))


def get_issue(client: PaperclipClient, issue_id: str) -> dict[str, Any]:
    """Get issue details."""
    return client.get(f"/issues/{issue_id}")


def create_issue(
    client: PaperclipClient,
    company_id: str,
    title: str,
    description: str = "",
    status: str = "backlog",
    priority: str = "medium",
    project_id: str = "",
    goal_id: str = "",
    parent_id: str = "",
    assignee_agent_id: str = "",
    billing_code: str = "",
    label_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Create a new issue."""
    body: dict[str, Any] = {"title": title, "status": status, "priority": priority}
    if description:
        body["description"] = description
    if project_id:
        body["projectId"] = project_id
    if goal_id:
        body["goalId"] = goal_id
    if parent_id:
        body["parentId"] = parent_id
    if assignee_agent_id:
        body["assigneeAgentId"] = assignee_agent_id
    if billing_code:
        body["billingCode"] = billing_code
    if label_ids:
        body["labelIds"] = label_ids
    return client.post(f"/companies/{company_id}/issues", body)


def update_issue(
    client: PaperclipClient,
    issue_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update issue fields."""
    return client.patch(f"/issues/{issue_id}", kwargs)


def checkout_issue(
    client: PaperclipClient,
    issue_id: str,
    agent_id: str,
    expected_statuses: list[str] | None = None,
) -> dict[str, Any]:
    """Checkout an issue to an agent for execution."""
    body: dict[str, Any] = {
        "agentId": agent_id,
        "expectedStatuses": expected_statuses or ["todo", "in_progress"],
    }
    return client.post(f"/issues/{issue_id}/checkout", body)


def release_issue(client: PaperclipClient, issue_id: str) -> dict[str, Any]:
    """Release an issue from agent execution."""
    return client.post(f"/issues/{issue_id}/release")


def get_comments(client: PaperclipClient, issue_id: str) -> list[dict[str, Any]]:
    """Get comments on an issue."""
    resp = client.get(f"/issues/{issue_id}/comments")
    if isinstance(resp, list):
        return resp
    return resp.get("comments", resp.get("data", []))


def add_comment(
    client: PaperclipClient,
    issue_id: str,
    body_text: str,
    reopen: bool = False,
    interrupt: bool = False,
) -> dict[str, Any]:
    """Add a comment to an issue."""
    body: dict[str, Any] = {"body": body_text}
    if reopen:
        body["reopen"] = True
    if interrupt:
        body["interrupt"] = True
    return client.post(f"/issues/{issue_id}/comments", body)


def get_heartbeat_context(client: PaperclipClient, issue_id: str) -> dict[str, Any]:
    """Get compact context for an issue (used by agents during heartbeats)."""
    return client.get(f"/issues/{issue_id}/heartbeat-context")
