from typing import Any, Optional

from langchain_anthropic import ChatAnthropic

from .base_client import BaseLLMClient
from .validators import validate_model


class AnthropicClient(BaseLLMClient):
    """支持 Anthropic Claude 系列模型的 LLM 客户端。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """返回配置好的 ChatAnthropic 实例。"""
        llm_kwargs = {"model": self.model}

        # 将支持的可选参数一并传入
        for key in ("timeout", "max_retries", "api_key", "max_tokens", "callbacks", "http_client", "http_async_client"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return ChatAnthropic(**llm_kwargs)

    def validate_model(self) -> bool:
        """验证 Anthropic 是否支持指定模型。"""
        return validate_model("anthropic", self.model)
