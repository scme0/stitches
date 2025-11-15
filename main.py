from manim import *
from grid import *

class SingleStitch(MovingCameraScene):
    def construct(self):
        g = Grid("Single Stitch", 1, 1)
        g.addStitch(Stitch(Point((0,0),Corner.TopLeft), Point((0,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,0),Corner.BottomRight), Point((0,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((0,0),Corner.TopRight), Point((0,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.draw(self)

class HorizontalStiches(MovingCameraScene):
    def construct(self):
        g = Grid("Horizontal Stitches", 3, 1)
        g.addStitch(Stitch(Point((0,0),Corner.TopLeft), Point((0,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,0),Corner.BottomRight), Point((0,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,0),Corner.TopLeft), Point((1,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,0),Corner.BottomRight), Point((1,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0),Corner.TopLeft), Point((2,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,0),Corner.BottomRight), Point((2,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0),Corner.TopRight), Point((2,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((2,0),Corner.BottomLeft), Point((2,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((1,0),Corner.TopRight), Point((1,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0),Corner.BottomLeft), Point((1,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,0),Corner.TopRight), Point((0,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.draw(self)

class VerticalStitches(MovingCameraScene):
    def construct(self):
        g = Grid("Vertical Stitches", 1, 3)
        g.addStitch(Stitch(Point((0,2),Corner.TopLeft), Point((0,2), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,2),Corner.BottomRight), Point((0,2), Corner.BottomLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((0,1),Corner.TopLeft), Point((0,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,1),Corner.BottomRight), Point((0,1), Corner.BottomLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((0,0),Corner.TopLeft), Point((0,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,0),Corner.BottomRight), Point((0,0), Corner.BottomLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((0,0),Corner.BottomLeft), Point((0,0), Corner.TopRight), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((0,0),Corner.TopRight), Point((0,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,1),Corner.BottomLeft), Point((0,1), Corner.TopRight), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((0,1),Corner.TopRight), Point((0,1), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,2),Corner.BottomLeft), Point((0,2), Corner.TopRight), StitchType.FrontTwo))
        g.draw(self)

class HorizontalExpandingDown(MovingCameraScene):
    def construct(self):
        g = Grid("Horizontal Expanding Down", 3, 2, {(0,1): True})
        g.addStitch(Stitch(Point((1,1),Corner.TopLeft), Point((1,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,1),Corner.BottomRight), Point((1,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1),Corner.TopLeft), Point((2,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,1),Corner.BottomRight), Point((2,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1),Corner.TopRight), Point((2,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((2,1),Corner.BottomLeft), Point((2,1), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((1,1),Corner.TopRight), Point((1,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((0,0),Corner.TopRight), Point((0,0), Corner.TopLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((0,0),Corner.TopLeft), Point((0,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,0),Corner.BottomRight), Point((0,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,0),Corner.TopLeft), Point((1,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,0),Corner.BottomRight), Point((1,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0),Corner.TopLeft), Point((2,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,0),Corner.BottomRight), Point((2,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0),Corner.TopRight), Point((2,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((2,0),Corner.BottomLeft), Point((2,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((1,0),Corner.TopRight), Point((1,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0),Corner.BottomLeft), Point((1,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,0),Corner.TopRight), Point((0,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.draw(self)

class HorizontalGoingAbove(MovingCameraScene):
    def construct(self):
        g = Grid("Horizontal Going Above", 3, 2, {(0,1): True})
        g.addStitch(Stitch(Point((0,0), Corner.TopLeft), Point((0,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,0), Corner.BottomRight), Point((0,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,0), Corner.TopLeft), Point((1,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,0), Corner.BottomRight), Point((1,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,1), Corner.BottomRight), Point((1,1), Corner.TopLeft), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,1), Corner.TopLeft), Point((1,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1), Corner.TopLeft), Point((2,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,1), Corner.BottomRight), Point((2,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1), Corner.TopRight), Point((2,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,1), Corner.BottomRight), Point((1,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,1), Corner.TopRight), Point((1,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0), Corner.TopLeft), Point((1,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0), Corner.TopLeft), Point((2,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,0), Corner.BottomRight), Point((2,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0), Corner.TopRight), Point((2,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((2,0), Corner.BottomLeft), Point((2,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((1,0), Corner.TopRight), Point((1,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0), Corner.BottomLeft), Point((1,0), Corner.TopLeft), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,0), Corner.TopRight), Point((0,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.draw(self)

class HorizontalGoingBelow(MovingCameraScene):
    def construct(self):
        g = Grid("Horizontal Going Below", 3, 2, {(0,0): True})
        g.addStitch(Stitch(Point((0,1), Corner.TopLeft), Point((0,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((0,1), Corner.BottomRight), Point((0,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,1), Corner.TopLeft), Point((1,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,1), Corner.BottomRight), Point((1,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1), Corner.TopLeft), Point((2,1), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,1), Corner.BottomRight), Point((2,1), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,1), Corner.TopRight), Point((2,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0), Corner.TopRight), Point((1,0), Corner.TopLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,0), Corner.TopLeft), Point((1,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((1,0), Corner.BottomRight), Point((1,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0), Corner.TopLeft), Point((2,0), Corner.BottomRight), StitchType.FrontOne))
        g.addStitch(Stitch(Point((2,0), Corner.BottomRight), Point((2,0), Corner.TopRight), StitchType.BackOne))
        g.addStitch(Stitch(Point((2,0), Corner.TopRight), Point((2,0), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,0), Corner.BottomRight), Point((1,0), Corner.BottomLeft), StitchType.BackOne))
        g.addStitch(Stitch(Point((1,0), Corner.BottomLeft), Point((1,0), Corner.TopRight), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((1,1), Corner.BottomRight), Point((1,1), Corner.TopRight), StitchType.BackTwo))
        g.addStitch(Stitch(Point((1,1), Corner.TopRight), Point((1,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.addStitch(Stitch(Point((0,1), Corner.BottomRight), Point((0,1), Corner.TopRight), StitchType.BackTwo))
        g.addStitch(Stitch(Point((0,1), Corner.TopRight), Point((0,1), Corner.BottomLeft), StitchType.FrontTwo))
        g.draw(self)

class HorizontalStackedLayers(MovingCameraScene):
    def construct(self):
        g = Grid("Horizontal Stacked Layers", 3, 2)
        g.addStitch(Stitch(Point))

