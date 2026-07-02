// 子任务 4 模型：假设同位且区间中存在含 9 的数，找数值最小的含 9 数。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool has9(ll x) { return to_string(x).find('9') != string::npos; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        ll l, r;
        cin >> l >> r;
        if (to_string(l).size() != to_string(r).size()) {
            cout << "0 0\n";
            continue;
        }
        ll ans = -1;
        for (ll x = l; x <= min(r, l + 10); ++x) if (has9(x)) { ans = x; break; }
        if (ans < 0) cout << "0 0\n";
        else cout << 9 << ' ' << ans << '\n';
    }
    return 0;
}
