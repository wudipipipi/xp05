# 数字橱窗代码模型

| 文件 | 算法/假设 | 预期用途 |
| :-- | :-- | :-- |
| `correct.cpp` | 短区间枚举 + 长区间常数候选 | 满分基准 |
| `subtask1_bruteforce.cpp` | `t<=20,r-l<=1e5` 完全枚举 | 测试点 1~2 |
| `subtask2_short_interval.cpp` | `r-l<10` 枚举 | 测试点 3~5 |
| `subtask3_same_length.cpp` | 同位数字典序等于数值序 | 测试点 6~9 |
| `subtask4_same_length_has9.cpp` | 同位且存在含 9 数 | 测试点 10~13 |
| `subtask5_span_at_least_10.cpp` | `r-l>=10` 时最大数码为 9 | 测试点 14~18 和满分长区间 |

矩阵结果见题包根目录 `提交矩阵.md`。
