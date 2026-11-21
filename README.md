# 数学建模技能集

本仓库收录 31 个数学建模竞赛技能，覆盖题目分析、建模求解、结果整理、中文 LaTeX 写作和交付审查。

## 快速入口

| 任务 | 入口 |
| --- | --- |
| 规划或推进整个数学建模任务 | [workflow-orchestrator](skills/workflow-orchestrator/SKILL.md) |
| 已有模型和结果，重新写作或排版 | [write-math-modeling-papers](skills/write-math-modeling-papers/SKILL.md) |
| 选择具体阶段的工具 | [完整技能目录](docs/CATALOG.md) |
| 安装到另一台电脑 | [安装与使用](docs/INSTALL.md) |
| 了解依赖及使用限制 | [可移植性与依赖](docs/PORTABILITY.md) |
| 查询来源和许可状态 | [来源说明](docs/PROVENANCE.md) |

## 已保留的写作约定

- 大框架依照随附国赛 TeXstudio 模板，结合写作经验作章内调整和排版小修。
- 每问独立使用 `\section`；结果分析、误差分析、敏感性分析分别放在本问的 `\subsection` 中，其他适用检验同级组织。
- 每问每个最终模型至少展示伪代码或流程图之一，内容对应实际模型和算法；模板中的 K-Means 仅示范伪代码形式。
- 写作技能依据已有技术材料成稿，明确区分材料证据、数值验证、编译及页面检查。LaTeX 为唯一论文正文源。

随附国赛 TeX 模板及其 TeXstudio 元数据。详细约束见[用户模板契约](skills/write-math-modeling-papers/references/user-template-contract.md)。

## 目录

```text
skills/                  各技能的 SKILL.md、references、assets 和界面元数据
docs/CATALOG.md          按任务阶段分类的技能目录
docs/INSTALL.md          安装与调用方法
docs/PORTABILITY.md      技能依赖及项目目录约定
docs/PROVENANCE.md       来源与许可状态
docs/source-manifest.json 本版技能文件的 SHA-256 校验清单
```

本快照范围仅为数学建模相关技能及其随附资源。项目题目、论文、原始数据、求解结果、会话记录、账号配置及系统/插件缓存均在导出范围之外。需要其他领域技能时另行扩展清单。

安装后可按校验清单核对技能文件，并按实际项目的输入、授权与赛规选择工作流程。
