import os

DEFAULT_CONFIG = {
    # 项目根目录：自动定位到当前模块所在文件夹
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    # 结果输出目录，可通过环境变量 TRADINGAGENTS_RESULTS_DIR 覆盖
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    # 数据缓存目录，存放从 yfinance / Alpha Vantage 获取的历史行情与新闻数据
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # ── LLM 配置 ──────────────────────────────────────────────────────────
    "llm_provider": "openai",            # 可选：openai / anthropic / google / ollama / openrouter / xai
    "deep_think_llm": "gpt-5.2",        # 深度思考模型（Research Manager / Risk Judge 等复杂决策节点）
    "quick_think_llm": "gpt-5-mini",    # 快速响应模型（各分析师、研究员、交易员等节点）
    "backend_url": "https://api.openai.com/v1",  # API 端点 URL（openai 兼容接口）
    # Provider 特定的推理参数
    "google_thinking_level": None,       # Gemini 思考级别：可选 "high" / "minimal" 等
    "openai_reasoning_effort": None,     # OpenAI 推理强度：可选 "medium" / "high" / "low"
    # ── 辩论轮次配置 ───────────────────────────────────────────────────────
    "max_debate_rounds": 1,              # 多空研究员辩论最大轮次（每轮含多空各一次发言）
    "max_risk_discuss_rounds": 1,        # 风险分析师三方讨论最大轮次
    "max_recur_limit": 100,              # LangGraph 图递归调用上限，防止死循环
    # ── 数据供应商配置 ─────────────────────────────────────────────────────
    # 类别级别配置（同类所有工具的默认供应商）
    "data_vendors": {
        "core_stock_apis": "yfinance",       # 股价 OHLCV 数据：可选 alpha_vantage / yfinance
        "technical_indicators": "yfinance",  # 技术指标数据：可选 alpha_vantage / yfinance
        "fundamental_data": "yfinance",      # 基本面数据（财报三表等）：可选 alpha_vantage / yfinance
        "news_data": "yfinance",             # 新闻数据：可选 alpha_vantage / yfinance
    },
    # 工具级别配置（优先级高于类别级别，可单独覆盖某个工具的供应商）
    "tool_vendors": {
        # 示例：单独指定 get_stock_data 使用 alpha_vantage
        # "get_stock_data": "alpha_vantage",
    },
}
