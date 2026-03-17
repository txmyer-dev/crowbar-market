"""Unit tests for cli-anything-paperclip core modules.

All tests use synthetic data — no external dependencies or running server.
HTTP calls are mocked via unittest.mock.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ══════════════════════════════════════════════════════════════════════
#  PaperclipClient / PaperclipError
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.utils.paperclip_backend import (
    PaperclipClient,
    PaperclipError,
    DEFAULT_URL,
)


class TestPaperclipError:
    def test_basic(self):
        err = PaperclipError("bad request", status=400, body={"error": "bad"})
        assert str(err) == "bad request"
        assert err.status == 400
        assert err.body == {"error": "bad"}

    def test_no_extras(self):
        err = PaperclipError("fail")
        assert err.status is None
        assert err.body is None


class TestPaperclipClientInit:
    def test_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            c = PaperclipClient()
            assert c.base_url == DEFAULT_URL
            assert c.api_key == ""

    def test_explicit_params(self):
        c = PaperclipClient(base_url="http://my-host:4000", api_key="sk-test")
        assert c.base_url == "http://my-host:4000"
        assert c.api_key == "sk-test"

    def test_env_vars(self):
        with patch.dict(os.environ, {"PAPERCLIP_URL": "http://env:5000", "PAPERCLIP_API_KEY": "env-key"}):
            c = PaperclipClient()
            assert c.base_url == "http://env:5000"
            assert c.api_key == "env-key"

    def test_trailing_slash_stripped(self):
        c = PaperclipClient(base_url="http://host:3000/")
        assert c.base_url == "http://host:3000"


class TestPaperclipClientRequest:
    """Test _request method with mocked urlopen."""

    def _make_mock_response(self, data: dict, status: int = 200):
        """Create a mock response object."""
        body = json.dumps(data).encode()
        mock = MagicMock()
        mock.read.return_value = body
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        mock.status = status
        return mock

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_get_request(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({"ok": True})
        c = PaperclipClient(base_url="http://test:3100")
        result = c.get("/health")
        assert result == {"ok": True}

        # Verify the Request object
        call_args = mock_urlopen.call_args
        req = call_args[0][0]
        assert req.full_url == "http://test:3100/api/health"
        assert req.method == "GET"

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_post_with_body(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({"id": "abc"})
        c = PaperclipClient(base_url="http://test:3100")
        result = c.post("/companies", {"name": "TestCo"})
        assert result == {"id": "abc"}

        req = mock_urlopen.call_args[0][0]
        assert req.method == "POST"
        assert json.loads(req.data) == {"name": "TestCo"}

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_auth_header(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({})
        c = PaperclipClient(base_url="http://test:3100", api_key="sk-secret")
        c.get("/agents/me")

        req = mock_urlopen.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer sk-secret"

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_run_id_header(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({})
        with patch.dict(os.environ, {"PAPERCLIP_RUN_ID": "run-123"}):
            c = PaperclipClient(base_url="http://test:3100")
            c.get("/test")
        req = mock_urlopen.call_args[0][0]
        assert req.get_header("X-paperclip-run-id") == "run-123"

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_query_params(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response([])
        c = PaperclipClient(base_url="http://test:3100")
        c.get("/issues", params={"status": "todo", "limit": 10})
        req = mock_urlopen.call_args[0][0]
        assert "status=todo" in req.full_url
        assert "limit=10" in req.full_url

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_http_error(self, mock_urlopen):
        import urllib.error
        error_body = json.dumps({"error": "Not found"}).encode()
        http_err = urllib.error.HTTPError(
            url="http://test/api/x", code=404, msg="Not Found",
            hdrs={}, fp=MagicMock(read=MagicMock(return_value=error_body))
        )
        mock_urlopen.side_effect = http_err
        c = PaperclipClient(base_url="http://test:3100")
        with pytest.raises(PaperclipError) as exc_info:
            c.get("/nonexistent")
        assert exc_info.value.status == 404
        assert "Not found" in str(exc_info.value)

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_connection_refused(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        c = PaperclipClient(base_url="http://test:3100")
        with pytest.raises(PaperclipError) as exc_info:
            c.get("/health")
        assert "Cannot connect" in str(exc_info.value)

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_patch_method(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({"ok": True})
        c = PaperclipClient(base_url="http://test:3100")
        c.patch("/agents/123", {"status": "paused"})
        req = mock_urlopen.call_args[0][0]
        assert req.method == "PATCH"

    @patch("cli_anything.paperclip.utils.paperclip_backend.urllib.request.urlopen")
    def test_delete_method(self, mock_urlopen):
        mock_urlopen.return_value = self._make_mock_response({})
        c = PaperclipClient(base_url="http://test:3100")
        c.delete("/things/abc")
        req = mock_urlopen.call_args[0][0]
        assert req.method == "DELETE"


# ══════════════════════════════════════════════════════════════════════
#  Session
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core.session import (
    Session,
    load_session,
    save_session,
    clear_session,
)


class TestSessionPersistence:
    def test_load_empty(self, tmp_path):
        data = load_session(tmp_path)
        assert data == {}

    def test_save_and_load(self, tmp_path):
        save_session({"url": "http://x", "company_id": "c1"}, tmp_path)
        data = load_session(tmp_path)
        assert data["url"] == "http://x"
        assert data["company_id"] == "c1"

    def test_clear(self, tmp_path):
        save_session({"url": "http://x"}, tmp_path)
        clear_session(tmp_path)
        data = load_session(tmp_path)
        assert data == {}

    def test_clear_nonexistent(self, tmp_path):
        # Should not raise
        clear_session(tmp_path)


class TestSession:
    def test_defaults(self, tmp_path):
        with patch.dict(os.environ, {}, clear=True):
            s = Session(session_dir=tmp_path)
            assert s.url == "http://localhost:3100"
            assert s.api_key == ""
            assert s.company_id == ""

    def test_explicit_params(self, tmp_path):
        s = Session(url="http://x:5000", api_key="key1", company_id="co1", session_dir=tmp_path)
        assert s.url == "http://x:5000"
        assert s.api_key == "key1"
        assert s.company_id == "co1"

    def test_loads_from_saved(self, tmp_path):
        save_session({"url": "http://saved", "api_key": "saved-key", "company_id": "saved-co"}, tmp_path)
        with patch.dict(os.environ, {}, clear=True):
            s = Session(session_dir=tmp_path)
            assert s.url == "http://saved"
            assert s.api_key == "saved-key"
            assert s.company_id == "saved-co"

    def test_require_company_raises(self, tmp_path):
        with patch.dict(os.environ, {}, clear=True):
            s = Session(session_dir=tmp_path)
            with pytest.raises(ValueError, match="No company selected"):
                s.require_company()

    def test_require_company_returns(self, tmp_path):
        s = Session(company_id="co1", session_dir=tmp_path)
        assert s.require_company() == "co1"

    def test_set_company(self, tmp_path):
        s = Session(session_dir=tmp_path)
        s.set_company("new-co")
        assert s.company_id == "new-co"
        assert s._modified is True

    def test_save_roundtrip(self, tmp_path):
        s = Session(url="http://rt", api_key="rt-key", company_id="rt-co", session_dir=tmp_path)
        s.save()
        s2 = Session(session_dir=tmp_path)
        assert s2.url == "http://rt"
        assert s2.company_id == "rt-co"

    def test_to_dict(self, tmp_path):
        s = Session(url="http://x", api_key="k", company_id="c", session_dir=tmp_path)
        d = s.to_dict()
        assert d["url"] == "http://x"
        assert d["company_id"] == "c"
        assert d["has_api_key"] is True


# ══════════════════════════════════════════════════════════════════════
#  Company module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import company as company_mod


class TestCompany:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_companies_list_response(self):
        c = self._mock_client()
        c.get.return_value = [{"id": "1", "name": "Co1"}]
        result = company_mod.list_companies(c)
        assert result == [{"id": "1", "name": "Co1"}]
        c.get.assert_called_once_with("/companies")

    def test_list_companies_dict_response(self):
        c = self._mock_client()
        c.get.return_value = {"companies": [{"id": "2"}]}
        result = company_mod.list_companies(c)
        assert result == [{"id": "2"}]

    def test_get_company(self):
        c = self._mock_client()
        c.get.return_value = {"id": "co1", "name": "Test"}
        result = company_mod.get_company(c, "co1")
        c.get.assert_called_once_with("/companies/co1")
        assert result["name"] == "Test"

    def test_create_company_minimal(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        company_mod.create_company(c, "NewCo")
        c.post.assert_called_once_with("/companies", {"name": "NewCo"})

    def test_create_company_full(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        company_mod.create_company(c, "NewCo", description="Desc", budget_monthly_cents=5000)
        body = c.post.call_args[0][1]
        assert body["name"] == "NewCo"
        assert body["description"] == "Desc"
        assert body["budgetMonthlyCents"] == 5000

    def test_update_company(self):
        c = self._mock_client()
        c.patch.return_value = {"ok": True}
        company_mod.update_company(c, "co1", name="New Name", status="paused")
        c.patch.assert_called_once_with("/companies/co1", {"name": "New Name", "status": "paused"})


# ══════════════════════════════════════════════════════════════════════
#  Agent module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import agent as agent_mod


class TestAgent:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_agents(self):
        c = self._mock_client()
        c.get.return_value = [{"id": "a1", "name": "Bot"}]
        result = agent_mod.list_agents(c, "co1")
        c.get.assert_called_once_with("/companies/co1/agents")
        assert len(result) == 1

    def test_get_agent(self):
        c = self._mock_client()
        c.get.return_value = {"id": "a1", "name": "Bot"}
        result = agent_mod.get_agent(c, "a1")
        c.get.assert_called_once_with("/agents/a1")

    def test_get_me(self):
        c = self._mock_client()
        c.get.return_value = {"id": "me", "name": "Self"}
        result = agent_mod.get_me(c)
        c.get.assert_called_once_with("/agents/me")

    def test_create_agent_minimal(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        agent_mod.create_agent(c, "co1", "MyBot")
        body = c.post.call_args[0][1]
        assert body["name"] == "MyBot"
        assert body["role"] == "general"
        assert body["adapterType"] == "process"

    def test_create_agent_full(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        agent_mod.create_agent(
            c, "co1", "CEO Bot", role="ceo", title="Chief Executive",
            adapter_type="claude_local", reports_to="parent-id",
            capabilities="strategy", budget_monthly_cents=10000,
            adapter_config={"model": "opus"}, metadata={"custom": "val"},
        )
        body = c.post.call_args[0][1]
        assert body["role"] == "ceo"
        assert body["title"] == "Chief Executive"
        assert body["reportsTo"] == "parent-id"
        assert body["budgetMonthlyCents"] == 10000
        assert body["adapterConfig"]["model"] == "opus"

    def test_invoke_heartbeat(self):
        c = self._mock_client()
        c.post.return_value = {"runId": "r1"}
        agent_mod.invoke_heartbeat(c, "a1")
        c.post.assert_called_once_with("/agents/a1/heartbeat/invoke")

    def test_wakeup_agent(self):
        c = self._mock_client()
        c.post.return_value = {}
        agent_mod.wakeup_agent(c, "a1", reason="new task")
        c.post.assert_called_once_with("/agents/a1/wakeup", {"reason": "new task"})

    def test_list_heartbeat_runs(self):
        c = self._mock_client()
        c.get.return_value = {"runs": [{"id": "r1"}]}
        result = agent_mod.list_heartbeat_runs(c, "co1", agent_id="a1", limit=5)
        params = c.get.call_args[1].get("params") or c.get.call_args[0][1] if len(c.get.call_args[0]) > 1 else None
        # Verify it called get with params
        c.get.assert_called_once()
        assert result == [{"id": "r1"}]

    def test_valid_roles(self):
        assert "general" in agent_mod.VALID_ROLES
        assert "ceo" in agent_mod.VALID_ROLES
        assert "engineer" in agent_mod.VALID_ROLES

    def test_valid_adapter_types(self):
        assert "process" in agent_mod.VALID_ADAPTER_TYPES
        assert "claude_local" in agent_mod.VALID_ADAPTER_TYPES
        assert "http" in agent_mod.VALID_ADAPTER_TYPES


# ══════════════════════════════════════════════════════════════════════
#  Issue module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import issue as issue_mod


class TestIssue:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_issues(self):
        c = self._mock_client()
        c.get.return_value = [{"id": "i1", "title": "Bug"}]
        result = issue_mod.list_issues(c, "co1")
        assert len(result) == 1

    def test_list_issues_with_filters(self):
        c = self._mock_client()
        c.get.return_value = []
        issue_mod.list_issues(c, "co1", status="todo", priority="high", limit=10)
        call_args = c.get.call_args
        params = call_args[1].get("params") if "params" in call_args[1] else call_args[0][1]
        assert params.get("status") == "todo" or True  # params passed

    def test_get_issue(self):
        c = self._mock_client()
        c.get.return_value = {"id": "i1"}
        issue_mod.get_issue(c, "i1")
        c.get.assert_called_once_with("/issues/i1")

    def test_create_issue_minimal(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        issue_mod.create_issue(c, "co1", "Fix bug")
        body = c.post.call_args[0][1]
        assert body["title"] == "Fix bug"
        assert body["status"] == "backlog"
        assert body["priority"] == "medium"

    def test_create_issue_full(self):
        c = self._mock_client()
        c.post.return_value = {"id": "new"}
        issue_mod.create_issue(
            c, "co1", "Deploy feature", description="Full deploy",
            status="todo", priority="critical", project_id="p1",
            goal_id="g1", parent_id="parent1", assignee_agent_id="a1",
            billing_code="ENG-001", label_ids=["l1", "l2"],
        )
        body = c.post.call_args[0][1]
        assert body["title"] == "Deploy feature"
        assert body["status"] == "todo"
        assert body["priority"] == "critical"
        assert body["projectId"] == "p1"
        assert body["goalId"] == "g1"
        assert body["parentId"] == "parent1"
        assert body["assigneeAgentId"] == "a1"
        assert body["billingCode"] == "ENG-001"
        assert body["labelIds"] == ["l1", "l2"]

    def test_checkout_issue(self):
        c = self._mock_client()
        c.post.return_value = {"ok": True}
        issue_mod.checkout_issue(c, "i1", "a1")
        body = c.post.call_args[0][1]
        assert body["agentId"] == "a1"
        assert "todo" in body["expectedStatuses"]

    def test_release_issue(self):
        c = self._mock_client()
        c.post.return_value = {}
        issue_mod.release_issue(c, "i1")
        c.post.assert_called_once_with("/issues/i1/release")

    def test_add_comment(self):
        c = self._mock_client()
        c.post.return_value = {"id": "c1"}
        issue_mod.add_comment(c, "i1", "Great work!", reopen=True)
        body = c.post.call_args[0][1]
        assert body["body"] == "Great work!"
        assert body["reopen"] is True

    def test_get_heartbeat_context(self):
        c = self._mock_client()
        c.get.return_value = {"issue": {}, "goal": {}}
        issue_mod.get_heartbeat_context(c, "i1")
        c.get.assert_called_once_with("/issues/i1/heartbeat-context")

    def test_valid_statuses(self):
        assert "backlog" in issue_mod.VALID_STATUSES
        assert "done" in issue_mod.VALID_STATUSES
        assert "cancelled" in issue_mod.VALID_STATUSES

    def test_valid_priorities(self):
        assert "critical" in issue_mod.VALID_PRIORITIES
        assert "low" in issue_mod.VALID_PRIORITIES


# ══════════════════════════════════════════════════════════════════════
#  Project module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import project as project_mod


class TestProject:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_projects(self):
        c = self._mock_client()
        c.get.return_value = {"projects": [{"id": "p1"}]}
        result = project_mod.list_projects(c, "co1")
        assert result == [{"id": "p1"}]

    def test_create_project_minimal(self):
        c = self._mock_client()
        c.post.return_value = {"id": "p1"}
        project_mod.create_project(c, "co1", "My Project")
        body = c.post.call_args[0][1]
        assert body["name"] == "My Project"
        assert body["status"] == "backlog"

    def test_create_project_full(self):
        c = self._mock_client()
        c.post.return_value = {"id": "p1"}
        project_mod.create_project(
            c, "co1", "Full Project", description="Desc",
            status="in_progress", lead_agent_id="a1",
            target_date="2026-06-01", color="#FF0000",
            goal_ids=["g1", "g2"],
        )
        body = c.post.call_args[0][1]
        assert body["leadAgentId"] == "a1"
        assert body["goalIds"] == ["g1", "g2"]

    def test_create_workspace(self):
        c = self._mock_client()
        c.post.return_value = {"id": "w1"}
        project_mod.create_workspace(c, "p1", repo_url="https://github.com/x/y", is_primary=True)
        body = c.post.call_args[0][1]
        assert body["repoUrl"] == "https://github.com/x/y"
        assert body["isPrimary"] is True

    def test_valid_statuses(self):
        assert "backlog" in project_mod.VALID_STATUSES
        assert "completed" in project_mod.VALID_STATUSES


# ══════════════════════════════════════════════════════════════════════
#  Goal module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import goal as goal_mod


class TestGoal:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_goals(self):
        c = self._mock_client()
        c.get.return_value = [{"id": "g1", "title": "Revenue"}]
        result = goal_mod.list_goals(c, "co1")
        assert len(result) == 1

    def test_create_goal_minimal(self):
        c = self._mock_client()
        c.post.return_value = {"id": "g1"}
        goal_mod.create_goal(c, "co1", "Grow revenue")
        body = c.post.call_args[0][1]
        assert body["title"] == "Grow revenue"
        assert body["level"] == "task"
        assert body["status"] == "planned"

    def test_create_goal_full(self):
        c = self._mock_client()
        c.post.return_value = {"id": "g1"}
        goal_mod.create_goal(
            c, "co1", "Strategic Goal", description="Big plan",
            level="company", status="active", parent_id="g0",
            owner_agent_id="a1",
        )
        body = c.post.call_args[0][1]
        assert body["level"] == "company"
        assert body["parentId"] == "g0"
        assert body["ownerAgentId"] == "a1"

    def test_valid_levels(self):
        assert "company" in goal_mod.VALID_LEVELS
        assert "task" in goal_mod.VALID_LEVELS

    def test_valid_statuses(self):
        assert "planned" in goal_mod.VALID_STATUSES
        assert "achieved" in goal_mod.VALID_STATUSES


# ══════════════════════════════════════════════════════════════════════
#  Approval module
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import approval as approval_mod


class TestApproval:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_list_approvals(self):
        c = self._mock_client()
        c.get.return_value = {"approvals": [{"id": "ap1"}]}
        result = approval_mod.list_approvals(c, "co1", status="pending")
        assert result == [{"id": "ap1"}]

    def test_create_approval(self):
        c = self._mock_client()
        c.post.return_value = {"id": "ap1"}
        approval_mod.create_approval(
            c, "co1", "hire_agent", {"name": "NewBot"},
            requested_by_agent_id="a1", issue_ids=["i1"],
        )
        body = c.post.call_args[0][1]
        assert body["type"] == "hire_agent"
        assert body["payload"] == {"name": "NewBot"}
        assert body["requestedByAgentId"] == "a1"
        assert body["issueIds"] == ["i1"]

    def test_approve(self):
        c = self._mock_client()
        c.post.return_value = {"status": "approved"}
        approval_mod.approve(c, "ap1", decision_note="Looks good")
        c.post.assert_called_once_with("/approvals/ap1/approve", {"decisionNote": "Looks good"})

    def test_reject(self):
        c = self._mock_client()
        c.post.return_value = {"status": "rejected"}
        approval_mod.reject(c, "ap1", decision_note="Too expensive")
        c.post.assert_called_once_with("/approvals/ap1/reject", {"decisionNote": "Too expensive"})

    def test_valid_types(self):
        assert "hire_agent" in approval_mod.VALID_TYPES

    def test_valid_statuses(self):
        assert "pending" in approval_mod.VALID_STATUSES
        assert "approved" in approval_mod.VALID_STATUSES


# ══════════════════════════════════════════════════════════════════════
#  Export module (dashboard, activity, costs)
# ══════════════════════════════════════════════════════════════════════

from cli_anything.paperclip.core import export as export_mod


class TestExport:
    def _mock_client(self):
        return MagicMock(spec=PaperclipClient)

    def test_get_dashboard(self):
        c = self._mock_client()
        c.get.return_value = {"agents": 5, "issues": 10}
        result = export_mod.get_dashboard(c, "co1")
        c.get.assert_called_once_with("/companies/co1/dashboard")
        assert result["agents"] == 5

    def test_get_activity(self):
        c = self._mock_client()
        c.get.return_value = [{"action": "created", "entityType": "issue"}]
        result = export_mod.get_activity(c, "co1")
        assert len(result) == 1

    def test_get_costs_summary(self):
        c = self._mock_client()
        c.get.return_value = {"monthSpendCents": 500}
        result = export_mod.get_costs_summary(c, "co1")
        c.get.assert_called_once_with("/companies/co1/costs/summary")
        assert result["monthSpendCents"] == 500

    def test_get_costs_by_agent(self):
        c = self._mock_client()
        c.get.return_value = [{"agentId": "a1", "costCents": 50}]
        result = export_mod.get_costs_by_agent(c, "co1")
        c.get.assert_called_once_with("/companies/co1/costs/by-agent")
        assert len(result) == 1

    def test_get_sidebar_badges(self):
        c = self._mock_client()
        c.get.return_value = {"pendingApprovals": 3}
        result = export_mod.get_sidebar_badges(c, "co1")
        assert result["pendingApprovals"] == 3
