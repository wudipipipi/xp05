# 最后一包馍片代码模型

| 文件 | 算法/假设 | 预期用途 |
| :-- | :-- | :-- |
| `correct.cpp` | 216 状态压缩 DP | 满分基准 |
| `subtask1_bruteforce.cpp` | `n<=20` 枚举扔/不扔 | 测试点 1~2 |
| `subtask2_all_equal.cpp` | 全相等答案为 `n` | 测试点 3~4 |
| `subtask3_n2000_dp.cpp` | `n<=2000` 使用 DP | 测试点 5~8 |
| `subtask4_adjacent_gain4.cpp` | 相邻贡献全 4 公式 | 测试点 9~12 |
| `subtask5_nondecreasing.cpp` | 单调不降时枚举 3^5 分配 | 测试点 13~17 |

矩阵结果见题包根目录 `提交矩阵.md`。
