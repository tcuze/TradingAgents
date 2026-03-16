from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor


@tool
def get_stock_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    获取指定股票代码的价格数据（OHLCV：开盘价/最高价/最低价/收盘价/成交量）。
    供应商屁1 core_stock_apis 配置决定：可选 alpha_vantage 或 yfinance。
    Args:
        symbol (str): 公司股票代码，如 AAPL, TSM
        start_date (str): 起始日期，格式 yyyy-mm-dd
        end_date (str): 结束日期，格式 yyyy-mm-dd
    Returns:
        str: 包含指定日期区间内股价数据的格式化表格字符串
    """
    return route_to_vendor("get_stock_data", symbol, start_date, end_date)
