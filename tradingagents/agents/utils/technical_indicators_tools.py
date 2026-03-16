from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_indicators(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[str, "The current trading date you are trading on, YYYY-mm-dd"],
    look_back_days: Annotated[int, "how many days to look back"] = 30,
) -> str:
    """
    获取指定股票的单个技术指标数据。
    供应商屁1 technical_indicators 配置决定：可选 alpha_vantage 或 yfinance。
    Args:
        symbol (str): 公司股票代码，如 AAPL, TSM
        indicator (str): 单个技术指标名称，如 'rsi', 'macd'。每次调用只传一个指标。
        curr_date (str): 当前交易日期，格式 YYYY-mm-dd
        look_back_days (int): 回看天数，默认 30 天
    Returns:
        str: 包含指定股票和指标数据的格式化表格字符串
    """
    # LLM 有时会将多个指标作为逗号分隔的字符串传入，需拆分后逐个处理
    indicators = [i.strip() for i in indicator.split(",") if i.strip()]
    if len(indicators) > 1:
        results = []
        for ind in indicators:
            results.append(route_to_vendor("get_indicators", symbol, ind, curr_date, look_back_days))
        return "\n\n".join(results)
    return route_to_vendor("get_indicators", symbol, indicator.strip(), curr_date, look_back_days)