// 满分模型：双指针求每个右端点的最左合法左端点，再用前缀和和二分回答询问。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n + 1), f(n + 1), cnt(20);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    int L = 1;
    for (int R = 1; R <= n; ++R) {
        for (int b = 0; b < 20; ++b) if ((a[R] >> b) & 1) ++cnt[b];
        while (true) {
            bool bad = false;
            for (int b = 0; b < 20; ++b) bad |= cnt[b] > 1;
            if (!bad) break;
            for (int b = 0; b < 20; ++b) if ((a[L] >> b) & 1) --cnt[b];
            ++L;
        }
        f[R] = L;
    }
    vector<ll> pref(n + 1);
    for (int i = 1; i <= n; ++i) pref[i] = pref[i - 1] + i - f[i] + 1;
    while (q--) {
        int l, r;
        cin >> l >> r;
        int mid = int(upper_bound(f.begin() + l, f.begin() + r + 1, l) - f.begin()) - 1;
        ll ans = 0;
        if (mid >= l) {
            ll len = mid - l + 1;
            ans += len * (len + 1) / 2;
        }
        if (mid < r) ans += pref[r] - pref[max(mid, l - 1)];
        cout << ans << '\n';
    }
    return 0;
}
