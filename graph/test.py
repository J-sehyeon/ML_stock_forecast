# graph생성 테스트
# https://docs.langchain.com/langsmith/test-react-agent-pytest#setup
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_community.tools import TavilySearchResults

model = init_chat_model(
    "gpt-5",
    temperature=0
)

# Define search tool
search_tool = TavilySearchResults(
    max_results=5,
    include_raw_content=True,
)

# typeddict가 뭔지 찾아보기


