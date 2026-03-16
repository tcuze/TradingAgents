from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor


@tool
def get_fundamentals(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    获取指定股票的综合基本面数据报告。
    供应商屁1 fundamental_data 配置决定：可选 alpha_vantage 或 yfinance。
    Args:
        ticker (str): 公司股票代码
        curr_date (str): 当前交易日期，格式 yyyy-mm-dd
    Returns:
        str: 包含综合基本面数据的格式化报告
    """
    return route_to_vendor("get_fundamentals", ticker, curr_date)


@tool
def get_balance_sheet(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    获取指定股票的资产负债表数据。
    供应商屁1 fundamental_data 配置决定。
    Args:
        ticker (str): 公司股票代码
        freq (str): 报告频率： annual（年报）/quarterly（季报），默认季报
        curr_date (str): 当前交易日期，格式 yyyy-mm-dd
    Returns:
        str: 包含资产负债表数据的格式化报告
    """
    return route_to_vendor("get_balance_sheet", ticker, freq, curr_date)


@tool
def get_cashflow(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    获取指定股票的现金流量表数据。
    供应商屁1 fundamental_data 配置决定。
    Args:
        ticker (str): 公司股票代码
        freq (str): 报告频率： annual / quarterly，默认季报
        curr_date (str): 当前交易日期，格式 yyyy-mm-dd
    Returns:
        str: 包含现金流量表数据的格式化报告
    """
    return route_to_vendor("get_cashflow", ticker, freq, curr_date)


@tool
def get_income_statement(
    ticker: Annotated[str, "ticker symbol"],
    freq: Annotated[str, "reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"] = None,
) -> str:
    """
    获取指定股票的利润表数据。
    供应商屁1 fundamental_data 配置决定。
    Args:
        ticker (str): 公司股票代码
        freq (str): 报告频率： annual / quarterly，默认季报
        curr_date (str): 当前交易日期，格式 yyyy-mm-dd
    Returns:
        str: 包含利润表数据的格式化报告
    """
    return route_to_vendor("get_income_statement", ticker, freq, curr_date)