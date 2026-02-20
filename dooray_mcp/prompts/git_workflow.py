"""MCP prompts for Dooray git workflows."""

from dooray_mcp import mcp


@mcp.prompt()
def commit_message_convention(project_code: str = "APS") -> str:
    """Commit message convention for linking commits to Dooray tasks."""
    return f"""\
## 커밋 메시지 컨벤션

모든 커밋 메시지는 다음 형식을 따릅니다:

```
[#{project_code}/태스크번호] 한글로 커밋 메시지 작성
```

### 규칙
- 대괄호 안에 `#프로젝트코드/태스크번호`를 포함합니다
- 커밋 메시지는 **한글**로 작성합니다
- 프로젝트 코드는 Dooray 프로젝트 코드입니다 (예: {project_code})
- 태스크 번호는 Dooray 업무 번호입니다

### 예시
```
[#{project_code}/1964] 스케줄러 캘린더 처리 로직 수정
[#{project_code}/1520] 인라인 공정 시간 계산 버그 수정
[#{project_code}/2001] 새로운 리소스 할당 알고리즘 추가
```
"""


@mcp.prompt()
def update_issues_from_commits(
    author: str = "jaeyoung.heo",
    commit_count: int = 10,
) -> str:
    """Update Dooray issues with details from recent git commits."""
    return f"""\
Follow these steps to update Dooray issues from recent git commits:

## 1. Find commits with issue references

Run this command:
```
git log --author="{author}" --oneline -{commit_count}
```

- Only process commits by **{author}**
- Parse `[#PROJECT/NUMBER]` or `[PROJECT/NUMBER]` patterns from commit messages
- Group commits by issue number (multiple commits may reference the same issue)

## 2. Understand the code changes

For each commit:
- Read the **actual diff**: `git diff HASH^..HASH`
- Read the **source files** that were changed to understand context
- Do NOT just summarize the commit message — analyze the real code changes

## 3. Find the Dooray issue

- Use `find_task_by_number` with the project code and task number
- If that returns wrong results, use `list_tasks` with keyword search
- Common project codes: APS, A.I.-RL

## 4. Update the issue body

- Use `update_task` to set the body content
- Write in **Korean** (matching team convention)
- Format in markdown with:
  - `## 변경 내용` — one-line summary of what changed and why
  - Subsections per major change area (file or feature)
  - Explain the **what** and **why**, not just list files
  - Reference actual class names, method names, and technical details from the code
  - `### 커밋` — list all related commit hashes with messages at the bottom
"""
