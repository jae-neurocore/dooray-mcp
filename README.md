# dooray-mcp

[NHN Dooray](https://dooray.com) 프로젝트 관리를 위한 MCP (Model Context Protocol) 서버입니다.

Claude 같은 AI 어시스턴트가 Dooray 업무에 직접 접근할 수 있게 해줍니다.

## 도구

| 도구 | 설명 |
|---|---|
| `search_projects` | 프로젝트 코드로 프로젝트 검색/목록 조회 |
| `list_tasks` | 필터를 사용한 업무 목록 조회 (워크플로우, 태그, 담당자, 키워드) |
| `get_task` | 단일 업무 상세 조회 |
| `create_task` | 업무 생성 (제목, 본문, 우선순위, 담당자, 태그, 마일스톤, 마감일) |
| `update_task` | 업무 필드 수정 |
| `set_task_workflow` | 업무 워크플로우 상태 변경 |
| `mark_task_done` | 업무 완료 처리 |
| `find_task_by_number` | 프로젝트 코드 + 번호로 업무 찾기 (예: `APS/1689`) |

## 프롬프트

| 프롬프트 | 설명 |
|---|---|
| `commit_message_convention` | 커밋 메시지 형식: `[#PROJECT/NUMBER] 한글 메시지` |
| `update_issues_from_commits` | git 커밋을 스캔하여 연관된 Dooray 이슈를 변경 내용으로 업데이트 |

## 설치

### 1. Dooray API 토큰 발급

**Dooray → 설정 → API**에서 토큰을 생성합니다.

### 2. 설치

```bash
git clone https://github.com/your-username/dooray-mcp.git
cd dooray-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Claude Code 설정

`~/.claude/settings.json`에 추가:

```json
{
  "mcpServers": {
    "dooray": {
      "command": "/path/to/dooray-mcp/.venv/bin/dooray-mcp",
      "env": {
        "DOORAY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

Claude Code를 재시작하면 Dooray 도구를 사용할 수 있습니다.

### 4. CLAUDE.md 설정 (권장)

프로젝트의 `CLAUDE.md` (또는 전역 설정은 `~/.claude/CLAUDE.md`)에 아래 내용을 추가하면 Claude가 Dooray 이슈를 더 잘 처리합니다:

```markdown
## Dooray Issue Update

When asked to update Dooray issues:
- Find commits by `--author="your-name"` and parse `[#PROJECT/NUMBER]` patterns
- Read actual diffs to understand changes (don't just summarize commit messages)
- Write issue body in **Korean**, markdown format
```

## 활용 예시

Claude Code에서 다음과 같이 사용할 수 있습니다:

```
> 최근 커밋 중 태스크 번호 1722에 관련된 커밋을 찾아서 이슈 본문을 작성해줘

> [#APS/1689] 관련 커밋들의 변경 내용을 정리해서 Dooray 이슈를 업데이트해줘

> 최근 10개 커밋에서 Dooray 이슈 번호를 찾아서 전부 업데이트해줘
```

---

# English

MCP (Model Context Protocol) server for [NHN Dooray](https://dooray.com) project management.

Gives AI assistants like Claude direct access to your Dooray tasks.

## Tools

| Tool | Description |
|---|---|
| `search_projects` | Search/list projects by code |
| `list_tasks` | List tasks with filters (workflow, tags, assignee, keyword) |
| `get_task` | Get a single task's full details |
| `create_task` | Create a task with subject, body, priority, assignees, tags, milestone, due date |
| `update_task` | Update task fields |
| `set_task_workflow` | Change a task's workflow status |
| `mark_task_done` | Mark a task as done |
| `find_task_by_number` | Find a task by project code + number (e.g. `APS/1689`) |

## Prompts

| Prompt | Description |
|---|---|
| `commit_message_convention` | Commit message format: `[#PROJECT/NUMBER] 한글 메시지` |
| `update_issues_from_commits` | Scan git commits and update referenced Dooray issues with change details |

## Setup

### 1. Get a Dooray API token

Go to **Dooray → Settings → API** and generate a token.

### 2. Install

```bash
git clone https://github.com/your-username/dooray-mcp.git
cd dooray-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "dooray": {
      "command": "/path/to/dooray-mcp/.venv/bin/dooray-mcp",
      "env": {
        "DOORAY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

Restart Claude Code and the Dooray tools will be available.

### 4. Add CLAUDE.md instructions (recommended)

Add the following to your project's `CLAUDE.md` (or `~/.claude/CLAUDE.md` for global use) so Claude knows how to work with Dooray issues:

```markdown
## Dooray Issue Update

When asked to update Dooray issues:
- Find commits by `--author="your-name"` and parse `[#PROJECT/NUMBER]` patterns
- Read actual diffs to understand changes (don't just summarize commit messages)
- Write issue body in **Korean**, markdown format
```

## Usage examples

Example prompts you can use in Claude Code:

```
> Find my recent commits related to task 1722 and write the issue body

> Update the Dooray issue for [#APS/1689] with a summary of the code changes

> Scan the last 10 commits and update all referenced Dooray issues
```

## License

MIT
