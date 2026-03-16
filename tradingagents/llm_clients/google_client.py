from typing import Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI

from .base_client import BaseLLMClient
from .validators import validate_model


class NormalizedChatGoogleGenerativeAI(ChatGoogleGenerativeAI):
    """ChatGoogleGenerativeAI 子类：将 Gemini 3 返回的列表式 content 正则化为字符串。

    Gemini 3 模型返回的 content 格式为：[{'type': 'text', 'text': '...'}]
    此子类将其统一转换为字符串，确保下游处理的一致性。
    """

    def _normalize_content(self, response):
        """将列表式内容合并为单一字符串。"""
        content = response.content
        if isinstance(content, list):
            texts = [
                item.get("text", "") if isinstance(item, dict) and item.get("type") == "text"
                else item if isinstance(item, str) else ""
                for item in content
            ]
            response.content = "\n".join(t for t in texts if t)
        return response

    def invoke(self, input, config=None, **kwargs):
        """执行调用并对内容进行正则化。"""
        return self._normalize_content(super().invoke(input, config, **kwargs))


class GoogleClient(BaseLLMClient):
    """支持 Google Gemini 系列模型的 LLM 客户端。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """返回配置好的 NormalizedChatGoogleGenerativeAI 实例。"""
        llm_kwargs = {"model": self.model}

        for key in ("timeout", "max_retries", "google_api_key", "callbacks", "http_client", "http_async_client"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        # 将 thinking_level 映射到对应的 API 参数
        # Gemini 3 Pro: low, high
        # Gemini 3 Flash: minimal, low, medium, high
        # Gemini 2.5: thinking_budget（0=禁用, -1=动态）
        thinking_level = self.kwargs.get("thinking_level")
        if thinking_level:
            model_lower = self.model.lower()
            if "gemini-3" in model_lower:
                # Gemini 3 Pro 不支持 "minimal"，自动降级为 "low"
                if "pro" in model_lower and thinking_level == "minimal":
                    thinking_level = "low"
                llm_kwargs["thinking_level"] = thinking_level
            else:
                # Gemini 2.5 使用 thinking_budget 控制思考深度
                llm_kwargs["thinking_budget"] = -1 if thinking_level == "high" else 0

        return NormalizedChatGoogleGenerativeAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """验证 Google 是否支持指定模型。"""
        return validate_model("google", self.model)
