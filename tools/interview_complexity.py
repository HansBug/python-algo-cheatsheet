"""
面试手写复杂度评估工具

用途：
- 分析一段 Python 代码在面试现场手写时的体感复杂度
- 输出综合分数、风险等级、关键坑点和基础复杂度指标
- 支持 Python 3.8+（依赖 complexipy 和 radon）

核心思路：
- 用 cognitive complexity 估计人脑理解负担
- 用 cyclomatic complexity 补充路径分支数量
- 再加少量 AST 规则，专门捕捉面试手写时容易出错的模式
"""

import argparse
import ast
import io
import json
import re
import sys
import textwrap
import tokenize
from dataclasses import asdict, dataclass
from typing import Iterable, List, Optional, Sequence, Set, Tuple

try:
    from complexipy import code_complexity
    from radon.complexity import cc_visit
except ImportError as exc:  # pragma: no cover - 依赖缺失时只做提示
    raise SystemExit(
        "缺少第三方依赖，请先执行: python -m pip install -r requirements.txt"
    ) from exc


MUTATING_METHODS = {
    "add",
    "append",
    "clear",
    "discard",
    "extend",
    "insert",
    "pop",
    "remove",
    "setdefault",
    "update",
}
POINTER_ATTRS = {"next", "prev", "left", "right", "parent", "child"}
INDEX_HINTS = {"i", "j", "k", "l", "r", "lo", "hi", "left", "right"}
FRIENDLY_CALLS = {
    "bisect_left": 0.5,
    "bisect_right": 0.5,
    "defaultdict": 0.5,
    "deque": 0.5,
    "heapq.heapify": 0.5,
    "heapq.heappop": 0.5,
    "heapq.heappush": 0.5,
}
LEVELS = (
    (6.0, "很容易手写"),
    (12.0, "正常可写"),
    (18.0, "坑比较多"),
    (float("inf"), "现场高风险"),
)
EXAMPLE_NAME_HINTS = {
    "benchmark",
    "bench",
    "demo",
    "example",
    "examples",
    "sample",
    "samples",
    "test",
    "tests",
    "usage",
}


@dataclass
class Trigger:
    kind: str
    points: float
    message: str


@dataclass
class Target:
    name: str
    kind: str
    source: str
    lineno: int
    end_lineno: int
    default_visible: bool
    summary_visible: bool


@dataclass
class Report:
    name: str
    kind: str
    line_range: str
    score: float
    level: str
    cognitive_complexity: float
    cyclomatic_complexity: float
    nloc: int
    token_count: int
    max_nesting: int
    arg_count: int
    risk_flags: List[Trigger]
    bonuses: List[Trigger]


class RiskVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.depth = 0
        self.max_depth = 0
        self.arg_count = 0
        self.risk_flags = []  # type: List[Trigger]
        self.bonuses = []  # type: List[Trigger]
        self.called_names = set()  # type: Set[str]
        self._iter_stack = []  # type: List[Set[str]]
        self._friendly_hits = set()  # type: Set[str]

    def visit_block(self, nodes: Sequence[ast.stmt]) -> None:
        for node in nodes:
            self.visit(node)

    def _push_depth(self, nodes: Sequence[ast.stmt]) -> None:
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        self.visit_block(nodes)
        self.depth -= 1

    def _record_risk(self, kind: str, points: float, message: str) -> None:
        self.risk_flags.append(Trigger(kind=kind, points=points, message=message))

    def _record_bonus(self, kind: str, points: float, message: str) -> None:
        self.bonuses.append(Trigger(kind=kind, points=points, message=message))

    def visit_If(self, node: ast.If) -> None:
        if self._is_guard_clause(node):
            self._record_bonus("guard_clause", 1.0, "使用 guard clause 拍平了嵌套")

        self.visit(node.test)
        self._push_depth(node.body)
        if node.orelse:
            self._push_depth(node.orelse)

    def visit_For(self, node: ast.For) -> None:
        self.visit(node.iter)
        iter_names = self._extract_names(node.iter)
        self._iter_stack.append(iter_names)
        self._push_depth(node.body)
        self._iter_stack.pop()
        if node.orelse:
            self._push_depth(node.orelse)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.visit_For(node)

    def visit_While(self, node: ast.While) -> None:
        self.visit(node.test)
        if self._has_manual_index_update(node):
            self._record_risk("manual_index", 2.0, "while 循环里手动维护多个下标，容易写炸")
        self._push_depth(node.body)
        if node.orelse:
            self._push_depth(node.orelse)

    def visit_Try(self, node: ast.Try) -> None:
        self._record_risk("try_except", 1.5, "核心逻辑里出现 try/except，现场手写更容易漏边界")
        self._push_depth(node.body)
        for handler in node.handlers:
            self._push_depth(handler.body)
        if node.orelse:
            self._push_depth(node.orelse)
        if node.finalbody:
            self._push_depth(node.finalbody)

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            self.visit(item.context_expr)
        self._push_depth(node.body)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.visit_With(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        kinds = self._collect_bool_ops(node)
        if len(kinds) > 1:
            self._record_risk("bool_mix", 2.0, "条件里混用了 and/or，脑内状态切换比较多")
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        operands = [node.left] + list(node.comparators)
        has_unit_offset = any(self._contains_unit_offset(item) for item in operands)
        has_tight_bound = any(isinstance(op, (ast.LtE, ast.GtE)) for op in node.ops)
        if has_unit_offset or (has_tight_bound and self._extract_names_from_nodes(operands) & INDEX_HINTS):
            self._record_risk("boundary", 1.5, "边界判断看起来有 off-by-one 风险")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        call_name = self._dotted_name(node.func)
        if call_name:
            self.called_names.add(call_name)
            if call_name in FRIENDLY_CALLS and call_name not in self._friendly_hits:
                self._friendly_hits.add(call_name)
                self._record_bonus(
                    "friendly_stdlib",
                    FRIENDLY_CALLS[call_name],
                    "使用了面试友好的标准库套路: %s" % call_name,
                )

            for iter_names in self._iter_stack:
                if self._is_mutating_iterable(call_name, iter_names):
                    self._record_risk("mutate_iter", 2.0, "遍历容器时又修改它，容易出隐藏 bug")
                    break
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self._check_pointer_rewire(node.targets)
        self._check_iterable_mutation(node.targets)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        self._check_pointer_rewire([node.target])
        self._check_iterable_mutation([node.target])
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._check_pointer_rewire([node.target])
        self._check_iterable_mutation([node.target])
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete) -> None:
        self._check_iterable_mutation(node.targets)
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._check_comprehension(node.generators)
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self._check_comprehension(node.generators)
        self.generic_visit(node)

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self._check_comprehension(node.generators)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._check_comprehension(node.generators)
        self.generic_visit(node)

    def _check_comprehension(self, generators: Sequence[ast.comprehension]) -> None:
        if len(generators) > 1 or any(generator.ifs for generator in generators):
            self._record_risk("comprehension", 1.0, "推导式里带多层生成器或过滤条件，可读性下降")

    def _is_guard_clause(self, node: ast.If) -> bool:
        if self.depth != 0 or node.orelse:
            return False
        if not node.body:
            return False
        tail = node.body[-1]
        return isinstance(tail, (ast.Return, ast.Raise, ast.Continue, ast.Break))

    def _has_manual_index_update(self, node: ast.While) -> bool:
        updated = set()
        for child in ast.walk(node):
            if isinstance(child, ast.AugAssign) and isinstance(child.target, ast.Name):
                if child.target.id in INDEX_HINTS:
                    updated.add(child.target.id)
            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name) and target.id in INDEX_HINTS:
                        updated.add(target.id)
        return len(updated) >= 2 or (updated and bool(self._extract_names(node.test) & INDEX_HINTS))

    def _collect_bool_ops(self, node: ast.AST) -> Set[str]:
        kinds = set()
        for child in ast.walk(node):
            if isinstance(child, ast.BoolOp):
                kinds.add(type(child.op).__name__)
        return kinds

    def _contains_unit_offset(self, node: ast.AST) -> bool:
        for child in ast.walk(node):
            if isinstance(child, ast.BinOp) and isinstance(child.op, (ast.Add, ast.Sub)):
                if isinstance(child.right, ast.Constant) and child.right.value == 1:
                    return True
                if isinstance(child.left, ast.Constant) and child.left.value == 1:
                    return True
        return False

    def _extract_names(self, node: ast.AST) -> Set[str]:
        names = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                names.add(child.id)
        return names

    def _extract_names_from_nodes(self, nodes: Iterable[ast.AST]) -> Set[str]:
        names = set()
        for node in nodes:
            names.update(self._extract_names(node))
        return names

    def _dotted_name(self, node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            parent = self._dotted_name(node.value)
            if parent:
                return "%s.%s" % (parent, node.attr)
            return node.attr
        return None

    def _is_mutating_iterable(self, call_name: str, iter_names: Set[str]) -> bool:
        if "." not in call_name:
            return False
        owner, method = call_name.rsplit(".", 1)
        return owner in iter_names and method in MUTATING_METHODS

    def _check_pointer_rewire(self, targets: Sequence[ast.AST]) -> None:
        for target in targets:
            if isinstance(target, ast.Attribute) and target.attr in POINTER_ATTRS:
                self._record_risk("pointer_rewire", 3.0, "存在指针/树节点改线，现场手写很容易漏")

    def _check_iterable_mutation(self, targets: Sequence[ast.AST]) -> None:
        if not self._iter_stack:
            return
        iter_names = set()
        for names in self._iter_stack:
            iter_names.update(names)

        for target in targets:
            if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name):
                if target.value.id in iter_names:
                    self._record_risk("mutate_iter", 2.0, "遍历容器时直接改它的元素，读写状态不好跟")
                    return
            if isinstance(target, ast.Name) and target.id in iter_names:
                self._record_risk("mutate_iter", 2.0, "循环里直接重写正在遍历的变量，容易混乱")
                return


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="评估 Python 代码在面试现场手写时的复杂度体感",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "示例:\n"
            "  python -m tools.interview_complexity -i algos/heap/heap_manual.py\n"
            "  python -m tools.interview_complexity -i algos/heap/heap_manual.py -s Heap._sift_down\n"
            "  python -m tools.interview_complexity -i algos/heap/heapq_native.py --include-examples\n"
            "  python -m tools.interview_complexity -c \"for i in range(n):\\n    if a[i] > 0:\\n        ans += 1\"\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="待分析的 Python 文件路径")
    group.add_argument("-c", "--code", help="直接传入待分析的代码字符串")
    group.add_argument("--stdin", action="store_true", help="从标准输入读取代码")
    parser.add_argument("-s", "--symbol", help="指定函数/方法/类名，如 Heap.push")
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="把 __main__ / demo / example / test 等示例代码也纳入摘要",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser.parse_args(argv)


def read_source(args: argparse.Namespace) -> Tuple[str, str]:
    if args.input:
        with open(args.input, "r", encoding="utf-8") as file:
            return file.read(), args.input
    if args.code is not None:
        return decode_cli_code(args.code), "<cli>"
    return sys.stdin.read(), "<stdin>"


def normalize_source(source: str) -> str:
    if not source.endswith("\n"):
        source += "\n"
    return source


def decode_cli_code(source: str) -> str:
    if "\n" not in source and "\\n" in source:
        try:
            return source.encode("utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            return source
    return source


def dedented_segment(source: str, lineno: int, end_lineno: int) -> str:
    lines = source.splitlines(True)
    segment = "".join(lines[lineno - 1 : end_lineno])
    return textwrap.dedent(segment)


def line_range(lineno: int, end_lineno: int) -> str:
    if lineno == end_lineno:
        return str(lineno)
    return "%s-%s" % (lineno, end_lineno)


def gather_targets(source: str, strict_core: bool = True) -> List[Target]:
    tree = ast.parse(source)
    targets = []  # type: List[Target]
    top_level_blocks = []  # type: List[List[ast.stmt]]
    fallback_blocks = []  # type: List[ast.stmt]
    current_block = []  # type: List[ast.stmt]

    for index, node in enumerate(tree.body):
        if index == 0 and is_module_docstring(node):
            continue
        if strict_core and is_main_guard(node):
            if current_block:
                top_level_blocks.append(current_block)
                current_block = []
            fallback_blocks.append(node)
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if current_block:
                top_level_blocks.append(current_block)
                current_block = []
            is_example = strict_core and is_example_name(node.name)
            targets.append(
                Target(
                    name=node.name,
                    kind="function",
                    source=dedented_segment(source, decorator_lineno(node), node.end_lineno),
                    lineno=decorator_lineno(node),
                    end_lineno=node.end_lineno,
                    default_visible=not is_example,
                    summary_visible=True,
                )
            )
        elif isinstance(node, ast.ClassDef):
            if current_block:
                top_level_blocks.append(current_block)
                current_block = []
            class_is_example = strict_core and is_example_name(node.name)
            methods = [child for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))]
            targets.append(
                Target(
                    name=node.name,
                    kind="class",
                    source=dedented_segment(source, decorator_lineno(node), node.end_lineno),
                    lineno=decorator_lineno(node),
                    end_lineno=node.end_lineno,
                    default_visible=not methods and not class_is_example,
                    summary_visible=not methods,
                )
            )
            for child in methods:
                start = decorator_lineno(child)
                is_example = class_is_example or is_example_name(child.name)
                targets.append(
                    Target(
                        name="%s.%s" % (node.name, child.name),
                        kind="method",
                        source=dedented_segment(source, start, child.end_lineno),
                        lineno=start,
                        end_lineno=child.end_lineno,
                        default_visible=not is_example,
                        summary_visible=True,
                    )
                )
        else:
            current_block.append(node)

    if current_block:
        top_level_blocks.append(current_block)

    if strict_core and fallback_blocks and not targets and top_level_blocks and all_import_blocks(top_level_blocks):
        top_level_blocks = []

    if top_level_blocks:
        targets.extend(make_top_level_targets(source, top_level_blocks))
    if fallback_blocks and not any(target.kind in {"function", "method", "class"} for target in targets):
        targets.extend(
            make_top_level_targets(
                source,
                [[node] for node in fallback_blocks],
                prefix="<main>",
                default_visible=not strict_core,
            )
        )

    if not targets:
        targets.append(
            Target(
                name="<module>",
                kind="block",
                source=textwrap.dedent(source),
                lineno=1,
                end_lineno=max(len(source.splitlines()), 1),
                default_visible=True,
                summary_visible=True,
            )
        )
    return targets


def make_top_level_targets(
    source: str,
    blocks: Sequence[Sequence[ast.stmt]],
    prefix: str = "<top-level>",
    default_visible: bool = True,
) -> List[Target]:
    items = []  # type: List[Target]
    single = len(blocks) == 1
    for block in blocks:
        start = block[0].lineno
        end = block[-1].end_lineno
        name = prefix if single else "%s@%s" % (prefix, start)
        items.append(
            Target(
                name=name,
                kind="block",
                source=dedented_segment(source, start, end),
                lineno=start,
                end_lineno=end,
                default_visible=default_visible,
                summary_visible=True,
            )
        )
    return items


def is_module_docstring(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def is_main_guard(node: ast.stmt) -> bool:
    if not isinstance(node, ast.If):
        return False
    test = node.test
    if not isinstance(test, ast.Compare):
        return False
    if len(test.ops) != 1 or len(test.comparators) != 1:
        return False
    return (
        isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and isinstance(test.ops[0], ast.Eq)
        and isinstance(test.comparators[0], ast.Constant)
        and test.comparators[0].value == "__main__"
    )


def all_import_blocks(blocks: Sequence[Sequence[ast.stmt]]) -> bool:
    for block in blocks:
        for node in block:
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                return False
    return True


def is_example_name(name: str) -> bool:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    tokens = [token for token in re.split(r"[^a-z0-9]+", normalized.replace(".", "_")) if token]
    return any(token in EXAMPLE_NAME_HINTS for token in tokens)


def decorator_lineno(node: ast.AST) -> int:
    decorators = getattr(node, "decorator_list", None) or []
    if decorators:
        return min(item.lineno for item in decorators)
    return node.lineno


def count_nloc(source: str) -> int:
    count = 0
    for line in source.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def count_tokens(source: str) -> int:
    stream = io.StringIO(source)
    ignored = {
        tokenize.COMMENT,
        tokenize.ENCODING,
        tokenize.ENDMARKER,
        tokenize.INDENT,
        tokenize.DEDENT,
        tokenize.NEWLINE,
        tokenize.NL,
    }
    count = 0
    for info in tokenize.generate_tokens(stream.readline):
        if info.type not in ignored:
            count += 1
    return count


def analyze_target(target: Target) -> Report:
    cognitive = cognitive_score(target)
    cyclomatic = cyclomatic_score(target)
    visitor = inspect_target(target)
    nloc = count_nloc(target.source)
    tokens = count_tokens(target.source)
    score = compose_score(cognitive, cyclomatic, nloc, tokens, visitor)
    return Report(
        name=target.name,
        kind=target.kind,
        line_range=line_range(target.lineno, target.end_lineno),
        score=score,
        level=score_level(score),
        cognitive_complexity=cognitive,
        cyclomatic_complexity=cyclomatic,
        nloc=nloc,
        token_count=tokens,
        max_nesting=visitor.max_depth,
        arg_count=visitor.arg_count,
        risk_flags=visitor.risk_flags,
        bonuses=visitor.bonuses,
    )


def cognitive_score(target: Target) -> float:
    result = code_complexity(target.source)
    if target.kind in {"function", "method"} and result.functions:
        return float(result.functions[0].complexity)
    return float(result.complexity)


def cyclomatic_score(target: Target) -> float:
    code = target.source
    if target.kind == "block":
        code = wrap_block(code)

    items = cc_visit(code)
    if not items:
        return 1.0

    if target.kind in {"function", "method", "block"}:
        return float(items[-1].complexity)

    first = items[0]
    if hasattr(first, "real_complexity"):
        return float(first.real_complexity)
    return float(first.complexity)


def wrap_block(code: str) -> str:
    return "def __snippet__():\n%s" % textwrap.indent(code, "    ")


def inspect_target(target: Target) -> RiskVisitor:
    tree = ast.parse(target.source)
    visitor = RiskVisitor()

    if target.kind in {"function", "method"}:
        node = tree.body[0]
        visitor.arg_count = count_args(node.args)
        visitor.visit_block(node.body)
    elif target.kind == "class":
        node = tree.body[0]
        visitor.visit_block(node.body)
    else:
        visitor.visit_block(tree.body)

    if visitor.max_depth > 2:
        visitor.risk_flags.insert(
            0,
            Trigger(
                kind="nesting",
                points=float(visitor.max_depth - 2),
                message="嵌套深度达到 %s 层，写对边界会更费神" % visitor.max_depth,
            ),
        )

    return visitor


def count_args(args: ast.arguments) -> int:
    total = len(args.args) + len(args.kwonlyargs)
    total += len(getattr(args, "posonlyargs", []))
    if args.vararg:
        total += 1
    if args.kwarg:
        total += 1
    return total


def compose_score(
    cognitive: float,
    cyclomatic: float,
    nloc: int,
    tokens: int,
    visitor: RiskVisitor,
) -> float:
    risk_total = sum(item.points for item in visitor.risk_flags)
    bonus_total = sum(item.points for item in visitor.bonuses)

    surface = 0.0
    surface += max(nloc - 12, 0) * 0.25
    surface += max(tokens - 60, 0) * 0.04
    surface += max(visitor.arg_count - 3, 0) * 0.5

    score = cognitive
    score += max(cyclomatic - 1.0, 0.0) * 0.6
    score += surface
    score += risk_total
    score -= bonus_total
    return round(max(score, 0.0), 1)


def score_level(score: float) -> str:
    for upper, label in LEVELS:
        if score <= upper:
            return label
    return LEVELS[-1][1]


def select_targets(
    targets: Sequence[Target], symbol: Optional[str], include_examples: bool
) -> List[Target]:
    if symbol:
        selected = [target for target in targets if target.name == symbol]
        if not selected:
            available = ", ".join(target.name for target in targets)
            raise SystemExit("没有找到符号 %r，可用符号有: %s" % (symbol, available))
        return selected

    if include_examples:
        visible = [target for target in targets if target.summary_visible]
    else:
        visible = [target for target in targets if target.summary_visible and target.default_visible]
    if visible:
        return visible
    return []


def print_summary(reports: Sequence[Report], source_name: str) -> None:
    print("面试手写复杂度摘要: %s" % source_name)
    print(
        "%-24s %-9s %-6s %-8s %-4s %-4s %-5s %-5s"
        % ("Target", "Lines", "Score", "Level", "Cog", "CC", "NLOC", "Tok")
    )
    print("-" * 78)
    for report in sorted(reports, key=lambda item: (-item.score, item.name)):
        print(
            "%-24s %-9s %-6s %-8s %-4s %-4s %-5s %-5s"
            % (
                report.name[:24],
                report.line_range,
                report.score,
                report.level[:8],
                int(report.cognitive_complexity),
                int(report.cyclomatic_complexity),
                report.nloc,
                report.token_count,
            )
        )
    print("\n可用 -s/--symbol 指定函数、方法或类名做详细分析。")


def print_report(report: Report, source_name: str) -> None:
    print("面试手写复杂度报告: %s" % source_name)
    print("Target: %s (%s, lines %s)" % (report.name, report.kind, report.line_range))
    print("Score : %s  ->  %s" % (report.score, report.level))
    print(
        "Metrics: cognitive=%s, cyclomatic=%s, nloc=%s, tokens=%s, nesting=%s, args=%s"
        % (
            int(report.cognitive_complexity),
            int(report.cyclomatic_complexity),
            report.nloc,
            report.token_count,
            report.max_nesting,
            report.arg_count,
        )
    )

    if report.risk_flags:
        print("\n风险点:")
        for item in report.risk_flags:
            print("- +%s %s" % (item.points, item.message))

    if report.bonuses:
        print("\n减分项:")
        for item in report.bonuses:
            print("- -%s %s" % (item.points, item.message))


def print_no_core_targets(source_name: str) -> None:
    print("面试手写复杂度报告: %s" % source_name)
    print("未发现默认规则下的核心代码目标。")
    print("默认会忽略 __main__、以及 demo/example/test 等示例代码。")
    print("如果你确实想把这些部分也纳入分析，可加 --include-examples。")


def reports_to_json(reports: Sequence[Report], source_name: str) -> str:
    payload = {
        "source": source_name,
        "reports": [serialize_report(report) for report in reports],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def empty_reports_json(source_name: str) -> str:
    payload = {
        "source": source_name,
        "reports": [],
        "message": "未发现默认规则下的核心代码目标",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def serialize_report(report: Report) -> dict:
    data = asdict(report)
    data["risk_flags"] = [asdict(item) for item in report.risk_flags]
    data["bonuses"] = [asdict(item) for item in report.bonuses]
    return data


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    source, source_name = read_source(args)
    source = normalize_source(source)

    try:
        targets = gather_targets(source, strict_core=bool(args.input))
        selected = select_targets(targets, args.symbol, args.include_examples)
        reports = [analyze_target(target) for target in selected]
    except SyntaxError as exc:
        raise SystemExit("代码无法解析，请确认输入的是合法的 Python 代码: %s" % exc) from exc

    if not reports:
        if args.json:
            print(empty_reports_json(source_name))
            return 0
        print_no_core_targets(source_name)
        return 0

    if args.json:
        print(reports_to_json(reports, source_name))
        return 0

    if len(reports) == 1:
        print_report(reports[0], source_name)
        return 0

    print_summary(reports, source_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
