from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    获取指定股票的相关新闻数据。
    供应商屁1 news_data 配置决定：可选 alpha_vantage 或 yfinance。
    Args:
        ticker (str): 股票代码
        start_date (str): 起始日期，格式 yyyy-mm-dd
        end_date (str): 结束日期，格式 yyyy-mm-dd
    Returns:
        str: 包含新闻数据的格式化字符串
    """
    return route_to_vendor("get_news", ticker, start_date, end_date)

@tool
def get_global_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 5,
) -> str:
    """
    获取全球宏观新闻数据（经济、政治等市场相关新闻）。
    供应商屁1 news_data 配置决定。
    Args:
        curr_date (str): 当前日期，格式 yyyy-mm-dd
        look_back_days (int): 回看天数，默认 7 天
        limit (int): 返回文章数量上限，默认 5 条
    Returns:
        str: 包含全球新闻数据的格式化字符串
    """
    return route_to_vendor("get_global_news", curr_date, look_back_days, limit)

@tool
def get_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
) -> str:
    """
    获取指定公司内部人士買卖记录。
    供应商屁1 news_data 配置决定。
    Args:
        ticker (str): 公司股票代码
    Returns:
        str: 内部人士交易数据报告
    """
    return route_to_vendor("get_insider_transactions", ticker)
