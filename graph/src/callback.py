from langchain_core.callbacks import BaseCallbackHandler


class UniversalTokenUsageHandler(BaseCallbackHandler):
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def on_llm_end(self, response, **kwargs):
        usage = response.llm_output.get("token_usage") if response.llm_output else None
       
        if usage:
            self.total_prompt_tokens += usage.get("prompt_tokens") or usage.get("input_tokens") or 0
            self.total_completion_tokens += usage.get("completion_tokens") or usage.get("output_tokens") or 0
            return

        for generations in response.generations:
            for generation in generations:
                if hasattr(generation, 'message'):
                    metadata = getattr(generation.message, 'usage_metadata', {})
                    if metadata:
                        self.total_prompt_tokens += metadata.get("input_tokens", 0)
                        self.total_completion_tokens += metadata.get("output_tokens", 0)

    def report(self):
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
        }