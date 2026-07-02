// 子任务 1 模型：n,q<=100 时直接枚举询问内所有子段；超出假设时输出占位答案。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    if (n > 100 || q > 100) {
        while (q--) {
            int l, r;
            cin >> l >> r;
            cout << 0 << '\n';
        }
        return 0;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        ll ans = 0;
        for (int L = l; L <= r; ++L) {
            int mask = 0;
            for (int R = L; R <= r; ++R) {
                if (mask & a[R]) break;
                mask |= a[R];
                ++ans;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
