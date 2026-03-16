from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from dotenv import load_dotenv

# 从 .env 文件加载环境变量（API 密钥等配置）
load_dotenv()

# 基于默认配置创建自定义配置副本
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-5-mini"  # 深度思考 LLM（用于 Research Manager / Risk Judge 等复杂决策节点）
config["quick_think_llm"] = "gpt-5-mini"  # 快速响应 LLM（用于各分析师、研究员等节点）
config["max_debate_rounds"] = 1  # 多空研究员辩论最大轮次

# 配置数据供应商（默认使用 yfinance，无需额外 API 密钥）
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # 可选：alpha_vantage / yfinance（股价 OHLCV 数据）
    "technical_indicators": "yfinance",      # 可选：alpha_vantage / yfinance（技术指标数据）
    "fundamental_data": "yfinance",          # 可选：alpha_vantage / yfinance（基本面数据）
    "news_data": "yfinance",                 # 可选：alpha_vantage / yfinance（新闻数据）
}

# 使用自定义配置初始化 TradingAgents 图
ta = TradingAgentsGraph(debug=True, config=config)

# 正向传播：运行所有 Agent 节点，获取最终交易决策
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# 反思与记忆：基于持仓盈亏更新各 Agent 记忆库（形成自我改进闭环）
# ta.reflect_and_remember(1000)  # 参数为本次持仓盈亏金额（正数盈利，负数亏损）
