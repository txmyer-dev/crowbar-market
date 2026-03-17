"""E2E tests for cli-anything-paperclip.

These tests require a running Paperclip server. The server is a HARD
DEPENDENCY — tests will fail (not skip) if it is unreachable.

Also includes CLI subprocess tests using _resolve_cli().
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient, PaperclipError
from cli_anything.paperclip.core.session import Session, save_session, load_session, clear_session
from cli_anything.paperclip.core import company as company_mod
from cli_anything.paperclip.core import agent as agent_mod
from cli_anything.paperclip.core import issue as issue_mod
from cli_anything.paperclip.core import project as project_mod
from cli_anything.paperclip.core import goal as goal_mod
from cli_anything.paperclip.core import approval as approval_mod
from cli_anything.paperclip.core import export as export_mod


# ── Helpers ───────────────────────────────────────────────────────────

def _get_client() -> PaperclipClient:
    """Create a client pointing at the test server."""
    url = os.environ.get("PAPERCLIP_URL", "http://localhost:3100")
    api_key = os.environ.get("PAPERCLIP_API_KEY", "")
    return PaperclipClient(base_url=url, api_key=api_key)


def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev.

    Set env CLI_ANYTHING_FORCE_INSTALLED=1 to require the installed command.
    """
    import shutil
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = name.replace("cli-anything-", "cli_anything.") + "." + name.split("-")[-1] + "_cli"
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]


@pytest.fixture(scope="module")
def client():
    """Provide a PaperclipClient that talks to the real server."""
    c = _get_client()
    # Verify server is reachable — fail fast if not
    try:
        c.health()
    except PaperclipError as exc:
        pytest.fail(
            f"Paperclip server is not reachable at {c.base_url}. "
            f"Start it with: cd <paperclip-dir> && pnpm dev\n"
            f"Error: {exc}"
        )
    return c


@pytest.fixture(scope="module")
def test_company(client):
    """Create a test company for the E2E test session."""
    data = company_mod.create_company(client, f"E2E-Test-Co-{os.getpid()}")
    company_id = data.get("id") or data.get("company", {}).get("id", "")
    assert company_id, f"Failed to create test company: {data}"
    print(f"\n  Test company: {company_id}")
    return company_id


# ══════════════════════════════════════════════════════════════════════
#  Server Integration Tests
# ══════════════════════════════════════════════════════════════════════

class TestHealth:
    def test_health(self, client):
        """Server returns a valid health response."""
        data = client.health()
        assert isinstance(data, dict)
        print(f"\n  Health: {data}")


class TestCompanyLifecycle:
    def test_list_companies(self, client):
        """Can list companies."""
        companies = company_mod.list_companies(client)
        assert isinstance(companies, list)
        print(f"\n  Companies: {len(companies)}")

    def test_get_company(self, client, test_company):
        """Can get a specific company."""
        data = company_mod.get_company(client, test_company)
        assert data.get("id") == test_company or data.get("company", {}).get("id") == test_company
        print(f"\n  Company: {data.get('name', data.get('company', {}).get('name', ''))}")


class TestAgentLifecycle:
    def test_create_and_list_agents(self, client, test_company):
        """Create an agent and verify it appears in the list."""
        created = agent_mod.create_agent(
            client, test_company, f"TestBot-{os.getpid()}",
            role="engineer", title="Test Engineer",
        )
        agent_id = created.get("id") or created.get("agent", {}).get("id", "")
        assert agent_id, f"Failed to create agent: {created}"
        print(f"\n  Created agent: {agent_id}")

        agents = agent_mod.list_agents(client, test_company)
        ids = [a.get("id") for a in agents]
        assert agent_id in ids, f"Agent {agent_id} not in list: {ids}"


class TestIssueLifecycle:
    def test_create_and_get_issue(self, client, test_company):
        """Create an issue, retrieve it, add a comment."""
        created = issue_mod.create_issue(
            client, test_company, f"E2E Test Issue {os.getpid()}",
            description="Created by E2E test", priority="high",
        )
        issue_id = created.get("id") or created.get("issue", {}).get("id", "")
        assert issue_id, f"Failed to create issue: {created}"
        print(f"\n  Created issue: {issue_id}")

        fetched = issue_mod.get_issue(client, issue_id)
        assert fetched.get("id") == issue_id or fetched.get("issue", {}).get("id") == issue_id

        # Add comment
        comment = issue_mod.add_comment(client, issue_id, "E2E test comment")
        assert comment is not None
        print(f"\n  Added comment to {issue_id}")

        # List comments
        comments = issue_mod.get_comments(client, issue_id)
        assert isinstance(comments, list)


class TestProjectLifecycle:
    def test_create_and_list_projects(self, client, test_company):
        """Create a project and list it."""
        created = project_mod.create_project(
            client, test_company, f"E2E Project {os.getpid()}",
            description="Test project",
        )
        project_id = created.get("id") or created.get("project", {}).get("id", "")
        assert project_id, f"Failed to create project: {created}"
        print(f"\n  Created project: {project_id}")

        projects = project_mod.list_projects(client, test_company)
        assert isinstance(projects, list)


class TestGoalLifecycle:
    def test_create_and_list_goals(self, client, test_company):
        """Create a goal and list it."""
        created = goal_mod.create_goal(
            client, test_company, f"E2E Goal {os.getpid()}",
            level="team", status="planned",
        )
        goal_id = created.get("id") or created.get("goal", {}).get("id", "")
        assert goal_id, f"Failed to create goal: {created}"
        print(f"\n  Created goal: {goal_id}")

        goals = goal_mod.list_goals(client, test_company)
        assert isinstance(goals, list)


class TestDashboardAndActivity:
    def test_dashboard(self, client, test_company):
        """Dashboard returns data."""
        data = export_mod.get_dashboard(client, test_company)
        assert isinstance(data, dict)
        print(f"\n  Dashboard keys: {list(data.keys())}")

    def test_activity(self, client, test_company):
        """Activity log returns entries."""
        entries = export_mod.get_activity(client, test_company)
        assert isinstance(entries, list)
        print(f"\n  Activity entries: {len(entries)}")


class TestSessionPersistence:
    def test_session_roundtrip(self, tmp_path):
        """Session save and load round-trip."""
        save_session({"url": "http://test:3100", "company_id": "c1", "api_key": "k1"}, tmp_path)
        loaded = load_session(tmp_path)
        assert loaded["url"] == "http://test:3100"
        assert loaded["company_id"] == "c1"
        clear_session(tmp_path)
        assert load_session(tmp_path) == {}
        print(f"\n  Session round-trip: OK")


class TestIssueWorkflow:
    """Full workflow: create agent → create issue → assign → update status → comment → done."""

    def test_full_workflow(self, client, test_company):
        # Create an agent to be the assignee
        agent_data = agent_mod.create_agent(
            client, test_company, f"WorkflowBot-{os.getpid()}",
            role="engineer",
        )
        agent_id = agent_data.get("id") or agent_data.get("agent", {}).get("id", "")
        assert agent_id
        print(f"\n  Workflow agent: {agent_id}")

        # Create issue assigned to the agent
        created = issue_mod.create_issue(
            client, test_company, f"Workflow Issue {os.getpid()}",
            status="todo", priority="medium", assignee_agent_id=agent_id,
        )
        issue_id = created.get("id") or created.get("issue", {}).get("id", "")
        assert issue_id
        print(f"\n  Workflow issue: {issue_id}")

        # Update to in_progress (allowed because it has an assignee)
        issue_mod.update_issue(client, issue_id, status="in_progress")
        fetched = issue_mod.get_issue(client, issue_id)
        status = fetched.get("status") or fetched.get("issue", {}).get("status", "")
        assert status == "in_progress", f"Expected in_progress, got {status}"

        # Comment
        issue_mod.add_comment(client, issue_id, "Working on it...")

        # Mark done
        issue_mod.update_issue(client, issue_id, status="done")
        fetched = issue_mod.get_issue(client, issue_id)
        status = fetched.get("status") or fetched.get("issue", {}).get("status", "")
        assert status == "done", f"Expected done, got {status}"
        print(f"\n  Workflow complete: {issue_id} -> done")


# ══════════════════════════════════════════════════════════════════════
#  CLI Subprocess Tests
# ══════════════════════════════════════════════════════════════════════

class TestCLISubprocess:
    CLI_BASE = _resolve_cli("cli-anything-paperclip")

    def _run(self, args, check=True):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True, text=True,
            check=check,
        )

    def test_help(self):
        """--help exits 0 and shows usage."""
        result = self._run(["--help"])
        assert result.returncode == 0
        assert "paperclip" in result.stdout.lower() or "Usage" in result.stdout
        print(f"\n  --help: OK ({len(result.stdout)} chars)")

    def test_version(self):
        """--version shows version string."""
        result = self._run(["--version"])
        assert result.returncode == 0
        assert "1.0.0" in result.stdout
        print(f"\n  --version: {result.stdout.strip()}")

    def test_health_json(self, client):
        """--json health returns valid JSON."""
        result = self._run(["--json", "health"], check=False)
        if result.returncode != 0:
            pytest.fail(f"health command failed: {result.stderr}")
        data = json.loads(result.stdout)
        assert isinstance(data, dict)
        print(f"\n  --json health: {list(data.keys())}")

    def test_session_show_json(self):
        """--json session show returns JSON."""
        result = self._run(["--json", "session", "show"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "url" in data
        print(f"\n  session show: {data}")

    def test_company_list_json(self, client):
        """--json company list returns JSON array."""
        result = self._run(["--json", "company", "list"], check=False)
        if result.returncode != 0:
            pytest.fail(f"company list failed: {result.stderr}")
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        print(f"\n  company list: {len(data)} companies")

    def test_issue_create_json(self, client, test_company):
        """Create an issue via subprocess."""
        result = self._run([
            "--json", "--company", test_company,
            "issue", "create", "-t", f"Subprocess Issue {os.getpid()}",
        ], check=False)
        if result.returncode != 0:
            pytest.fail(f"issue create failed: {result.stderr}")
        data = json.loads(result.stdout)
        issue_id = data.get("id") or data.get("issue", {}).get("id", "")
        assert issue_id
        print(f"\n  Created via subprocess: {issue_id}")

    def test_agent_list_json(self, client, test_company):
        """List agents via subprocess."""
        result = self._run([
            "--json", "--company", test_company, "agent", "list",
        ], check=False)
        if result.returncode != 0:
            pytest.fail(f"agent list failed: {result.stderr}")
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        print(f"\n  agent list: {len(data)} agents")

    def test_full_workflow_subprocess(self, client, test_company):
        """Full workflow via subprocess: create agent → create issue → assign → update → verify."""
        # Create agent
        result = self._run([
            "--json", "--company", test_company,
            "agent", "create", "-n", f"SubBot-{os.getpid()}", "-r", "engineer",
        ], check=False)
        if result.returncode != 0:
            pytest.fail(f"agent create failed: {result.stderr}")
        agent_data = json.loads(result.stdout)
        agent_id = agent_data.get("id") or agent_data.get("agent", {}).get("id", "")
        assert agent_id
        print(f"\n  Subprocess workflow agent: {agent_id}")

        # Create issue with assignee
        result = self._run([
            "--json", "--company", test_company,
            "issue", "create", "-t", f"Full E2E Sub {os.getpid()}",
            "--priority", "high", "--assignee", agent_id,
        ], check=False)
        if result.returncode != 0:
            pytest.fail(f"issue create failed: {result.stderr}")
        data = json.loads(result.stdout)
        issue_id = data.get("id") or data.get("issue", {}).get("id", "")
        assert issue_id
        print(f"\n  Subprocess workflow issue: {issue_id}")

        # Update status to in_progress
        result = self._run([
            "--json", "issue", "update", issue_id, "--status", "in_progress",
        ], check=False)
        if result.returncode != 0:
            pytest.fail(f"issue update failed: {result.stderr}")

        # Get and verify
        result = self._run(["--json", "issue", "get", issue_id], check=False)
        if result.returncode != 0:
            pytest.fail(f"issue get failed: {result.stderr}")
        data = json.loads(result.stdout)
        status = data.get("status") or data.get("issue", {}).get("status", "")
        assert status == "in_progress", f"Expected in_progress, got {status}"
        print(f"\n  Subprocess workflow: issue updated to in_progress")
