// 子任务 2 模型：m=1 时枚举单个色泽，最坏偏差为 max(a,k-a)。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    ll k;
    if (!(cin >> n >> m >> k)) return 0;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    if (m != 1) {
        cout << 0 << '\n';
        return 0;
    }
    ll ans = k;
    for (ll x : a) ans = min(ans, max(x, k - x));
    cout << ans << '\n';
    return 0;
}
