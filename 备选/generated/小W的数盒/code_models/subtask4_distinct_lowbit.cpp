// 子任务 4 模型：假设 lowbit 两两不同，所有非最小权值直接并入最小权值。
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
        set<ll> st(w.begin(), w.end());
        if ((int)st.size() != n) {
            cout << 0 << '\n';
            continue;
        }
        ll mn = *min_element(w.begin(), w.end());
        ll ans = 0;
        for (ll x : w) if (x != mn) ans += x + mn;
        cout << ans << '\n';
    }
    return 0;
}
