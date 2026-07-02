// 满分模型：状态压缩 DP，维护两段子序列的首尾味道。
#include <bits/stdc++.h>
using namespace std;
const int NEG = -1000000000;

int gain(int x, int y) { return (y - x + 5) % 5; }
int enc(int x, int y, int z) { return (x * 6 + y) * 6 + z; }

int solve(const vector<int> &a) {
    vector<int> dp(216, NEG), ndp(216, NEG);
    dp[0] = 0;
    for (int v : a) {
        fill(ndp.begin(), ndp.end(), NEG);
        for (int x = 0; x <= 5; ++x) for (int y = 0; y <= 5; ++y) for (int z = 0; z <= 5; ++z) {
            int cur = dp[enc(x, y, z)];
            if (cur == NEG) continue;
            int nx = v, add = x ? gain(x, v) : 0;
            ndp[enc(nx, y, z)] = max(ndp[enc(nx, y, z)], cur + add);
            if (!y) ndp[enc(x, v, v)] = max(ndp[enc(x, v, v)], cur);
            else ndp[enc(x, y, v)] = max(ndp[enc(x, y, v)], cur + gain(z, v));
        }
        dp.swap(ndp);
    }
    int best = 0;
    for (int x = 0; x <= 5; ++x) for (int y = 0; y <= 5; ++y) for (int z = 0; z <= 5; ++z) {
        int cur = dp[enc(x, y, z)];
        if (cur == NEG) continue;
        if (x && y) cur += gain(x, y);
        best = max(best, cur);
    }
    return (int)a.size() + best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    cout << solve(a) << '\n';
    return 0;
}
