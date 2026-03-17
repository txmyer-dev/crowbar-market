"""Agent management — create, list, update, invoke heartbeats, manage API keys."""

from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


VALID_ROLES = [
    "general", "ceo", "cto", "cmo", "cfo", "engineer", "designer",
    "pm", "qa", "devops", "researcher",
]

VALID_ADAPTER_TYPES = [
    "process", "http", "claude_local", "codex_local", "opencode_local",
    "pi_local", "cursor", "openclaw_gateway", "hermes_local",
]

VALID_STATUSES = [
    "active", "paused", "idle", "running", "error",
    "pending_approval", "terminated",
]


def list_agents(client: PaperclipClient, company_id: str) -> list[dict[str, Any]]:
    """List all agents in a company."""
    resp = client.get(f"/companies/{company_id}/agents")
    if isinstance(resp, list):
        return resp
    return resp.get("agents", resp.get("data", []))


def get_agent(client: PaperclipClient, agent_id: str) -> dict[str, Any]:
    """Get agent details by ID."""
    return client.get(f"/agents/{agent_id}")


def get_me(client: PaperclipClient) -> dict[str, Any]:
    """Get the current agent's identity (requires agent API key)."""
    return client.get("/agents/me")


def create_agent(
    client: PaperclipClient,
    company_id: str,
    name: str,
    role: str = "general",
    title: str = "",
    adapter_type: str = "process",
    reports_to: str = "",
    capabilities: str = "",
    budget_monthly_cents: int = 0,
    adapter_config: dict | None = None,
    runtime_config: dict | None = None,
    metadata: dict | None = None,
) -> dict[str, Any]:
    """Create a new agent in a company."""
    body: dict[str, Any] = {"name": name, "role": role, "adapterType": adapter_type}
    if title:
        body["title"] = title
    if reports_to:
        body["reportsTo"] = reports_to
    if capabilities:
        body["capabilities"] = capabilities
    if budget_monthly_cents > 0:
        body["budgetMonthlyCents"] = budget_monthly_cents
    if adapter_config:
        body["adapterConfig"] = adapter_config
    if runtime_config:
        body["runtimeConfig"] = runtime_config
    if metadata:
        body["metadata"] = metadata
    return client.post(f"/companies/{company_id}/agents", body)


def update_agent(
    client: PaperclipClient,
    agent_id: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Update agent fields. Pass only the fields to change."""
    return client.patch(f"/agents/{agent_id}", kwargs)


def invoke_heartbeat(client: PaperclipClient, agent_id: str) -> dict[str, Any]:
    """Manually invoke an agent's heartbeat."""
    return client.post(f"/agents/{agent_id}/heartbeat/invoke")


def wakeup_agent(client: PaperclipClient, agent_id: str, reason: str = "") -> dict[str, Any]:
    """Send a wakeup request to an agent."""
    body: dict[str, Any] = {}
    if reason:
        body["reason"] = reason
    return client.post(f"/agents/{agent_id}/wakeup", body)


def get_runtime_state(client: PaperclipClient, agent_id: str) -> dict[str, Any]:
    """Get agent runtime state (session, tokens, costs)."""
    return client.get(f"/agents/{agent_id}/runtime-state")


def list_heartbeat_runs(
    client: PaperclipClient, company_id: str, agent_id: str = "", limit: int = 20
) -> list[dict[str, Any]]:
    """List heartbeat runs for a company, optionally filtered by agent."""
    params: dict[str, Any] = {"limit": limit}
    if agent_id:
        params["agentId"] = agent_id
    resp = client.get(f"/companies/{company_id}/heartbeat-runs", params)
    if isinstance(resp, list):
        return resp
    return resp.get("runs", resp.get("data", []))


def cancel_heartbeat_run(client: PaperclipClient, run_id: str) -> dict[str, Any]:
    """Cancel a running heartbeat."""
    return client.post(f"/heartbeat-runs/{run_id}/cancel")
