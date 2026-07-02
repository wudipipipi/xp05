// 子任务 4 模型：假设 k<=5000，在值域上预处理存在色泽并二分答案。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool check(const vector<int> &exist, int m, int k, int d) {
    int cur = 0, used = 0;
    while (cur <= k) {
        int best = -1;
        int L = max(0, cur - d), R = min(k, cur + d);
        for (int x = R; x >= L; --x) if (exist[x]) { best = x; break; }
        if (best < 0) return false;
        if (++used > m) return false;
        cur = best + d + 1;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    ll kk;
    if (!(cin >> n >> m >> kk)) return 0;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    if (kk > 5000) {
        cout << 0 << '\n';
        return 0;
    }
    int k = (int)kk;
    vector<int> exist(k + 1);
    for (ll x : a) exist[(int)x] = 1;
    int l = 0, r = k;
    while (l < r) {
        int mid = (l + r) / 2;
        if (check(exist, m, k, mid)) r = mid;
        else l = mid + 1;
    }
    cout << l << '\n';
    return 0;
}
