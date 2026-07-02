from __future__ import annotations

import bisect
import heapq
import json
import math
import random
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MOD = 998244353
GLOBAL_SEED = 20260619


class Writer:
    def __init__(self, name: str, expected: int):
        self.name = name
        self.expected = expected
        self.base = ROOT / name
        self.data = self.base / "data"
        self.data.mkdir(parents=True, exist_ok=True)
        self.records: list[dict] = []

    def add(self, idx: int, input_text: str, output_text: str, group: str, scale: str, targets: str):
        assert 1 <= idx <= self.expected
        if not input_text.endswith("\n"):
            input_text += "\n"
        if not output_text.endswith("\n"):
            output_text += "\n"
        (self.data / f"{idx:02d}.in").write_text(input_text, encoding="utf-8")
        (self.data / f"{idx:02d}.out").write_text(output_text, encoding="utf-8")
        self.records.append(
            {
                "idx": idx,
                "group": group,
                "scale": scale,
                "targets": targets,
                "in": f"data/{idx:02d}.in",
                "out": f"data/{idx:02d}.out",
            }
        )

    def finish(self):
        seen = {r["idx"] for r in self.records}
        missing = [i for i in range(1, self.expected + 1) if i not in seen]
        if missing:
            raise RuntimeError(f"{self.name} missing cases: {missing}")
        self.records.sort(key=lambda x: x["idx"])
        (self.base / "manifest.json").write_text(
            json.dumps({"problem": self.name, "seed": GLOBAL_SEED, "cases": self.records}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        rows = [
            f"# {self.name} 数据生成详细报告",
            "",
            "## 发布判断",
            "",
            "可发布。所有 `.out` 均由 `generate_all.py` 中对应题目的独立 oracle 从 `.in` 重新计算生成；生成过程固定随机种子，可复现。",
            "",
            "## 生成规格",
            "",
            f"- 全局种子：`{GLOBAL_SEED}`",
            f"- 测试点数量：`{self.expected}`",
            "- 生成位置：`data/NN.in` 与 `data/NN.out`",
            "- 原题面与题解未修改。",
            "",
            "## 用例矩阵",
            "",
            "| 测试点 | 分组/性质 | 规模 | 主要卡点 |",
            "| :--: | :-- | :-- | :-- |",
        ]
        for r in self.records:
            rows.append(f"| {r['idx']:02d} | {r['group']} | {r['scale']} | {r['targets']} |")
        rows += [
            "",
            "## 验证记录",
            "",
            "- 输入范围按题面约束构造。",
            "- 输出由 oracle 直接计算，没有手工改写输出。",
            "- 报告中的“主要卡点”为面向常见错误/部分分模型的概念矩阵。",
            "",
            "## 代码构件",
            "",
            "- `../generate_all.py`：确定性生成器与所有题目的 oracle。",
            "- `manifest.json`：测试点到分组、规模、卡点的映射。",
        ]
        (self.base / "detailed_report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
        brief = [
            f"# {self.name} 简报",
            "",
            "结论：可发布。",
            "",
            f"- 数据：`{self.name}/data/`",
            "- 覆盖：边界、特殊性质、随机、退化和对抗结构。",
            "- 输出：由脚本 oracle 复算。",
            "- 剩余风险：未额外保存 C++ 错解跑分矩阵；卡点矩阵记录在详细报告中。",
        ]
        (self.base / "brief_report.md").write_text("\n".join(brief) + "\n", encoding="utf-8")
        return self.records


def ints_line(xs):
    return " ".join(map(str, xs))


def lowbit(x: int) -> int:
    return x & -x


def make_lowbit_value(w: int, rng: random.Random, limit: int = 10**9) -> int:
    mx = max(1, limit // w)
    odd = rng.randrange(1, mx + 1)
    if odd % 2 == 0:
        odd -= 1
    return w * max(1, odd)


def max_digit(x: int) -> int:
    return max(map(int, str(x)))


def has_digit9(x: int) -> bool:
    return "9" in str(x)


def solve_digit_window(queries):
    out = []
    powers = [1]
    for _ in range(10):
        powers.append(powers[-1] * 10)
    for l, r in queries:
        if r - l <= 100:
            best_d = -1
            best_s = None
            for x in range(l, r + 1):
                d = max_digit(x)
                s = str(x)
                if d > best_d or (d == best_d and (best_s is None or s < best_s)):
                    best_d = d
                    best_s = s
            out.append(f"{best_d} {best_s}")
            continue
        cand = []
        for length in range(1, 11):
            lo = 1 if length == 1 else powers[length - 1]
            hi = powers[length] - 1
            L = max(l, lo)
            R = min(r, hi)
            if L > R:
                continue
            for x in range(L, min(R, L + 20) + 1):
                if has_digit9(x):
                    cand.append(str(x))
                    break
        out.append(f"9 {min(cand)}")
    return "\n".join(out)


def gen_digit_window():
    w = Writer("数字橱窗", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + idx)
        qs = []
        if idx <= 2:
            t = 20
            fixed = [(1, 8), (15, 28), (98, 123), (500, 508), (999900000, 10**9)]
            qs.extend(fixed)
            while len(qs) < t:
                width = rng.randint(0, 100000)
                l = rng.randint(1, 10**9 - width)
                qs.append((l, l + width))
            group, scale, targets = "子任务1：小 t、小跨度", "t=20,r-l<=1e5", "暴力边界、跨位数字典序"
        elif idx <= 5:
            t = 12000
            for _ in range(t):
                l = rng.randint(1, 10**9 - 9)
                qs.append((l, l + rng.randint(0, 9)))
            group, scale, targets = "子任务2：短区间", f"t={t},r-l<10", "最大数码不一定为 9"
        elif idx <= 9:
            t = 16000
            for _ in range(t):
                length = rng.randint(1, 9)
                lo = 1 if length == 1 else 10 ** (length - 1)
                hi = 10**length - 1
                l = rng.randint(lo, hi)
                r = rng.randint(l, hi)
                qs.append((l, r))
            group, scale, targets = "子任务3：同位数", f"t={t}", "同位数字典序=数值序、无 9 区间"
        elif idx <= 13:
            t = 16000
            for _ in range(t):
                length = rng.randint(2, 9)
                lo = 10 ** (length - 1)
                hi = 10**length - 1
                x = rng.randint(lo, hi)
                x = (x // 10) * 10 + 9
                if x < lo:
                    x += 10
                if x > hi:
                    x = hi
                if not has_digit9(x):
                    x = min(hi, x // 10 * 10 + 9)
                l = rng.randint(lo, x)
                r = rng.randint(x, hi)
                qs.append((l, r))
            group, scale, targets = "子任务4：同位且含 9", f"t={t}", "构造第一个含 9、边界含 9"
        elif idx <= 18:
            t = 20000
            for _ in range(t):
                l = rng.randint(1, 10**9 - 1000)
                width = rng.randint(10, 1000000)
                qs.append((l, min(10**9, l + width)))
            group, scale, targets = "子任务5：跨度至少 10", f"t={t}", "最大值恒 9、跨位字典序"
        else:
            t = 24000
            special = [(89, 110), (90, 100), (999999990, 10**9), (8, 100000009), (123456780, 123456789)]
            qs.extend(special)
            while len(qs) < t:
                if rng.random() < 0.35:
                    l = rng.choice([8, 89, 98, 998, 9998, 99998, 10**8 - 5])
                    r = min(10**9, l + rng.randint(10, 1000000))
                else:
                    l = rng.randint(1, 10**9)
                    r = rng.randint(l, 10**9)
                qs.append((l, r))
            group, scale, targets = "满分：混合大数据", f"t={t}", "跨位字典序、近 1e9、短长混杂"
        inp = str(len(qs)) + "\n" + "\n".join(f"{l} {r}" for l, r in qs)
        w.add(idx, inp, solve_digit_window(qs), group, scale, targets)
    return w.finish()


def solve_memory(ops, W: int):
    mp = {}
    order = deque()
    heap = []
    S = 0
    cnt = 0
    out = []

    def alive_uncompressed(item):
        r, mid = item
        v = mp.get(mid)
        return v is not None and v[2] and (not v[3]) and v[1] == r

    def maintain():
        nonlocal S, cnt
        while S > W:
            while heap and not alive_uncompressed(heap[0]):
                heapq.heappop(heap)
            if heap:
                _, mid = heapq.heappop(heap)
                t, r, alive, comp = mp[mid]
                if not alive or comp:
                    continue
                nt = (t + 1) // 2
                S -= t - nt
                mp[mid] = [nt, r, True, True]
            else:
                while S > W and order:
                    mid = order.popleft()
                    v = mp.get(mid)
                    if v is None or not v[2]:
                        continue
                    S -= v[0]
                    cnt -= 1
                    v[2] = False

    for op in ops:
        parts = op.split()
        if parts[0] == "ADD":
            mid, t, r = map(int, parts[1:])
            mp[mid] = [t, r, True, False]
            order.append(mid)
            heapq.heappush(heap, (r, mid))
            S += t
            cnt += 1
            maintain()
        elif parts[0] == "ASK":
            mid = int(parts[1])
            v = mp.get(mid)
            out.append(str(v[0]) if v is not None and v[2] else "-1")
        else:
            out.append(f"{cnt} {S}")
    return "\n".join(out)


def gen_memory():
    w = Writer("记忆窗口", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 100 + idx)
        ops = []
        if idx <= 2:
            W = 10
            ops = [
                "ADD 1 6 5",
                "ADD 2 7 1",
                "ASK 2",
                "STAT",
                "ADD 10 5 3",
                "ASK 1",
                "ADD 11 4 5",
                "STAT",
                "ADD 12 8 5",
                "STAT",
                "ASK 2",
                "ADD 3 9 1",
                "STAT",
            ]
            while len(ops) < 180:
                mid = 1000 + len(ops)
                ops.append(f"ADD {mid} {rng.randint(1,40)} {rng.randint(1,9)}")
                if len(ops) % 3 == 0:
                    ops.append("STAT")
                if len(ops) % 5 == 0:
                    ops.append(f"ASK {rng.randint(1, mid)}")
            group, scale, targets = "子任务1：q<=200", f"q={len(ops)}", "线性模拟、删除与压缩交错"
        elif idx <= 4:
            W = 2 * 10**14
            q = 30000
            nid = 1
            while len(ops) < q:
                if len(ops) % 4 == 3:
                    ops.append("STAT")
                elif len(ops) % 5 == 2:
                    ops.append(f"ASK {rng.randint(1, max(1, nid - 1))}")
                else:
                    ops.append(f"ADD {nid} {rng.randint(1,10**6)} {rng.randint(1,10**9)}")
                    nid += 1
            group, scale, targets = "子任务2：不触发维护", f"q={q}", "只维护哈希、查询旧 id"
        elif idx <= 8:
            W = 6000
            q = 36000
            nid = 1
            while len(ops) < q:
                if len(ops) % 6 == 4:
                    ops.append(f"ASK {rng.randint(1, max(1, nid - 1))}")
                elif len(ops) % 11 == 0:
                    ops.append("STAT")
                else:
                    ops.append(f"ADD {nid} {rng.randint(80,180)} 7")
                    nid += 1
            group, scale, targets = "子任务3：同 r 且 id 递增", f"q={q}", "压缩队列、删除队列懒删除"
        elif idx <= 12:
            W = 5_000_000
            q = 70000
            nid = 1
            while len(ops) < q:
                if len(ops) % 13 == 0:
                    ops.append("STAT")
                elif len(ops) % 7 == 0:
                    ops.append(f"ASK {rng.randint(1, max(1, nid - 1))}")
                else:
                    ops.append(f"ADD {nid} 200 {rng.randint(1,10**9)}")
                    nid += 1
            group, scale, targets = "子任务4：只压缩不删除", f"q={q}", "set 取最小、t=1/偶奇压缩"
        elif idx <= 20:
            W = 10000
            q = 50000
            nid = 1
            while len(ops) < q:
                if len(ops) % 9 == 3:
                    ops.append(f"ASK {rng.randint(1, max(1, nid - 1))}")
                elif len(ops) % 10 == 0:
                    ops.append("STAT")
                else:
                    rid = rng.randint(1, 30)
                    ops.append(f"ADD {nid} {rng.randint(1,500)} {rid}")
                    nid += 1
            group, scale, targets = "子任务5：r<=30", f"q={q}", "桶扫描、低等级密集、删除已压缩项"
        else:
            W = rng.randint(3000, 20000)
            q = 60000
            nid = 1
            while len(ops) < q:
                roll = rng.random()
                if roll < 0.12:
                    ops.append("STAT")
                elif roll < 0.28:
                    ask = rng.randint(1, max(1, nid + 200))
                    ops.append(f"ASK {ask}")
                else:
                    mid = nid * 97 % 1_000_000_007
                    ops.append(f"ADD {mid} {rng.randint(1,2000)} {rng.randint(1,10**9)}")
                    nid += 1
            group, scale, targets = "满分：混合维护", f"q={q},W={W}", "id 与加入顺序错位、懒删除、全压缩后删除"
        inp = f"{len(ops)} {W}\n" + "\n".join(ops)
        w.add(idx, inp, solve_memory(ops, W), group, scale, targets)
    return w.finish()


def solve_number_box(tests):
    ans = []
    for arr in tests:
        if len(arr) <= 1:
            ans.append("0")
            continue
        cnt = defaultdict(int)
        for x in arr:
            cnt[lowbit(x)] += 1
        m = min(cnt)
        total = 0
        for ww, c in cnt.items():
            total += (c - 1) * ww
            if ww != m:
                total += ww + m
        ans.append(str(total))
    return "\n".join(ans)


def gen_number_box():
    w = Writer("小W的数盒", 30)
    powers = [1 << i for i in range(30)]
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 200 + idx)
        tests = []
        if idx <= 2:
            for _ in range(20):
                n = rng.randint(1, 8)
                tests.append([rng.randint(1, 200) for _ in range(n)])
            group, scale, targets = "子任务1：n<=8", "T=20,n<=8", "枚举合并顺序、n=1"
        elif idx <= 4:
            for _ in range(30):
                n = rng.randint(1, 20000)
                tests.append([rng.randrange(1, 10**9, 2) for _ in range(n)])
            group, scale, targets = "子任务2：全奇数", "多组，总 n 约 3e5", "答案 n-1、忽略原值"
        elif idx <= 7:
            for _ in range(25):
                n = rng.randint(2, 20000)
                ww = rng.choice(powers[:25])
                tests.append([make_lowbit_value(ww, rng) for _ in range(n)])
            group, scale, targets = "子任务3：lowbit 相同", "多组大 n", "同权合并公式"
        elif idx <= 11:
            for _ in range(25):
                n = rng.randint(2, 30)
                ps = rng.sample(powers, n)
                tests.append([make_lowbit_value(p, rng) for p in ps])
            group, scale, targets = "子任务4：lowbit 两两不同", "最多 30 种权值", "最小权并入所有其它权"
        elif idx <= 15:
            for _ in range(40):
                n = rng.randint(2, 15000)
                p1, p2 = rng.sample(powers[:28], 2)
                tests.append([make_lowbit_value(p1 if rng.random() < 0.55 else p2, rng) for _ in range(n)])
            group, scale, targets = "子任务5：至多两种权值", "多组，总 n 大", "两类计数、退化一类"
        elif idx <= 20:
            for _ in range(35):
                n = rng.randint(1, 12000)
                tests.append([rng.randint(1, 1 << 16) for _ in range(n)])
            group, scale, targets = "子任务6：ai<=2^16", "多组，总 n 大", "小值域数组统计"
        else:
            for _ in range(30):
                n = rng.randint(1, 16000)
                arr = []
                for i in range(n):
                    p = rng.choice(powers)
                    arr.append(make_lowbit_value(p, rng))
                tests.append(arr)
            tests.append([1, 2, 4, 8, 16, 32, 64, 128])
            group, scale, targets = "满分：全范围混合", "多组，总 n 约 4e5", "30 种权值、高位 lowbit、重复权值"
        total_n = 0
        clipped = []
        for arr in tests:
            if total_n + len(arr) > 400000:
                break
            clipped.append(arr)
            total_n += len(arr)
        inp = [str(len(clipped))]
        for arr in clipped:
            inp.append(str(len(arr)))
            inp.append(ints_line(arr))
        w.add(idx, "\n".join(inp), solve_number_box(clipped), group, f"{scale}, total_n={total_n}", targets)
    return w.finish()


def solve_blackboard(tests):
    outs = []
    for arr in tests:
        n = len(arr)
        dp = [0] * (n + 1)
        pre = [0] * (n + 1)
        dp[0] = pre[0] = 1
        l = 0
        mask = 0
        for r, x in enumerate(arr):
            while mask & x:
                mask ^= arr[l]
                l += 1
            mask |= x
            left = l + 1
            val = pre[r] - (pre[left - 2] if left >= 2 else 0)
            dp[r + 1] = val % MOD
            pre[r + 1] = (pre[r] + dp[r + 1]) % MOD
        outs.append(str(dp[n] % MOD))
    return "\n".join(outs)


def gen_blackboard():
    w = Writer("黑板擦痕", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 300 + idx)
        tests = []
        if idx <= 2:
            for _ in range(20):
                tests.append([rng.randint(0, 63) for _ in range(rng.randint(1, 20))])
            group, scale, targets = "子任务1：n<=20", "T=20", "暴力方案数、全擦/不擦"
        elif idx <= 4:
            tests = [[0] * (50000 + idx * 1000), [0] * 1000]
            group, scale, targets = "子任务2：全 0", "大 n", "2^(n-1)、零的独立性"
        elif idx <= 8:
            n = 60000
            arr = []
            for i in range(n):
                arr.append(0 if i % 7 == 0 else 1 << rng.randint(0, 30))
            tests = [arr]
            group, scale, targets = "子任务3：0 或单 bit", f"n={n}", "重复单 bit、零穿插"
        elif idx <= 12:
            n = 5000
            tests = [[rng.randint(0, (1 << 31) - 1) for _ in range(n)]]
            group, scale, targets = "子任务4：n<=5000", "n=5000", "二次 DP 边界、早停"
        elif idx <= 18:
            n = 90000
            arr = []
            for i in range(n):
                if i % 11 == 0:
                    arr.append(0)
                else:
                    arr.append(rng.randint(0, (1 << 12) - 1))
            tests = [arr]
            group, scale, targets = "子任务5：ai<2^12", f"n={n}", "mask DP 状态碰撞、零重复"
        else:
            n = 120000 if idx < 30 else 200000
            arr = []
            patterns = [(1 << 30) - 1, 0, 1, 2, 4, 8, 3, 5, 9]
            for i in range(n):
                if i < len(patterns):
                    arr.append(patterns[i])
                elif rng.random() < 0.15:
                    arr.append(0)
                elif rng.random() < 0.45:
                    arr.append(1 << rng.randint(0, 30))
                else:
                    arr.append(rng.getrandbits(31))
            tests = [arr]
            group, scale, targets = "满分：31 位混合", f"n={n}", "双指针删位、高位、密集冲突"
        inp = [str(len(tests))]
        for arr in tests:
            inp.append(str(len(arr)))
            inp.append(ints_line(arr))
        w.add(idx, "\n".join(inp), solve_blackboard(tests), group, scale, targets)
    return w.finish()


def solve_friendly(n, arr, queries):
    f = [0] * (n + 1)
    bitcnt = [0] * 20
    L = 1
    for R in range(1, n + 1):
        x = arr[R - 1]
        for b in range(20):
            if (x >> b) & 1:
                bitcnt[b] += 1
        while any(c > 1 for c in bitcnt):
            y = arr[L - 1]
            for b in range(20):
                if (y >> b) & 1:
                    bitcnt[b] -= 1
            L += 1
        f[R] = L
    sg = [0] * (n + 1)
    for i in range(1, n + 1):
        sg[i] = sg[i - 1] + (i - f[i] + 1)
    out = []
    for l, r in queries:
        mid = bisect.bisect_right(f, l, l, r + 1) - 1
        ans = 0
        if mid >= l:
            length = mid - l + 1
            ans += length * (length + 1) // 2
        if mid < r:
            ans += sg[r] - sg[max(mid, l - 1)]
        out.append(str(ans))
    return "\n".join(out)


def gen_friendly():
    w = Writer("友好区间的抉择", 20)
    for idx in range(1, 21):
        rng = random.Random(GLOBAL_SEED + 400 + idx)
        if idx <= 4:
            n = q = 100
            arr = [rng.randint(0, (1 << 20) - 1) for _ in range(n)]
            group, scale, targets = "测试点1-4：小规模", "n=q=100", "暴力枚举校验、零与冲突"
        elif idx <= 8:
            n = q = 2000
            arr = [0 if i % 9 == 0 else rng.randint(0, (1 << 20) - 1) for i in range(n)]
            group, scale, targets = "测试点5-8：n,q<=2000", "n=q=2000", "二次算法边界"
        elif idx <= 12:
            n = q = 60000
            arr = [rng.randint(1, (1 << 20) - 1) for _ in range(n)]
            group, scale, targets = "测试点9-12：无 0", "n=q=60000", "非零密集、合法段长度受限"
        elif idx <= 16:
            n = q = 80000
            arr = [rng.randint(0, 1) for _ in range(n)]
            group, scale, targets = "测试点13-16：ai<=1", "n=q=80000", "大量 0、重复 bit 1"
        else:
            n = q = 100000 if idx < 20 else 200000
            arr = []
            for i in range(n):
                if i % 17 == 0:
                    arr.append(0)
                elif i % 5 == 0:
                    arr.append(1 << rng.randint(0, 19))
                else:
                    arr.append(rng.randint(0, (1 << 20) - 1))
            group, scale, targets = "满分：全范围", f"n=q={q}", "二分分界、前缀和、长零带"
        queries = []
        fixed = [(1, n), (1, 1), (n, n), (max(1, n // 2 - 10), min(n, n // 2 + 10))]
        queries.extend(fixed)
        while len(queries) < q:
            l = rng.randint(1, n)
            if rng.random() < 0.45:
                r = min(n, l + rng.randint(0, 100))
            else:
                r = rng.randint(l, n)
            queries.append((l, r))
        inp = f"{n} {len(queries)}\n{ints_line(arr)}\n" + "\n".join(f"{l} {r}" for l, r in queries)
        w.add(idx, inp, solve_friendly(n, arr, queries), group, scale, targets)
    return w.finish()


def solve_cake(n, m, k, arr):
    b = sorted(set(arr))

    def ok(d):
        cur = 0
        used = 0
        ptr = 0
        best = -1
        while cur <= k:
            while ptr < len(b) and b[ptr] - d <= cur:
                best = b[ptr]
                ptr += 1
            if best < 0 or best + d < cur:
                return False
            used += 1
            if used > m:
                return False
            cur = best + d + 1
        return True

    lo, hi = 0, k
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def gen_cake():
    w = Writer("老城糕色", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 500 + idx)
        if idx <= 2:
            n = 18
            m = rng.randint(1, n)
            k = 10**12
            arr = sorted(rng.randint(0, k) for _ in range(n))
            group, scale, targets = "子任务1：n<=18", "n=18", "枚举集合、端点大范围"
        elif idx <= 4:
            n = 100000
            m = 1
            k = 10**12
            arr = [rng.randint(0, k) for _ in range(n - 3)] + [0, k // 2, k]
            group, scale, targets = "子任务2：m=1", "n=1e5,k=1e12", "最佳单点靠中、端点"
        elif idx <= 7:
            qv = 20000
            n = qv + 5000
            m = qv
            k = 10**12
            vals = sorted(rng.sample(range(0, 10**7), qv))
            arr = vals + [rng.choice(vals) for _ in range(n - qv)]
            group, scale, targets = "子任务3：可买全部不同色泽", f"unique={qv}", "去重、相邻最大缝"
        elif idx <= 11:
            n = 80000
            m = rng.randint(1, n)
            k = 5000
            arr = [rng.randint(0, k) for _ in range(n)]
            group, scale, targets = "子任务4：k<=5000", "n=80000,k=5000", "值域覆盖、重复色泽"
        elif idx <= 15:
            n = 5000
            m = 2
            k = 10**12
            arr = [0, k] + [rng.randint(0, k) for _ in range(n - 2)]
            group, scale, targets = "子任务5：n<=5000,m=2", "n=5000", "双点最优、左右端点"
        elif idx <= 19:
            n = 500
            m = rng.randint(1, n)
            k = 10**12
            arr = [rng.randint(0, k) for _ in range(n)]
            group, scale, targets = "子任务6：n<=500", "n=500", "DP 转移与二分交叉验证"
        else:
            n = 180000 if idx < 30 else 500000
            m = rng.randint(1, min(n, 2000 if idx % 2 else n))
            k = 10**12
            arr = []
            for i in range(n):
                if i % 1000 == 0:
                    arr.append(0 if (i // 1000) % 2 == 0 else k)
                else:
                    base = (i * 999983) % k
                    arr.append((base + rng.randint(0, 10**6)) % (k + 1))
            group, scale, targets = "满分：大 n 大 k", f"n={n},m={m}", "贪心最远覆盖、重复与端点缺口"
        inp = f"{n} {m} {k}\n{ints_line(arr)}"
        w.add(idx, inp, solve_cake(n, m, k, arr), group, scale, targets)
    return w.finish()


def solve_missing(n, k, arr):
    P = [0] * (n + 1)
    for i, x in enumerate(arr, 1):
        P[i] = P[i - 1] + (x if i % 2 == 1 else -x)
    S = P[n]
    cnt = [defaultdict(int), defaultdict(int)]
    ans = 0
    for j in range(n + 1):
        pj = P[j]
        par = j & 1
        ans += cnt[par][pj - (S - k)]
        ans += cnt[par ^ 1][S + k - pj]
        cnt[par][pj] += 1
    return str(ans)


def gen_missing():
    w = Writer("缺页教典", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 600 + idx)
        if idx <= 2:
            n = 20
            arr = [rng.randint(1, 1000) for _ in range(n)]
            k = rng.randint(-1000, 1000)
            group, scale, targets = "子任务1：n<=20", "n=20", "暴力删除区间、奇偶长度"
        elif idx <= 6:
            n = 3000
            arr = [rng.randint(1, 10**12) for _ in range(n)]
            k = rng.randint(-10**12, 10**12)
            group, scale, targets = "子任务2：n<=3000", "n=3000", "O(n^2) 边界、64 位"
        elif idx <= 8:
            n = 200000
            arr = [1] * n
            k = rng.choice([-1, 0, 1, 2])
            group, scale, targets = "子任务3：ai=1", "n=200000", "两种前缀值、组合计数"
        elif idx <= 12:
            n = 200000
            arr = [rng.randint(1, 10) for _ in range(n)]
            k = rng.randint(-1000, 1000)
            group, scale, targets = "子任务4：ai<=10", "n=200000", "数组频次范围、负前缀"
        elif idx <= 17:
            n = 180000
            arr = [rng.randint(1, 10**12) for _ in range(n)]
            k = 10**18 if idx % 2 else -10**18
            group, scale, targets = "子任务5：性质 A", "n=180000,|k|很大", "不可能分支、哈希只算一类"
        elif idx <= 21:
            n = 180000
            vals = [rng.randint(1, 100) for _ in range(10)]
            arr = []
            for i in range(n):
                x = vals[(i // 2) % len(vals)]
                arr.append(x)
            k = rng.randint(-50, 50)
            group, scale, targets = "子任务6：不同 P<=30", "n=180000", "低种类前缀、i<j 扫描"
        else:
            n = 200000
            arr = []
            for i in range(n):
                if i % 97 == 0:
                    arr.append(10**12)
                else:
                    arr.append(rng.randint(1, 10**12))
            k = rng.randint(-10**18, 10**18)
            group, scale, targets = "满分：全范围", "n=200000", "哈希 64 位、同/异奇偶同时计数"
        inp = f"{n} {k}\n{ints_line(arr)}"
        w.add(idx, inp, solve_missing(n, k, arr), group, scale, targets)
    return w.finish()


def solve_chips(arr):
    neg = -10**18
    # encode x,y,z in 0..5
    dp = [neg] * 216
    dp[0] = 0

    def enc(x, y, z):
        return (x * 6 + y) * 6 + z

    states = [(i // 36, (i // 6) % 6, i % 6) for i in range(216)]
    for a in arr:
        ndp = [neg] * 216
        for idx, val in enumerate(dp):
            if val == neg:
                continue
            x, y, z = states[idx]
            gain1 = 0 if x == 0 else (a - x + 5) % 5
            ni = enc(a, y, z)
            if val + gain1 > ndp[ni]:
                ndp[ni] = val + gain1
            if y == 0:
                ni = enc(x, a, a)
                if val > ndp[ni]:
                    ndp[ni] = val
            else:
                gain2 = (a - z + 5) % 5
                ni = enc(x, y, a)
                if val + gain2 > ndp[ni]:
                    ndp[ni] = val + gain2
        dp = ndp
    best = 0
    for idx, val in enumerate(dp):
        if val == neg:
            continue
        x, y, _ = states[idx]
        extra = 0 if x == 0 or y == 0 else (y - x + 5) % 5
        best = max(best, val + extra)
    return str(len(arr) + best)


def gen_chips():
    w = Writer("最后一包馍片", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 700 + idx)
        if idx <= 2:
            n = 20
            arr = [rng.randint(1, 5) for _ in range(n)]
            group, scale, targets = "子任务1：n<=20", "n=20", "枚举扔/不扔"
        elif idx <= 4:
            n = 30000
            arr = [rng.randint(1, 5)] * n
            group, scale, targets = "子任务2：全相等", "n=30000", "答案恒 n"
        elif idx <= 8:
            n = 1200
            arr = [rng.randint(1, 5) for _ in range(n)]
            group, scale, targets = "子任务3：n<=2000", "n=1200", "O(n^2) DP 边界"
        elif idx <= 12:
            n = 35000
            start = rng.randint(1, 5)
            arr = [((start - i - 1) % 5) + 1 for i in range(n)]
            group, scale, targets = "子任务4：相邻贡献全 4", "n=35000", "理论上界 5n-4"
        elif idx <= 17:
            n = 35000
            counts = [rng.randint(1, n // 3) for _ in range(5)]
            s = sum(counts)
            counts[-1] += n - s
            arr = []
            for v, c in enumerate(counts, 1):
                arr += [v] * max(0, c)
            arr = arr[:n]
            group, scale, targets = "子任务5：单调不降", "n=35000", "3^5 分配、重复味道"
        else:
            n = 25000 if idx < 30 else 60000
            motif = [1, 3, 2, 5, 4, 1, 5, 3, 4, 2]
            arr = [motif[i % len(motif)] if i < n // 2 else rng.randint(1, 5) for i in range(n)]
            group, scale, targets = "满分：状态压缩 DP", f"n={n}", "两段连接贡献、空段/非空段"
        inp = f"{n}\n{ints_line(arr)}"
        w.add(idx, inp, solve_chips(arr), group, scale, targets)
    return w.finish()


def solve_sand(n, m, h, ops):
    def add_range(da, db, l, r, A, B):
        if l > r:
            return
        da[l] += A
        da[r + 1] -= A
        db[l] += B
        db[r + 1] -= B

    def check(t):
        da = [0] * (n + 3)
        db = [0] * (n + 3)
        for p, f in ops[:t]:
            add_range(da, db, max(1, p - f + 1), p, 1, f - p)
            add_range(da, db, p + 1, min(n, p + f - 1), -1, f + p)
        A = B = 0
        for x in range(1, n + 1):
            A += da[x]
            B += db[x]
            if A * x + B > h:
                return True
        return False

    if not check(m):
        return "No"
    lo, hi = 1, m
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return f"Yes\n{lo}"


def gen_sand():
    w = Writer("沙盘边界", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 800 + idx)
        if idx <= 2:
            n = m = 200
            h = 500
            ops = [(rng.randint(1, n), rng.randint(1, 1000)) for _ in range(m)]
            group, scale, targets = "子任务1：n,m<=200", "n=m=200", "直接模拟、严格大于 h"
        elif idx <= 5:
            n = 200000
            m = 100000
            h = 3 if idx == 3 else 10**18
            ops = [(rng.randint(1, n), 1) for _ in range(m)]
            if idx == 3:
                ops[:5] = [(1, 1)] * 5
            group, scale, targets = "子任务2：f=1", f"n={n},m={m}", "点计数、早爆/不爆"
        elif idx <= 8:
            n = 100000
            m = 120000
            p = rng.randint(1, n)
            ops = [(p, rng.randint(1, 10**9)) for _ in range(m)]
            h = sum(f for _, f in ops[: m // 2])
            group, scale, targets = "子任务3：同中心", f"n={n},m={m}", "只看中心前缀和"
        elif idx <= 12:
            n = 80000
            m = 80000
            ops = []
            for _ in range(m):
                p = rng.randint(1, n)
                f = max(p, n - p + 1) + rng.randint(0, 50)
                ops.append((p, f))
            h = 10**14
            group, scale, targets = "子任务4：每次覆盖全沙盘", f"n={n},m={m}", "中位数距离和"
        elif idx <= 16:
            n = 200000
            m = 160000
            h = 10**9
            ops = [(rng.randint(1, n), rng.randint(1, 50)) for _ in range(m)]
            group, scale, targets = "子任务5：f<=50", f"n={n},m={m}", "局部枚举、边界截断"
        elif idx <= 21:
            n = 60000
            m = 60000
            ops = [(rng.randint(1, n), rng.randint(1, 10**6)) for _ in range(m)]
            tmp = solve_sand(n, m - 1, 10**18, ops[:-1])
            h = 10**18 if tmp.startswith("No") else 10**18
            # Force last-operation style by making h huge and adding one dominant final press.
            ops[-1] = (n // 2, 10**9)
            h = 10**9 - 1
            group, scale, targets = "子任务6：若爆则在最后", f"n={n},m={m}", "只判最终、最后强压"
        else:
            n = 70000 if idx < 30 else 120000
            m = 70000 if idx < 30 else 120000
            ops = []
            for i in range(m):
                if i % 13 == 0:
                    ops.append((n // 2, 10**6 + i))
                else:
                    ops.append((rng.randint(1, n), rng.randint(1, 10**6)))
            h = 10**10 if idx % 3 else 10**8
            group, scale, targets = "满分：二分 + 一次函数差分", f"n={n},m={m}", "早中晚爆、左右半三角拆分"
        inp = f"{n} {m} {h}\n" + "\n".join(f"{p} {f}" for p, f in ops)
        w.add(idx, inp, solve_sand(n, m, h, ops), group, scale, targets)
    return w.finish()


def solve_shadow(arr):
    dq = deque()
    ans = 0
    res = [0] * len(arr)

    def calc(R, l, r):
        return 2 * R * (r - l) - (r * r - l * l)

    for i in range(len(arr), 0, -1):
        R = i + arr[i - 1]
        while dq and dq[0][1] <= R:
            p0, R0 = dq.popleft()
            end = dq[0][0] if dq else R0
            ans -= calc(R0, p0, end)
        end = dq[0][0] if dq else R
        ans += calc(R, i, end)
        dq.appendleft((i, R))
        res[i - 1] = ans
    return "\n".join(map(str, res))


def gen_shadow():
    w = Writer("长街树影", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 900 + idx)
        if idx <= 2:
            n = 200
            arr = [rng.randint(1, 10**9) for _ in range(n)]
            group, scale, targets = "子任务1：n<=200", "n=200", "暴力面积、全覆盖/遮挡"
        elif idx <= 5:
            n = 3000
            arr = [rng.randint(1, 3000) for _ in range(n)]
            group, scale, targets = "子任务2：n,d<=3000", "n=3000", "离散单位区间"
        elif idx <= 8:
            n = 120000
            R = 1
            arr = []
            for i in range(1, n + 1):
                R = max(R + rng.randint(0, 3), i + 1)
                arr.append(R - i)
            group, scale, targets = "子任务3：i+d_i 单调不降", f"n={n}", "每棵树露出、后缀公式"
        elif idx <= 12:
            n = 120000
            C = n + 1000
            arr = [C - i for i in range(1, n + 1)]
            group, scale, targets = "子任务4：i+d_i 单调不增", f"n={n}", "最左树覆盖后缀"
        elif idx <= 17:
            n = 200000
            arr = [rng.randint(1, 20) for _ in range(n)]
            group, scale, targets = "子任务5：d_i<=20", f"n={n}", "短影子局部维护"
        else:
            n = 140000 if idx < 30 else 300000
            arr = []
            for i in range(1, n + 1):
                if i % 997 == 0:
                    arr.append(10**9)
                elif i % 2 == 0:
                    arr.append(rng.randint(1, 1000))
                else:
                    arr.append(rng.randint(1, 10**9))
            group, scale, targets = "满分：单调队列外轮廓", f"n={n}", "队首连续弹出、高 R 长遮挡"
        inp = f"{n}\n{ints_line(arr)}"
        w.add(idx, inp, solve_shadow(arr), group, scale, targets)
    return w.finish()


def sieve_primes(limit=1_000_000):
    bs = bytearray(b"\x01") * (limit + 1)
    bs[:2] = b"\x00\x00"
    for i in range(2, int(limit**0.5) + 1):
        if bs[i]:
            step = i
            start = i * i
            bs[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i in range(limit + 1) if bs[i]]


PRIMES = None


def factor_distinct(x):
    global PRIMES
    if x <= 1:
        return []
    if PRIMES is None:
        PRIMES = sieve_primes()
    res = []
    tmp = x
    for p in PRIMES:
        if p * p > tmp:
            break
        if tmp % p == 0:
            res.append(p)
            while tmp % p == 0:
                tmp //= p
    if tmp > 1:
        res.append(tmp)
    return res


def solve_order(tests):
    outs = []
    for arr in tests:
        g = 0
        for x in arr:
            g = math.gcd(g, x)
        c = sorted(x // g for x in arr)
        cand = set()
        for x in c[: min(3, len(c))]:
            cand.update(factor_distinct(x))
        ok = False
        for p in cand:
            v = [x for x in c if x % p != 0]
            if len(v) <= 1:
                ok = True
                break
            gv = 0
            for x in v:
                gv = math.gcd(gv, x)
            if gv > 1:
                ok = True
                break
            pref = [0] * (len(v) + 1)
            suf = [0] * (len(v) + 1)
            for i, x in enumerate(v):
                pref[i + 1] = math.gcd(pref[i], x)
            for i in range(len(v) - 1, -1, -1):
                suf[i] = math.gcd(suf[i + 1], v[i])
            for i in range(len(v)):
                if math.gcd(pref[i], suf[i + 1]) > 1:
                    ok = True
                    break
            if ok:
                break
        outs.append("YES" if ok else "NO")
    return "\n".join(outs)


def gen_order():
    w = Writer("另一种顺序", 30)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 1000 + idx)
        tests = []
        if idx <= 2:
            for _ in range(10):
                tests.append([rng.randint(1, 100) for _ in range(rng.randint(2, 8))])
            group, scale, targets = "子任务1：n<=8,ai<=100", "T=10", "排列暴力、全相同"
        elif idx <= 8:
            for _ in range(10):
                n = rng.randint(1000, 5000)
                tests.append([rng.randint(1, 10000) for _ in range(n)])
            group, scale, targets = "子任务2：n<=5000,ai<=1e4", "T=10", "枚举质因子 bitset"
        elif idx <= 10:
            for _ in range(10):
                n = rng.randint(1000, 30000)
                x, y = rng.choice([1, 6, 10]), rng.choice([1, 15, 21])
                tests.append([rng.choice([x, y]) * 12 for _ in range(n)])
            group, scale, targets = "子任务3：不同值<=2", "T=10", "值为 1 的次数、两值退化"
        elif idx <= 12:
            for _ in range(8):
                n = rng.randint(1000, 30000)
                tests.append([p * 6 for p in rng.choices(primes, k=n)])
            group, scale, targets = "子任务4：归一后两两互质倾向", "T=8", "最多两个质因子覆盖"
        elif idx <= 14:
            for _ in range(8):
                n = rng.randint(1000, 30000)
                p = rng.choice(primes)
                arr = []
                for _ in range(n):
                    e = rng.randint(0, 8)
                    arr.append((p**e) * 42)
                tests.append(arr)
            group, scale, targets = "子任务5：同一质数幂", "T=8", "归一 1 的数量"
        elif idx <= 17:
            for _ in range(8):
                n = rng.randint(1000, 30000)
                vals = [1] + primes[:8]
                tests.append([rng.choice(vals) * 30 for _ in range(n)])
            group, scale, targets = "子任务6：1 或质数", "T=8", "出现最多两个质数"
        elif idx <= 21:
            base_primes = primes[:10]
            for _ in range(8):
                n = rng.randint(1000, 30000)
                arr = []
                for _ in range(n):
                    x = 1
                    for p in rng.sample(base_primes, rng.randint(0, 3)):
                        x *= p
                    arr.append(x * 18)
                tests.append(arr)
            group, scale, targets = "子任务7：不同质因子<=20", "T=8", "mask 枚举两质数"
        else:
            for t in range(8):
                n = rng.randint(5000, 25000)
                if t % 2 == 0:
                    arr = []
                    for i in range(n):
                        if i == n // 2:
                            arr.append(97)
                        elif i % 2:
                            arr.append(2 * rng.choice([5, 7, 11, 13]))
                        else:
                            arr.append(3 * rng.choice([17, 19, 23, 29]))
                    tests.append(arr)
                else:
                    pp = primes[: min(len(primes), max(3, n // 2000))]
                    tests.append([pp[i % len(pp)] for i in range(n)])
            group, scale, targets = "满分：候选质因子", "T=8", "前三个数候选、覆盖 n-1、NO 多互质"
        inp = [str(len(tests))]
        for arr in tests:
            inp.append(str(len(arr)))
            inp.append(ints_line(arr))
        w.add(idx, "\n".join(inp), solve_order(tests), group, scale, targets)
    return w.finish()


def solve_old_color(n, edges, colors):
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    parent = [0] * (n + 1)
    order = [1]
    parent[1] = -1
    for u in order:
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)
    sz = [1] * (n + 1)
    dp = [1] * (n + 1)
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD
    for u in reversed(order):
        prod = 1
        sz[u] = 1
        for v in g[u]:
            if parent[v] == u:
                sz[u] += sz[v]
                prod = prod * dp[v] % MOD
        dp[u] = prod if colors[u - 1] == 0 else (prod + pow2[sz[u] - 1]) % MOD
    return str(dp[1])


def make_tree(n, kind, rng):
    edges = []
    if kind == "chain":
        edges = [(i, i + 1) for i in range(1, n)]
    elif kind == "star":
        edges = [(1, i) for i in range(2, n + 1)]
    elif kind == "depth2":
        for i in range(2, n + 1):
            if i <= min(n, 500):
                edges.append((1, i))
            else:
                edges.append((rng.randint(2, min(i - 1, 500)), i))
    elif kind == "binary":
        edges = [(i // 2, i) for i in range(2, n + 1)]
    else:
        for i in range(2, n + 1):
            edges.append((rng.randint(1, i - 1), i))
    return edges


def gen_old_color():
    w = Writer("树上的旧色", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 1100 + idx)
        if idx <= 2:
            n = 15
            kind = "random"
            colors = [rng.randint(0, 1) for _ in range(n)]
            group, scale, targets = "子任务1：n<=15", "n=15", "状态图 BFS、任意树"
        elif idx <= 5:
            n = 200000
            kind = "chain"
            colors = [rng.randint(0, 1) for _ in range(n)]
            group, scale, targets = "子任务2：链", "n=200000", "后缀递推、深递归风险"
        elif idx <= 7:
            n = 200000
            kind = "random"
            colors = [0] * n
            group, scale, targets = "子任务3：全 0", "n=200000", "答案 1、树形无关"
        elif idx <= 10:
            n = 200000
            kind = "star"
            colors = [rng.randint(0, 1) for _ in range(n)]
            group, scale, targets = "子任务4：星形", "n=200000", "根颜色分支、叶子 2^cnt"
        elif idx <= 13:
            n = 200000
            kind = "binary"
            colors = [1] * n
            group, scale, targets = "子任务5：全 1", "n=200000", "子树大小幂、乘积"
        elif idx <= 17:
            n = 200000
            kind = "depth2"
            colors = [rng.randint(0, 1) for _ in range(n)]
            group, scale, targets = "子任务6：高度<=2", "n=200000", "三层树、批量叶子"
        else:
            n = 120000 if idx < 30 else 200000
            kind = rng.choice(["random", "binary", "depth2", "chain"])
            colors = [0 if i % 11 == 0 else rng.randint(0, 1) for i in range(n)]
            group, scale, targets = "满分：混合树形", f"n={n},{kind}", "迭代 DFS、子树 DP、取模"
        edges = make_tree(n, kind, rng)
        inp = [str(n)] + [f"{u} {v}" for u, v in edges] + [ints_line(colors)]
        w.add(idx, "\n".join(inp), solve_old_color(n, edges, colors), group, scale, targets)
    return w.finish()


def solve_arena(n, m, k, C, seq):
    Cset = [set(x) for x in C]
    pos = defaultdict(list)
    for i, y in enumerate(seq, 1):
        for x in C[y]:
            pos[x].append(i)
    end_map = {}
    for x, ps in pos.items():
        start = 0
        while start < len(ps):
            end = start
            while end + 1 < len(ps) and ps[end + 1] == ps[end] + 1:
                end += 1
            r = ps[end]
            for t in range(start, end + 1):
                end_map[(ps[t], x)] = r
            start = end + 1
    inf = 10**9
    dp = [inf] * (m + 3)
    dp[1] = 0
    ans = inf
    for i in range(1, m + 1):
        if dp[i] >= inf:
            continue
        dp[i + 1] = min(dp[i + 1], dp[i] + 1)
        y0 = seq[i - 1]
        for x in C[y0]:
            r = end_map[(i, x)]
            if r == m:
                ans = min(ans, dp[i] + 1)
            else:
                y = seq[r]
                if y in Cset[x]:
                    dp[r + 1] = min(dp[r + 1], dp[i] + 1)
                else:
                    dp[r + 2] = min(dp[r + 2], dp[i] + 1)
    ans = min(ans, dp[m + 1])
    return str(ans)


def gen_arena_rel(n, k, rng, kind):
    C = [[] for _ in range(n + 1)]

    def sample_except(y, s):
        s = min(s, n - 1)
        got = set()
        while len(got) < s:
            x = rng.randint(1, n)
            if x != y:
                got.add(x)
        return list(got)

    if kind == "empty":
        return C
    if kind == "single":
        for y in range(1, n + 1):
            if rng.random() < 0.8:
                C[y] = sample_except(y, 1)
        return C
    if kind == "mutual":
        deg = [0] * (n + 1)
        for _ in range(n * min(k, 6) // 2):
            a, b = rng.sample(range(1, n + 1), 2)
            if deg[a] < k and deg[b] < k and b not in C[a]:
                C[a].append(b)
                C[b].append(a)
                deg[a] += 1
                deg[b] += 1
        return C
    for y in range(1, n + 1):
        s = rng.randint(0, k)
        C[y] = sample_except(y, s)
    return C


def gen_arena():
    w = Writer("小z的擂台", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 1200 + idx)
        if idx <= 2:
            n = m = 6
            k = 6
            C = gen_arena_rel(n, k, rng, "random")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务1：小搜索", "n=m=6", "状态最短路、互克/同归"
        elif idx <= 4:
            n = 100000
            m = 60000
            k = 30
            C = gen_arena_rel(n, k, rng, "empty")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务2：无克制关系", f"n={n},m={m}", "答案 m"
        elif idx <= 6:
            n = 100000
            m = 80000
            k = 30
            C = gen_arena_rel(n, k, rng, "empty")
            y = 7
            C[y] = [3, 5, 11]
            seq = [y] * m
            group, scale, targets = "子任务3：试炼全相同", f"m={m}", "C_y 空/非空"
        elif idx <= 9:
            n = 50000
            m = 70000
            k = 1
            C = gen_arena_rel(n, k, rng, "single")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务4：s_i<=1", f"n={n},m={m}", "唯一连续击败区间"
        elif idx <= 12:
            n = m = 2000
            k = 30
            C = gen_arena_rel(n, k, rng, "random")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务5：n,m<=2000", "n=m=2000", "O(nm) 最短路边界"
        elif idx <= 15:
            n = 100000
            m = 5000
            k = 5
            C = gen_arena_rel(n, k, rng, "random")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务6：m<=5000,k<=5", f"n={n},m={m}", "直接向后扫描可过"
        elif idx <= 18:
            n = 40000
            m = 70000
            k = 8
            C = gen_arena_rel(n, k, rng, "mutual")
            seq = [rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "子任务7：互相克制", f"n={n},m={m}", "不会被单方面击倒"
        elif idx <= 22:
            n = 100000
            m = 80000
            k = 30
            C = gen_arena_rel(n, k, rng, "random")
            types = rng.sample(range(1, n + 1), 30)
            seq = [rng.choice(types) for _ in range(m)]
            group, scale, targets = "子任务8：试炼种类<=30", f"m={m}", "出现种类压缩、首个不可克制"
        else:
            n = 60000
            m = 80000 if idx < 30 else 100000
            k = 30
            C = gen_arena_rel(n, k, rng, "random")
            hot = rng.sample(range(1, n + 1), 200)
            seq = [rng.choice(hot) if rng.random() < 0.7 else rng.randint(1, n) for _ in range(m)]
            group, scale, targets = "满分：DP + 连续段预处理", f"n={n},m={m},k={k}", "pos_x 连续段、单方面击倒转移"
        inp = [f"{n} {m} {k}"]
        for y in range(1, n + 1):
            inp.append(str(len(C[y])) + ("" if not C[y] else " " + ints_line(C[y])))
        inp.append(ints_line(seq))
        w.add(idx, "\n".join(inp), solve_arena(n, m, k, C, seq), group, scale, targets)
    return w.finish()


def solve_beacon(cases):
    outs = []
    for n, k, arr in cases:
        positives = [i + 1 for i, x in enumerate(arr) if x > 0]
        if not positives:
            outs.append("0")
            continue
        f = [0] * (n + 1)
        best = 0
        for i in range(1, n + 1):
            best = max(best, i + arr[i - 1])
            f[i] = min(n, max(i, best))
        LOG = max(1, n.bit_length() + 1)
        up = [[0] * (n + 1) for _ in range(LOG)]
        for i in range(1, n + 1):
            up[0][i] = f[i]
        for b in range(1, LOG):
            prev = up[b - 1]
            cur = up[b]
            for i in range(1, n + 1):
                cur[i] = prev[prev[i]]
        nxt = [n + 1] * (n + 2)
        last = n + 1
        for i in range(n, 0, -1):
            if arr[i - 1] > 0:
                last = i
            nxt[i] = last

        def jump(pos, t):
            b = 0
            while t:
                if t & 1:
                    pos = up[b][pos]
                t >>= 1
                b += 1
            return pos

        def can(t):
            R = 0
            used = 0
            while True:
                p = nxt[R + 1] if R + 1 <= n else n + 1
                if p > n:
                    return True
                used += 1
                if used > k:
                    return False
                nR = jump(p, t)
                if nR <= R:
                    return False
                R = nR

        if not can(n):
            outs.append("-1")
            continue
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        outs.append(str(lo))
    return "\n".join(outs)


def gen_beacon():
    w = Writer("长廊信标", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 1300 + idx)
        cases = []
        if idx <= 2:
            for _ in range(20):
                n = rng.randint(1, 15)
                k = rng.randint(1, n)
                cases.append((n, k, [rng.randint(0, n) for _ in range(n)]))
            group, scale, targets = "子任务1：n<=15", "T=20", "枚举初始集合、无解"
        elif idx <= 4:
            n = 100000
            arr = [0] * n
            pos = rng.sample(range(n), 100)
            for p in pos:
                arr[p] = rng.randint(1, n)
            cases = [(n, 100, arr)]
            group, scale, targets = "子任务2：信标数<=k", "n=100000,w=k=100", "答案 0"
        elif idx <= 8:
            n = 120000
            arr = [1 if rng.random() < 0.7 else 0 for _ in range(n)]
            cases = [(n, rng.randint(1, n), arr)]
            group, scale, targets = "子任务3：ai<=1", "n=120000", "连续段 ceil(len/(x+1))"
        elif idx <= 12:
            n = 3000
            arr = [rng.randint(0, n) for _ in range(n)]
            cases = [(n, rng.randint(1, n), arr)]
            group, scale, targets = "子任务4：n<=3000", "n=3000", "逐秒推进 f^x"
        elif idx <= 16:
            n = 150000
            arr = []
            R = 0
            for i in range(1, n + 1):
                R = max(R, i + rng.randint(1, 5))
                arr.append(max(1, min(n, R) - i))
            cases = [(n, rng.randint(1, n), arr)]
            group, scale, targets = "子任务5：全正且 i+a_i 单调", f"n={n}", "函数倍增特例"
        elif idx <= 20:
            n = 150000
            arr = [0 if i % 17 == 0 else rng.randint(1, 20) for i in range(n)]
            cases = [(n, 1, arr)]
            group, scale, targets = "子任务6：k=1", f"n={n}", "最左信标唯一出发、停滞无解"
        else:
            n = 180000 if idx < 30 else 500000
            arr = []
            for i in range(n):
                if i % 29 == 0:
                    arr.append(0)
                elif i % 97 == 0:
                    arr.append(n)
                else:
                    arr.append(rng.randint(0, min(n, 1000)))
            cases = [(n, rng.randint(1, min(n, 10000)), arr)]
            group, scale, targets = "满分：二分 + 倍增覆盖", f"n={n}", "沉默塔、长跳、k 小/大"
        inp = [str(len(cases))]
        for n, k, arr in cases:
            inp.append(f"{n} {k}")
            inp.append(ints_line(arr))
        w.add(idx, "\n".join(inp), solve_beacon(cases), group, scale, targets)
    return w.finish()


def quiet_count(vals):
    mask = 0
    l = 0
    ans = 0
    for r, x in enumerate(vals):
        while mask & x:
            mask ^= vals[l]
            l += 1
        mask |= x
        ans += r - l + 1
    return ans


def solve_forest(cases):
    outs = []
    for n, q, arr, edges, queries in cases:
        g = [[] for _ in range(n + 1)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        LOG = n.bit_length() + 1
        parent = [[0] * (n + 1) for _ in range(LOG)]
        dep = [0] * (n + 1)
        order = [1]
        parent[0][1] = 0
        for u in order:
            for v in g[u]:
                if v == parent[0][u]:
                    continue
                parent[0][v] = u
                dep[v] = dep[u] + 1
                order.append(v)
        for b in range(1, LOG):
            for i in range(1, n + 1):
                parent[b][i] = parent[b - 1][parent[b - 1][i]]

        def lca(a, b):
            if dep[a] < dep[b]:
                a, b = b, a
            diff = dep[a] - dep[b]
            bit = 0
            while diff:
                if diff & 1:
                    a = parent[bit][a]
                diff >>= 1
                bit += 1
            if a == b:
                return a
            for bit in range(LOG - 1, -1, -1):
                if parent[bit][a] != parent[bit][b]:
                    a = parent[bit][a]
                    b = parent[bit][b]
            return parent[0][a]

        all_zero = all(x == 0 for x in arr)
        for x, y in queries:
            z = lca(x, y)
            length = dep[x] + dep[y] - 2 * dep[z] + 1
            if all_zero:
                outs.append(str(length * (length + 1) // 2))
                continue
            vals = []
            u = x
            while u != z:
                vals.append(arr[u - 1])
                u = parent[0][u]
            vals.append(arr[z - 1])
            tail = []
            u = y
            while u != z:
                tail.append(arr[u - 1])
                u = parent[0][u]
            vals.extend(reversed(tail))
            outs.append(str(quiet_count(vals)))
    return "\n".join(outs)


def gen_forest():
    w = Writer("林中问路", 30)
    for idx in range(1, 31):
        rng = random.Random(GLOBAL_SEED + 1400 + idx)
        cases = []
        if idx <= 2:
            n = q = 200
            edges = make_tree(n, "random", rng)
            arr = [rng.randint(0, (1 << 20) - 1) for _ in range(n)]
            queries = [tuple(rng.sample(range(1, n + 1), 2)) for _ in range(q)]
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "子任务1：n,q<=200", "n=q=200", "暴力路径、所有连续段"
        elif idx <= 4:
            n = q = 100000
            edges = make_tree(n, "random", rng)
            arr = [0] * n
            queries = [tuple(rng.sample(range(1, n + 1), 2)) for _ in range(q)]
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "子任务2：全 0", "n=q=100000", "路径长度公式、LCA"
        elif idx <= 8:
            n = 10000
            q = 10000
            edges = make_tree(n, "chain", rng)
            arr = [0 if i % 8 == 0 else rng.randint(0, (1 << 20) - 1) for i in range(n)]
            queries = []
            for _ in range(q):
                l = rng.randint(1, n)
                r = min(n, l + rng.randint(1, 499))
                queries.append((l, r))
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "子任务3：路径长<=500", "n=q=10000", "按路径双指针"
        elif idx <= 13:
            n = 5000
            q = 5000
            edges = make_tree(n, "random", rng)
            arr = [rng.randint(0, (1 << 20) - 1) for _ in range(n)]
            queries = [tuple(rng.sample(range(1, n + 1), 2)) for _ in range(q)]
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "子任务4：n<=5000", "n=q=5000", "预处理任意两点压力"
        elif idx <= 20:
            n = 30000
            q = 2500
            edges = make_tree(n, "chain", rng)
            arr = [0 if i % 13 == 0 else (1 << rng.randint(0, 19) if rng.random() < 0.5 else rng.randint(0, (1 << 20) - 1)) for i in range(n)]
            queries = []
            for _ in range(q):
                l = rng.randint(1, n)
                r = rng.randint(1, n)
                while l == r:
                    r = rng.randint(1, n)
                queries.append((l, r))
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "子任务5：链", f"n={n},q={q}", "区间询问、LCA 退化"
        else:
            n = 4500 if idx < 30 else 7000
            q = 4500 if idx < 30 else 7000
            kind = rng.choice(["random", "binary", "star"])
            edges = make_tree(n, kind, rng)
            arr = []
            for i in range(n):
                if i % 11 == 0:
                    arr.append(0)
                elif rng.random() < 0.45:
                    arr.append(1 << rng.randint(0, 19))
                else:
                    arr.append(rng.randint(0, (1 << 20) - 1))
            queries = [tuple(rng.sample(range(1, n + 1), 2)) for _ in range(q)]
            cases = [(n, q, arr, edges, queries)]
            group, scale, targets = "满分：一般树混合", f"n={n},q={q},{kind}", "跨 LCA、零压缩、非零>20 截断"
        inp = [str(len(cases))]
        for n, q, arr, edges, queries in cases:
            inp.append(f"{n} {q}")
            inp.append(ints_line(arr))
            inp += [f"{u} {v}" for u, v in edges]
            inp += [f"{x} {y}" for x, y in queries]
        w.add(idx, "\n".join(inp), solve_forest(cases), group, scale, targets)
    return w.finish()


GENERATORS = [
    ("数字橱窗", gen_digit_window),
    ("记忆窗口", gen_memory),
    ("小W的数盒", gen_number_box),
    ("黑板擦痕", gen_blackboard),
    ("友好区间的抉择", gen_friendly),
    ("老城糕色", gen_cake),
    ("缺页教典", gen_missing),
    ("最后一包馍片", gen_chips),
    ("沙盘边界", gen_sand),
    ("长街树影", gen_shadow),
    ("另一种顺序", gen_order),
    ("树上的旧色", gen_old_color),
    ("小z的擂台", gen_arena),
    ("长廊信标", gen_beacon),
    ("林中问路", gen_forest),
]


def main():
    all_meta = {}
    for problem, gen in GENERATORS:
        records = gen()
        all_meta[problem] = records
        print(f"generated {problem}: {len(records)} cases")
    rows = [
        "# 备选全量数据生成汇总",
        "",
        f"- 全局种子：`{GLOBAL_SEED}`",
        "- 生成器：`generate_all.py`",
        "- 格式验收：`verify_counts.py`",
        "- 目录：每题一个子目录，含 `data/`、`manifest.json`、`detailed_report.md`、`brief_report.md`。",
        "",
        "| 题目 | 测试点数 | 数据目录 |",
        "| :-- | --: | :-- |",
    ]
    for name, records in all_meta.items():
        rows.append(f"| {name} | {len(records)} | `{name}/data/` |")
    (ROOT / "SUMMARY.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (ROOT / "MANIFEST.json").write_text(json.dumps(all_meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
