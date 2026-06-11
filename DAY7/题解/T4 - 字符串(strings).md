# 字符串

## 题目大意

给定一个长度为 $n$ 的字符串，字符集大小为 $m$。其中有些位置已经确定，有些位置为 `-1`，表示可以填成任意一个 $1\sim m$ 中的字符。

如果一个字符串可以被切分成若干段，并且每一段都不是回文串，那么称它为 `Non-Palindrome`。

要求计算有多少种填法可以得到 `Non-Palindrome` 字符串，答案对 $998244353$ 取模。

## 思路分析

这道题如果直接去计算有多少种合法切分方案，会很容易算重。因为一个字符串可能有很多种切分方式，直接 DP 会遇到大量重叠。

所以我们考虑补集：

$$
\text{答案}=\text{所有填法数}-\text{无法被合法切分的坏串数量}
$$

假设原串中 `-1` 的数量为 $cnt$，那么所有填法数就是：

$$
m^{cnt}
$$

接下来关键就是数出坏串数量。

什么样的字符串无论怎么切，都不能切成若干个非回文串？通过观察回文串的结构，可以得到下面的结论。

### 偶数长度

如果 $n$ 是偶数，那么坏串必须是所有字符完全相同的字符串，也就是形如：

$$
aaaa\dots a
$$

只要存在相邻两个字符不同，我们就可以在合适的位置切开，使得至少能产生非回文段。因此偶数长度下，只有全等串会堵死所有合法切分。

### 奇数长度

如果 $n$ 是奇数，坏串有两种形态。

第一种是除了中间位置以外，其他位置全部相同，例如：

$$
aaaaBaaaa
$$

记作 Type A。

第二种是奇数位全部相同，偶数位全部相同，例如：

$$
abababa
$$

记作 Type B。

这两类会有交集：如果一个串既满足 Type A，又满足 Type B，那么它只能是所有位置完全相同的字符串。

所以奇数长度的坏串数量可以用容斥计算：

$$
\text{bad}=\text{Type A}+\text{Type B}-\text{All Equal}
$$

不过当 $n=3$ 时，Type A 和 Type B 表示的是同一种结构，直接令：

$$
\text{bad}=\text{Type A}
$$

即可。

下面的问题就变成了：在已有若干确定字符的限制下，分别统计这些形态有多少种填法。

比如统计全等串时，如果所有已知字符都相同，那么：

- 如果没有任何已知字符，可以任选一个字符，方案数为 $m$；
- 否则只能填成这个已知字符，方案数为 $1$。

如果已知字符中出现了不同字符，那么这种形态方案数为 $0$。

Type A 和 Type B 也是同理：

- Type A 只要求除中心外全部相等，中心可以单独选择；
- Type B 要求奇数位一类、偶数位一类，各自内部相等。

下面是正解：

```c++
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int MOD = 998244353;

ll power(ll a, ll b) {
    ll res = 1;
    a %= MOD;
    while (b) {
        if (b & 1) res = res * a % MOD;
        a = a * a % MOD;
        b >>= 1;
    }
    return res;
}

ll count_same(const vector<int> &s, int m, const vector<int> &pos) {
    int fixed = -1;
    for (int i : pos) {
        if (s[i] == -1) continue;
        if (fixed == -1) fixed = s[i];
        else if (fixed != s[i]) return 0;
    }
    return fixed == -1 ? m : 1;
}

void solve() {
    int n, m;
    cin >> n >> m;

    vector<int> s(n);
    int cnt = 0;
    for (int i = 0; i < n; i++) {
        cin >> s[i];
        if (s[i] == -1) cnt++;
    }

    if (n == 1) {
        cout << 0 << '\n';
        return;
    }

    ll total = power(m, cnt);
    ll bad = 0;

    vector<int> all;
    for (int i = 0; i < n; i++) all.push_back(i);

    if (n % 2 == 0) {
        bad = count_same(s, m, all);
    } else {
        int mid = n / 2;

        // All Equal
        ll all_equal = count_same(s, m, all);

        // Type A：除了中心外全部相等
        vector<int> outer;
        for (int i = 0; i < n; i++) {
            if (i != mid) outer.push_back(i);
        }

        ll type_a = count_same(s, m, outer);
        if (type_a != 0 && s[mid] == -1) {
            type_a = type_a * m % MOD;
        }

        // Type B：奇偶位置分别相等
        vector<int> even_pos, odd_pos;
        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) even_pos.push_back(i);
            else odd_pos.push_back(i);
        }

        ll type_b = count_same(s, m, even_pos) * count_same(s, m, odd_pos) % MOD;

        if (n == 3) {
            bad = type_a;
        } else {
            bad = (type_a + type_b - all_equal + MOD) % MOD;
        }
    }

    cout << (total - bad + MOD) % MOD << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        solve();
    }

    return 0;
}
```

每个测试用例只需要扫描常数遍字符串，时间复杂度为 $O(n)$。由于 $\sum n\le 5\times 10^5$，可以通过本题数据范围。

