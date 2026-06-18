# PRTS 的危机演算

## 题目大意

给定两个整数序列 $A$ 和 $B$，长度分别为 $n,m$。把所有 $A_i\times B_j$ 放到一起，一共有 $n\times m$ 个数。

现在要求把这些乘积从小到大排序后，第 $K$ 个数是多少。

序列中的数可能为正数、负数或 $0$，并且乘积可能超过 `int` 范围，所以需要使用 `long long`。

## 思路分析

最直接的想法是枚举所有乘积。

我们可以把每一对 $(i,j)$ 的 $A_iB_j$ 都算出来，然后排序，最后输出第 $K$ 个。这样一共有 $nm$ 个乘积，复杂度至少是：

$$
O(nm\log(nm))
$$

这个做法只能通过 $n,m\le 1000$ 的小数据。

如果 $K=1$ 或 $K=nm$，只要求所有乘积中的最小值或最大值。最大值和最小值一定来自两个序列中的最大值、最小值组合，所以只要检查：

$$
\min A\times \min B,\quad \min A\times \max B,\quad \max A\times \min B,\quad \max A\times \max B
$$

这四种情况即可。

接下来考虑一般情况。因为要求的是第 $K$ 小值，很自然想到二分答案。

假设当前二分的值是 $x$，如果我们能够快速求出：

$$
cnt(x)=\#\{(i,j)\mid A_iB_j\le x\}
$$

那么：

- 如果 $cnt(x)\ge K$，说明第 $K$ 小值不大于 $x$；
- 如果 $cnt(x)<K$，说明第 $K$ 小值大于 $x$。

于是答案就是最小的满足 $cnt(x)\ge K$ 的 $x$。

问题变成如何快速统计不超过 $x$ 的乘积个数。

### 全为正数的情况

如果两个序列中所有数都是正数，那么把 $A,B$ 排序后，乘积矩阵有单调性。

对每个 $A_i$，满足 $A_iB_j\le x$ 的 $B_j$ 是一个前缀。可以对每个 $A_i$ 二分，也可以用双指针统计。

双指针做法是：

- 枚举 $A_i$ 从小到大；
- 指针 $j$ 指向当前还能满足 $A_iB_j\le x$ 的最大位置；
- 随着 $A_i$ 变大，合法的 $j$ 只会往左移动。

这样一次统计就是 $O(n+m)$。

### 处理正负号

满分数据中会出现正数、负数和 $0$，所以需要分类。

我们把两个序列分别拆成三类：

- 正数；
- 负数的绝对值；
- $0$ 的个数。

例如 $-5$ 会放进“负数绝对值”数组，值为 $5$。

这样所有乘积可以分成三类。

#### 负乘积

负乘积来自：

- $A$ 的负数 $\times B$ 的正数；
- $A$ 的正数 $\times B$ 的负数。

如果当前 $x\ge 0$，那么所有负乘积一定都 $\le x$，可以直接全部计入。

如果当前 $x<0$，设负乘积为 $-p$，其中 $p>0$。要求：

$$
-p\le x
$$

等价于：

$$
p\ge -x
$$

所以只要统计两个正数数组中，乘积至少为 $-x$ 的对数即可。

#### 零乘积

只要 $A_i=0$ 或 $B_j=0$，乘积就是 $0$。

零乘积个数为：

$$
cnt_0=zero_A\cdot m+zero_B\cdot n-zero_A\cdot zero_B
$$

最后一项是因为 $(0,0)$ 被算了两次。

如果 $x\ge 0$，这些零乘积都要计入；如果 $x<0$，零乘积不满足条件。

#### 正乘积

正乘积来自：

- 正数 $\times$ 正数；
- 负数 $\times$ 负数。

因为负数已经取了绝对值，所以它们也可以看成两个正数数组的乘积。

当 $x\ge 0$ 时，统计正乘积中不超过 $x$ 的对数即可；当 $x<0$ 时，没有正乘积会被计入。

于是我们只需要写一个函数：

```c++
count_le(X, Y, x)
```

表示两个升序正数数组 $X,Y$ 中，有多少对乘积不超过 $x$。这个函数用双指针即可。

乘积至少为 $need$ 的对数，则可以用：

$$
|X|\cdot |Y|-count\_le(X,Y,need-1)
$$

求出来。

下面是正解：

```c++
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

ll count_le_product(const vector<ll> &a, const vector<ll> &b, ll x) {
    if (a.empty() || b.empty() || x <= 0) return 0;

    ll cnt = 0;
    int j = (int)b.size() - 1;

    for (ll v : a) {
        while (j >= 0 && v * b[j] > x) {
            j--;
        }
        cnt += j + 1;
    }

    return cnt;
}

ll count_ge_product(const vector<ll> &a, const vector<ll> &b, ll x) {
    if (a.empty() || b.empty()) return 0;

    ll total = (ll)a.size() * (ll)b.size();
    return total - count_le_product(a, b, x - 1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    ll K;
    cin >> n >> m >> K;

    vector<ll> posA, negA, posB, negB;
    ll zeroA = 0, zeroB = 0;

    for (int i = 0; i < n; i++) {
        ll x;
        cin >> x;

        if (x > 0) posA.push_back(x);
        else if (x < 0) negA.push_back(-x);
        else zeroA++;
    }

    for (int i = 0; i < m; i++) {
        ll x;
        cin >> x;

        if (x > 0) posB.push_back(x);
        else if (x < 0) negB.push_back(-x);
        else zeroB++;
    }

    sort(posA.begin(), posA.end());
    sort(negA.begin(), negA.end());
    sort(posB.begin(), posB.end());
    sort(negB.begin(), negB.end());

    ll negative_cnt = (ll)negA.size() * (ll)posB.size()
                    + (ll)posA.size() * (ll)negB.size();

    ll zero_cnt = zeroA * m + zeroB * n - zeroA * zeroB;

    auto count_not_greater = [&](ll x) {
        ll cnt = 0;

        if (x < 0) {
            ll need = -x;

            // -p <= x 等价于 p >= -x
            cnt += count_ge_product(negA, posB, need);
            cnt += count_ge_product(posA, negB, need);
        } else {
            cnt += negative_cnt;
            cnt += zero_cnt;

            cnt += count_le_product(posA, posB, x);
            cnt += count_le_product(negA, negB, x);
        }

        return cnt;
    };

    ll l = -1000000000000000000LL;
    ll r = 1000000000000000000LL;

    while (l < r) {
        ll mid = l + (r - l) / 2;

        if (count_not_greater(mid) >= K) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }

    cout << l << '\n';

    return 0;
}
```

每次检查答案时，四个双指针统计的总复杂度为 $O(n+m)$。二分值域大约进行 $60$ 次，所以总时间复杂度为：

$$
O((n+m)\log V)
$$

其中 $V$ 是答案值域。排序复杂度为 $O(n\log n+m\log m)$。

空间复杂度为 $O(n+m)$。
