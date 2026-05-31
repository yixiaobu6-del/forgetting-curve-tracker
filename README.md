# 知识遗忘曲线追踪

> 基于艾宾浩斯遗忘曲线的学习复习管理工具，科学对抗遗忘

---

## Features / 功能特点

| 功能 | 说明 |
|------|------|
| 学习录入 | 记录学习内容、分类、日期等完整信息 |
| 遗忘曲线 | 基于艾宾浩斯遗忘曲线展示记忆保留率变化 |
| 复习提醒 | 自动在 1/2/4/7/15/30 天关键时间点提醒复习 |
| 记忆状态 | 已掌握/待复习/遗忘风险三级状态一目了然 |
| 进度统计 | 总条目数、已复习数、待复习数、遗忘风险数 |
| 分类统计 | 各学习类别数量占比环图可视化 |
| 复习操作 | 一键标记完成复习，自动更新记忆保留率 |
| 本地存储 | 所有数据保存于浏览器 localStorage |

## Installation / 安装

无需安装，直接在浏览器中打开 `index.html` 即可使用。

```bash
# 克隆仓库
git clone https://github.com/yourusername/forgetting-curve-tracker.git

cd forgetting-curve-tracker
open index.html
```

## Usage / 使用方法

### 基础用法

1. 打开 `index.html`
2. 在「新增学习」Tab 记录学习内容
3. 返回「仪表盘」查看记忆保留率和进度
4. 在「复习列表」Tab 查看需要复习的内容
5. 完成复习后点击「完成」按钮更新进度

### 艾宾浩斯遗忘曲线复习时间点

| 复习次数 | 复习时间 | 记忆保留率（理论值） |
|:--------:|:--------:|:-------------------:|
| 第1次 | 学习后 1 天 | 约 70% |
| 第2次 | 学习后 2 天 | 约 75% |
| 第3次 | 学习后 4 天 | 约 85% |
| 第4次 | 学习后 7 天 | 约 90% |
| 第5次 | 学习后 15 天 | 约 95% |
| 第6次 | 学习后 30 天 | 接近 100% |

### JavaScript 核心逻辑

```javascript
// 获取待复习条目
function getDueItems() {
  const now = Date.now();
  return items.filter(item => {
    const intervals = [1, 2, 4, 7, 15, 30]; // 天数
    const reviewCount = item.reviewCount || 0;
    if (reviewCount >= intervals.length) return false;
    const daysSinceLast = (now - new Date(item.lastReview || item.createdAt).getTime()) / (1000 * 60 * 60 * 24);
    return daysSinceLast >= intervals[reviewCount];
  });
}

// 标记复习完成
function markReviewed(id) {
  const item = items.find(i => i.id === id);
  if (item) {
    item.reviewCount = (item.reviewCount || 0) + 1;
    item.lastReview = new Date().toISOString();
    saveItems();
    renderDashboard();
    renderReviewList();
  }
}
```

### 记忆保留率算法

```javascript
function retentionRate(createdAt, lastReview, reviewCount) {
  const now = Date.now();
  const hoursElapsed = (now - new Date(createdAt).getTime()) / (1000 * 60 * 60);
  // 基于艾宾浩斯曲线，指数衰减模型
  const rate = Math.exp(-hoursElapsed / (24 * (1 + reviewCount)));
  return Math.max(0, Math.min(1, rate));
}
```

## Contributing / 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

## License / 许可证

MIT License - 参见 [LICENSE](LICENSE)

---

> 版本：1.0.0 | 更新日期：2026-05-30