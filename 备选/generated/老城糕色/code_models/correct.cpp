// 满分模型：二分答案，贪心选择能覆盖当前最左未覆盖点的最右色泽。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool ok(const vector<ll> &b, int m, ll k, ll d) {
    ll cur = 0, best = -1;
    int used = 0, ptr = 0;
    while (cur <= k) {
        while (ptr < (int)b.size() && b[ptr] - d <= cur) best = b[ptr++];
        if (best < 0 || best + d < cur) return false;
        if (++used > m) return false;
        cur = best + d + 1;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    ll k;
    if (!(cin >> n >> m >> k)) return 0;
    vector<ll> b(n);
    for (ll &x : b) cin >> x;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    ll l = 0, r = k;
    while (l < r) {
        ll mid = (l + r) / 2;
        if (ok(b, m, k, mid)) r = mid;
        else l = mid + 1;
    }
    cout << l << '\n';
    return 0;
}
