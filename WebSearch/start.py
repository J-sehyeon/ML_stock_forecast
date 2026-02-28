from tavily import TavilyClient

tavily_client = TavilyClient(api_key="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")
response = tavily_client.search("엔비디아의 최근 소식")

print(response)

