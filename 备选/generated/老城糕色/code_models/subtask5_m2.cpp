// 子任务 5 模型：假设 n<=5000,m=2，枚举选择的两个色泽。
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
    if (n > 5000 || m != 2) {
        cout << 0 << '\n';
        return 0;
    }
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    ll ans = k;
    for (int i = 0; i < (int)b.size(); ++i) {
        for (int j = i; j < (int)b.size(); ++j) {
            ans = min(ans, max({b[i], k - b[j], (b[j] - b[i]) / 2}));
        }
    }
    cout << ans << '\n';
    return 0;
}
