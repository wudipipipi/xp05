# 小W的数盒代码模型

| 文件 | 算法/假设 | 预期用途 |
| :-- | :-- | :-- |
| `correct.cpp` | 统计所有 lowbit 并套满分公式 | 满分基准 |
| `subtask1_bruteforce.cpp` | `n<=8` 合并顺序搜索 | 测试点 1~2 |
| `subtask2_all_odd.cpp` | 全奇数公式 `n-1` | 测试点 3~4 |
| `subtask3_same_lowbit.cpp` | 同 lowbit 公式 | 测试点 5~7 |
| `subtask4_distinct_lowbit.cpp` | lowbit 两两不同公式 | 测试点 8~11 |
| `subtask5_two_lowbits.cpp` | 至多两种 lowbit 公式 | 测试点 12~15 |
| `subtask6_small_value.cpp` | `ai<=2^16` 小值域计数 | 测试点 16~20 |

矩阵结果见题包根目录 `提交矩阵.md`。
