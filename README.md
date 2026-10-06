# Finance-education：美股投资对话学习

面向零基础学习者的美股基本面课程。通过中文对话、手算练习和真实财报，逐步建立独立研究能力。案例路线为 **MSFT → MU**，学习时间可碎片化安排。

## 从哪里开始

- [学习计划](./学习计划.md)：8 个关卡、33 个小课、练习与材料索引。
- [学习进度模板](./学习进度模板.md)：首次初始化后生成本机的学习进度.md。
- [AGENTS.md](./AGENTS.md)：教学规则，包含提问、反馈、数据核验与断点保存。

| 可用时间 | 这次做什么 |
|---|---|
| 5 分钟 | 复习一个概念或纠正一道错题 |
| 15 分钟 | 学一个概念，自己完成一道小题 |
| 30 分钟以上 | 阅读财报或做一段综合公司研究 |

一课可以跨多次对话完成。先讲例子，再让学习者练习；根据理解证据推进，不按固定周数或短期模拟收益验收。

## 在本机初始化

需要 Git 与 Python 3.10 或更高版本。初始化脚本只使用 Python 标准库，各上游应用的依赖在用到对应课程时再安装。

先普通克隆本项目，再运行初始化脚本：

    git clone https://github.com/zja2004/Finance-education.git
    cd Finance-education
    python scripts/bootstrap.py

脚本会读取固定上游版本，完整克隆五个项目，核验提交与 Git 对象，处理 Windows 文件名问题，并在本机生成学习进度.md 和 repos/克隆核验.json。已有仓库或学习记录会先检查并保留，不覆盖不一致的内容。

核验已有安装：

    python scripts/bootstrap.py --check

Windows 请使用上述脚本初始化。Finance-Education 有一个含问号的文件名，直接递归检出全部子模块会在 Windows 失败。脚本保留完整历史、仅排除非法工作区路径，并生成内容一致的改名副本。参见 [Windows 兼容说明](./materials/Finance-Education-Windows/README.md)。

## 课程路线

| 关卡 | 主题 |
|---|---|
| 1 | 股票、收益、复利、ETF、美股机制与成本 |
| 2 | 利润表、资产负债表、现金流量表及报告期间 |
| 3 | 商业模式、竞争优势、盈利质量和资本效率 |
| 4 | P/E、P/S、P/B、EV/EBITDA 与适用边界 |
| 5 | 现金流、资本成本、DCF 与敏感性分析 |
| 6 | MU 的库存、供需、资本开支与周期估值 |
| 7 | 分散、回撤、ETF、再平衡与模拟组合 |
| 8 | 证据整理、反方论证、AI 输出核验与研究报告 |

首课已准备“股票、股价与市值”的讲解和模拟练习。初始化后，可以让你的对话助手读取 AGENTS.md 与本机学习进度.md，再说“开始第一课”或“继续学投资”。

## 五个上游项目

| 项目 | 用途 | 本地目录 |
|---|---|---|
| [Finance-Education](https://github.com/engineerinvestor/Finance-Education) | 复利、收益与组合专题 | repos/Finance-Education |
| [fundamental-analysis-toolkit](https://github.com/linusschulze-quant/fundamental-analysis-toolkit) | 固定 MSFT 数据、财务分析与估值 | repos/fundamental-analysis-toolkit |
| [equity-research-lab](https://github.com/mariasfondrini/equity-research-lab) | SEC 数据、财务口径与完整研究流程 | repos/equity-research-lab |
| [sellside-research-engine](https://github.com/DogInfantry/sellside-research-engine) | 多种估值、Reverse DCF 与风险 | repos/sellside-research-engine |
| [analyst-agent](https://github.com/jacob187/analyst-agent) | 财报辅助研究与 AI 输出审计 | repos/analyst-agent |

上游通过固定提交的 Git 子模块接入，原仓库历史与作者信息保留。具体提交及兼容映射记录在 [upstreams.json](./upstreams.json)。课程中的上游材料链接也固定到对应提交，避免默认分支更新改变教材。

## 学习记录与资料日期

学习进度.md 是本机学习记录，默认被 Git 忽略；公共仓库提供的是初始模板。运行脚本时只在该文件不存在时生成，后续会话更新本机文件。

MSFT 教学快照的年度数据为 FY2025，季度快照为 2025-09-30，市场快照为 2025-12-26。这些历史资料用于练习，当前公司研究需重新核验当时已经公开的原始披露。练习使用历史财报与模拟组合。

课程与克隆准备好后，各上游项目仍需要按其 README 单独配置环境。仓库引用与文件核验不代表五套应用已经运行通过。

## 许可证与来源

本项目原创内容使用 [MIT](./LICENSE)。上游代码与数据分别适用原作者的许可条件，详见 [第三方来源说明](./THIRD_PARTY_NOTICES.md)。其中两个固定版本未声明许可证，相关内容保留上游引用，未作为本项目的 MIT 内容重新分发。
