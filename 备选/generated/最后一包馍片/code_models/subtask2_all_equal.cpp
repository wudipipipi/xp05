// 子任务 2 模型：假设所有味道相同，额外贡献恒为 0，答案为 n。
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
        if (i && a[i] != a[0]) ok = false;
    }
    cout << (ok ? n : 0) << '\n';
    return 0;
}
