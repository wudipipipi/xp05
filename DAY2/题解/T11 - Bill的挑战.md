# Bill的挑战

## 题目大意

给定 $N$ 个长度相同的字符串，每个字符串由小写字母和 `?` 组成。现在要统计有多少个只包含小写字母的字符串 $T$，恰好能和这 $N$ 个字符串中的 $K$ 个匹配。

其中 `?` 可以匹配任意小写字母，普通字母只能匹配自己。

答案对 $1000003$ 取模。

## 思路分析

首先看数据范围，$N\le 15$，这提示我们可以用二进制状态表示当前匹配了哪些字符串。

对于一个已经构造出的前缀，我们只关心它目前还可能匹配哪些给定字符串。设一个二进制集合 `mask`，第 $j$ 位为 $1$ 表示当前前缀仍然可以匹配第 $j$ 个字符串。

一开始还没有填任何字符，所以所有字符串都能匹配：

$$
mask=(1<<N)-1
$$

接下来逐位填写 $T$。

对于第 $i$ 个位置，如果我们填入字符 $ch$，它能匹配哪些字符串是可以提前算出来的。记：

$$
match[i][ch]
$$

表示第 $i$ 位填入 $ch$ 时，这一位可以匹配的字符串集合。

如果当前状态是 `mask`，那么填入 $ch$ 之后，仍然能匹配的字符串就是：

$$
mask\ \&\ match[i][ch]
$$

于是可以做状态压缩 DP。

设：

$$
dp[i][mask]
$$

表示已经填完前 $i$ 个位置后，当前还能匹配的字符串集合为 `mask` 的方案数。

初始状态：

$$
dp[0][(1<<N)-1]=1
$$

转移：

```c++
nxt = mask & match[i][ch];
dp[i + 1][nxt] += dp[i][mask];
```

最后处理完整个字符串后，枚举所有 `mask`，如果其中恰好有 $K$ 个 $1$，就把对应方案数加入答案。

下面是正解：

```c++
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000003;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;

        vector<string> s(n);
        for (int i = 0; i < n; i++) {
            cin >> s[i];
        }

        int len = (int)s[0].size();
        int full = (1 << n) - 1;

        vector<vector<int>> match(len, vector<int>(26, 0));

        for (int i = 0; i < len; i++) {
            for (int ch = 0; ch < 26; ch++) {
                int mask = 0;
                for (int j = 0; j < n; j++) {
                    if (s[j][i] == '?' || s[j][i] == char('a' + ch)) {
                        mask |= (1 << j);
                    }
                }
                match[i][ch] = mask;
            }
        }

        vector<vector<int>> dp(len + 1, vector<int>(1 << n, 0));
        dp[0][full] = 1;

        for (int i = 0; i < len; i++) {
            for (int mask = 0; mask <= full; mask++) {
                if (dp[i][mask] == 0) continue;

                for (int ch = 0; ch < 26; ch++) {
                    int nxt = mask & match[i][ch];
                    dp[i + 1][nxt] += dp[i][mask];
                    if (dp[i + 1][nxt] >= MOD) {
                        dp[i + 1][nxt] -= MOD;
                    }
                }
            }
        }

        int ans = 0;
        for (int mask = 0; mask <= full; mask++) {
            if (__builtin_popcount((unsigned)mask) == k) {
                ans += dp[len][mask];
                if (ans >= MOD) ans -= MOD;
            }
        }

        cout << ans << '\n';
    }

    return 0;
}
```

设字符串长度为 $L$，状态数为 $2^N$，每个状态枚举 $26$ 个字符，所以时间复杂度为：

$$
O(L\cdot 2^N\cdot 26)
$$

空间复杂度为 $O(L\cdot 2^N)$，也可以用滚动数组优化到 $O(2^N)$。

