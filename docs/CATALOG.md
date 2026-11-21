# 技能目录

保留技能原名，以维持已有调用和相对引用。MATLAB 分支及通用编译技能按任务选用。

## 入口与任务协调

| 技能 | 入口说明 |
| --- | --- |
| [workflow-orchestrator](../skills/workflow-orchestrator/SKILL.md) | 协调逐问进度、材料门槛和技能调用。 |
| [write-math-modeling-papers](../skills/write-math-modeling-papers/SKILL.md) | 依据已有技术材料，按国赛模板撰写、排版和审查论文。 |

## 题目、数据与模型

| 技能 | 入口说明 |
| --- | --- |
| [problem-parser](../skills/problem-parser/SKILL.md) | 提取题目目标、对象、约束、数据、输出和各问接口。 |
| [problem-classifier](../skills/problem-classifier/SKILL.md) | 分析各问题型和建模任务特征。 |
| [data-auditor-cleaner](../skills/data-auditor-cleaner/SKILL.md) | 审查数据质量，记录清洗处理及其影响。 |
| [related-paper-analyzer](../skills/related-paper-analyzer/SKILL.md) | 整理相关论文中的方法与适用依据。 |
| [model-assumptions-builder](../skills/model-assumptions-builder/SKILL.md) | 组织模型假设及其依据、作用和适用边界。 |
| [symbol-table-builder](../skills/symbol-table-builder/SKILL.md) | 维护符号、含义、单位和跨问一致性。 |
| [method-selector](../skills/method-selector/SKILL.md) | 比较候选方法、验证可行性并支持方法选择。 |
| [formula-derivation](../skills/formula-derivation/SKILL.md) | 组织公式、假设和推导链，形成可追踪的理论材料。 |

## 代码与结果

| 技能 | 入口说明 |
| --- | --- |
| [model-code-analyzer](../skills/model-code-analyzer/SKILL.md) | 将已确定的模型关系拆解为代码实现要求。 |
| [python-model-code-generator](../skills/python-model-code-generator/SKILL.md) | 依据模型与接口要求编写 Python 求解代码。 |
| [python-code-reviewer](../skills/python-code-reviewer/SKILL.md) | 审查 Python 实现、数据处理与模型一致性。 |
| [matlab-model-code-generator](../skills/matlab-model-code-generator/SKILL.md) | 依据模型与接口要求编写 MATLAB 求解代码。 |
| [matlab-code-reviewer](../skills/matlab-code-reviewer/SKILL.md) | 审查 MATLAB 实现及模型一致性。 |
| [code-reviewer](../skills/code-reviewer/SKILL.md) | 识别编程语言并路由到相应数学建模代码审查技能。 |
| [result-report-generator](../skills/result-report-generator/SKILL.md) | 整理逐问实验输出、结果和对应证据。 |
| [final-method-explainer](../skills/final-method-explainer/SKILL.md) | 整理最终方法说明及选择依据，供写作交接。 |
| [robustness-checker](../skills/robustness-checker/SKILL.md) | 组织稳健性、敏感性及稳定性检验。 |
| [solution-package-builder](../skills/solution-package-builder/SKILL.md) | 汇总逐问方法、结果、检验和冻结数据，交接给写作者。 |

## 图表、写作与编译

| 技能 | 入口说明 |
| --- | --- |
| [figure-table-planner](../skills/figure-table-planner/SKILL.md) | 规划逐问图表、过程展示及其正文位置。 |
| [math-figure-generator](../skills/math-figure-generator/SKILL.md) | 生成服务于数学建模结论的学术图表。 |
| [paper-section-writer](../skills/paper-section-writer/SKILL.md) | 根据逐问交接材料撰写模型与结果章节。 |
| [paper-polisher](../skills/paper-polisher/SKILL.md) | 润色论文表达，保持技术含义及证据强度。 |
| [reference-manager](../skills/reference-manager/SKILL.md) | 维护引用来源、参考文献及正文对应关系。 |
| [paper-compile](../skills/paper-compile/SKILL.md) | 编译 LaTeX、处理排版错误并核查输出；按宿主环境适配。 |

## 决策记录与质量审查

| 技能 | 入口说明 |
| --- | --- |
| [decision-prompt-builder](../skills/decision-prompt-builder/SKILL.md) | 将需人工判断的事项组织为简短决策问题。 |
| [modeler-decision-logger](../skills/modeler-decision-logger/SKILL.md) | 记录建模决策、依据、来源及版本。 |
| [consistency-auditor](../skills/consistency-auditor/SKILL.md) | 审查模型、代码、结果和论文之间的一致性。 |
| [completeness-auditor](../skills/completeness-auditor/SKILL.md) | 审查逐问任务、所需材料和交付内容的完整性。 |
| [quality-assurance-auditor](../skills/quality-assurance-auditor/SKILL.md) | 整合质量审查并记录可交付状态和限制。 |
