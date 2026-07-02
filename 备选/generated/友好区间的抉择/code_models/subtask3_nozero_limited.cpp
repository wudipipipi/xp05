// 子任务 3 模型：假设没有 0，合法段长度至多 20；枚举短合法段并离线回答。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<int> bit;
    explicit Fenwick(int n = 0) : n(n), bit(n + 1) {}
    void add(int i, int v) { for (; i <= n; i += i & -i) bit[i] += v; }
    int sum(int i) const {
        int r = 0;
        for (; i > 0; i -= i & -i) r += bit[i];
        return r;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    vector<array<int, 3>> queries(q);
    for (int i = 0; i < q; ++i) cin >> queries[i][0] >> queries[i][1], queries[i][2] = i;
    vector<pair<int, int>> segs;
    for (int L = 1; L <= n; ++L) {
        int mask = 0;
        for (int R = L; R <= n && R < L + 20; ++R) {
            if (mask & a[R]) break;
            mask |= a[R];
            segs.push_back({R, L});
        }
    }
    sort(segs.begin(), segs.end());
    sort(queries.begin(), queries.end(), [](auto x, auto y) { return x[1] < y[1]; });
    Fenwick fw(n);
    vector<ll> ans(q);
    int p = 0;
    for (auto qu : queries) {
        int l = qu[0], r = qu[1], id = qu[2];
        while (p < (int)segs.size() && segs[p].first <= r) fw.add(segs[p++].second, 1);
        ans[id] = fw.sum(n) - fw.sum(l - 1);
    }
    for (ll x : ans) cout << x << '\n';
    return 0;
}
