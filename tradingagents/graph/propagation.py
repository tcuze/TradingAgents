# TradingAgents/graph/propagation.py

from typing import Dict, Any, List, Optional
from tradingagents.agents.utils.agent_states import (
    AgentState,
    InvestDebateState,
    RiskDebateState,
)


class Propagator:
    """Handles state initialization and propagation through the graph."""

    def __init__(self, max_recur_limit=100):
        """Initialize with configuration parameters."""
        self.max_recur_limit = max_recur_limit

    def create_initial_state(
        self, company_name: str, trade_date: str
    ) -> Dict[str, Any]:
        """创建 Agent 图的初始状态字典。"""
        return {
            "messages": [("human", company_name)],  # 初始消息：含股票代码
            "company_of_interest": company_name,      # 当前分析的公司
            "trade_date": str(trade_date),             # 交易日期
            "investment_debate_state": InvestDebateState(
                {
                    "bull_history": "",       # 多方历史发言
                    "bear_history": "",       # 空方历史发言
                    "history": "",            # 全部辩论历史
                    "current_response": "",   # 最新一次发言
                    "judge_decision": "",     # Research Manager 的裁判结果
                    "count": 0,               # 当前辩论轮次计数
                }
            ),
            "risk_debate_state": RiskDebateState(
                {
                    "aggressive_history": "",           # 激进方历史发言
                    "conservative_history": "",         # 保守方历史发言
                    "neutral_history": "",              # 中性方历史发言
                    "history": "",                      # 全部讨论历史
                    "latest_speaker": "",               # 最近一次发言的分析师
                    "current_aggressive_response": "",  # 激进方最新辩论
                    "current_conservative_response": "",# 保守方最新辩论
                    "current_neutral_response": "",     # 中性方最新辩论
                    "judge_decision": "",               # Risk Judge 的最终裁判
                    "count": 0,                         # 当前讨论轮次计数
                }
            ),
            "market_report": "",        # 市场技术指标分析报告
            "fundamentals_report": "",  # 基本面分析报告
            "sentiment_report": "",     # 社交媒体情绪分析报告
            "news_report": "",          # 全球宏观新闻分析报告
        }

    def get_graph_args(self, callbacks: Optional[List] = None) -> Dict[str, Any]:
        """Get arguments for the graph invocation.

        Args:
            callbacks: Optional list of callback handlers for tool execution tracking.
                       Note: LLM callbacks are handled separately via LLM constructor.
        """
        config = {"recursion_limit": self.max_recur_limit}
        if callbacks:
            config["callbacks"] = callbacks
        return {
            "stream_mode": "values",
            "config": config,
        }
