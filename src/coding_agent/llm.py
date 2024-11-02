import os

from llmlib import (
    AnthropicModel,
    LLMClient,
    Provider,
)



class LLM:
    def __init__(self):
        self.client = LLMClient(
            provider=Provider.ANTHROPIC,
            model=AnthropicModel.CLAUDE_3_5_SONNET,
            anthropic_key=os.environ["ANTHROPIC_API_KEY"],
        )
