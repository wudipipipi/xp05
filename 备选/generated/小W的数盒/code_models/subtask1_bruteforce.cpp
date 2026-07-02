// 子任务 1 模型：n<=8 时记忆化搜索所有合并顺序；超出假设输出占位答案。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll lowbit(ll x) { return x & -x; }

map<vector<ll>, ll> memo;

ll dfs(vector<ll> s) {
    sort(s.begin(), s.end());
    if (s.size() <= 1) return 0;
    if (memo.count(s)) return memo[s];
    ll best = (1LL << 60);
    int n = (int)s.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            vector<ll> t;
            for (int k = 0; k < n; ++k) if (k != i && k != j) t.push_back(s[k]);
            t.push_back(min(s[i], s[j]));
            best = min(best, (s[i] | s[j]) + dfs(t));
        }
    }
    return memo[s] = best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        cin >> n;
        vector<ll> a(n);
        for (ll &x : a) cin >> x, x = lowbit(x);
        if (n > 8) {
            cout << 0 << '\n';
            continue;
        }
        memo.clear();
        cout << dfs(a) << '\n';
    }
    return 0;
}
