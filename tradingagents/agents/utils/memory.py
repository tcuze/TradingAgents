"""基于 BM25 算法的金融情境记忆模块。

使用 BM25（Best Matching 25）词频统计算法进行文本相似度检索。
无需 API 调用，无 Token 限制，完全离线运行，兼容任意 LLM 供应商。
"""

from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re


class FinancialSituationMemory:
    """基于 BM25 的金融情境记忆系统，用于存储和检索历史经验。"""

    def __init__(self, name: str, config: dict = None):
        """初始化记忆系统。

        Args:
            name: 当前记忆实例的标识名称
            config: 配置字典（保留以兼容接口，BM25 模式下不使用）
        """
        self.name = name
        self.documents: List[str] = []       # 存储市场情境文本
        self.recommendations: List[str] = [] # 存储对应的反思建议
        self.bm25 = None                     # BM25 索引对象

    def _tokenize(self, text: str) -> List[str]:
        """对文本进行分词，用于 BM25 索引构建和查询。

        使用简单的空白符 + 标点符号分割策略，并统一转为小写。
        """
        # 转为小写并按非字母数字字符分割
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _rebuild_index(self):
        """添加文档后重新构建 BM25 索引。"""
        if self.documents:
            tokenized_docs = [self._tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized_docs)
        else:
            self.bm25 = None

    def add_situations(self, situations_and_advice: List[Tuple[str, str]]):
        """添加金融情境及对应的反思建议。

        Args:
            situations_and_advice: (市场情境描述, 改进建议) 元组列表
        """
        for situation, recommendation in situations_and_advice:
            self.documents.append(situation)
            self.recommendations.append(recommendation)

        # 重建 BM25 索引以包含新增文档
        self._rebuild_index()

    def get_memories(self, current_situation: str, n_matches: int = 1) -> List[dict]:
        """使用 BM25 相似度搜索最匹配的历史经验。

        Args:
            current_situation: 当前市场情境描述文本
            n_matches: 返回的最佳匹配数量

        Returns:
            包含 matched_situation、recommendation、similarity_score 的字典列表
        """
        if not self.documents or self.bm25 is None:
            return []  # 记忆库为空时直接返回空列表

        # 对查询文本进行分词
        query_tokens = self._tokenize(current_situation)

        # 计算所有文档的 BM25 分数
        scores = self.bm25.get_scores(query_tokens)

        # 按分数降序排列，取前 n 个索引
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_matches]

        # 构建结果列表，将分数归一化到 [0, 1] 区间
        results = []
        max_score = max(scores) if max(scores) > 0 else 1  # 避免除以零

        for idx in top_indices:
            normalized_score = scores[idx] / max_score if max_score > 0 else 0
            results.append({
                "matched_situation": self.documents[idx],
                "recommendation": self.recommendations[idx],
                "similarity_score": normalized_score,
            })

        return results

    def clear(self):
        """清空所有存储的记忆。"""
        self.documents = []
        self.recommendations = []
        self.bm25 = None


if __name__ == "__main__":
    # Example usage
    matcher = FinancialSituationMemory("test_memory")

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
