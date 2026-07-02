// 子任务 2 模型：假设所有 ai 都是奇数，答案为 n-1。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        cin >> n;
        bool ok = true;
        for (int i = 0; i < n; ++i) {
            ll x;
            cin >> x;
            ok &= x % 2 == 1;
        }
        cout << (ok ? n - 1 : 0) << '\n';
    }
    return 0;
}
