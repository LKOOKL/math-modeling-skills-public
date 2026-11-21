# 可移植性与依赖

## 技能依赖与项目目录

- 建模决策的授权范围、实际决策者及证据记录使用包内的[决策约定](../skills/workflow-orchestrator/references/decision-authority.md)。相关技能安装时应保留协调器及其参考文档。
- `formula-derivation` 提及 `proof-writer` 作为特定证明任务的后继；该扩展技能未纳入本次范围。相应任务可在另行安装后使用，或根据已有材料登记缺口。
- 本套件的建模结果报告由 `result-report-generator` 整理。其他工具集中的同名“实验报告”流程可能需要不同的指标和输入。
- 建模协调入口是 `workflow-orchestrator`，写作入口是 `write-math-modeling-papers`。
- `planning/`、`methods/`、`results/`、`paper/` 等路径通常指执行任务时产生的项目文件；其中示例记录与模板占位内容须由真实材料填写。
- 中文编译按项目引擎与文献工具在隔离目录执行。交付前按本题规则核对正文边界及 PDF，详见 [paper-compile](../skills/paper-compile/SKILL.md)。

## 检查的含义

可通过 [SHA-256 清单](source-manifest.json)核对随附技能文件。本文档不代表已执行建模、数值实验、LaTeX 编译或跨平台运行。赛事链接仍须在实际使用时按技能要求核对当届有效版本。
