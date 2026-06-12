# fangz 的分数

## 题目描述

fangz 是 ACGO 平台的一名用户，他曾经在 ACGO 上参加过 $n$ 场比赛，在第 $i$ 场比赛中的表现评分为 $a_i$。

fangz 觉得自己的分数太低了，于是他黑进了 ACGO 的后台。他将选择一个区间 $[l,r]$，其中 $1 \leq l \leq r \leq n$，并删除第 $l$ 场到第 $r$ 场的比赛。

删除比赛后，fangz 的分数会按照如下规则重新计算：

- fangz 的分数记为 $x$，初始时 $x=0$；
- 对于 $1 \leq i \leq n$，在第 $i$ 场比赛之后：
  - 如果 $l \leq i \leq r$，则这场比赛被删除，fangz 的分数不变；
  - 否则：
    - 如果 $a_i > x$，那么 fangz 的分数增加 $1$；
    - 如果 $a_i = x$，那么 fangz 的分数不变；
    - 如果 $a_i < x$，那么 fangz 的分数减少 $1$。

fangz 想知道，应该如何选择一个区间 $[l,r]$，才能使最后的分数最高。

注：fangz 至少要删除一场比赛。

## 输入格式

每个测试包含多个测试用例。

输入的第一行包含一个整数 $t$，表示测试用例的数量。

对于每个测试用例，输入的第一行包含一个整数 $n$，表示比赛的数量。

输入的第二行包含 $n$ 个整数 $a_1,a_2,\dots,a_n$，表示每场比赛的表现评分。

## 输出格式

对于每个测试用例，输出一行一个整数，表示 fangz 能获得的最高评分。

## 样例

### 样例 1 输入

```text
5
6
1 2 3 4 5 6
7
1 2 1 1 1 3 4
1
1
9
9 9 8 2 4 4 3 5 3
10
1 2 3 4 1 3 2 1 1 10
```

### 样例 1 输出

```text
5
4
0
4
5
```

## 提示

### 【样例 1 解释】

在第一个测试用例中，fangz 必须至少删除一场比赛。若删除任意一个长度为 $1$ 的区间，重新计算后的评分将为 $5$。

在第二个测试用例中，fangz 的最优选择是区间 $[3,5]$。重新计算过程中，他的评分变化如下：

$0 \xrightarrow{a_1=1} 1 \xrightarrow{a_2=2} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{\mathtt{删除}} 2 \xrightarrow{a_6=3} 3 \xrightarrow{a_7=4} 4$

在第三个测试用例中，fangz 必须删除唯一一场比赛，因此他的评分将保持初始值 $0$。

在第四个测试用例中，fangz 的最优选择是区间 $[7,9]$。重新计算过程中，他的评分变化如下：

$0 \xrightarrow{a_1=9} 1 \xrightarrow{a_2=9} 2 \xrightarrow{a_3=8} 3 \xrightarrow{a_4=2} 2 \xrightarrow{a_5=4} 3 \xrightarrow{a_6=4} 4 \xrightarrow{\mathtt{删除}} 4 \xrightarrow{\mathtt{删除}} 4 \xrightarrow{\mathtt{删除}} 4$

在第五个测试用例中，fangz 的最优选择是区间 $[5,9]$。

### 【数据范围】

对于所有测试数据，保证：

- $1 \leq t \leq 5 \times 10^4$；
- $1 \leq n \leq 3 \times 10^5$；
- $1 \leq a_i \leq n$；
- 所有测试用例的 $n$ 之和不超过 $3 \times 10^5$。

| 测试点编号 | $n \leq$ | 特殊性质 |
| :--: | :--: | :--: |
| $1 \sim 2$ | $3 \times 10^5$ | A |
| $3 \sim 6$ | $\sum n \leq 1000$ | 无 |
| $7 \sim 20$ | $3 \times 10^5$ | 无 |

特殊性质 A：对于所有 $1 \leq i \leq n$，均有 $a_i=i$。
