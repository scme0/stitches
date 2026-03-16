from enum import StrEnum
from math import sqrt
from json import dumps
from collections import namedtuple
from typing import Iterable


def stringify(object):
    return dumps(object.__dict__)


class StitchType(StrEnum):
    FrontOne  = "Front1"
    FrontTwo  = "Front2"
    BackOne   = "Back1"
    BackTwo   = "Back2"
    Automatic = "Automatic"


class Corner(StrEnum):
    TopLeft     = "TopLeft"
    TopRight    = "TopRight"
    BottomLeft  = "BottomLeft"
    BottomRight = "BottomRight"


StitchPoint = tuple[int, Corner]


class Stitch:
    def __init__(self, fro: StitchPoint, to: StitchPoint, type: StitchType):
        self.fro  = fro
        self.to   = to
        self.type = type


class SimpleStitch:
    def __init__(self, squareId: int, fro: Corner, to: Corner,
                 type: StitchType = StitchType.Automatic):
        self.squareId = squareId
        self.fro      = fro
        self.to       = to
        self.type     = type


class Square:
    def __init__(self, x: int, y: int, count: int):
        self.x = x
        self.y = y
        self.corners: dict[Corner, tuple[float, float, float]] = {
            Corner.TopLeft:     (x - .5, y + .5, 0),
            Corner.TopRight:    (x + .5, y + .5, 0),
            Corner.BottomLeft:  (x - .5, y - .5, 0),
            Corner.BottomRight: (x + .5, y - .5, 0),
        }
        self.verticies = [
            (count * 4),
            1 + (count * 4),
            2 + (count * 4),
            3 + (count * 4),
        ]
        self.edges = [
            (self.verticies[0], self.verticies[1]),
            (self.verticies[1], self.verticies[2]),
            (self.verticies[2], self.verticies[3]),
            (self.verticies[3], self.verticies[0]),
        ]
        self.layouts = {
            self.verticies[0]: self.corners[Corner.BottomLeft],
            self.verticies[1]: self.corners[Corner.BottomRight],
            self.verticies[2]: self.corners[Corner.TopRight],
            self.verticies[3]: self.corners[Corner.TopLeft],
        }


class Aida:
    def __init__(self, title: str, x: int, y: int, removed={}):
        self.title    = title
        self.x        = x
        self.y        = y
        self.disabled = removed
        self.squares: list[Square]            = []
        self.stiches: list[Stitch|SimpleStitch] = []
        for yIdx in reversed(range(self.y)):
            for xIdx in range(self.x):
                if (xIdx, yIdx) not in self.disabled:
                    self.squares.append(Square(xIdx, yIdx, len(self.squares)))

    def addStitch(self, stitch: Stitch | SimpleStitch):
        self.stiches.append(stitch)


# ---------------------------------------------------------------------------
# Planner internals
# ---------------------------------------------------------------------------

_Task = namedtuple('Task', ['cell_id', 'kind', 'node_a', 'node_b'])

_FRONT_CORNERS = {
    'front1': {
        'fwd': (Corner.TopLeft,     Corner.BottomRight),
        'rev': (Corner.BottomRight, Corner.TopLeft),
    },
    'front2': {
        'fwd': (Corner.TopRight,    Corner.BottomLeft),
        'rev': (Corner.BottomLeft,  Corner.TopRight),
    },
}


def plan_stitching(
    title: str,
    cols: int,
    rows: int,
    cells: Iterable[tuple[int, int]],
    removed: Iterable[tuple[int, int]] | None = None,
) -> Aida:
    """
    Graph-traversal cross stitch planner.

    Rules:
      1. Stitches alternate strictly Front / Back throughout.
      2. Back stitches are H or V, distance >= 1 unit; zero-distance back
         stitches are never emitted.
      3. FrontOne (\\ diagonal, TL->BR) precedes FrontTwo (/ diagonal,
         TR->BL) for every individual cell.
      4. The path starts at one end of the longest straight run so the
         thread tail is hidden under a long sequence of back stitches.

    Scoring priority (ascending = better):
      (is_diagonal, kind_pref, is_jump, back_dist, not_same_row)

    Args:
        title:   Display title shown above the grid in the animation.
        cols:    Total grid width in cells.
        rows:    Total grid height in cells.
        cells:   (col, row) pairs to stitch.  row 0 is the bottom of the grid.
        removed: Optional (col, row) pairs omitted from the displayed grid.

    Returns:
        Aida instance with the planned stitch sequence already added.
    """
    cells_set   = {tuple(c) for c in cells}
    removed_set = {tuple(c) for c in removed} if removed else set()

    grid       = Aida(title, cols, rows, removed=removed_set)
    cell_to_id = {(sq.x, sq.y): i for i, sq in enumerate(grid.squares)}
    valid      = {c for c in cells_set if c in cell_to_id}

    if not valid:
        return grid

    active_sq_ids = sorted(cell_to_id[c] for c in valid)

    # ------------------------------------------------------------------ #
    # Node canonicalisation                                                #
    # ------------------------------------------------------------------ #
    node_map: dict[tuple, int] = {}
    for sq in grid.squares:
        for coord in sq.corners.values():
            key = (coord[0], coord[1])
            if key not in node_map:
                node_map[key] = len(node_map)

    node_coords: dict[int, tuple] = {v: k for k, v in node_map.items()}

    cell_nodes: dict[int, dict] = {
        sq_id: {
            corner: node_map[(coord[0], coord[1])]
            for corner, coord in grid.squares[sq_id].corners.items()
        }
        for sq_id in range(len(grid.squares))
    }

    node_to_sq_corners: dict[int, list] = {}
    for sq_id, corners in cell_nodes.items():
        for corner, node_id in corners.items():
            node_to_sq_corners.setdefault(node_id, []).append((sq_id, corner))

    # ------------------------------------------------------------------ #
    # Tasks  (2 per active cell: front1 and front2)                       #
    # ------------------------------------------------------------------ #
    all_tasks: list[_Task] = []
    for sq_id in active_sq_ids:
        cn = cell_nodes[sq_id]
        all_tasks.append(_Task(sq_id, 'front1', cn[Corner.TopLeft],  cn[Corner.BottomRight]))
        all_tasks.append(_Task(sq_id, 'front2', cn[Corner.TopRight], cn[Corner.BottomLeft]))

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #
    def node_dist(a: int, b: int) -> float:
        ax, ay = node_coords[a]
        bx, by = node_coords[b]
        return sqrt((ax - bx) ** 2 + (ay - by) ** 2)

    def available_tasks(done: set, front1_done: set) -> list:
        return [
            t for t in all_tasks
            if t not in done
            and (t.kind == 'front1' or t.cell_id in front1_done)
        ]

    def best_candidate(current: int, avail: list, current_y: int) -> tuple:
        best_score = None
        best_task  = None
        best_dir   = None
        cx, cy = node_coords[current]
        # End cells are deferred until no non-end tasks remain.
        has_non_end = any(t.cell_id not in end_sq_ids for t in avail)
        for task in avail:
            # Skip reserved end-run cells until all other work is done, then
            # visit them in run order (end_pos) so the back stitches form
            # a clean sequential chain the thread tail can be tucked under.
            if has_non_end and task.cell_id in end_sq_ids:
                continue
            task_y = grid.squares[task.cell_id].y
            end_pos = end_order_map.get(task.cell_id, 0)
            for direction in ('fwd', 'rev'):
                start = task.node_a if direction == 'fwd' else task.node_b
                d = node_dist(current, start)
                if d < 1e-9:
                    continue  # zero-distance back stitch — not allowed
                sx, sy       = node_coords[start]
                is_diagonal  = 0 if (sx == cx or sy == cy) else 1
                kind_pref    = 0 if task.kind == 'front1' else 1
                is_jump      = 1 if d > 1.0 + 1e-9 else 0
                not_same_row = 0 if task_y == current_y else 1
                score = (is_diagonal, kind_pref, is_jump, d, not_same_row,
                         end_pos)
                if best_score is None or score < best_score:
                    best_score = score
                    best_task  = task
                    best_dir   = direction
        return best_task, best_dir

    def emit_front(task: _Task, direction: str) -> None:
        fro_c, to_c = _FRONT_CORNERS[task.kind][direction]
        stype = StitchType.FrontOne if task.kind == 'front1' else StitchType.FrontTwo
        grid.addStitch(SimpleStitch(task.cell_id, fro_c, to_c, stype))

    def emit_back(from_node: int, to_node: int) -> None:
        d     = node_dist(from_node, to_node)
        btype = StitchType.BackOne if d <= 1.0 + 1e-9 else StitchType.BackTwo
        from_reps = node_to_sq_corners[from_node]
        to_reps   = node_to_sq_corners[to_node]
        shared    = {r[0] for r in from_reps} & {r[0] for r in to_reps}
        if shared:
            sq_id = next(iter(shared))
            fro_c = next(r[1] for r in from_reps if r[0] == sq_id)
            to_c  = next(r[1] for r in to_reps   if r[0] == sq_id)
            grid.addStitch(SimpleStitch(sq_id, fro_c, to_c, btype))
        else:
            from_sq, fro_c = from_reps[0]
            to_sq,   to_c  = to_reps[0]
            grid.addStitch(Stitch((from_sq, fro_c), (to_sq, to_c), btype))

    # ------------------------------------------------------------------ #
    # Start position: end of the longest boundary run closest to a corner #
    # ------------------------------------------------------------------ #
    def find_start_run() -> list:
        all_xs = [c[0] for c in valid]
        all_ys = [c[1] for c in valid]
        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)

        # Corners preferred as start points: top-left and bottom-right,
        # the two ends of the main diagonal of the bounding box.
        preferred = {(min_x, max_y), (max_x, min_y)}
        any_corner = {(min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)}

        # Collect every maximal contiguous run (H and V).
        all_runs: list[list] = []

        row_map: dict[int, list] = {}
        for x, y in sorted(valid):
            row_map.setdefault(y, []).append(x)
        for y, xs in sorted(row_map.items()):
            cur = [xs[0]]
            for x in xs[1:]:
                if x == cur[-1] + 1:
                    cur.append(x)
                else:
                    all_runs.append([(xi, y) for xi in cur])
                    cur = [x]
            all_runs.append([(xi, y) for xi in cur])

        col_map: dict[int, list] = {}
        for x, y in sorted(valid):
            col_map.setdefault(x, []).append(y)
        for x, ys in sorted(col_map.items()):
            cur = [ys[0]]
            for y in ys[1:]:
                if y == cur[-1] + 1:
                    cur.append(y)
                else:
                    all_runs.append([(x, yi) for yi in cur])
                    cur = [y]
            all_runs.append([(x, yi) for yi in cur])

        def run_score(run: list) -> tuple:
            first, last = run[0], run[-1]
            y0 = first[1]
            x0 = first[0]
            is_h    = (y0 == last[1])
            on_edge = (y0 in (min_y, max_y)) if is_h else (x0 in (min_x, max_x))
            has_preferred = first in preferred or last in preferred
            has_corner    = first in any_corner or last in any_corner
            return (
                -min(len(run), 4),
                0 if on_edge       else 1,
                0 if has_preferred else 1,
                0 if has_corner    else 1,
            )

        all_runs.sort(key=run_score)
        run = all_runs[0]

        # Orient so we start from a preferred corner, then any corner, then keep as-is.
        first, last = run[0], run[-1]
        if last in preferred and first not in preferred:
            run = list(reversed(run))
        elif last in any_corner and first not in any_corner:
            run = list(reversed(run))

        return run

    longest_run = find_start_run()
    start_sq_id = cell_to_id[longest_run[0]]
    start_task  = next(t for t in all_tasks if t.cell_id == start_sq_id and t.kind == 'front1')

    # Reserve the last 3 cells of the run so the sequence finishes with a
    # clean sequential traversal — the stitcher can tuck the finishing thread
    # under those consecutive back stitches.  Only applied when the run is
    # long enough (≥ 4 cells) to leave at least one non-reserved cell before
    # the end section; shorter runs fall naturally into run order already.
    end_count     = min(3, len(longest_run) - 1) if len(longest_run) >= 4 else 0
    end_run       = longest_run[-end_count:] if end_count else []
    end_sq_ids    = {cell_to_id[c] for c in end_run}
    end_order_map = {cell_to_id[c]: i for i, c in enumerate(end_run)}

    # ------------------------------------------------------------------ #
    # Main traversal loop                                                  #
    # ------------------------------------------------------------------ #
    def end_node(task: _Task, direction: str) -> int:
        return task.node_b if direction == 'fwd' else task.node_a

    def start_node(task: _Task, direction: str) -> int:
        return task.node_a if direction == 'fwd' else task.node_b

    done: set        = set()
    front1_done: set = set()

    emit_front(start_task, 'fwd')
    current   = end_node(start_task, 'fwd')
    current_y = grid.squares[start_task.cell_id].y
    done.add(start_task)
    front1_done.add(start_task.cell_id)

    while len(done) < len(all_tasks):
        avail = available_tasks(done, front1_done)
        best_task, best_dir = best_candidate(current, avail, current_y)
        if best_task is None:
            break

        emit_back(current, start_node(best_task, best_dir))
        emit_front(best_task, best_dir)
        current   = end_node(best_task, best_dir)
        current_y = grid.squares[best_task.cell_id].y
        done.add(best_task)
        if best_task.kind == 'front1':
            front1_done.add(best_task.cell_id)

    return grid
