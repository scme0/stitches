from enum import StrEnum
from manim import MovingCameraScene, Graph, Text, MovingCamera, Line, DashedLine, Create
from manim import UP, WHITE, PURPLE, GREEN, YELLOW, RED, GRAY
from json import dumps
from collections import namedtuple

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