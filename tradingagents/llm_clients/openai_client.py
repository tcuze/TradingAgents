import os
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient
from .validators import validate_model


class UnifiedChatOpenAI(ChatOpenAI):
    """ChatOpenAI 子类：对 GPT-5 系列模型过滤 temperature/top_p 参数。

    GPT-5 系列模型内置推理能力，task temperature/top_p 仅在
    reasoning.effort='none' 时被接受。其他情况下 API 会拒绝这些参数。
    LangChain 默认 temperature=0.7，必须主动过滤以避免报错。

    非 GPT-5 模型（GPT-4.1、xAI、Ollama 等）不受影响。
    """

    def __init__(self, **kwargs):
        # 如果是 GPT-5 系列模型，删除 temperature 和 top_p 参数
        if "gpt-5" in kwargs.get("model", "").lower():
            kwargs.pop("temperature", None)
            kwargs.pop("top_p", None)
        super().__init__(**kwargs)


class OpenAIClient(BaseLLMClient):
    """支持 OpenAI、Ollama、OpenRouter 和 xAI 四种 Provider 的 LLM 客户端。"""

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        provider: str = "openai",
        **kwargs,
    ):
        super().__init__(model, base_url, **kwargs)
        self.provider = provider.lower()

    def get_llm(self) -> Any:
        """返回配置好的 ChatOpenAI 实例。"""
        llm_kwargs = {"model": self.model}

        if self.provider == "xai":
            # xAI 使用其岂属 API 端点
            llm_kwargs["base_url"] = "https://api.x.ai/v1"
            api_key = os.environ.get("XAI_API_KEY")
            if api_key:
                llm_kwargs["api_key"] = api_key
        elif self.provider == "openrouter":
            # OpenRouter 路由至各大模型供应商
            llm_kwargs["base_url"] = "https://openrouter.ai/api/v1"
            api_key = os.environ.get("OPENROUTER_API_KEY")
            if api_key:
                llm_kwargs["api_key"] = api_key
        elif self.provider == "ollama":
            # Ollama 本地模型服务无需认证
            llm_kwargs["base_url"] = "http://localhost:11434/v1"
            llm_kwargs["api_key"] = "ollama"  # Ollama 不需要真实认证 key
        elif self.base_url:
            llm_kwargs["base_url"] = self.base_url

        # 将支持的可选参数一并传入
        for key in ("timeout", "max_retries", "reasoning_effort", "api_key", "callbacks", "http_client", "http_async_client"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return UnifiedChatOpenAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """验证当前 Provider 是否支持指定模型。"""
        return validate_model(self.provider, self.model)
