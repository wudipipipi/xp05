// 子任务 3 模型：假设 l,r 位数相同，同位数下字典序等于数值序。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int max_digit(ll x) {
    int res = 0;
    while (x) res = max<int>(res, x % 10), x /= 10;
    return res;
}

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
        if (r - l <= 100) {
            int best = -1;
            string ans;
            for (ll x = l; x <= r; ++x) {
                int d = max_digit(x);
                string s = to_string(x);
                if (d > best || (d == best && (ans.empty() || s < ans))) best = d, ans = s;
            }
            cout << best << ' ' << ans << '\n';
        } else {
            ll ans = -1;
            for (ll x = l; x <= min(r, l + 10); ++x) if (has9(x)) { ans = x; break; }
            cout << 9 << ' ' << ans << '\n';
        }
    }
    return 0;
}
