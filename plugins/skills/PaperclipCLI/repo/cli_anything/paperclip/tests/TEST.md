# TEST.md — Test Plan and Results for cli-anything-paperclip

## Test Inventory Plan

| File               | Type    | Estimated Tests |
|--------------------|---------|------------------|
| `test_core.py`     | Unit    | ~45 tests       |
| `test_full_e2e.py` | E2E     | ~20 tests       |

## Unit Test Plan (`test_core.py`)

### Module: `paperclip_backend.py` (~8 tests)
- `PaperclipClient.__init__` — defaults, env var override, explicit params
- `PaperclipClient._request` — builds correct URL, headers, body
- `PaperclipClient._request` — handles HTTP errors → PaperclipError
- `PaperclipClient._request` — handles connection refused → PaperclipError
- `PaperclipClient.get/post/patch/delete` — delegate to _request
- `PaperclipError` — stores status and body

### Module: `session.py` (~8 tests)
- `load_session` — returns empty dict when no file
- `load_session` — returns saved data when file exists
- `save_session` — writes JSON to disk
- `clear_session` — removes file
- `Session.__init__` — loads from saved state, env, or defaults
- `Session.require_company` — raises when no company set
- `Session.set_company` — updates and marks modified
- `Session.save` — persists to disk and returns path

### Module: `company.py` (~5 tests)
- `list_companies` — extracts list from response
- `get_company` — passes correct path
- `create_company` — builds correct body with optional fields
- `update_company` — passes kwargs correctly
- `export_company` / `import_company` — correct endpoints

### Module: `agent.py` (~7 tests)
- `list_agents` — extracts list from response
- `get_agent` / `get_me` — correct endpoints
- `create_agent` — builds body with all optional fields
- `update_agent` — passes kwargs
- `invoke_heartbeat` — POSTs to correct endpoint
- `wakeup_agent` — POSTs with reason
- `list_heartbeat_runs` — passes params correctly

### Module: `issue.py` (~8 tests)
- `list_issues` — passes filter params correctly
- `get_issue` — correct path
- `create_issue` — builds body with all optional fields
- `update_issue` — passes kwargs
- `checkout_issue` — sends agentId and expectedStatuses
- `release_issue` — POSTs to correct endpoint
- `get_comments` / `add_comment` — correct paths and bodies
- `get_heartbeat_context` — correct path

### Module: `project.py` (~5 tests)
- `list_projects` / `get_project` — correct paths
- `create_project` — builds body with optional fields
- `update_project` — passes kwargs
- `create_workspace` — sends workspace config

### Module: `goal.py` (~4 tests)
- `list_goals` / `get_goal` — correct paths
- `create_goal` — builds body with all fields
- `update_goal` — passes kwargs

### Module: `approval.py` (~4 tests)
- `list_approvals` — passes status filter
- `get_approval` — correct path
- `approve` / `reject` — correct endpoints with decision note

### Module: `export.py` (~4 tests)
- `get_dashboard` — passes company filter
- `get_activity` — passes filters
- `get_costs` — passes agent filter
- `get_sidebar_badges` — passes company filter

### Edge Cases
- Empty/missing response fields handled gracefully
- VALID_* constants contain correct values
- PaperclipClient handles auth header, run ID header

## E2E Test Plan (`test_full_e2e.py`)

### Server Integration Tests (~12 tests)
These tests require a running Paperclip server (hard dependency).

- `test_health` — Server health check returns valid response
- `test_company_lifecycle` — Create, get, update, list companies
- `test_agent_lifecycle` — Create, get, update, list agents
- `test_issue_lifecycle` — Create, get, update, list, comment on issues
- `test_project_lifecycle` — Create, get, update, list projects
- `test_goal_lifecycle` — Create, get, update, list goals
- `test_approval_lifecycle` — Create, list approvals
- `test_dashboard` — Dashboard returns data
- `test_activity` — Activity log returns entries
- `test_costs` — Cost data returns
- `test_session_persistence` — Save/load session round-trip
- `test_issue_workflow` — Full workflow: create issue → assign → checkout → comment → complete

### CLI Subprocess Tests (~8 tests)
Test the installed `cli-anything-paperclip` command via subprocess.

- `test_help` — `--help` exits 0 with usage text
- `test_version` — `--version` shows version
- `test_health_json` — `--json health` returns valid JSON
- `test_company_list_json` — `--json company list` returns JSON array
- `test_session_show_json` — `--json session show` returns session data
- `test_agent_list_json` — `--json agent list` returns JSON
- `test_issue_create_json` — Full issue create via subprocess
- `test_full_workflow_subprocess` — End-to-end: company → agent → issue → update

## Realistic Workflow Scenarios

### Workflow 1: Bootstrap a Company
- **Simulates**: First-time setup of an AI company
- **Operations**: Create company → set as active → create CEO agent → create engineer agents → set reporting hierarchy → create company goal
- **Verified**: All entities exist, org chart is correct, goal is linked

### Workflow 2: Task Delegation Pipeline
- **Simulates**: CEO delegates work through the org chart
- **Operations**: Create project → create goal → create parent issue → create sub-issues → assign to agents → checkout → add comments → mark done
- **Verified**: Issue statuses flow correctly, comments persist, hierarchy intact

### Workflow 3: Cost Monitoring
- **Simulates**: Budget tracking and cost analysis
- **Operations**: List agents with budgets → query cost events → check dashboard → verify budget enforcement
- **Verified**: Cost data aggregates correctly, budget fields present

---

## Test Results

```
$ CLI_ANYTHING_FORCE_INSTALLED=1 python3 -m pytest cli_anything/paperclip/tests/ -v --tb=no

============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
[_resolve_cli] Using installed command: /home/ubuntu/.local/bin/cli-anything-paperclip
collected 94 items

cli_anything/paperclip/tests/test_core.py::TestPaperclipError::test_basic PASSED [  1%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipError::test_no_extras PASSED [  2%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientInit::test_defaults PASSED [  3%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientInit::test_explicit_params PASSED [  4%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientInit::test_env_vars PASSED [  5%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientInit::test_trailing_slash_stripped PASSED [  6%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_get_request PASSED [  7%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_post_with_body PASSED [  8%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_auth_header PASSED [  9%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_run_id_header PASSED [ 10%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_query_params PASSED [ 11%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_http_error PASSED [ 12%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_connection_refused PASSED [ 13%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_patch_method PASSED [ 14%]
cli_anything/paperclip/tests/test_core.py::TestPaperclipClientRequest::test_delete_method PASSED [ 15%]
cli_anything/paperclip/tests/test_core.py::TestSessionPersistence::test_load_empty PASSED [ 17%]
cli_anything/paperclip/tests/test_core.py::TestSessionPersistence::test_save_and_load PASSED [ 18%]
cli_anything/paperclip/tests/test_core.py::TestSessionPersistence::test_clear PASSED [ 19%]
cli_anything/paperclip/tests/test_core.py::TestSessionPersistence::test_clear_nonexistent PASSED [ 20%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_defaults PASSED [ 21%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_explicit_params PASSED [ 22%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_loads_from_saved PASSED [ 23%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_require_company_raises PASSED [ 24%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_require_company_returns PASSED [ 25%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_set_company PASSED [ 26%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_save_roundtrip PASSED [ 27%]
cli_anything/paperclip/tests/test_core.py::TestSession::test_to_dict PASSED [ 28%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_list_companies_list_response PASSED [ 29%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_list_companies_dict_response PASSED [ 30%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_get_company PASSED [ 31%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_create_company_minimal PASSED [ 32%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_create_company_full PASSED [ 34%]
cli_anything/paperclip/tests/test_core.py::TestCompany::test_update_company PASSED [ 35%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_list_agents PASSED [ 36%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_get_agent PASSED [ 37%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_get_me PASSED [ 38%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_create_agent_minimal PASSED [ 39%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_create_agent_full PASSED [ 40%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_invoke_heartbeat PASSED [ 41%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_wakeup_agent PASSED [ 42%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_list_heartbeat_runs PASSED [ 43%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_valid_roles PASSED [ 44%]
cli_anything/paperclip/tests/test_core.py::TestAgent::test_valid_adapter_types PASSED [ 45%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_list_issues PASSED [ 46%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_list_issues_with_filters PASSED [ 47%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_get_issue PASSED [ 48%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_create_issue_minimal PASSED [ 50%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_create_issue_full PASSED [ 51%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_checkout_issue PASSED [ 52%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_release_issue PASSED [ 53%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_add_comment PASSED [ 54%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_get_heartbeat_context PASSED [ 55%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_valid_statuses PASSED [ 56%]
cli_anything/paperclip/tests/test_core.py::TestIssue::test_valid_priorities PASSED [ 57%]
cli_anything/paperclip/tests/test_core.py::TestProject::test_list_projects PASSED [ 58%]
cli_anything/paperclip/tests/test_core.py::TestProject::test_create_project_minimal PASSED [ 59%]
cli_anything/paperclip/tests/test_core.py::TestProject::test_create_project_full PASSED [ 60%]
cli_anything/paperclip/tests/test_core.py::TestProject::test_create_workspace PASSED [ 61%]
cli_anything/paperclip/tests/test_core.py::TestProject::test_valid_statuses PASSED [ 62%]
cli_anything/paperclip/tests/test_core.py::TestGoal::test_list_goals PASSED [ 63%]
cli_anything/paperclip/tests/test_core.py::TestGoal::test_create_goal_minimal PASSED [ 64%]
cli_anything/paperclip/tests/test_core.py::TestGoal::test_create_goal_full PASSED [ 65%]
cli_anything/paperclip/tests/test_core.py::TestGoal::test_valid_levels PASSED [ 67%]
cli_anything/paperclip/tests/test_core.py::TestGoal::test_valid_statuses PASSED [ 68%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_list_approvals PASSED [ 69%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_create_approval PASSED [ 70%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_approve PASSED [ 71%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_reject PASSED [ 72%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_valid_types PASSED [ 73%]
cli_anything/paperclip/tests/test_core.py::TestApproval::test_valid_statuses PASSED [ 74%]
cli_anything/paperclip/tests/test_core.py::TestExport::test_get_dashboard PASSED [ 75%]
cli_anything/paperclip/tests/test_core.py::TestExport::test_get_activity PASSED [ 76%]
cli_anything/paperclip/tests/test_core.py::TestExport::test_get_costs_summary PASSED [ 77%]
cli_anything/paperclip/tests/test_core.py::TestExport::test_get_costs_by_agent PASSED [ 78%]
cli_anything/paperclip/tests/test_core.py::TestExport::test_get_sidebar_badges PASSED [ 79%]
cli_anything/paperclip/tests/test_full_e2e.py::TestHealth::test_health PASSED [ 80%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCompanyLifecycle::test_list_companies PASSED [ 81%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCompanyLifecycle::test_get_company PASSED [ 82%]
cli_anything/paperclip/tests/test_full_e2e.py::TestAgentLifecycle::test_create_and_list_agents PASSED [ 84%]
cli_anything/paperclip/tests/test_full_e2e.py::TestIssueLifecycle::test_create_and_get_issue PASSED [ 85%]
cli_anything/paperclip/tests/test_full_e2e.py::TestProjectLifecycle::test_create_and_list_projects PASSED [ 86%]
cli_anything/paperclip/tests/test_full_e2e.py::TestGoalLifecycle::test_create_and_list_goals PASSED [ 87%]
cli_anything/paperclip/tests/test_full_e2e.py::TestDashboardAndActivity::test_dashboard PASSED [ 88%]
cli_anything/paperclip/tests/test_full_e2e.py::TestDashboardAndActivity::test_activity PASSED [ 89%]
cli_anything/paperclip/tests/test_full_e2e.py::TestSessionPersistence::test_session_roundtrip PASSED [ 90%]
cli_anything/paperclip/tests/test_full_e2e.py::TestIssueWorkflow::test_full_workflow PASSED [ 91%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_help PASSED [ 92%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_version PASSED [ 93%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_health_json PASSED [ 94%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_session_show_json PASSED [ 95%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_company_list_json PASSED [ 96%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_issue_create_json PASSED [ 97%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_agent_list_json PASSED [ 98%]
cli_anything/paperclip/tests/test_full_e2e.py::TestCLISubprocess::test_full_workflow_subprocess PASSED [100%]

============================== 94 passed in 1.32s ==============================
```

### Summary Statistics

| Metric          | Value    |
|-----------------|----------|
| Total tests     | 94       |
| Passed          | 94       |
| Failed          | 0        |
| Pass rate       | **100%** |
| Execution time  | 1.32s    |

### Test Breakdown

| File               | Type                | Tests | Status     |
|--------------------|---------------------|-------|------------|
| `test_core.py`     | Unit (mocked)       | 75    | All passed |
| `test_full_e2e.py` | E2E (live server)   | 11    | All passed |
| `test_full_e2e.py` | CLI subprocess      | 8     | All passed |

### Subprocess Tests

All subprocess tests used the installed command:
```
[_resolve_cli] Using installed command: /home/ubuntu/.local/bin/cli-anything-paperclip
```

### Coverage Notes

- All core modules (backend, session, company, agent, issue, project, goal, approval, export) have unit tests
- All E2E tests hit the real Paperclip server (hard dependency — no mocking)
- CLI subprocess tests verify the installed `cli-anything-paperclip` command end-to-end
- Full issue workflow tested: create agent → create issue → assign → update status → comment → mark done
- Session persistence tested with save/load/clear round-trip
