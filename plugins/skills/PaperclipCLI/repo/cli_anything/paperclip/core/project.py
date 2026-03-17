"""Project management — create, list, update, manage workspaces."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


VALID_STATUSES = ["backlog", "planned", "in_progress", "completed", "cancelled"]


def list_projects(client: PaperclipClient, company_id: str) -> list[dict[str, Any]]:
    """List all projects in a company."""
    resp = client.get(f"/companies/{company_id}/projects")
    if isinstance(resp, list):
        return resp
    return resp.get("projects", resp.get("data", []))


def get_project(client: PaperclipClient, project_id: str) -> dict[str, Any]:
    """Get project details."""
    return client.get(f"/projects/{project_id}")


def create_project(
    client: PaperclipClient,
    company_id: str,
    name: str,
    description: str = "",
    status: str = "backlog",
    lead_agent_id: str = "",
    target_date: str = "",
    color: str = "",
    goal_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Create a new project."""
    body: dict[str, Any] = {"name": name, "status": status}
    if description:
        body["description"] = description
    if lead_agent_id:
        body["leadAgentId"] = lead_agent_id
    if target_date:
        body["targetDate"] = target_date
    if color:
        body["color"] = color
    if goal_ids:
        body["goalIds"] = goal_ids
    return client.post(f"/companies/{company_id}/projects", body)


def update_project(
    client: PaperclipClient,
    project_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update project fields."""
    return client.patch(f"/projects/{project_id}", kwargs)


def create_workspace(
    client: PaperclipClient,
    project_id: str,
    cwd: str = "",
    repo_url: str = "",
    repo_ref: str = "",
    name: str = "",
    is_primary: bool = False,
) -> dict[str, Any]:
    """Create a workspace for a project."""
    body: dict[str, Any] = {}
    if cwd:
        body["cwd"] = cwd
    if repo_url:
        body["repoUrl"] = repo_url
    if repo_ref:
        body["repoRef"] = repo_ref
    if name:
        body["name"] = name
    if is_primary:
        body["isPrimary"] = True
    return client.post(f"/projects/{project_id}/workspaces", body)
