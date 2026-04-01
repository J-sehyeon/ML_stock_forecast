# graph생성 테스트
# https://docs.langchain.com/langsmith/test-react-agent-pytest#setup

from src.tools import think_tool
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from deepagents import create_deep_agent

# Create model
model = ChatOpenAI(
    model='gpt-5',
    temperature=0,
)

tools = []

from src.prompts import (   # 수정 필요
    RESEARCHER_INSTRUCTIONS,
    ANALYST_INSTRUCTIONS,
    ONTOLOGY,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,   
)

# Limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Combine orchestrator instructions (RESEARCHERINSTRUCTIONS only for sub-agents)
INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 88
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_researcher_iterations,
    )
)
# Create sub-agents
analyze_sub_agent = {
    "name": "analyze-agent",
    "description": "Delegate analyze to the sub-agent analyst. Only give this analyst one content that is the output of the researcher at a time.",
    "system_prompt": ANALYST_INSTRUCTIONS + ONTOLOGY,
    "tools": [think_tool],
}
subagents = []

agent = create_deep_agent(
    model=model,
    tools=tools,
    system_prompt=INSTRUCTIONS,
    subagents=subagents,
)

