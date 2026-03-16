from langchain_core.messages import HumanMessage, RemoveMessage

# 从各工具文件按类别导入所有工具函数
# 股价核心数据工具
from tradingagents.agents.utils.core_stock_tools import (
    get_stock_data
)
# 技术指标工具
from tradingagents.agents.utils.technical_indicators_tools import (
    get_indicators
)
# 基本面数据工具（财务报表三表）
from tradingagents.agents.utils.fundamental_data_tools import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement
)
# 新闻和内部交易数据工具
from tradingagents.agents.utils.news_data_tools import (
    get_news,
    get_insider_transactions,
    get_global_news
)

def create_msg_delete():
    def delete_messages(state):
        """清除消息队列并添加占位消息，防止上下文过长影响性能和费用。

        注意：Anthropic Claude API 要求消息列表中必须至少有一条 Human 消息，
        因此保留一个 "Continue" 占位符而不是彻底清空。
        """
        messages = state["messages"]

        # 将所有消息标记为待删除
        removal_operations = [RemoveMessage(id=m.id) for m in messages]

        # 添加最小占位符消息（为 Anthropic 展示达抄兼容性）
        placeholder = HumanMessage(content="Continue")

        return {"messages": removal_operations + [placeholder]}

    return delete_messages


        