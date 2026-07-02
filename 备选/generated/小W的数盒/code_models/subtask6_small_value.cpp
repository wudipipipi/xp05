// 子任务 6 模型：假设 ai<=2^16，用小值域 lowbit 计数；出现更高值时输出占位答案。
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
        vector<int> cnt(17);
        bool ok = true;
        for (int i = 0; i < n; ++i) {
            ll x;
            cin >> x;
            ok &= x <= (1LL << 16);
            if (x <= (1LL << 16)) {
                int e = __builtin_ctzll(x);
                ++cnt[e];
            }
        }
        if (!ok) {
            cout << 0 << '\n';
            continue;
        }
        int first = -1;
        for (int i = 0; i <= 16; ++i) if (cnt[i] && first < 0) first = i;
        if (first < 0) {
            cout << 0 << '\n';
            continue;
        }
        ll mn = 1LL << first, ans = 0;
        for (int i = 0; i <= 16; ++i) if (cnt[i]) {
            ll w = 1LL << i;
            ans += 1LL * (cnt[i] - 1) * w;
            if (w != mn) ans += w + mn;
        }
        cout << ans << '\n';
    }
    return 0;
}
