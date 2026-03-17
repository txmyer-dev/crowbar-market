"""Export / reporting — dashboard overview, activity log, cost tracking.

For Paperclip, 'export' means extracting data from the server for reporting.
The real software (Paperclip server) is always the source of truth.
"""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


def get_dashboard(client: PaperclipClient, company_id: str) -> dict[str, Any]:
    """Get dashboard overview data for a company."""
    return client.get(f"/companies/{company_id}/dashboard")


def get_activity(
    client: PaperclipClient,
    company_id: str,
    entity_type: str = "",
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get activity log entries for a company."""
    params: dict[str, Any] = {"limit": limit}
    if entity_type:
        params["entityType"] = entity_type
    resp = client.get(f"/companies/{company_id}/activity", params)
    if isinstance(resp, list):
        return resp
    return resp.get("activity", resp.get("data", []))


def get_costs_summary(
    client: PaperclipClient,
    company_id: str,
) -> dict[str, Any]:
    """Get cost summary for a company."""
    return client.get(f"/companies/{company_id}/costs/summary")


def get_costs_by_agent(
    client: PaperclipClient,
    company_id: str,
) -> list[dict[str, Any]]:
    """Get costs broken down by agent."""
    resp = client.get(f"/companies/{company_id}/costs/by-agent")
    if isinstance(resp, list):
        return resp
    return resp.get("data", [])


def get_costs_by_project(
    client: PaperclipClient,
    company_id: str,
) -> list[dict[str, Any]]:
    """Get costs broken down by project."""
    resp = client.get(f"/companies/{company_id}/costs/by-project")
    if isinstance(resp, list):
        return resp
    return resp.get("data", [])


def get_sidebar_badges(client: PaperclipClient, company_id: str) -> dict[str, Any]:
    """Get sidebar badge counts (pending approvals, unread issues, etc.)."""
    return client.get(f"/companies/{company_id}/sidebar-badges")
