from manim import MovingCameraScene, Graph, Text, MovingCamera, Line, DashedLine, Create
from manim import UP, WHITE, PURPLE, GREEN, YELLOW, RED, GRAY

from stitching import (  # noqa: F401  (re-export for backward compatibility)
    stringify, StitchType, Corner, StitchPoint,
    Stitch, SimpleStitch, Square, Aida,
    plan_stitching,
)


def _draw(self, scene: MovingCameraScene):
    verticies = []
    edges     = []
    lt        = {}
    for square in self.squares:
        verticies.extend(square.verticies)
        edges.extend(square.edges)
        lt.update(square.layouts)
    g = Graph(verticies, edges, layout=lt,
              edge_config={"stroke_color": GRAY, "stroke_width": 1})
    scene.add(g)
    t = Text(self.title, font="Arial", color=WHITE, font_size=24).next_to(g, UP)
    scene.add(t)
    if isinstance(scene.camera, MovingCamera):
        scene.camera.auto_zoom([g, t], margin=2.0, animate=False)

    for stitch in self.stiches:
        if isinstance(stitch, Stitch):
            fromSquare = self.squares[stitch.fro[0]]
            toSquare   = self.squares[stitch.to[0]]
            fromPoint  = fromSquare.corners[stitch.fro[1]]
            toPoint    = toSquare.corners[stitch.to[1]]
            if stitch.type == StitchType.Automatic:
                raise KeyError("Stitch cannot use Automatic Stitch type",
                               stringify(stitch))
        elif isinstance(stitch, SimpleStitch):
            fro    = stitch.fro
            to     = stitch.to
            square = self.squares[stitch.squareId]
            fromPoint = square.corners[fro]
            toPoint   = square.corners[to]
            if stitch.type == StitchType.Automatic:
                if (fro == Corner.TopLeft and to == Corner.BottomRight) or \
                   (fro == Corner.BottomRight and to == Corner.TopLeft):
                    stitch.type = StitchType.FrontOne
                elif fro == Corner.BottomRight and \
                     (to == Corner.TopRight or to == Corner.BottomLeft):
                    stitch.type = StitchType.BackOne
                elif (fro == Corner.TopRight and to == Corner.BottomLeft) or \
                     (fro == Corner.BottomLeft and to == Corner.TopRight):
                    stitch.type = StitchType.FrontTwo
                elif (fro == Corner.BottomLeft or fro == Corner.TopRight) and \
                     to == Corner.TopLeft:
                    stitch.type = StitchType.BackTwo
                else:
                    raise KeyError(
                        "Unable to decide which stitch to use for given SimpleStitch",
                        stringify(stitch))
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


Aida.draw = _draw
