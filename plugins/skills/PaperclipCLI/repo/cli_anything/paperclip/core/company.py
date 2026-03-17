"""Company management — create, list, update, inspect companies."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


def list_companies(client: PaperclipClient) -> list[dict[str, Any]]:
    """List all companies."""
    resp = client.get("/companies")
    if isinstance(resp, list):
        return resp
    return resp.get("companies", resp.get("data", []))


def get_company(client: PaperclipClient, company_id: str) -> dict[str, Any]:
    """Get company details."""
    return client.get(f"/companies/{company_id}")


def create_company(
    client: PaperclipClient,
    name: str,
    description: str = "",
    budget_monthly_cents: int = 0,
) -> dict[str, Any]:
    """Create a new company."""
    body: dict[str, Any] = {"name": name}
    if description:
        body["description"] = description
    if budget_monthly_cents > 0:
        body["budgetMonthlyCents"] = budget_monthly_cents
    return client.post("/companies", body)


def update_company(
    client: PaperclipClient,
    company_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update company fields. Pass only the fields to change."""
    return client.patch(f"/companies/{company_id}", kwargs)


def export_company(client: PaperclipClient, company_id: str) -> dict[str, Any]:
    """Export a company configuration."""
    return client.get(f"/companies/{company_id}/export")


def import_company(client: PaperclipClient, data: dict[str, Any]) -> dict[str, Any]:
    """Import a company configuration."""
    return client.post("/companies/import", data)
