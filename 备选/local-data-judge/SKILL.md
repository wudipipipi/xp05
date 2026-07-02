---
name: local-data-judge
description: Use when validating an OI/CSP programming problem with local official data or a full problem package. Compile and run std, brute, partial, wrong, checker, validator, and data locally; verify statement-data-code consistency; produce reports, issue documents, and test matrices.
---

# Local Data Judge

## Core Principle

Use this skill only when local official data, a problem package, checker, validator, std, or other source programs are available. Prefer local closed-loop validation over OJ blackbox inference. Do not assume std, checker, validator, or official outputs are correct until cross-checked.

Every conclusion must be tied to evidence: file path, test number, command, status, output difference, assertion condition, log excerpt, or reproduction step.

## Workflow

### 1. Inventory The Package

Identify:

- Statement, samples, and down/sample files.
- Official input/output data.
- `std`, `brute`/`baoli`, `partial`, `wrong`, `slow`, `overflow`.
- `checker`, `validator`, `generator`, scripts, and judging config.
- Subtask mapping, test numbering, score configuration, `.cdf`, yaml/json, or existing records.

If the package is incomplete, list missing items and say whether each missing item blocks local validation.

### 2. Check Statement And Data Consistency

Verify:

- Input/output format matches all data files.
- Samples match the statement and down/sample files are synchronized.
- Bounds, subtasks, and special properties can be checked by validator or assertions.
- Multi-solution, precision, modulo, no-solution, empty-set, duplicate, and boundary behavior are defined.
- Every test point maps to a subtask or data type.
- Data covers minima, maxima, extreme structures, random cases, constructive counterexamples, and combined boundaries.

### 3. Compile

Default to:

```bash
g++ -std=c++17 -O2
```

Compile std, brute, partial, wrong, slow, overflow, checker, and validator when present. Record compile failures as CE with concise error summaries. If Chinese or spaced paths cause trouble, compile from the source directory with relative paths. Clean temporary `.exe`, `.out`, and `.tmp` files unless they are needed as evidence.

### 4. Run Local Validation

For every official input:

- Run validator to confirm input legality.
- Run std and confirm no RE/TLE.
- If official `.out` exists, compare std output with official output.
- If checker exists, use it to judge output legality.
- For small data, cross-check std against brute.
- Use validator or assertion probes to check subtasks and special properties.

For multi-solution problems, prefer checker over plain text diff. If checker is unavailable, explicitly state that diff is not final correctness evidence.

### 5. Test Partial And Wrong Solutions

Run partial/wrong/slow/overflow programs on relevant data or all data. Record:

- Passed tests.
- Failed tests.
- Failure type.
- Whether the result matches expectation.
- Why abnormal passes or abnormal failures occurred.

Analysis order:

- Partial scores too high: first decide whether the partial is actually full, then consider data weakness.
- Partial scores too low: first check bugs, complexity, boundaries, and statement interpretation.
- Wrong solution scores too high: identify the wrong assumption and propose constructive counterexamples.
- Slow solution scores too high: inspect data scale, time limits, constants, and stronger complexity probes.
- Overflow solution scores too high: inspect extreme values and answer range.

### 6. Maintain Matrices

Program summary:

```text
程序名 | 算法/假设 | 预期通过范围 | 实际通过测试点 | 失败测试点 | 结论
```

Full test matrix:

```text
程序名 | 样例1 | 样例2 | ... | 1 | 2 | ... | 20
```

Use:

- AC: accepted by checker or matching official output.
- WA: wrong output.
- TLE: timeout.
- RE: runtime error, assertion failure, out-of-bounds, or abnormal exit.
- CE: compile error.
- SKIP: skipped for a stated reason.

### 7. Output Reports

Generate these sections:

```text
【验题结论】
- 是否建议通过验题：
- 主要风险等级：
- 阻塞问题：

【题面与子任务检查】
- 题面问题：
- 子任务定义问题：
- 样例/down 同步问题：

【数据合法性检查】
- validator 结果：
- 子任务限制检查：
- 特殊性质检查：
- 边界覆盖评价：

【标准程序与 checker 风险】
- std 正确性：
- std 复杂度：
- std 边界/溢出：
- checker 正确性与宽严程度：

【本地运行矩阵】
- 汇总 std、brute、partial、wrong、slow、overflow 的结果。
- 明确每份程序通过和未通过的测试点。
- 对异常通过/失败给出原因分析。

【数据强度评价】
- 哪些错误算法被有效卡住；
- 哪些错误算法没有被卡住；
- 哪些子任务或数据类型可能需要补强；
- 具体补数据建议。

【问题清单】
- 问题描述；
- 风险等级；
- 证据；
- 影响；
- 修复建议；
- 复验方式。
```

When asked to save reports, prefer:

- `验题报告.md`: complete conclusion, matrices, and data strength evaluation.
- `问题文档.md`: key issues, evidence, impact, and fixes.
- `本地运行记录.md`: compile commands, run commands, failure summaries, and reproduction steps.
- `code_models/` or `judge_models/`: representative source models and README if new code models are created.

## Code Requirements

- Use C++17 by default.
- Use standard input/output.
- Avoid debug output.
- Use sufficiently large integer types.
- Avoid undersized arrays that could mislead validation.
- Locally verify anything that can be locally verified.
- Clearly state residual risk for anything that cannot be verified.
