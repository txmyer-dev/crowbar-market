# Issues Workflow

Create, list, update, and manage Paperclip issues (tasks).

## Intent-to-Action Mapping

| User Says | Action | Command |
|-----------|--------|---------|
| "create issue", "new task" | Create | `issue create` |
| "list issues", "show tasks" | List | `issue list` |
| "show issue [id]" | Get details | `issue get` |
| "assign [issue] to [agent]" | Checkout | `issue checkout` |
| "release issue", "unassign" | Release | `issue release` |
| "comment on issue" | Add comment | `issue comment` |
| "update issue" | Update | `issue update` |

## Create Issue

```bash
cli-anything-paperclip --json issue create \
  --title "TITLE" \
  --description "DESCRIPTION" \
  --priority PRIORITY \
  --assignee-agent-id AGENT_ID \
  --project-id PROJECT_ID
```

### Priority Mapping

| User Says | Value |
|-----------|-------|
| "critical", "urgent" | critical |
| "high", "important" | high |
| "medium" (default) | medium |
| "low", "whenever" | low |

## List Issues

```bash
# All issues
cli-anything-paperclip --json issue list

# By status
cli-anything-paperclip --json issue list --status todo
cli-anything-paperclip --json issue list --status in_progress

# By agent
cli-anything-paperclip --json issue list --assignee-agent-id AGENT_ID
```

## Checkout (Assign) Issue

```bash
cli-anything-paperclip --json issue checkout ISSUE_ID --agent-id AGENT_ID
```

## Add Comment

```bash
cli-anything-paperclip --json issue comment ISSUE_ID --body "COMMENT_TEXT"
```

## Update Issue

```bash
cli-anything-paperclip --json issue update ISSUE_ID --status done
```
