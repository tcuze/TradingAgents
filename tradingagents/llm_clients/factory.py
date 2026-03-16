from typing import Optional

from .base_client import BaseLLMClient
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient
from .google_client import GoogleClient


def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """工厂函数：根据指定 Provider 创建对应的 LLM 客户端实例。

    Args:
        provider: LLM 供应商（openai / anthropic / google / xai / ollama / openrouter）
        model: 模型名称/标识符
        base_url: 可选 API 端点 URL
        **kwargs: Provider 特定的额外参数：
            - http_client: 自定义 httpx.Client（SSL 代理或证书自定义）
            - http_async_client: 自定义 httpx.AsyncClient
            - timeout: 请求超时秒数
            - max_retries: 最大重试次数
            - api_key: API 密钥
            - callbacks: LangChain 回调处理器

    Returns:
        已配置的 BaseLLMClient 实例

    Raises:
        ValueError: 供应商不受支持时抛出异常
    """
    provider_lower = provider.lower()

    # openai / ollama / openrouter 均使用 OpenAI 兼容接口
    if provider_lower in ("openai", "ollama", "openrouter"):
        return OpenAIClient(model, base_url, provider=provider_lower, **kwargs)

    # xAI Grok 系列也将使用 OpenAI 客户端（自定义 API 地址）
    if provider_lower == "xai":
        return OpenAIClient(model, base_url, provider="xai", **kwargs)

    if provider_lower == "anthropic":
        return AnthropicClient(model, base_url, **kwargs)

    if provider_lower == "google":
        return GoogleClient(model, base_url, **kwargs)

    raise ValueError(f"Unsupported LLM provider: {provider}")
