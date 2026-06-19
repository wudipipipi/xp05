from pathlib import Path


ROOT = Path(__file__).resolve().parent


SINGLE_LINE = {"老城糕色", "缺页教典", "最后一包馍片", "树上的旧色", "小z的擂台"}
FIRST_IS_T = {"数字橱窗", "小W的数盒", "黑板擦痕", "另一种顺序", "长廊信标"}


def count_lines(path: Path) -> int:
    data = path.read_bytes()
    if not data:
        return 0
    return data.rstrip(b"\r\n").count(b"\n") + 1


def expected_lines(problem: str, path: Path, out_lines: int) -> int:
    if problem in SINGLE_LINE:
        return 1
    if problem == "沙盘边界":
        return out_lines if out_lines in (1, 2) else -1

    with path.open("r", encoding="utf-8") as f:
        head = f.readline().split()
        if problem in FIRST_IS_T:
            return int(head[0])
        if problem == "友好区间的抉择":
            return int(head[1])
        if problem == "长街树影":
            return int(head[0])
        if problem == "记忆窗口":
            q = int(head[0])
            total = 0
            for _ in range(q):
                op = f.readline()
                if op.startswith("ASK") or op.startswith("STAT"):
                    total += 1
            return total
        if problem == "林中问路":
            T = int(head[0])
            total = 0
            for _ in range(T):
                n, q = map(int, f.readline().split())
                total += q
                f.readline()
                for _ in range(n - 1):
                    f.readline()
                for _ in range(q):
                    f.readline()
            return total
    raise ValueError(f"unknown problem: {problem}")


def main():
    bad = []
    total = 0
    for problem_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "data").exists()):
        problem = problem_dir.name
        for inp in sorted((problem_dir / "data").glob("*.in")):
            total += 1
            out = inp.with_suffix(".out")
            if not out.exists():
                bad.append((problem, inp.name, "missing .out", 0))
                continue
            out_lines = count_lines(out)
            expect = expected_lines(problem, inp, out_lines)
            if out_lines != expect:
                bad.append((problem, inp.name, expect, out_lines))
    if bad:
        for row in bad[:30]:
            print(row)
        raise SystemExit(f"line-count validation failed: {len(bad)} issue(s)")
    print(f"line-count validation passed: {total} cases")


if __name__ == "__main__":
    main()
