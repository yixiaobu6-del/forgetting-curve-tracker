"""知识遗忘曲线追踪 - 基于艾宾浩斯遗忘曲线的复习提醒"""

import json
from datetime import datetime, timedelta


class KnowledgeItem:
    """知识条目，记录学过的知识和复习历史，基于艾宾浩斯遗忘曲线追踪。"""

    def __init__(self, title: str, content: str, category: str = "", tags: list = None):
        """初始化知识条目。

        Args:
            title: 知识标题
            content: 内容摘要（最多200字）
            category: 分类，如"编程"、"认知科学"
            tags: 标签列表
        """
        self.title = title
        self.content = content[:200]
        self.category = category
        self.tags = tags or []
        self.created = datetime.now()
        self.reviews = []

    def add_review(self):
        """记录一次复习，将当前时间追加到复习历史中。"""
        self.reviews.append(datetime.now())

    @property
    def review_count(self) -> int:
        """获取已复习次数。

        Returns:
            复习次数
        """
        return len(self.reviews)

    @property
    def retention_rate(self) -> float:
        """模拟计算当前记忆保留率。

        基于艾宾浩斯遗忘曲线公式近似计算。

        Returns:
            保留率百分比（0-100），无复习时返回0
        """
        if not self.reviews:
            return 0.0
        days_since = (datetime.now() - self.reviews[-1]).days
        # 艾宾浩斯遗忘曲线模拟
        return max(0, 100 - 50 * (1 - 2.718 ** (-days_since / 7)))


class ForgettingCurve:
    """遗忘曲线管理器，基于艾宾浩斯复习计划调度知识复习。"""

    REVIEW_SCHEDULE = [1, 2, 4, 7, 15, 30, 60, 120]  # 复习间隔（天）

    def __init__(self):
        """初始化曲线管理器，创建空知识条目列表。"""
        self.items = []

    def add(self, item: KnowledgeItem):
        """添加知识条目到管理列表。

        Args:
            item: KnowledgeItem 实例

        Returns:
            返回自身以支持链式调用
        """
        self.items.append(item)
        return self

    def next_review(self, item: KnowledgeItem) -> datetime | None:
        """计算知识条目的下次复习时间。

        Args:
            item: 要查询的知识条目

        Returns:
            下次复习时间，如已超过最大间隔则返回 None
        """
        n = item.review_count
        if n >= len(self.REVIEW_SCHEDULE):
            return None
        last = item.reviews[-1] if item.reviews else item.created
        return last + timedelta(days=self.REVIEW_SCHEDULE[n])

    def due_items(self) -> list:
        """获取所有到期待复习的知识条目列表。

        Returns:
            待复习条目列表，按截止时间升序排列，每项为(item, next_review_time)元组
        """
        now = datetime.now()
        due = []
        for item in self.items:
            next_review = self.next_review(item)
            if next_review and next_review <= now:
                due.append((item, next_review))
        return sorted(due, key=lambda x: x[1])

    def summary(self) -> str:
        """生成知识复习状态报告。

        Returns:
            格式化的文本报告，包含条目总数、待复习数量、复习日历等
        """
        total = len(self.items)
        due = len(self.due_items())
        lines = [
            f"知识遗忘曲线追踪",
            f"{'='*40}",
            f"总计: {total} 条知识",
            f"待复习: {due} 条",
            f"平均复习次数: {sum(i.review_count for i in self.items)/max(total,1):.1f}",
            "\n复习日历:",
        ]
        for item, next_time in self.due_items()[:10]:
            lines.append(f"  [待复习] {item.title} — 下次复习: {next_time.strftime('%m-%d')}")
        return "\n".join(lines)


if __name__ == "__main__":
    curve = ForgettingCurve()
    item = KnowledgeItem("Python装饰器原理",
                         "装饰器是一个接受函数并返回函数的高阶函数",
                         "编程", ["Python"])
    item.add_review()
    curve.add(item)

    item2 = KnowledgeItem("艾宾浩斯遗忘曲线",
                          "遗忘在学习之后立即开始，最初遗忘速度很快",
                          "认知科学", ["学习方法"])
    item2.add_review()
    item2.add_review()
    curve.add(item2)

    print(curve.summary())
