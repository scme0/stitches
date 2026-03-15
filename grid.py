from enum import StrEnum
from manim import MovingCameraScene, Graph, Text, MovingCamera, Line, DashedLine, Create
from manim import UP, WHITE, PURPLE, GREEN, YELLOW, RED, GRAY
from json import dumps
from collections import namedtuple
from typing import Iterable

def stringify(object):
    return dumps(object.__dict__)

class StitchType(StrEnum):
    FrontOne = "Front1"
    FrontTwo = "Front2"
    BackOne = "Back1"
    BackTwo = "Back2"
    Automatic = "Automatic"

class Corner(StrEnum):
    TopLeft = "TopLeft"
    TopRight = "TopRight"
    BottomLeft = "BottomLeft"
    BottomRight = "BottomRight"

StitchPoint = tuple[int, Corner]

class Stitch:
    def __init__(self, fro: StitchPoint, to: StitchPoint, type: StitchType):
        self.fro = fro
        self.to = to
        self.type = type

class SimpleStitch:
    def __init__(self, squareId: int, fro: Corner, to: Corner, type: StitchType = StitchType.Automatic):
        self.squareId = squareId
        self.fro = fro
        self.to = to
        self.type = type

class Square:
    def __init__(self, x: int, y: int, count: int):
        self.x = x
        self.y = y
        self.layouts = {}
        self.verticies = []
        self.corners: dict[Corner, tuple[float, float, float]] = {
            Corner.TopLeft: (x-.5, y+.5, 0),
            Corner.TopRight: (x+.5, y+.5, 0),
            Corner.BottomLeft: (x-.5, y-.5, 0),
            Corner.BottomRight: (x+.5, y-.5, 0),
        }
        self.verticies = [
            (count*4),
            1+(count*4),
            2+(count*4),
            3+(count*4),
        ]
        self.edges = [
            (self.verticies[0], self.verticies[1]),
            (self.verticies[1], self.verticies[2]),
            (self.verticies[2], self.verticies[3]),
            (self.verticies[3], self.verticies[0])
        ]
        self.layouts = {
            self.verticies[0]: self.corners[Corner.BottomLeft],
            self.verticies[1]: self.corners[Corner.BottomRight],
            self.verticies[2]: self.corners[Corner.TopRight],
            self.verticies[3]: self.corners[Corner.TopLeft],
        }

class Aida:
    def __init__(self, title: str, x: int, y: int, removed = {}):
        self.title = title
        self.x = x
        self.y = y
        self.disabled = removed
        self.squares: list[Square] = []
        self.stiches: list[Stitch|SimpleStitch] = []
        for yIdx in reversed(range(self.y)):
            for xIdx in range(self.x):
                if (xIdx,yIdx) not in self.disabled:
                    self.squares.append(Square(xIdx, yIdx, len(self.squares)))
    
    def addStitch(self, stitch: Stitch | SimpleStitch):
        self.stiches.append(stitch)
    
    def draw(self, scene: MovingCameraScene):
        verticies = []
        edges = []
        lt = {}
        for square in self.squares:
            verticies.extend(square.verticies)
            edges.extend(square.edges)
            lt.update(square.layouts)
        g = Graph(verticies, edges, layout=lt, edge_config={"stroke_color": GRAY, "stroke_width": 1})
        scene.add(g)
        t = Text(self.title, font="Arial", color=WHITE, font_size=24).next_to(g, UP)
        scene.add(t)
        if isinstance(scene.camera, MovingCamera):
            scene.camera.auto_zoom([g,t], margin=2.0, animate=False)

        for stitch in self.stiches:
            if isinstance(stitch, Stitch):
                fromSquare = self.squares[stitch.fro[0]]
                toSquare = self.squares[stitch.to[0]]
                fromPoint = fromSquare.corners[stitch.fro[1]]
                toPoint = toSquare.corners[stitch.to[1]]
                if stitch.type == StitchType.Automatic:
                    raise KeyError("Stitch cannot use Automatic Stitch type", stringify(stitch))
            elif isinstance(stitch, SimpleStitch):
                to = stitch.to
                fro = stitch.fro
                square = self.squares[stitch.squareId]
                fromPoint = square.corners[fro]
                toPoint = square.corners[to]
                if stitch.type == StitchType.Automatic:

                    if (fro == Corner.TopLeft and to == Corner.BottomRight) or (fro == Corner.BottomRight and to == Corner.TopLeft):
                        stitch.type = StitchType.FrontOne
                    elif fro == Corner.BottomRight and (to == Corner.TopRight or to == Corner.BottomLeft):
                        stitch.type = StitchType.BackOne
                    elif (fro == Corner.TopRight and to == Corner.BottomLeft) or (fro == Corner.BottomLeft and to == Corner.TopRight):
                        stitch.type = StitchType.FrontTwo
                    elif (fro == Corner.BottomLeft or fro == Corner.TopRight) and to == Corner.TopLeft:
                        stitch.type = StitchType.BackTwo
                    else:
                        raise KeyError("Unable to decide which stitch to use for given SimpleStitch", stringify(stitch))
            else:
                raise KeyError("Unknown Stitch Type", stringify(stitch))
            match stitch.type:
                case StitchType.FrontOne:
                    l = Line(fromPoint, toPoint, color=PURPLE)
                case StitchType.FrontTwo:
                    l = Line(fromPoint, toPoint, color=GREEN)
                case StitchType.BackOne:
                    l = DashedLine(fromPoint, toPoint, dash_length=.2, color=YELLOW)
                case StitchType.BackTwo:
                    l = DashedLine(fromPoint, toPoint, dash_length=.05, color=RED)
                    
            scene.play(Create(l))


def plan_stitching(
    title: str,
    cols: int,
    rows: int,
    cells: Iterable[tuple[int, int]],
    removed: Iterable[tuple[int, int]] | None = None,
) -> Aida:
    """
    Automatically plan a cross stitch path for a layout of cells.

    Rules applied, in priority order:
      1. Back stitches on the fabric reverse are always horizontal or vertical.
      2. FrontOne ('\\' diagonal, top-left ↔ bottom-right) is stitched before
         FrontTwo ('/' diagonal) for every individual cell.
      3. Thread usage is minimised — segments in the same row chain together
         with no jumping; adjacent rows connect at a shared corner with no
         extra stitch at all.
      4. The starting row is whichever row contains the longest single
         contiguous segment, giving the thread tail the longest possible
         runway of consecutive back stitches to be tucked under.

    Strategy — horizontal boustrophedon:
      For each row, each contiguous horizontal segment is stitched:
        • FrontOne pass  (left → right): TL→BR per cell, BR→TR back stitch
          between cells (vertical, up the right side).  Cells share their
          TR / TL corners, so no extra connector is needed.
        • Transition on the last cell: BR→TR (positions needle for FrontTwo).
        • FrontTwo pass  (right → left): TR→BL per cell, BL→TL back stitch
          between cells (vertical, up the left side).
      Each run ends at the BottomLeft of its leftmost cell.  That point is
      identical to the TopLeft of the cell directly below it, so adjacent
      rows chain with zero waste thread.

    Args:
        title:   Display title shown above the grid in the animation.
        cols:    Total grid width in cells.
        rows:    Total grid height in cells.
        cells:   (col, row) pairs to stitch.  row 0 is the bottom of the grid.
        removed: Optional (col, row) pairs omitted from the displayed grid.

    Returns:
        Aida instance with the planned stitch sequence already added.
    """
    cells_set = {tuple(c) for c in cells}
    removed_set = {tuple(c) for c in removed} if removed else set()

    grid = Aida(title, cols, rows, removed=removed_set)
    cell_to_id = {(sq.x, sq.y): i for i, sq in enumerate(grid.squares)}
    valid = {c for c in cells_set if c in cell_to_id}

    if not valid:
        return grid

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def contiguous_segments(xs: list[int]) -> list[list[int]]:
        """Split a sorted list of x-values into contiguous groups."""
        xs = sorted(xs)
        segs, cur = [], [xs[0]]
        for x in xs[1:]:
            if x == cur[-1] + 1:
                cur.append(x)
            else:
                segs.append(cur)
                cur = [x]
        segs.append(cur)
        return segs

    def corner_point(sq_id: int, corner: Corner) -> tuple:
        return grid.squares[sq_id].corners[corner]

    def same_point(sq_a: int, c_a: Corner, sq_b: int, c_b: Corner) -> bool:
        return corner_point(sq_a, c_a) == corner_point(sq_b, c_b)

    def add_connector(from_sq: int, from_c: Corner, to_sq: int, to_c: Corner):
        """Add a back-stitch connector only when the two corners differ."""
        if same_point(from_sq, from_c, to_sq, to_c):
            return
        fa, ta = grid.squares[from_sq], grid.squares[to_sq]
        hv = (fa.x == ta.x) or (fa.y == ta.y)
        btype = StitchType.BackOne if hv else StitchType.BackTwo
        grid.addStitch(Stitch((from_sq, from_c), (to_sq, to_c), btype))

    # ------------------------------------------------------------------ #
    # Organise valid cells into rows                                       #
    # ------------------------------------------------------------------ #

    row_map: dict[int, list[int]] = {}
    for x, y in valid:
        row_map.setdefault(y, []).append(x)

    # ------------------------------------------------------------------ #
    # Runway optimisation                                                  #
    # The row whose longest contiguous segment is the longest overall is  #
    # placed first so the thread tail has the maximum number of straight  #
    # back stitches to hide under at the very start.  All other rows are  #
    # processed top-to-bottom after the start row.                        #
    # ------------------------------------------------------------------ #

    def longest_seg_len(y: int) -> int:
        return max(len(s) for s in contiguous_segments(row_map[y]))

    # Tiebreak by highest y (topmost row) so equal-length patterns process
    # top-to-bottom and adjacent rows chain with no extra connector stitches.
    best_start_y = max(row_map, key=lambda y: (longest_seg_len(y), y))

    all_rows: list[int] = sorted(row_map.keys(), reverse=True)  # top → bottom
    if best_start_y != all_rows[0]:
        all_rows.remove(best_start_y)
        all_rows.insert(0, best_start_y)

    # ------------------------------------------------------------------ #
    # Stitch generation                                                    #
    # ------------------------------------------------------------------ #

    prev_sq: int | None = None
    prev_c: Corner | None = None

    for y in all_rows:
        segs = contiguous_segments(row_map[y])
        for seg in segs:
            n = len(seg)
            first_id = cell_to_id[(seg[0], y)]
            last_id = cell_to_id[(seg[-1], y)]

            # ---- Connect from previous end-point -------------------------
            if prev_sq is not None:
                fsq = grid.squares[prev_sq]
                # If we're still in the same display row and the exit corner
                # is BottomLeft (below the row centre), climb back up to
                # TopLeft first so the gap connector runs horizontally along
                # the top edge rather than diagonally across the row.
                if fsq.y == y and prev_c == Corner.BottomLeft:
                    grid.addStitch(SimpleStitch(prev_sq, Corner.BottomLeft, Corner.TopLeft))
                    add_connector(prev_sq, Corner.TopLeft, first_id, Corner.TopLeft)
                else:
                    add_connector(prev_sq, prev_c, first_id, Corner.TopLeft)

            # ---- FrontOne pass  (left → right) ---------------------------
            # TL→BR for every cell; BR→TR back stitch between cells.
            # TR of cell x  ==  TL of cell x+1, so cells chain automatically.
            for i, x in enumerate(seg):
                sq_id = cell_to_id[(x, y)]
                grid.addStitch(SimpleStitch(sq_id, Corner.TopLeft, Corner.BottomRight))
                if i < n - 1:
                    grid.addStitch(SimpleStitch(sq_id, Corner.BottomRight, Corner.TopRight))

            # Transition: BR→TR on the last cell positions the needle at
            # TopRight, ready for the FrontTwo pass going right → left.
            grid.addStitch(SimpleStitch(last_id, Corner.BottomRight, Corner.TopRight))

            # ---- FrontTwo pass  (right → left) ---------------------------
            # TR→BL for every cell; BL→TL back stitch between cells.
            # TL of cell x  ==  TR of cell x-1, so cells chain automatically.
            for i, x in enumerate(reversed(seg)):
                sq_id = cell_to_id[(x, y)]
                grid.addStitch(SimpleStitch(sq_id, Corner.TopRight, Corner.BottomLeft))
                if i < n - 1:
                    grid.addStitch(SimpleStitch(sq_id, Corner.BottomLeft, Corner.TopLeft))

            # End position: BottomLeft of the leftmost cell.
            # BL of (x, y)  ==  TL of (x, y-1), so the next row begins
            # at exactly this point with no connector stitch needed.
            prev_sq = first_id
            prev_c = Corner.BottomLeft

    return grid