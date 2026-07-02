// 子任务 3 模型：假设所有 lowbit 相同，答案为 (n-1)*w。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll lowbit(ll x) { return x & -x; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        cin >> n;
        vector<ll> w(n);
        for (int i = 0; i < n; ++i) {
            ll x;
            cin >> x;
            w[i] = lowbit(x);
        }
        bool ok = true;
        for (ll x : w) ok &= x == w[0];
        cout << (ok ? 1LL * (n - 1) * w[0] : 0) << '\n';
    }
    return 0;
}
