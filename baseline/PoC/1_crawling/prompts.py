"""검색 에이전트를 위한 프롬프트 템플릿과 도구 설명이다."""

RESEARCH_ALL_INSTRUCTIONS = """# 최초 검색 워크플로우

이 프롬프트는 대상 기업에 대한 전반적인 데이터가 부족할 때 광범위한 조사를 하기 위한 프롬프트이다.
아래의 워크플로우를 따라 조사해라.

1. **Plan**: 먼저 todo 리스트를 생성하고 조사하고자 하는 기업과 관련있는 객체({Entities})들을 조사할 계획을 세워라. 아래 TODO의 구조를 참고하라.
2. **Save the request**: todo 리스트에 따라 조사하고자 하는 기업과 관련있는 대상 사이의 관계를 조사하고 '/final_report.md'파일에 작성하라. 아래 Report 구조를 참고하라.
3. **Verify**: '/final_report.md'파일을 읽고 이 결과물이 조사하고자 한 기업과 이와 관련있는 대상들 사이의 관계가 맞는지 다시 확인해라.

## TODO Writing Guidelines

todo 리스트를 작성할 때 아래 구조 패턴을 따라라.

**기업 설명**
조사하고자 하는 기업의 도메인과 외부 활동 등을 1줄로 요약

**관련 Entities 찾기**
조사하고자 하는 기업과 관련있는 객체들을 
- entity1
- entity2
의 형식으로 작성하라.
이 때 각 객체는 가능한 독립적이어야 한다. 예를 들자면 삼성 전자는 삼성 기업과 구분하여 entity로 작성하지 않는다.

## Report Writing Guidelines

'/final_report.md' 파일을 작성할 때 아래의 구조를 따라라.

result = {
    'entity1': [
        '기업은 entity1과 어느 상품에 대해 경쟁관계이다.',
        '기업과 entity1은 entity3에 상품을 공급한다.'
    ],
    'entity2': [
        '기업은 entity2에 속한 기업이다.',
        '6월2일에 entity2는 기업에 특정 세금 규제를 내렸다.'
    ]
}

**description**
위 구조는 Dict[str, list[str, ...]]의 구조로, 조사하고자 하는 기업에 대해 관련있는 객체들이 key값으로 오고 관계에 대한 설명이 list value의 원소로 온다.
관계에 대한 설명은 그 방향이 정확해야 한다. 예를 들자면 '삼성전자는 소비자에게 휴대폰을 판다'는 맞는 문장이지만, '소비자는 삼성전자에게 휴대폰을 판다'는 거짓된 문장이다.
관계에 대한 설명은 두 객체와 그 사이의 관계가 명확해야 하며 그 외의 것은 필요한 경우에만 허용해야 한다.
"""

TOOL_FEEDBACK_INSTRUCTIONS = """# 도구 실행 피드백 워크플로우

이 지시문은 에이전트가 도구를 실행한 뒤 도구 메시지를 읽고, 발생한 오류와 개선 사항을 별도의 Markdown 파일에 기록하기 위한 프롬프트이다.

도구를 실행한 뒤에는 도구 메시지의 내용을 반드시 확인하라.

1. **Check status**: 도구 메시지가 성공인지 실패인지 판단하라.
2. **Diagnose**: 실패했다면 실패 원인을 짧게 요약하라.
3. **Improve**: 같은 실패를 반복하지 않도록 쿼리, 경로, 파일 형식, 입력값 중 하나를 수정해 다시 시도하라.
4. **Record**: 도구 실행 중 발생한 오류, 재시도 내용, 개선 사항을 Markdown 파일에 작성하라.

## Success And Failure Rules

- 도구 메시지가 `SUCCESS` 또는 성공 내용을 포함하면, 어떤 결과가 생성되었는지 확인하고 다음 단계로 진행하라.
- 도구 메시지가 `FAILED`, `Error`, `Exception` 또는 실패 내용을 포함하면, 실패 원인을 기록하고 개선된 입력으로 다시 시도하라.
- 도구 실패를 숨기지 마라. 실패가 최종 결과에 영향을 줄 수 있으면 남은 한계를 명확히 작성하라.
- 파일 작성 도구가 `.md` 파일만 허용한다고 응답하면, 반드시 Markdown 파일 경로로 다시 호출하라.
- 같은 도구 호출이 2회 이상 실패하면, 무한 반복하지 말고 실패 원인과 대체 전략을 기록한 뒤 가능한 다른 도구나 다른 검색어를 사용하라.

## Markdown Record Format

도구 실행 오류와 개선 사항은 아래 구조로 Markdown 파일에 작성하라.

```markdown
# Tool Execution Notes

## Summary
- Overall status: success | partial | failed
- Final output path:
- Remaining limitations:

## Tool Attempts

### 1. <tool_name>
- Status: success | failed | improved
- Input:
- Message:
- Issue:
- Improvement:
- Impact:
```

## Writing Rules

- 작성 대상 파일은 반드시 `.md` 확장자를 사용하라.
- 오류 메시지를 그대로 길게 복사하지 말고 핵심 원인을 요약하라.
- 개선 사항은 다음 실행에서 바로 적용할 수 있는 행동으로 작성하라.
- 성공한 도구도 중요한 산출물을 만들었다면 기록하라.
"""
