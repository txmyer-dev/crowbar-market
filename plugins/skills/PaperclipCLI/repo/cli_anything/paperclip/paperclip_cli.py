"""cli-anything-paperclip: CLI harness for the Paperclip agent orchestration platform.

Provides both one-shot subcommands and an interactive REPL for managing
companies, agents, issues, projects, goals, approvals, and costs through
the Paperclip REST API.

Usage:
    cli-anything-paperclip                          # enter REPL
    cli-anything-paperclip --json company list       # one-shot JSON
    cli-anything-paperclip issue create -t "Fix bug" # one-shot human
"""

import json
import shlex
import sys

import click

from cli_anything.paperclip import __version__
from cli_anything.paperclip.core.session import Session
from cli_anything.paperclip.core import company as company_mod
from cli_anything.paperclip.core import agent as agent_mod
from cli_anything.paperclip.core import issue as issue_mod
from cli_anything.paperclip.core import project as project_mod
from cli_anything.paperclip.core import goal as goal_mod
from cli_anything.paperclip.core import approval as approval_mod
from cli_anything.paperclip.core import export as export_mod
from cli_anything.paperclip.utils.paperclip_backend import PaperclipError


# ── Helpers ───────────────────────────────────────────────────────────

def _output(ctx: click.Context, data, human_fn=None):
    """Output data as JSON or human-readable."""
    if ctx.obj.get("json_mode"):
        click.echo(json.dumps(data, indent=2, default=str))
    elif human_fn:
        human_fn(data)
    else:
        click.echo(json.dumps(data, indent=2, default=str))


def _err(msg: str):
    click.echo(f"Error: {msg}", err=True)


def _get_session(ctx: click.Context) -> Session:
    return ctx.obj["session"]


def _table(headers: list[str], rows: list[list[str]]):
    """Print a simple table."""
    if not rows:
        click.echo("  (none)")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    click.echo(fmt.format(*headers))
    click.echo(fmt.format(*["-" * w for w in widths]))
    for row in rows:
        click.echo(fmt.format(*[str(c) for c in row]))


# ── Main CLI Group ────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.option("--url", envvar="PAPERCLIP_URL", default=None, help="Paperclip server URL")
@click.option("--api-key", envvar="PAPERCLIP_API_KEY", default=None, help="API key for authentication")
@click.option("--company", "company_id", envvar="PAPERCLIP_COMPANY_ID", default=None, help="Company ID context")
@click.option("--json", "json_mode", is_flag=True, default=False, help="Output as JSON")
@click.version_option(__version__, prog_name="cli-anything-paperclip")
@click.pass_context
def cli(ctx, url, api_key, company_id, json_mode):
    """CLI harness for the Paperclip agent orchestration platform."""
    ctx.ensure_object(dict)
    ctx.obj["json_mode"] = json_mode
    ctx.obj["session"] = Session(url=url, api_key=api_key, company_id=company_id)

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


# ── REPL Command ──────────────────────────────────────────────────────

@cli.command(hidden=True)
@click.pass_context
def repl(ctx):
    """Interactive REPL mode."""
    from cli_anything.paperclip.utils.repl_skin import ReplSkin

    skin = ReplSkin("paperclip", version=__version__)
    skin.print_banner()

    session = _get_session(ctx)

    # Check server connectivity
    try:
        health = session.client.health()
        skin.success(f"Connected to {session.url}")
    except PaperclipError as exc:
        skin.error(str(exc))
        skin.warning("Some commands may fail until the server is available.")

    pt_session = skin.create_prompt_session()

    commands_help = {
        "company list|get|create|use": "Manage companies",
        "agent list|get|create|update|heartbeat|wakeup": "Manage agents",
        "issue list|get|create|update|checkout|release|comment": "Manage issues",
        "project list|get|create|update": "Manage projects",
        "goal list|get|create|update": "Manage goals",
        "approval list|get|create|approve|reject": "Manage approvals",
        "dashboard": "Show dashboard overview",
        "activity": "Show activity log",
        "costs": "Show cost events",
        "health": "Check server health",
        "session": "Show/save session state",
        "help": "Show this help",
        "quit / exit": "Exit the REPL",
    }

    while True:
        try:
            company_name = session.company_id[:8] if session.company_id else ""
            line = skin.get_input(pt_session, context=company_name)
        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

        if not line:
            continue

        if line in ("quit", "exit", "q"):
            session.save()
            skin.print_goodbye()
            break

        if line == "help":
            skin.help(commands_help)
            continue

        # Parse and dispatch through Click
        try:
            args = shlex.split(line)
        except ValueError as exc:
            skin.error(f"Parse error: {exc}")
            continue

        try:
            cli.main(args, standalone_mode=False, **{"parent": ctx, "obj": ctx.obj})
        except SystemExit:
            pass
        except PaperclipError as exc:
            skin.error(str(exc))
        except click.UsageError as exc:
            skin.error(str(exc))
        except Exception as exc:
            skin.error(f"{type(exc).__name__}: {exc}")


# ── Health Command ────────────────────────────────────────────────────

@cli.command()
@click.pass_context
def health(ctx):
    """Check Paperclip server health."""
    session = _get_session(ctx)
    data = session.client.health()

    def _human(d):
        click.echo(f"  Status: OK")
        for k, v in d.items():
            click.echo(f"  {k}: {v}")

    _output(ctx, data, _human)


# ── Session Command ───────────────────────────────────────────────────

@cli.command("session")
@click.argument("action", default="show", type=click.Choice(["show", "save", "clear"]))
@click.pass_context
def session_cmd(ctx, action):
    """Show, save, or clear session state."""
    session = _get_session(ctx)
    if action == "show":
        _output(ctx, session.to_dict(), lambda d: [click.echo(f"  {k}: {v}") for k, v in d.items()])
    elif action == "save":
        p = session.save()
        _output(ctx, {"saved": str(p)}, lambda d: click.echo(f"  Session saved to {d['saved']}"))
    elif action == "clear":
        from cli_anything.paperclip.core.session import clear_session
        clear_session()
        _output(ctx, {"cleared": True}, lambda _: click.echo("  Session cleared."))


# ══════════════════════════════════════════════════════════════════════
#  COMPANY COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def company(ctx):
    """Manage companies."""
    pass


@company.command("list")
@click.pass_context
def company_list(ctx):
    """List all companies."""
    session = _get_session(ctx)
    companies = company_mod.list_companies(session.client)

    def _human(items):
        rows = [[c.get("id", "")[:8], c.get("name", ""), c.get("status", "")] for c in items]
        _table(["ID", "Name", "Status"], rows)

    _output(ctx, companies, _human)


@company.command("get")
@click.argument("company_id", required=False)
@click.pass_context
def company_get(ctx, company_id):
    """Get company details."""
    session = _get_session(ctx)
    cid = company_id or session.require_company()
    data = company_mod.get_company(session.client, cid)

    def _human(d):
        for k in ("id", "name", "description", "status", "budgetMonthlyCents", "spentMonthlyCents"):
            if k in d:
                click.echo(f"  {k}: {d[k]}")

    _output(ctx, data, _human)


@company.command("create")
@click.option("-n", "--name", required=True, help="Company name")
@click.option("-d", "--description", default="", help="Company description")
@click.option("--budget", "budget_cents", type=int, default=0, help="Monthly budget in cents")
@click.pass_context
def company_create(ctx, name, description, budget_cents):
    """Create a new company."""
    session = _get_session(ctx)
    data = company_mod.create_company(session.client, name, description, budget_cents)
    new_id = data.get("id", "")
    _output(ctx, data, lambda d: click.echo(f"  Created company: {d.get('name', '')} ({new_id[:8]})"))


@company.command("use")
@click.argument("company_id")
@click.pass_context
def company_use(ctx, company_id):
    """Set the active company context."""
    session = _get_session(ctx)
    session.set_company(company_id)
    session.save()
    _output(ctx, {"company_id": company_id}, lambda d: click.echo(f"  Active company: {company_id[:8]}"))


@company.command("update")
@click.argument("company_id", required=False)
@click.option("-n", "--name", default=None, help="New name")
@click.option("--budget", "budgetMonthlyCents", type=int, default=None)
@click.option("--status", type=click.Choice(["active", "paused", "archived"]), default=None)
@click.pass_context
def company_update(ctx, company_id, name, budgetmonthlycents, status):
    """Update a company."""
    session = _get_session(ctx)
    cid = company_id or session.require_company()
    kwargs = {}
    if name is not None:
        kwargs["name"] = name
    if budgetmonthlycents is not None:
        kwargs["budgetMonthlyCents"] = budgetmonthlycents
    if status is not None:
        kwargs["status"] = status
    if not kwargs:
        _err("No fields to update.")
        return
    data = company_mod.update_company(session.client, cid, **kwargs)
    _output(ctx, data, lambda d: click.echo(f"  Company updated."))


# ══════════════════════════════════════════════════════════════════════
#  AGENT COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def agent(ctx):
    """Manage agents."""
    pass


@agent.command("list")
@click.pass_context
def agent_list(ctx):
    """List agents in the active company."""
    session = _get_session(ctx)
    cid = session.require_company()
    agents = agent_mod.list_agents(session.client, cid)

    def _human(items):
        rows = [
            [a.get("id", "")[:8], a.get("name", ""), a.get("role", ""),
             a.get("status", ""), a.get("adapterType", "")]
            for a in items
        ]
        _table(["ID", "Name", "Role", "Status", "Adapter"], rows)

    _output(ctx, agents, _human)


@agent.command("get")
@click.argument("agent_id")
@click.pass_context
def agent_get(ctx, agent_id):
    """Get agent details."""
    session = _get_session(ctx)
    data = agent_mod.get_agent(session.client, agent_id)

    def _human(d):
        for k in ("id", "name", "role", "title", "status", "adapterType",
                   "reportsTo", "capabilities", "budgetMonthlyCents", "spentMonthlyCents"):
            if d.get(k):
                click.echo(f"  {k}: {d[k]}")

    _output(ctx, data, _human)


@agent.command("me")
@click.pass_context
def agent_me(ctx):
    """Get current agent identity (requires API key)."""
    session = _get_session(ctx)
    data = agent_mod.get_me(session.client)
    _output(ctx, data, lambda d: click.echo(f"  Agent: {d.get('name', '')} ({d.get('id', '')[:8]})"))


@agent.command("create")
@click.option("-n", "--name", required=True, help="Agent name")
@click.option("-r", "--role", default="general",
              type=click.Choice(agent_mod.VALID_ROLES), help="Role")
@click.option("--title", default="", help="Display title")
@click.option("--adapter", "adapter_type", default="process",
              type=click.Choice(agent_mod.VALID_ADAPTER_TYPES), help="Adapter type")
@click.option("--reports-to", default="", help="Manager agent ID")
@click.option("--capabilities", default="", help="Capability description")
@click.option("--budget", "budget_cents", type=int, default=0, help="Monthly budget (cents)")
@click.pass_context
def agent_create(ctx, name, role, title, adapter_type, reports_to, capabilities, budget_cents):
    """Create a new agent."""
    session = _get_session(ctx)
    cid = session.require_company()
    data = agent_mod.create_agent(
        session.client, cid, name, role=role, title=title,
        adapter_type=adapter_type, reports_to=reports_to,
        capabilities=capabilities, budget_monthly_cents=budget_cents,
    )
    _output(ctx, data, lambda d: click.echo(f"  Created agent: {d.get('name', '')} ({d.get('id', '')[:8]})"))


@agent.command("update")
@click.argument("agent_id")
@click.option("-n", "--name", default=None)
@click.option("--status", type=click.Choice(agent_mod.VALID_STATUSES), default=None)
@click.option("--budget", "budgetMonthlyCents", type=int, default=None)
@click.option("--title", default=None)
@click.option("--capabilities", default=None)
@click.pass_context
def agent_update(ctx, agent_id, name, status, budgetmonthlycents, title, capabilities):
    """Update an agent."""
    session = _get_session(ctx)
    kwargs = {}
    if name is not None:
        kwargs["name"] = name
    if status is not None:
        kwargs["status"] = status
    if budgetmonthlycents is not None:
        kwargs["budgetMonthlyCents"] = budgetmonthlycents
    if title is not None:
        kwargs["title"] = title
    if capabilities is not None:
        kwargs["capabilities"] = capabilities
    if not kwargs:
        _err("No fields to update.")
        return
    data = agent_mod.update_agent(session.client, agent_id, **kwargs)
    _output(ctx, data, lambda d: click.echo(f"  Agent updated."))


@agent.command("heartbeat")
@click.argument("agent_id")
@click.pass_context
def agent_heartbeat(ctx, agent_id):
    """Invoke an agent's heartbeat."""
    session = _get_session(ctx)
    data = agent_mod.invoke_heartbeat(session.client, agent_id)
    _output(ctx, data, lambda d: click.echo(f"  Heartbeat invoked for {agent_id[:8]}"))


@agent.command("wakeup")
@click.argument("agent_id")
@click.option("--reason", default="", help="Wakeup reason")
@click.pass_context
def agent_wakeup(ctx, agent_id, reason):
    """Send a wakeup request to an agent."""
    session = _get_session(ctx)
    data = agent_mod.wakeup_agent(session.client, agent_id, reason)
    _output(ctx, data, lambda d: click.echo(f"  Wakeup sent to {agent_id[:8]}"))


@agent.command("state")
@click.argument("agent_id")
@click.pass_context
def agent_state(ctx, agent_id):
    """Get agent runtime state."""
    session = _get_session(ctx)
    data = agent_mod.get_runtime_state(session.client, agent_id)
    _output(ctx, data)


@agent.command("runs")
@click.option("--agent-id", default="", help="Filter by agent ID")
@click.option("--limit", type=int, default=20, help="Max results")
@click.pass_context
def agent_runs(ctx, agent_id, limit):
    """List heartbeat runs."""
    session = _get_session(ctx)
    cid = session.require_company()
    runs = agent_mod.list_heartbeat_runs(session.client, cid, agent_id, limit)

    def _human(items):
        rows = [
            [r.get("id", "")[:8], r.get("status", ""), r.get("invocationSource", ""),
             str(r.get("createdAt", ""))[:19]]
            for r in items
        ]
        _table(["ID", "Status", "Source", "Created"], rows)

    _output(ctx, runs, _human)


# ══════════════════════════════════════════════════════════════════════
#  ISSUE COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def issue(ctx):
    """Manage issues/tasks."""
    pass


@issue.command("list")
@click.option("--status", type=click.Choice(issue_mod.VALID_STATUSES), default=None)
@click.option("--assignee", "assignee_agent_id", default="")
@click.option("--project", "project_id", default="")
@click.option("--priority", type=click.Choice(issue_mod.VALID_PRIORITIES), default=None)
@click.option("--limit", type=int, default=50)
@click.pass_context
def issue_list(ctx, status, assignee_agent_id, project_id, priority, limit):
    """List issues in the active company."""
    session = _get_session(ctx)
    cid = session.require_company()
    issues = issue_mod.list_issues(
        session.client, cid, status=status or "", assignee_agent_id=assignee_agent_id,
        project_id=project_id, priority=priority or "", limit=limit,
    )

    def _human(items):
        rows = [
            [i.get("identifier", i.get("id", "")[:8]), i.get("title", "")[:40],
             i.get("status", ""), i.get("priority", "")]
            for i in items
        ]
        _table(["ID", "Title", "Status", "Priority"], rows)

    _output(ctx, issues, _human)


@issue.command("get")
@click.argument("issue_id")
@click.pass_context
def issue_get(ctx, issue_id):
    """Get issue details."""
    session = _get_session(ctx)
    data = issue_mod.get_issue(session.client, issue_id)

    def _human(d):
        for k in ("id", "identifier", "title", "description", "status", "priority",
                   "assigneeAgentId", "projectId", "goalId", "parentId",
                   "createdAt", "startedAt", "completedAt"):
            if d.get(k):
                click.echo(f"  {k}: {d[k]}")

    _output(ctx, data, _human)


@issue.command("create")
@click.option("-t", "--title", required=True, help="Issue title")
@click.option("-d", "--description", default="", help="Description")
@click.option("--status", type=click.Choice(issue_mod.VALID_STATUSES), default="backlog")
@click.option("--priority", type=click.Choice(issue_mod.VALID_PRIORITIES), default="medium")
@click.option("--project", "project_id", default="", help="Project ID")
@click.option("--goal", "goal_id", default="", help="Goal ID")
@click.option("--parent", "parent_id", default="", help="Parent issue ID")
@click.option("--assignee", "assignee_agent_id", default="", help="Assignee agent ID")
@click.option("--billing-code", default="", help="Billing code")
@click.pass_context
def issue_create(ctx, title, description, status, priority, project_id, goal_id,
                 parent_id, assignee_agent_id, billing_code):
    """Create a new issue."""
    session = _get_session(ctx)
    cid = session.require_company()
    data = issue_mod.create_issue(
        session.client, cid, title, description=description, status=status,
        priority=priority, project_id=project_id, goal_id=goal_id,
        parent_id=parent_id, assignee_agent_id=assignee_agent_id,
        billing_code=billing_code,
    )
    ident = data.get("identifier", data.get("id", "")[:8])
    _output(ctx, data, lambda d: click.echo(f"  Created issue: {ident}"))


@issue.command("update")
@click.argument("issue_id")
@click.option("-t", "--title", default=None)
@click.option("--status", type=click.Choice(issue_mod.VALID_STATUSES), default=None)
@click.option("--priority", type=click.Choice(issue_mod.VALID_PRIORITIES), default=None)
@click.option("--assignee", "assignee_agent_id", default=None, help="Assignee agent ID")
@click.option("-d", "--description", default=None)
@click.pass_context
def issue_update(ctx, issue_id, title, status, priority, assignee_agent_id, description):
    """Update an issue."""
    session = _get_session(ctx)
    kwargs = {}
    if title is not None:
        kwargs["title"] = title
    if status is not None:
        kwargs["status"] = status
    if priority is not None:
        kwargs["priority"] = priority
    if assignee_agent_id is not None:
        kwargs["assigneeAgentId"] = assignee_agent_id
    if description is not None:
        kwargs["description"] = description
    if not kwargs:
        _err("No fields to update.")
        return
    data = issue_mod.update_issue(session.client, issue_id, **kwargs)
    _output(ctx, data, lambda d: click.echo(f"  Issue updated."))


@issue.command("checkout")
@click.argument("issue_id")
@click.argument("agent_id")
@click.pass_context
def issue_checkout(ctx, issue_id, agent_id):
    """Checkout an issue to an agent for execution."""
    session = _get_session(ctx)
    data = issue_mod.checkout_issue(session.client, issue_id, agent_id)
    _output(ctx, data, lambda d: click.echo(f"  Issue checked out to {agent_id[:8]}"))


@issue.command("release")
@click.argument("issue_id")
@click.pass_context
def issue_release(ctx, issue_id):
    """Release an issue from agent execution."""
    session = _get_session(ctx)
    data = issue_mod.release_issue(session.client, issue_id)
    _output(ctx, data, lambda d: click.echo(f"  Issue released."))


@issue.command("comments")
@click.argument("issue_id")
@click.pass_context
def issue_comments(ctx, issue_id):
    """List comments on an issue."""
    session = _get_session(ctx)
    comments = issue_mod.get_comments(session.client, issue_id)

    def _human(items):
        for c in items:
            author = c.get("actorType", "unknown")
            body = c.get("body", "")[:80]
            ts = str(c.get("createdAt", ""))[:19]
            click.echo(f"  [{ts}] {author}: {body}")

    _output(ctx, comments, _human)


@issue.command("comment")
@click.argument("issue_id")
@click.argument("body_text")
@click.option("--reopen", is_flag=True, default=False, help="Reopen if closed")
@click.option("--interrupt", is_flag=True, default=False, help="Interrupt running agent")
@click.pass_context
def issue_comment(ctx, issue_id, body_text, reopen, interrupt):
    """Add a comment to an issue."""
    session = _get_session(ctx)
    data = issue_mod.add_comment(session.client, issue_id, body_text, reopen=reopen, interrupt=interrupt)
    _output(ctx, data, lambda d: click.echo(f"  Comment added."))


@issue.command("context")
@click.argument("issue_id")
@click.pass_context
def issue_context(ctx, issue_id):
    """Get compact heartbeat context for an issue."""
    session = _get_session(ctx)
    data = issue_mod.get_heartbeat_context(session.client, issue_id)
    _output(ctx, data)


# ══════════════════════════════════════════════════════════════════════
#  PROJECT COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def project(ctx):
    """Manage projects."""
    pass


@project.command("list")
@click.pass_context
def project_list(ctx):
    """List projects in the active company."""
    session = _get_session(ctx)
    cid = session.require_company()
    projects = project_mod.list_projects(session.client, cid)

    def _human(items):
        rows = [
            [p.get("id", "")[:8], p.get("name", ""), p.get("status", "")]
            for p in items
        ]
        _table(["ID", "Name", "Status"], rows)

    _output(ctx, projects, _human)


@project.command("get")
@click.argument("project_id")
@click.pass_context
def project_get(ctx, project_id):
    """Get project details."""
    session = _get_session(ctx)
    data = project_mod.get_project(session.client, project_id)

    def _human(d):
        for k in ("id", "name", "description", "status", "leadAgentId", "targetDate"):
            if d.get(k):
                click.echo(f"  {k}: {d[k]}")

    _output(ctx, data, _human)


@project.command("create")
@click.option("-n", "--name", required=True, help="Project name")
@click.option("-d", "--description", default="", help="Description")
@click.option("--status", type=click.Choice(project_mod.VALID_STATUSES), default="backlog")
@click.option("--lead", "lead_agent_id", default="", help="Lead agent ID")
@click.option("--target-date", default="", help="Target date")
@click.option("--color", default="", help="Project color")
@click.pass_context
def project_create(ctx, name, description, status, lead_agent_id, target_date, color):
    """Create a new project."""
    session = _get_session(ctx)
    cid = session.require_company()
    data = project_mod.create_project(
        session.client, cid, name, description=description, status=status,
        lead_agent_id=lead_agent_id, target_date=target_date, color=color,
    )
    _output(ctx, data, lambda d: click.echo(f"  Created project: {d.get('name', '')} ({d.get('id', '')[:8]})"))


@project.command("update")
@click.argument("project_id")
@click.option("-n", "--name", default=None)
@click.option("--status", type=click.Choice(project_mod.VALID_STATUSES), default=None)
@click.option("-d", "--description", default=None)
@click.pass_context
def project_update(ctx, project_id, name, status, description):
    """Update a project."""
    session = _get_session(ctx)
    kwargs = {}
    if name is not None:
        kwargs["name"] = name
    if status is not None:
        kwargs["status"] = status
    if description is not None:
        kwargs["description"] = description
    if not kwargs:
        _err("No fields to update.")
        return
    data = project_mod.update_project(session.client, project_id, **kwargs)
    _output(ctx, data, lambda d: click.echo(f"  Project updated."))


@project.command("workspace")
@click.argument("project_id")
@click.option("--cwd", default="", help="Local directory path")
@click.option("--repo-url", default="", help="Git repository URL")
@click.option("--repo-ref", default="", help="Git branch/ref")
@click.option("--name", default="", help="Workspace name")
@click.option("--primary", is_flag=True, default=False, help="Make this the primary workspace")
@click.pass_context
def project_workspace(ctx, project_id, cwd, repo_url, repo_ref, name, primary):
    """Create a workspace for a project."""
    session = _get_session(ctx)
    data = project_mod.create_workspace(
        session.client, project_id, cwd=cwd, repo_url=repo_url,
        repo_ref=repo_ref, name=name, is_primary=primary,
    )
    _output(ctx, data, lambda d: click.echo(f"  Workspace created."))


# ══════════════════════════════════════════════════════════════════════
#  GOAL COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def goal(ctx):
    """Manage goals."""
    pass


@goal.command("list")
@click.pass_context
def goal_list(ctx):
    """List goals in the active company."""
    session = _get_session(ctx)
    cid = session.require_company()
    goals = goal_mod.list_goals(session.client, cid)

    def _human(items):
        rows = [
            [g.get("id", "")[:8], g.get("title", "")[:40], g.get("level", ""),
             g.get("status", "")]
            for g in items
        ]
        _table(["ID", "Title", "Level", "Status"], rows)

    _output(ctx, goals, _human)


@goal.command("get")
@click.argument("goal_id")
@click.pass_context
def goal_get(ctx, goal_id):
    """Get goal details."""
    session = _get_session(ctx)
    data = goal_mod.get_goal(session.client, goal_id)

    def _human(d):
        for k in ("id", "title", "description", "level", "status", "parentId", "ownerAgentId"):
            if d.get(k):
                click.echo(f"  {k}: {d[k]}")

    _output(ctx, data, _human)


@goal.command("create")
@click.option("-t", "--title", required=True, help="Goal title")
@click.option("-d", "--description", default="", help="Description")
@click.option("--level", type=click.Choice(goal_mod.VALID_LEVELS), default="task")
@click.option("--status", type=click.Choice(goal_mod.VALID_STATUSES), default="planned")
@click.option("--parent", "parent_id", default="", help="Parent goal ID")
@click.option("--owner", "owner_agent_id", default="", help="Owner agent ID")
@click.pass_context
def goal_create(ctx, title, description, level, status, parent_id, owner_agent_id):
    """Create a new goal."""
    session = _get_session(ctx)
    cid = session.require_company()
    data = goal_mod.create_goal(
        session.client, cid, title, description=description, level=level,
        status=status, parent_id=parent_id, owner_agent_id=owner_agent_id,
    )
    _output(ctx, data, lambda d: click.echo(f"  Created goal: {d.get('title', '')} ({d.get('id', '')[:8]})"))


@goal.command("update")
@click.argument("goal_id")
@click.option("-t", "--title", default=None)
@click.option("--status", type=click.Choice(goal_mod.VALID_STATUSES), default=None)
@click.option("-d", "--description", default=None)
@click.option("--level", type=click.Choice(goal_mod.VALID_LEVELS), default=None)
@click.pass_context
def goal_update(ctx, goal_id, title, status, description, level):
    """Update a goal."""
    session = _get_session(ctx)
    kwargs = {}
    if title is not None:
        kwargs["title"] = title
    if status is not None:
        kwargs["status"] = status
    if description is not None:
        kwargs["description"] = description
    if level is not None:
        kwargs["level"] = level
    if not kwargs:
        _err("No fields to update.")
        return
    data = goal_mod.update_goal(session.client, goal_id, **kwargs)
    _output(ctx, data, lambda d: click.echo(f"  Goal updated."))


# ══════════════════════════════════════════════════════════════════════
#  APPROVAL COMMANDS
# ══════════════════════════════════════════════════════════════════════

@cli.group()
@click.pass_context
def approval(ctx):
    """Manage approvals."""
    pass


@approval.command("list")
@click.option("--status", type=click.Choice(approval_mod.VALID_STATUSES), default=None)
@click.pass_context
def approval_list(ctx, status):
    """List approvals in the active company."""
    session = _get_session(ctx)
    cid = session.require_company()
    approvals = approval_mod.list_approvals(session.client, cid, status=status or "")

    def _human(items):
        rows = [
            [a.get("id", "")[:8], a.get("type", ""), a.get("status", ""),
             str(a.get("createdAt", ""))[:19]]
            for a in items
        ]
        _table(["ID", "Type", "Status", "Created"], rows)

    _output(ctx, approvals, _human)


@approval.command("get")
@click.argument("approval_id")
@click.pass_context
def approval_get(ctx, approval_id):
    """Get approval details."""
    session = _get_session(ctx)
    data = approval_mod.get_approval(session.client, approval_id)
    _output(ctx, data)


@approval.command("approve")
@click.argument("approval_id")
@click.option("--note", default="", help="Decision note")
@click.pass_context
def approval_approve(ctx, approval_id, note):
    """Approve an approval request."""
    session = _get_session(ctx)
    data = approval_mod.approve(session.client, approval_id, note)
    _output(ctx, data, lambda d: click.echo(f"  Approval approved."))


@approval.command("reject")
@click.argument("approval_id")
@click.option("--note", default="", help="Decision note")
@click.pass_context
def approval_reject(ctx, approval_id, note):
    """Reject an approval request."""
    session = _get_session(ctx)
    data = approval_mod.reject(session.client, approval_id, note)
    _output(ctx, data, lambda d: click.echo(f"  Approval rejected."))


# ══════════════════════════════════════════════════════════════════════
#  DASHBOARD / ACTIVITY / COSTS
# ══════════════════════════════════════════════════════════════════════

@cli.command("dashboard")
@click.pass_context
def dashboard(ctx):
    """Show dashboard overview."""
    session = _get_session(ctx)
    cid = session.require_company()
    data = export_mod.get_dashboard(session.client, cid)
    _output(ctx, data)


@cli.command("activity")
@click.option("--entity-type", default="", help="Filter by entity type")
@click.option("--limit", type=int, default=50)
@click.pass_context
def activity(ctx, entity_type, limit):
    """Show activity log."""
    session = _get_session(ctx)
    cid = session.require_company()
    entries = export_mod.get_activity(session.client, cid, entity_type, limit)

    def _human(items):
        for e in items:
            action = e.get("action", "")
            entity = e.get("entityType", "")
            actor = e.get("actorType", "")
            ts = str(e.get("createdAt", ""))[:19]
            click.echo(f"  [{ts}] {actor} {action} {entity}")

    _output(ctx, entries, _human)


@cli.command("costs")
@click.option("--view", type=click.Choice(["summary", "by-agent", "by-project"]), default="summary")
@click.pass_context
def costs(ctx, view):
    """Show cost data."""
    session = _get_session(ctx)
    cid = session.require_company()
    if view == "summary":
        data = export_mod.get_costs_summary(session.client, cid)
    elif view == "by-agent":
        data = export_mod.get_costs_by_agent(session.client, cid)
    else:
        data = export_mod.get_costs_by_project(session.client, cid)
    _output(ctx, data)


# ── Entry point ───────────────────────────────────────────────────────

def main():
    cli(auto_envvar_prefix="PAPERCLIP")


if __name__ == "__main__":
    main()
