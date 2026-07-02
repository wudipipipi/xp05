// 子任务 5 模型：假设序列单调不降，枚举每种味道分到两段的方式。
#include <bits/stdc++.h>
using namespace std;

int gain(int x, int y) { return (y - x + 5) % 5; }

int internal_gain(const vector<int> &v) {
    if (v.empty()) return 0;
    return v.back() - v.front();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n), cnt(6);
    bool ok = true;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        ++cnt[a[i]];
        if (i && a[i] < a[i - 1]) ok = false;
    }
    if (!ok) {
        cout << 0 << '\n';
        return 0;
    }
    int best = 0;
    function<void(int, vector<int>&, vector<int>&)> dfs = [&](int v, vector<int> &A, vector<int> &B) {
        if (v == 6) {
            if (A.empty() && B.empty()) return;
            int cur = internal_gain(A) + internal_gain(B);
            if (!A.empty() && !B.empty()) cur += gain(A.back(), B.front());
            best = max(best, cur);
            return;
        }
        if (!cnt[v]) {
            dfs(v + 1, A, B);
            return;
        }
        int as = A.size(), bs = B.size();
        A.push_back(v);
        dfs(v + 1, A, B);
        A.resize(as);
        B.push_back(v);
        dfs(v + 1, A, B);
        B.resize(bs);
        if (cnt[v] >= 2) {
            A.push_back(v);
            B.push_back(v);
            dfs(v + 1, A, B);
            A.resize(as);
            B.resize(bs);
        }
    };
    vector<int> A, B;
    dfs(1, A, B);
    cout << n + best << '\n';
    return 0;
}
