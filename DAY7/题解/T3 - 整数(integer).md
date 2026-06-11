# 整数

## 题目大意

给定一个正整数 $n$，有三种操作：

1. 将 $n$ 减去 $1$，代价为 $a$；
2. 将 $n$ 加上任意正整数，代价为 $b$；
3. 如果 $n$ 是偶数，可以将 $n$ 除以 $2$，代价为 $c$。

如果某个操作的代价为 $0$，表示这个操作不能使用。现在要把 $n$ 变成 $1$，求最小代价。

## 思路分析

首先考虑操作 $2$ 的特殊性：它可以把当前数加上任意正整数。

如果我们决定使用操作 $2$，那么它只需要使用一次。因为多次加法完全可以合并成一次加法，并且放在最开始执行，这样只花一次 $b$ 的代价，还不会因为中间加大数字而产生额外的减法。

所以整个过程只有两种情况：

- 完全不使用操作 $2$；
- 一开始使用一次操作 $2$，把 $n$ 变成某个 $M>n$，然后不再使用操作 $2$。

先考虑不使用操作 $2$ 的情况。

设 $F(x)$ 表示只使用操作 $1$ 和操作 $3$，把 $x$ 变成 $1$ 的最小代价。

如果只靠减法，代价是：

$$
(x-1)a
$$

如果 $x$ 是偶数，可以先除以 $2$：

$$
F(x)=\min((x-1)a,F(x/2)+c)
$$

如果 $x$ 是奇数，那么想使用除法，必须先减 $1$ 变成偶数，再除以 $2$：

$$
F(x)=\min((x-1)a,F(\lfloor x/2\rfloor)+a+c)
$$

当然，如果某个操作不可用，对应的转移就不能使用。

接下来考虑使用一次操作 $2$ 的情况。假设把 $n$ 变成了某个 $M>n$，那么总代价是：

$$
b+F(M)
$$

我们需要求：

$$
\min_{M>n}(b+F(M))
$$

于是定义：

$$
G(x)=\min_{K\ge x}F(K)
$$

这样使用操作 $2$ 的答案就是：

$$
b+G(n+1)
$$

下面考虑如何求 $G(x)$。

如果 $x$ 是偶数，那么我们可以选择一个偶数 $K\ge x$，先除以 $2$，它会变成某个 $\ge x/2$ 的数，所以有：

$$
G(x)=\min((x-1)a,G(x/2)+c)
$$

如果 $x$ 是奇数，那么最小的候选数可以是 $x$ 本身，也可以是更大的偶数。选择 $x$ 本身的代价是 $F(x)$；如果选择偶数，最小偶数至少是 $x+1$，除以 $2$ 后至少是 $(x+1)/2$，所以：

$$
G(x)=\min(F(x),G((x+1)/2)+c)
$$

由于每次递归都会把数除以 $2$，所以单次询问只会产生 $O(\log n)$ 个状态。用记忆化搜索即可。

下面是正解：

```c++
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const ll INF = (ll)2e18;

ll n, a, b, c;
map<ll, ll> memoF, memoG;

ll mul_cost(ll x, ll y) {
    __int128 v = (__int128)x * y;
    if (v > INF) return INF;
    return (ll)v;
}

ll F(ll x) {
    if (x == 1) return 0;
    if (memoF.count(x)) return memoF[x];

    ll res = INF;

    if (a != 0) {
        res = min(res, mul_cost(x - 1, a));
    }

    if (c != 0) {
        if (x % 2 == 0) {
            ll sub = F(x / 2);
            if (sub != INF) res = min(res, sub + c);
        } else if (a != 0) {
            ll sub = F(x / 2);
            if (sub != INF) res = min(res, sub + a + c);
        }
    }

    return memoF[x] = res;
}

ll G(ll x) {
    if (x == 1) return 0;
    if (memoG.count(x)) return memoG[x];

    ll res = INF;

    if (a != 0) {
        res = min(res, mul_cost(x - 1, a));
    }

    if (x % 2 == 0) {
        if (c != 0) {
            ll sub = G(x / 2);
            if (sub != INF) res = min(res, sub + c);
        }
    } else {
        res = min(res, F(x));

        if (c != 0) {
            ll sub = G((x + 1) / 2);
            if (sub != INF) res = min(res, sub + c);
        }
    }

    return memoG[x] = res;
}

void solve() {
    cin >> n >> a >> b >> c;

    memoF.clear();
    memoG.clear();

    ll ans = F(n);

    if (b != 0) {
        ll sub = G(n + 1);
        if (sub != INF) {
            ans = min(ans, sub + b);
        }
    }

    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        solve();
    }

    return 0;
}
```

每次递归都会把 $n$ 缩小到大约一半，所以单次询问的状态数是 $O(\log n)$。对于 $q\le 2\times 10^5$，总复杂度为 $O(q\log n)$，可以通过本题数据范围。

