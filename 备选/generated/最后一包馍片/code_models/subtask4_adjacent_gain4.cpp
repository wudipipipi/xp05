// 子任务 4 模型：假设原序列相邻贡献全为 4，原顺序达到上界 5n-4。
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    bool ok = true;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        if (i && a[i] != ((a[i - 1] - 2 + 5) % 5) + 1) ok = false;
    }
    cout << (ok ? 5 * n - 4 : 0) << '\n';
    return 0;
}
