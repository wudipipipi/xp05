// 子任务 2 模型：n,q<=2000 时预处理所有合法子段并做二维前缀和。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    vector<pair<int, int>> qs(q);
    for (auto &x : qs) cin >> x.first >> x.second;
    if (n > 2000 || q > 2000) {
        for (int i = 0; i < q; ++i) cout << 0 << '\n';
        return 0;
    }
    vector<vector<int>> s(n + 1, vector<int>(n + 1));
    for (int L = 1; L <= n; ++L) {
        int mask = 0;
        for (int R = L; R <= n; ++R) {
            if (mask & a[R]) break;
            mask |= a[R];
            s[L][R] = 1;
        }
    }
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            s[i][j] += s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];
        }
    }
    for (auto [l, r] : qs) {
        cout << s[r][r] - s[l - 1][r] - s[r][l - 1] + s[l - 1][l - 1] << '\n';
    }
    return 0;
}
