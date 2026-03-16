# TradingAgents/graph/signal_processing.py

from langchain_openai import ChatOpenAI


class SignalProcessor:
    """Processes trading signals to extract actionable decisions."""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """Initialize with an LLM for processing."""
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """
        解析完整交易信号，提取核心决策。

        Args:
            full_signal: 风险切山输出的完整文本信号

        Returns:
            抽取出的交易决策（BUY、SELL 或 HOLD）
        """
        messages = [
            (
                "system",
                # 系统提示：只输出决策关键词，不要额外说明
                "You are an efficient assistant designed to analyze paragraphs or financial reports provided by a group of analysts. Your task is to extract the investment decision: SELL, BUY, or HOLD. Provide only the extracted decision (SELL, BUY, or HOLD) as your output, without adding any additional text or information.",
            ),
            ("human", full_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
