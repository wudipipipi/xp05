// 满分模型：只统计每个 lowbit 权值出现次数，按最小权值合并公式计算。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll lowbit(ll x) { return x & -x; }

ll solve_one(const vector<ll> &a) {
    if (a.size() <= 1) return 0;
    map<ll, int> cnt;
    for (ll x : a) ++cnt[lowbit(x)];
    ll mn = cnt.begin()->first;
    ll ans = 0;
    for (auto [w, c] : cnt) {
        ans += 1LL * (c - 1) * w;
        if (w != mn) ans += w + mn;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        cin >> n;
        vector<ll> a(n);
        for (ll &x : a) cin >> x;
        cout << solve_one(a) << '\n';
    }
    return 0;
}
