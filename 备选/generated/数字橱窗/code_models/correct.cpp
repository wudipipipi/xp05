// 满分模型：短区间直接枚举，长区间枚举各位数长度的常数个含 9 候选。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int max_digit(ll x) {
    int res = 0;
    while (x) res = max<int>(res, x % 10), x /= 10;
    return res;
}

bool has9(ll x) { return to_string(x).find('9') != string::npos; }

pair<int, string> solve(ll l, ll r) {
    if (r - l <= 100) {
        int best = -1;
        string ans;
        for (ll x = l; x <= r; ++x) {
            int d = max_digit(x);
            string s = to_string(x);
            if (d > best || (d == best && (ans.empty() || s < ans))) best = d, ans = s;
        }
        return {best, ans};
    }
    vector<string> cand;
    for (int len = 1; len <= 10; ++len) {
        ll lo = len == 1 ? 1 : (ll)pow(10, len - 1);
        ll hi = min((ll)pow(10, len) - 1, 1000000000LL);
        ll L = max(l, lo), R = min(r, hi);
        if (L > R) continue;
        for (ll x = L; x <= min(R, L + 10); ++x) {
            if (has9(x)) {
                cand.push_back(to_string(x));
                break;
            }
        }
    }
    return {9, *min_element(cand.begin(), cand.end())};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        ll l, r;
        cin >> l >> r;
        auto [d, s] = solve(l, r);
        cout << d << ' ' << s << '\n';
    }
    return 0;
}
