// 子任务 1 模型：t<=20 且 r-l<=1e5 时完全枚举。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int max_digit(ll x) {
    int res = 0;
    while (x) res = max<int>(res, x % 10), x /= 10;
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        ll l, r;
        cin >> l >> r;
        if (r - l > 100000) {
            cout << "0 0\n";
            continue;
        }
        int best = -1;
        string ans;
        for (ll x = l; x <= r; ++x) {
            int d = max_digit(x);
            string s = to_string(x);
            if (d > best || (d == best && (ans.empty() || s < ans))) best = d, ans = s;
        }
        cout << best << ' ' << ans << '\n';
    }
    return 0;
}
