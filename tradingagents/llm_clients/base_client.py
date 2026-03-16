from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseLLMClient(ABC):
    """所有 LLM 客户端的抓象基类。定义统一接口，屏蔽不同 Provider 的差异。"""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        self.model = model       # 模型名称/标识符
        self.base_url = base_url # API 端点 URL
        self.kwargs = kwargs     # 扩展参数（timeout、api_key 等）

    @abstractmethod
    def get_llm(self) -> Any:
        """返回配置好的 LLM 实例。"""
        pass

    @abstractmethod
    def validate_model(self) -> bool:
        """验证该客户端是否支持指定模型。"""
        pass
