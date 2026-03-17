"""Approval management — create, list, resolve approval requests."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


VALID_TYPES = ["hire_agent", "approve_ceo_strategy"]
VALID_STATUSES = ["pending", "revision_requested", "approved", "rejected", "cancelled"]


def list_approvals(
    client: PaperclipClient,
    company_id: str,
    status: str = "",
) -> list[dict[str, Any]]:
    """List approvals in a company."""
    params: dict[str, Any] = {}
    if status:
        params["status"] = status
    resp = client.get(f"/companies/{company_id}/approvals", params)
    if isinstance(resp, list):
        return resp
    return resp.get("approvals", resp.get("data", []))


def get_approval(client: PaperclipClient, approval_id: str) -> dict[str, Any]:
    """Get approval details."""
    return client.get(f"/approvals/{approval_id}")


def create_approval(
    client: PaperclipClient,
    company_id: str,
    approval_type: str,
    payload: dict[str, Any],
    requested_by_agent_id: str = "",
    issue_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Create an approval request."""
    body: dict[str, Any] = {"type": approval_type, "payload": payload}
    if requested_by_agent_id:
        body["requestedByAgentId"] = requested_by_agent_id
    if issue_ids:
        body["issueIds"] = issue_ids
    return client.post(f"/companies/{company_id}/approvals", body)


def approve(
    client: PaperclipClient,
    approval_id: str,
    decision_note: str = "",
) -> dict[str, Any]:
    """Approve an approval request."""
    body: dict[str, Any] = {}
    if decision_note:
        body["decisionNote"] = decision_note
    return client.post(f"/approvals/{approval_id}/approve", body)


def reject(
    client: PaperclipClient,
    approval_id: str,
    decision_note: str = "",
) -> dict[str, Any]:
    """Reject an approval request."""
    body: dict[str, Any] = {}
    if decision_note:
        body["decisionNote"] = decision_note
    return client.post(f"/approvals/{approval_id}/reject", body)
