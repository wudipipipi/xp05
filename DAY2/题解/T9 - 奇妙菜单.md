# Emiya 家今天的饭

## 题目大意

有 $n$ 种烹饪方法和 $m$ 种主要食材。第 $i$ 种烹饪方法中，使用第 $j$ 种主要食材的菜有 $a_{i,j}$ 种。

每种烹饪方法最多选择一道菜，也可以不选。要求选择出的菜非空，并且不能存在某一种主要食材，使得它出现的次数超过所有菜数量的一半。

求合法方案数，答案对 $998244353$ 取模。

## 思路分析

首先考虑所有方案数。

对于第 $i$ 种烹饪方法，我们可以不选，也可以选择某一种主要食材对应的一道菜，所以这一行的选择数是：

$$
1+\sum_{j=1}^{m}a_{i,j}
$$

因此所有方案数为：

$$
\prod_{i=1}^{n}\left(1+\sum_{j=1}^{m}a_{i,j}\right)-1
$$

最后减去 $1$ 是为了去掉一道菜都不选的空方案。

接下来要减去不合法方案。

一个方案不合法，当且仅当存在某一种主要食材出现次数超过总菜数的一半。注意这样的食材最多只有一种，因为不可能有两种食材都严格超过一半。

所以我们可以枚举这一个“超标”的食材 $c$，统计它出现次数超过其他所有食材总次数的方案数，然后从总方案中减掉。

对于固定食材 $c$，定义一个差值：

$$
diff=\text{选择食材 }c\text{ 的次数}-\text{选择其他食材的次数}
$$

如果最终 $diff>0$，就说明食材 $c$ 的出现次数超过了一半。

对于第 $i$ 行，有三种选择：

1. 不选菜，$diff$ 不变，方案数乘 $1$；
2. 选择食材 $c$ 的菜，$diff+1$，方案数乘 $a_{i,c}$；
3. 选择其他食材的菜，$diff-1$，方案数乘 $\sum_j a_{i,j}-a_{i,c}$。

于是对每个食材 $c$ 做一个 DP 即可。

设：

$$
dp[i][d]
$$

表示处理完前 $i$ 行后，当前差值为 $d$ 的方案数。因为差值可能为负数，实际写代码时用一个偏移量 $n$，把差值 $d$ 存在下标 $d+n$ 中。

转移就是：

```c++
// 不选
ndp[d] += dp[d];

// 选择当前枚举的食材 c
ndp[d + 1] += dp[d] * a[i][c];

// 选择其他食材
ndp[d - 1] += dp[d] * (row_sum[i] - a[i][c]);
```

最后把所有 $d>0$ 的方案数加起来，就是当前食材 $c$ 导致的不合法方案数。

下面是正解：

```c++
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int MOD = 998244353;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    vector<vector<int>> a(n + 1, vector<int>(m + 1));
    vector<int> row_sum(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
            row_sum[i] += a[i][j];
            if (row_sum[i] >= MOD) row_sum[i] -= MOD;
        }
    }

    ll total = 1;
    for (int i = 1; i <= n; i++) {
        total = total * (row_sum[i] + 1) % MOD;
    }
    total = (total - 1 + MOD) % MOD;

    ll bad = 0;
    int base = n;

    for (int c = 1; c <= m; c++) {
        vector<int> dp(2 * n + 1, 0), ndp(2 * n + 1, 0);
        dp[base] = 1;

        for (int i = 1; i <= n; i++) {
            fill(ndp.begin(), ndp.end(), 0);

            int choose_c = a[i][c];
            int choose_other = (row_sum[i] - choose_c + MOD) % MOD;

            for (int d = -i + 1; d <= i - 1; d++) {
                int cur = dp[d + base];
                if (!cur) continue;

                // 不选这一行
                ndp[d + base] = (ndp[d + base] + cur) % MOD;

                // 选择食材 c
                ndp[d + 1 + base] = (ndp[d + 1 + base] + 1LL * cur * choose_c) % MOD;

                // 选择其他食材
                ndp[d - 1 + base] = (ndp[d - 1 + base] + 1LL * cur * choose_other) % MOD;
            }

            dp.swap(ndp);
        }

        for (int d = 1; d <= n; d++) {
            bad += dp[d + base];
            bad %= MOD;
        }
    }

    cout << (total - bad + MOD) % MOD << '\n';

    return 0;
}
```

枚举超标食材需要 $m$ 次，每次 DP 有 $O(n^2)$ 个状态，所以时间复杂度为：

$$
O(mn^2)
$$

空间复杂度为 $O(n)$。

