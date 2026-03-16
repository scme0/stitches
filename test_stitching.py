import unittest
from math import sqrt

from stitching import plan_stitching, StitchType, SimpleStitch, Stitch, Aida


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def stitch_types(grid: Aida) -> list[str]:
    return [s.type for s in grid.stiches]


def front_index(grid: Aida, sq_id: int, kind: StitchType) -> int | None:
    """Return position in stitch list of the first front stitch of given kind for sq_id."""
    return next(
        (i for i, s in enumerate(grid.stiches)
         if isinstance(s, SimpleStitch) and s.squareId == sq_id and s.type == kind),
        None,
    )


def back_stitch_coords(grid: Aida) -> list[tuple]:
    """Return (from_x, from_y, to_x, to_y) for every back stitch."""
    result = []
    for s in grid.stiches:
        if s.type not in (StitchType.BackOne, StitchType.BackTwo):
            continue
        if isinstance(s, SimpleStitch):
            sq = grid.squares[s.squareId]
            fx, fy, _ = sq.corners[s.fro]
            tx, ty, _ = sq.corners[s.to]
        else:
            fx, fy, _ = grid.squares[s.fro[0]].corners[s.fro[1]]
            tx, ty, _ = grid.squares[s.to[0]].corners[s.to[1]]
        result.append((fx, fy, tx, ty))
    return result


def max_jump(grid: Aida) -> float:
    """Return the longest back-stitch distance in the sequence."""
    worst = 0.0
    for fx, fy, tx, ty in back_stitch_coords(grid):
        worst = max(worst, sqrt((fx - tx) ** 2 + (fy - ty) ** 2))
    return worst


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestAlternation(unittest.TestCase):
    """Every stitch must alternate Front / Back."""

    def _check(self, grid: Aida, label: str):
        types = stitch_types(grid)
        self.assertTrue(len(types) > 0, f"{label}: no stitches generated")
        for i, t in enumerate(types):
            expected = "Front" if i % 2 == 0 else "Back"
            self.assertIn(expected, t,
                          f"{label}: position {i} expected {expected}, got {t}")

    def test_single_cell(self):
        self._check(plan_stitching("1x1", 1, 1, [(0, 0)]), "1x1")

    def test_horizontal_row(self):
        self._check(plan_stitching("3x1", 3, 1, [(x, 0) for x in range(3)]), "3x1")

    def test_vertical_column(self):
        self._check(plan_stitching("1x3", 1, 3, [(0, y) for y in range(3)]), "1x3")

    def test_rectangle(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        self._check(plan_stitching("3x3", 3, 3, cells), "3x3")

    def test_l_shape(self):
        cells = [(x, 1) for x in range(4)] + [(0, 0), (1, 0)]
        self._check(plan_stitching("L", 4, 2, cells), "L")

    def test_gapped_row(self):
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]
        self._check(plan_stitching("gapped", 5, 1, cells), "gapped")

    def test_staircase(self):
        cells = ([(x, 2) for x in range(3)] +
                 [(x, 1) for x in range(1, 4)] +
                 [(x, 0) for x in range(2, 5)])
        self._check(plan_stitching("staircase", 5, 3, cells), "staircase")


class TestFrontOneBeforeFrontTwo(unittest.TestCase):
    """FrontOne must appear before FrontTwo for every individual cell."""

    def _check(self, grid: Aida, label: str):
        for sq_id in range(len(grid.squares)):
            f1 = front_index(grid, sq_id, StitchType.FrontOne)
            f2 = front_index(grid, sq_id, StitchType.FrontTwo)
            if f1 is not None and f2 is not None:
                self.assertLess(f1, f2,
                                f"{label}: cell {sq_id} FrontOne at {f1}, FrontTwo at {f2}")

    def test_single_cell(self):
        self._check(plan_stitching("1x1", 1, 1, [(0, 0)]), "1x1")

    def test_horizontal_row(self):
        self._check(plan_stitching("3x1", 3, 1, [(x, 0) for x in range(3)]), "3x1")

    def test_vertical_column(self):
        self._check(plan_stitching("1x3", 1, 3, [(0, y) for y in range(3)]), "1x3")

    def test_rectangle(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        self._check(plan_stitching("3x3", 3, 3, cells), "3x3")

    def test_l_shape(self):
        cells = [(x, 1) for x in range(4)] + [(0, 0), (1, 0)]
        self._check(plan_stitching("L", 4, 2, cells), "L")

    def test_gapped_row(self):
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]
        self._check(plan_stitching("gapped", 5, 1, cells), "gapped")

    def test_staircase(self):
        cells = ([(x, 2) for x in range(3)] +
                 [(x, 1) for x in range(1, 4)] +
                 [(x, 0) for x in range(2, 5)])
        self._check(plan_stitching("staircase", 5, 3, cells), "staircase")


class TestNoZeroDistanceBackStitch(unittest.TestCase):
    """Back stitches must never have zero length."""

    def _check(self, grid: Aida, label: str):
        for fx, fy, tx, ty in back_stitch_coords(grid):
            d = sqrt((fx - tx) ** 2 + (fy - ty) ** 2)
            self.assertGreater(d, 1e-9,
                               f"{label}: zero-length back stitch at ({fx},{fy})")

    def test_single_cell(self):
        self._check(plan_stitching("1x1", 1, 1, [(0, 0)]), "1x1")

    def test_rectangle(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        self._check(plan_stitching("3x3", 3, 3, cells), "3x3")

    def test_gapped_row(self):
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]
        self._check(plan_stitching("gapped", 5, 1, cells), "gapped")


class TestNodiagonalBackStitch(unittest.TestCase):
    """Back stitches must be strictly horizontal or vertical (same x or same y)."""

    def _check(self, grid: Aida, label: str):
        for fx, fy, tx, ty in back_stitch_coords(grid):
            is_hv = abs(fx - tx) < 1e-9 or abs(fy - ty) < 1e-9
            self.assertTrue(is_hv,
                            f"{label}: diagonal back stitch ({fx},{fy})->({tx},{ty})")

    def test_single_cell(self):
        self._check(plan_stitching("1x1", 1, 1, [(0, 0)]), "1x1")

    def test_horizontal_row(self):
        self._check(plan_stitching("3x1", 3, 1, [(x, 0) for x in range(3)]), "3x1")

    def test_rectangle(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        self._check(plan_stitching("3x3", 3, 3, cells), "3x3")

    def test_l_shape(self):
        cells = [(x, 1) for x in range(4)] + [(0, 0), (1, 0)]
        self._check(plan_stitching("L", 4, 2, cells), "L")

    def test_gapped_row(self):
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]
        self._check(plan_stitching("gapped", 5, 1, cells), "gapped")

    def test_staircase(self):
        cells = ([(x, 2) for x in range(3)] +
                 [(x, 1) for x in range(1, 4)] +
                 [(x, 0) for x in range(2, 5)])
        self._check(plan_stitching("staircase", 5, 3, cells), "staircase")


class TestStitchCount(unittest.TestCase):
    """Total stitch count must equal 2n front + (2n-1) back = 4n-1 for n cells."""

    def _check(self, grid: Aida, n_cells: int, label: str):
        expected = 4 * n_cells - 1
        self.assertEqual(len(grid.stiches), expected,
                         f"{label}: expected {expected} stitches, got {len(grid.stiches)}")

    def test_single_cell(self):
        self._check(plan_stitching("1x1", 1, 1, [(0, 0)]), 1, "1x1")

    def test_horizontal_row(self):
        self._check(plan_stitching("3x1", 3, 1, [(x, 0) for x in range(3)]), 3, "3x1")

    def test_vertical_column(self):
        self._check(plan_stitching("1x3", 1, 3, [(0, y) for y in range(3)]), 3, "1x3")

    def test_rectangle(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        self._check(plan_stitching("3x3", 3, 3, cells), 9, "3x3")


class TestEmptyGrid(unittest.TestCase):
    def test_no_cells_returns_empty(self):
        grid = plan_stitching("empty", 3, 3, [])
        self.assertEqual(grid.stiches, [])

    def test_cells_outside_grid_ignored(self):
        grid = plan_stitching("out", 2, 2, [(5, 5)])
        self.assertEqual(grid.stiches, [])


class TestStartsAtCorner(unittest.TestCase):
    """The first stitch should begin at a bounding-box corner, not the interior."""

    def _start_cell(self, grid: Aida) -> tuple[int, int]:
        sq = grid.squares[grid.stiches[0].squareId]
        return (sq.x, sq.y)

    def _corners(self, cells: list) -> set[tuple[int, int]]:
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return {(min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)}

    def test_rectangle_starts_at_corner(self):
        cells = [(x, y) for x in range(3) for y in range(3)]
        grid  = plan_stitching("3x3", 3, 3, cells)
        self.assertIn(self._start_cell(grid), self._corners(cells))

    def test_wide_rectangle_starts_at_corner(self):
        cells = [(x, y) for x in range(4) for y in range(3)]
        grid  = plan_stitching("4x3", 4, 3, cells)
        self.assertIn(self._start_cell(grid), self._corners(cells))

    def test_l_shape_starts_at_corner(self):
        cells = [(x, 1) for x in range(4)] + [(0, 0), (1, 0)]
        grid  = plan_stitching("L", 4, 2, cells)
        self.assertIn(self._start_cell(grid), self._corners(cells))

    def test_preferred_corner_is_top_left_or_bottom_right(self):
        # For a symmetric rectangle both preferred corners are equally valid.
        cells  = [(x, y) for x in range(3) for y in range(3)]
        grid   = plan_stitching("3x3", 3, 3, cells)
        start  = self._start_cell(grid)
        all_xs = [c[0] for c in cells]
        all_ys = [c[1] for c in cells]
        preferred = {
            (min(all_xs), max(all_ys)),  # top-left
            (max(all_xs), min(all_ys)),  # bottom-right
        }
        self.assertIn(start, preferred)


class TestGappedRowJumps(unittest.TestCase):
    """Two smaller jumps are preferred over one large jump across a gap."""

    def test_max_jump_is_two_not_four(self):
        # Gap at x=2; naive completion of left group before crossing = d=4
        # Two-pass strategy (front1 across, front2 back) = d=2 each
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]
        grid  = plan_stitching("gapped", 5, 1, cells)
        self.assertLessEqual(max_jump(grid), 2.0 + 1e-9,
                             "expected max jump ≤ 2.0 for gapped row")

    def test_jump_count(self):
        cells  = [(0, 0), (1, 0), (3, 0), (4, 0)]
        grid   = plan_stitching("gapped", 5, 1, cells)
        jumps  = [s for s in grid.stiches if s.type == StitchType.BackTwo]
        self.assertEqual(len(jumps), 2, "expected exactly 2 jumps for gapped row")


class TestEndRunOrder(unittest.TestCase):
    """For runs >= 4 cells, the last 3 stitched cells must come from the
    start run in run order so the finishing thread can be tucked under them."""

    def _last_front_cells(self, grid: Aida, n: int) -> list[tuple[int, int]]:
        """Return (x, y) of the last n front-stitch cells in emission order."""
        front_stitches = [
            s for s in grid.stiches
            if s.type in (StitchType.FrontOne, StitchType.FrontTwo)
        ]
        last_n = front_stitches[-n:]
        return [(grid.squares[s.squareId].x, grid.squares[s.squareId].y)
                for s in last_n]

    def test_horizontal_row_5_cells_ends_in_run_order(self):
        cells = [(x, 0) for x in range(5)]
        grid  = plan_stitching("5x1", 5, 1, cells)
        last3_cells = self._last_front_cells(grid, 6)  # 6 front stitches = last 3 cells
        # The unique cells in last 6 front stitches should be 3 consecutive cells
        unique = list(dict.fromkeys(c for c in last3_cells))
        xs = [c[0] for c in unique]
        # Must be from the run (y=0) and consecutive
        self.assertEqual(len(unique), 3, "last 3 cells should be 3 distinct cells")
        self.assertTrue(xs == sorted(xs) or xs == sorted(xs, reverse=True),
                        f"last 3 cells must be in run order, got {unique}")

    def test_vertical_column_4_cells_ends_in_run_order(self):
        cells = [(0, y) for y in range(4)]
        grid  = plan_stitching("1x4", 1, 4, cells)
        last3_cells = self._last_front_cells(grid, 6)
        unique = list(dict.fromkeys(c for c in last3_cells))
        ys = [c[1] for c in unique]
        self.assertEqual(len(unique), 3)
        self.assertTrue(ys == sorted(ys) or ys == sorted(ys, reverse=True),
                        f"last 3 cells must be in run order, got {unique}")

    def test_short_run_no_reservation(self):
        # A 3-cell row (< 4) should NOT reserve end cells — all tests still pass.
        cells = [(x, 0) for x in range(3)]
        grid  = plan_stitching("3x1", 3, 1, cells)
        types = stitch_types(grid)
        self.assertTrue(len(types) > 0)
        for i, t in enumerate(types):
            expected = "Front" if i % 2 == 0 else "Back"
            self.assertIn(expected, t)


if __name__ == "__main__":
    unittest.main()
