// 子任务 4 模型：假设 ai<=1，问题变成统计区间内至多包含一个 1 的子段。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n + 1), pos;
    bool ok = true;
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
        if (a[i] > 1) ok = false;
        if (a[i] == 1) pos.push_back(i);
    }
    pos.insert(pos.begin(), 0);
    pos.push_back(n + 1);
    while (q--) {
        int l, r;
        cin >> l >> r;
        if (!ok) {
            cout << 0 << '\n';
            continue;
        }
        int first = int(lower_bound(pos.begin(), pos.end(), l) - pos.begin());
        int last = int(upper_bound(pos.begin(), pos.end(), r) - pos.begin()) - 1;
        ll ans = 0;
        int prev = l - 1;
        for (int i = first; i <= last; ++i) {
            int z = pos[i] - prev - 1;
            ans += 1LL * z * (z + 1) / 2;
            int left = pos[i] - max(l, pos[i - 1] + 1) + 1;
            int right = min(r, pos[i + 1] - 1) - pos[i] + 1;
            ans += 1LL * left * right;
            prev = pos[i];
        }
        int z = r - prev;
        ans += 1LL * z * (z + 1) / 2;
        cout << ans << '\n';
    }
    return 0;
}
