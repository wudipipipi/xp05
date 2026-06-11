# fangz 的分数

## 题目描述

fangz 是 ACGO 平台的一名用户，fangz 曾经在 ACGO 上参加过 $n$ 场比赛，在第 $i$ 场比赛中，他的表现评分为 $a_i$。

fangz 觉得自己的分数太低了！于是他黑进了 ACGO 的后台，他将选择一个区间 $[l,r]$（$1\leq l \leq r \leq n$），然后删除这个区间内的所有比赛。删除了比赛之后，fangz 的分数会被按照如下规则重新计算：

- 最开始，fangz 的分数为 $x=0$。
- 对于 $1\leq i \leq n$，在第 $i$ 场比赛之后，
- - 如果 $l\leq i\leq r$，这场比赛被删除了，fangz 的分数不变。
  - 否则的话，fangz 的分数会按照如下规则变化：
  - - 如果 $a_i > x$，那么 fangz 的分数会加 $1$。
    - 如果 $a_i = x$，那么 fangz 的分数不变。
    - 如果 $a_i < x$，那么 fangz 的分数会减少 $1$。

如果 fangz 以最佳方式选择了一个区间 $[l,r]$，那么 fangz 最后的分数最高是多少？请注意，fangz 必须至少删除一场比赛。

## 输入格式

每个测试包含多个测试用例。输入的第一行包含一个整数 $t$（$1\le t\le 5\cdot 10^4$）—— 测试用例的数量。接下来是测试用例的描述。

每个测试用例的第一行包含一个整数 $n$（$1\le n\le 3\cdot 10^5$）—— 比赛的数量。

第二行包含 $n$ 个整数 $a_1,a_2,\ldots,a_n$（$1\le a_i\le n$）—— 每场比赛的表现评分。

保证所有测试用例的 $n$ 之和不超过 $3 \cdot 10^5$。

## 输出格式

对于每个测试用例，输出一个整数 —— 表示 fangz 最优选择区间重新计算后可能达到的最大评分。


### 输入样例1

```
4
3 4 7
5 1 2
5 5 8
5 1 2 4 3
4 100 1000
1 1 1 1
5 9 13
2 5 5 1 1
```

### 输出样例1

```
2
7
0
1
```

## 说明/提示

#### 样例说明

在第一个测试用例中，fangz 必须至少删除一场比赛。如果他选择任意长度为 $1$ 的区间，重新计算后的评分将等于 $5$。

在第二个测试用例中，fangz 的最优选择是选择区间 $[3,5]$。重新计算过程中，他的评分变化如下：

$0 \xrightarrow{a_1=1} 1 \xrightarrow{a_2=2} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{a_6=3} 3 \xrightarrow{a_7=4} 4$

在第三个测试用例中，fangz 必须删除唯一一场比赛，因此他的评分将保持初始值 $0$。

在第四个测试用例中，fangz 的最优选择是选择区间 $[7,9]$。重新计算过程中，他的评分变化如下：

$0 \xrightarrow{a_1=9} 1 \xrightarrow{a_2=9} 2 \xrightarrow{a_3=8} 3 \xrightarrow{a_4=2} 2 \xrightarrow{a_5=4} 3 \xrightarrow{a_6=4} 4 \xrightarrow{\mathtt{删除}} 4 \xrightarrow{\mathtt{删除}} 4 \xrightarrow{\mathtt{删除}} 4$

在第五个测试用例中，fangz 的最优选择是选择区间 $[5,9]$。

#### 数据范围

对于所有测试数据，都满足 $1 \le t \le 5 \cdot 10^4$，$1 \le n \le 3 \cdot 10^5$， $1 \le l \le r \le 10^9$，$1 \le a_i \le n$，$\displaystyle\sum n \leq 3 \cdot 10^5$

|   测试点   |          $n$          |           特殊性质            |
| :--------: | :-------------------: | :---------------------------: |
| $1\sim 2$  | $n \leq 3 \cdot 10^5$ | 对于所有的 $a_i$ 满足 $a_i=i$ |
| $3\sim 6$  |  $\sum n \leq 1000$   |              无               |
| $7\sim 20$ | $n \leq 3 \cdot 10^5$ |              无               |

## 题目大意

fangz 是 ACGO 平台的一名用户，fangz 曾经在 ACGO 上参加过 $n$ 场比赛，在第 $i$ 场比赛中，他的表现评分为 $a_i$。

fangz 觉得自己的分数太低了！于是他黑进了 ACGO 的后台，他将选择一个区间 $[l,r]$（$1\leq l \leq r \leq n$），然后删除这个区间内的所有比赛。删除了比赛之后，fangz 的分数会被按照如下规则重新计算：

- 最开始，fangz 的分数为 $x=0$。
- 对于 $1\leq i \leq n$，在第 $i$ 场比赛之后，
- - 如果 $l\leq i\leq r$，这场比赛被删除了，fangz 的分数不变。
  - 否则的话，fangz 的分数会按照如下规则变化：
  - - 如果 $a_i > x$，那么 fangz 的分数会加 $1$。
    - 如果 $a_i = x$，那么 fangz 的分数不变。
    - 如果 $a_i < x$，那么 fangz 的分数会减少 $1$。

如果 fangz 以最佳方式选择了一个区间 $[l,r]$，那么 fangz 最后的分数最高是多少？请注意，fangz 必须至少删除一场比赛。

## 思路分析

先考虑特殊性质 $a_i=i$，对于这种数列我们的每一场比赛都能加一分，但是我们必须删除至少一场比赛，所以直接输出 $n-1$ 就可以通过前两个测试点。

对于 $\sum n \leq 1000$ 来说，我们可以枚举所有种类的区间，一共有 $O(n^2)$ 种区间选择，对于每一个区间我们暴力判断最后是多少分更新最大值，可以拿到这 $20$ 部分分。

```c++
void solve() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    int ans = -1e9;
    for (int l = 0; l < n; ++l) {
        for (int r = l; r < n; ++r) {
            int x = 0;
            for (int i = 0; i < n; ++i) {
                if (i >= l && i <= r) continue;
                if (a[i] > x) {
                    x += 1;
                } else if (a[i] < x) {
                    x -= 1;
                }
            }
            ans = max(ans, x);
        }
    }
    cout << ans << endl;
}
```

个人认为这个正解的 $\text{DP}$ 是比较难思考的，首先是对于每一场比赛来说只有三个状态，分别是在我们跳过的区间前、在我们跳过的区间内、在跳过的区间后。我们定义 $dp[i][0/1/2]$ 表示对于第 $i$ 场比赛来说，前面提到的三种状态对应的分数最大值。

那么我们使用 $f(a_i,x)$ 来表示在第 $i$ 场比赛时分数为 $x$ 的结果。

那么如果这场比赛在跳过区间之前，那么我们只能用 $f(dp[i-1][0],a[i])$ 来更新状态，我们只能接受这场比赛的结果。

如果这场比赛在跳过的区间之中，那么我们可以使用 $\max(dp[i-1][1],dp[i-1][0])$ 来更新，这是因为我们如果选择的区间内，第一场比赛是加分的，那我们一定不会把这场比赛选进区间里。

如果这场比赛已经在区间之后了，则使用 $\max(f(dp[i-1][1],a[i]),f(dp[i-1][2],a[i]))$ 来更新，因为我们必须至少跳过一场比赛，因此这场比赛的上一场比赛只有可能是在区间内或者不在区间内。

最后我们的答案是 $\max(dp[n][1], dp[n][2])$，因为我们必须跳过比赛，最后的第 $n$ 场比赛有可能作为跳过比赛区间的右端点。

```c++
int calc(int x,int y){
    if(x < y){
        return x + 1;
    }else if (x == y){
        return x;
    }else{
        return x - 1;
    }
}
void solve() {
    int n;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
    }
    vector<vector<int>> dp(n + 1, vector<int>(3, 0));
    dp[0][1] = dp[0][2] = INT_MIN;
    for (int i = 1; i <= n; ++i) {
        dp[i][0] = calc(dp[i - 1][0], a[i]);
        dp[i][1] = max(dp[i - 1][0], dp[i - 1][1]);
        dp[i][2] = max(calc(dp[i - 1][1], a[i]), calc(dp[i - 1][2], a[i]));
    }
    cout << max(dp[n][1], dp[n][2]) << endl;
}
```

