// 子任务 3 模型：n<=2000 时使用状态压缩 DP；超出假设输出占位答案。
#include <bits/stdc++.h>
using namespace std;
const int NEG = -1000000000;
int gain(int x, int y) { return (y - x + 5) % 5; }
int enc(int x, int y, int z) { return (x * 6 + y) * 6 + z; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    if (n > 2000) {
        cout << 0 << '\n';
        return 0;
    }
    vector<int> dp(216, NEG), ndp(216, NEG);
    dp[0] = 0;
    for (int v : a) {
        fill(ndp.begin(), ndp.end(), NEG);
        for (int x = 0; x <= 5; ++x) for (int y = 0; y <= 5; ++y) for (int z = 0; z <= 5; ++z) {
            int cur = dp[enc(x, y, z)];
            if (cur == NEG) continue;
            ndp[enc(v, y, z)] = max(ndp[enc(v, y, z)], cur + (x ? gain(x, v) : 0));
            if (!y) ndp[enc(x, v, v)] = max(ndp[enc(x, v, v)], cur);
            else ndp[enc(x, y, v)] = max(ndp[enc(x, y, v)], cur + gain(z, v));
        }
        dp.swap(ndp);
    }
    int best = 0;
    for (int x = 0; x <= 5; ++x) for (int y = 0; y <= 5; ++y) for (int z = 0; z <= 5; ++z) {
        int cur = dp[enc(x, y, z)];
        if (cur == NEG) continue;
        best = max(best, cur + (x && y ? gain(x, y) : 0));
    }
    cout << n + best << '\n';
    return 0;
}
