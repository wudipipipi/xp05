// 子任务 5 模型：假设 r-l>=10，最大数码必为 9，只需找字典序最小的含 9 数。
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
        if (r - l < 10) {
            cout << "0 0\n";
            continue;
        }
        vector<string> cand;
        for (int len = 1; len <= 10; ++len) {
            ll lo = len == 1 ? 1 : (ll)pow(10, len - 1);
            ll hi = min((ll)pow(10, len) - 1, 1000000000LL);
            ll L = max(l, lo), R = min(r, hi);
            if (L > R) continue;
            for (ll x = L; x <= min(R, L + 10); ++x) if (has9(x)) {
                cand.push_back(to_string(x));
                break;
            }
        }
        cout << 9 << ' ' << *min_element(cand.begin(), cand.end()) << '\n';
    }
    return 0;
}
