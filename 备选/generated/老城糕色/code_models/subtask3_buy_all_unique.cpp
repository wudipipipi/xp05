// 子任务 3 模型：假设可以买下所有不同色泽，直接计算相邻最大空隙。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

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
    if (m < (int)b.size()) {
        cout << 0 << '\n';
        return 0;
    }
    ll ans = max(b.front(), k - b.back());
    for (int i = 1; i < (int)b.size(); ++i) ans = max(ans, (b[i] - b[i - 1]) / 2);
    cout << ans << '\n';
    return 0;
}
