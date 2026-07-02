// 子任务 1 模型：n<=20 时枚举每包是否扔到最后；超出假设输出占位答案。
#include <bits/stdc++.h>
using namespace std;

int score(const vector<int> &s) {
    int ans = (int)s.size();
    for (int i = 1; i < (int)s.size(); ++i) ans += (s[i] - s[i - 1] + 5) % 5;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    if (n > 20) {
        cout << 0 << '\n';
        return 0;
    }
    int best = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        vector<int> keep, tail;
        for (int i = 0; i < n; ++i) ((mask >> i) & 1 ? tail : keep).push_back(a[i]);
        keep.insert(keep.end(), tail.begin(), tail.end());
        best = max(best, score(keep));
    }
    cout << best << '\n';
    return 0;
}
