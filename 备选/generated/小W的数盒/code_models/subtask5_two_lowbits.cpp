// 子任务 5 模型：假设 lowbit 至多两种，按两类计数公式计算。
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
        map<ll, int> cnt;
        for (int i = 0; i < n; ++i) {
            ll x;
            cin >> x;
            ++cnt[lowbit(x)];
        }
        if (cnt.size() > 2) {
            cout << 0 << '\n';
            continue;
        }
        ll ans = 0;
        for (auto [w, c] : cnt) ans += 1LL * (c - 1) * w;
        if (cnt.size() == 2) ans += cnt.begin()->first + cnt.rbegin()->first;
        cout << ans << '\n';
    }
    return 0;
}
