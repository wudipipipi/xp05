// 子任务 1 模型：n<=18 时枚举所有可购买集合。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll worst(vector<ll> s, ll k) {
    sort(s.begin(), s.end());
    s.erase(unique(s.begin(), s.end()), s.end());
    ll res = max(s.front(), k - s.back());
    for (int i = 1; i < (int)s.size(); ++i) res = max(res, (s[i] - s[i - 1]) / 2);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    ll k;
    if (!(cin >> n >> m >> k)) return 0;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    if (n > 18) {
        cout << 0 << '\n';
        return 0;
    }
    ll ans = k;
    for (int mask = 1; mask < (1 << n); ++mask) {
        if (__builtin_popcount((unsigned)mask) > m) continue;
        vector<ll> s;
        for (int i = 0; i < n; ++i) if ((mask >> i) & 1) s.push_back(a[i]);
        ans = min(ans, worst(s, k));
    }
    cout << ans << '\n';
    return 0;
}
