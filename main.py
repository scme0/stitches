from manim import MovingCameraScene
from grid import SimpleStitch, Aida, StitchType, Stitch, plan_stitching
from grid import Corner as C

class SingleStitch(MovingCameraScene):
    def construct(self):
        g = Aida("Single Stitch", 1, 1)
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.draw(self)

class HorizontalStiches(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Stitches", 3, 1)
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.draw(self)

class VerticalStitches(MovingCameraScene):
    def construct(self):
        g = Aida("Vertical Stitches", 1, 3)
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopRight, C.TopLeft))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopRight, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.BottomLeft, C.TopRight))
        g.draw(self)

class HorizontalExpandingDown(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Expanding Down", 3, 2, removed={(0,1)})
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.TopRight, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(4, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(4, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(4, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(4, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(3, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.draw(self)

class HorizontalGoingAbove(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Going Above", 3, 2, removed={(0,1)})
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.TopLeft, C.TopRight, StitchType.BackOne))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.TopRight, StitchType.BackOne))
        g.addStitch(SimpleStitch(4, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(4, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(4, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(4, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(3, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.draw(self)

class HorizontalGoingBelow(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Going Below", 3, 2, removed={(0,0)})
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(4, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(4, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(4, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.BottomLeft, C.TopRight))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.draw(self)

class HorizontalStackedLayers(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Stacked Layers", 3, 2)
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(1, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(0, C.BottomLeft, C.TopRight))
        g.addStitch(Stitch((0, C.TopRight), (3, C.BottomRight), StitchType.BackTwo))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.TopLeft))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.TopRight, StitchType.BackTwo))
        g.addStitch(SimpleStitch(4, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(4, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(5, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(5, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(5, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(5, C.BottomLeft, C.TopLeft))
        g.addStitch(SimpleStitch(4, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(4, C.BottomLeft, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(3, C.TopRight, C.BottomLeft))
        g.draw(self)

class HorizontalJump(MovingCameraScene):
    def construct(self):
        g = Aida("Horizontal Jump", 5, 1, removed={(2,0)})
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(Stitch((1, C.BottomRight), (2, C.BottomRight), StitchType.BackOne))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopLeft))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.TopRight, StitchType.BackOne))
        g.addStitch(SimpleStitch(3, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(3, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(3, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(3, C.BottomLeft, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.addStitch(Stitch((2, C.BottomLeft), (1, C.BottomLeft), StitchType.BackTwo))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopRight, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.draw(self)

class JumpAbove(MovingCameraScene):
    def construct(self):
        g = Aida("Jump Above", 5, 2, removed={(2,0),(3,0),(4,0),(0,1),(1,1),(2,1),(3,1)})
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.BottomRight, StitchType.BackOne))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.TopLeft))
        g.addStitch(Stitch((2, C.TopLeft), (0, C.BottomRight), StitchType.BackOne))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopLeft))
        g.addStitch(SimpleStitch(0, C.TopLeft, C.TopRight, StitchType.BackOne))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.addStitch(Stitch((0, C.BottomLeft), (2, C.TopRight), StitchType.BackTwo))
        g.addStitch(SimpleStitch(2, C.TopRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(1, C.TopRight, C.BottomLeft))
        g.draw(self)

class JumpBelow(MovingCameraScene):
    def construct(self):
        g = Aida("Jump Below", 5, 2, removed={(2,1),(3,1),(4,1),(0,0),(1,0),(2,0),(3,0)})
        g.addStitch(SimpleStitch(0, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(0, C.BottomRight, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopLeft, C.BottomRight))
        g.addStitch(Stitch((1, C.BottomRight),(2, C.TopLeft), StitchType.BackOne))
        g.addStitch(SimpleStitch(2, C.TopLeft, C.BottomRight))
        g.addStitch(SimpleStitch(2, C.BottomRight, C.BottomLeft))
        g.addStitch(SimpleStitch(2, C.BottomLeft, C.TopRight))
        g.addStitch(Stitch((2, C.TopRight), (1, C.BottomLeft), StitchType.BackTwo))
        g.addStitch(SimpleStitch(1, C.BottomLeft, C.TopRight))
        g.addStitch(SimpleStitch(1, C.TopRight, C.TopLeft, StitchType.BackOne))
        g.addStitch(SimpleStitch(0, C.TopRight, C.BottomLeft))
        g.draw(self)


# ---------------------------------------------------------------------------
# Scenes using the auto-planner
# ---------------------------------------------------------------------------

class PlannedHorizontal(MovingCameraScene):
    """Auto-planned equivalent of HorizontalStiches (3×1 row)."""
    def construct(self):
        cells = [(x, 0) for x in range(3)]
        g = plan_stitching("Planned: Horizontal", 3, 1, cells)
        g.draw(self)


class PlannedVertical(MovingCameraScene):
    """Auto-planned equivalent of VerticalStitches (1×3 column)."""
    def construct(self):
        cells = [(0, y) for y in range(3)]
        g = plan_stitching("Planned: Vertical", 1, 3, cells)
        g.draw(self)


class PlannedRectangle(MovingCameraScene):
    """Auto-planned 4×3 solid block — shows zero-waste row chaining."""
    def construct(self):
        cells = [(x, y) for x in range(4) for y in range(3)]
        g = plan_stitching("Planned: 4x3 Block", 4, 3, cells)
        g.draw(self)


class PlannedLShape(MovingCameraScene):
    """Auto-planned L-shaped layout — two rows of different widths."""
    def construct(self):
        cells = [(x, 1) for x in range(4)] + [(0, 0), (1, 0)]
        g = plan_stitching("Planned: L-Shape", 4, 2, cells)
        g.draw(self)


class PlannedGappedRow(MovingCameraScene):
    """Auto-planned row with a gap — tests the same-row segment connector."""
    def construct(self):
        cells = [(0, 0), (1, 0), (3, 0), (4, 0)]   # gap at x=2
        g = plan_stitching("Planned: Gapped Row", 5, 1, cells)
        g.draw(self)


class PlannedStaircase(MovingCameraScene):
    """Auto-planned staircase — rows stagger right; tests cross-row connectors."""
    def construct(self):
        cells = (
            [(x, 2) for x in range(3)] +
            [(x, 1) for x in range(1, 4)] +
            [(x, 0) for x in range(2, 5)]
        )
        g = plan_stitching("Planned: Staircase", 5, 3, cells)
        g.draw(self)
