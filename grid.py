from enum import Enum
from manim import MovingCameraScene, Graph, Text, MovingCamera, Line, DashedLine, Create
from manim import UP, WHITE, PURPLE, GREEN, YELLOW, RED

class StitchType(Enum):
    FrontOne = 0
    FrontTwo = 1
    BackOne = 2
    BackTwo = 3
    Automatic = 4

class Corner(Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3
        
class Point:
    def __init__(self, squareId: int, corner: Corner):
        self.squareId = squareId
        self.corner = corner

class Stitch:
    def __init__(self, fro: Point, to: Point, type: StitchType):
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
            (self.corners[Corner.TopLeft], self.corners[Corner.TopRight]),
            (self.corners[Corner.TopRight], self.corners[Corner.BottomRight]),
            (self.corners[Corner.BottomRight], self.corners[Corner.BottomLeft]),
            (self.corners[Corner.BottomLeft], self.corners[Corner.TopLeft])
        ]
        self.layouts = {
            self.verticies[0]: self.corners[Corner.BottomLeft],
            self.verticies[1]: self.corners[Corner.BottomRight],
            self.verticies[2]: self.corners[Corner.TopLeft],
            self.verticies[3]: self.corners[Corner.TopRight],
        }

class Grid:
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
        g = Graph(verticies, [], layout=lt)
        scene.add(g)
        t = Text(self.title, font="Arial", color=WHITE, font_size=24).next_to(g, UP)
        scene.add(t)
        if isinstance(scene.camera, MovingCamera):
            scene.camera.auto_zoom([g,t], margin=2.0, animate=False)

        for stitch in self.stiches:
            if isinstance(stitch, Stitch):
                fromSquare = self.squares[stitch.fro.squareId]
                toSquare = self.squares[stitch.to.squareId]
                fromPoint = fromSquare.corners[stitch.fro.corner]
                toPoint = toSquare.corners[stitch.to.corner]
                if stitch.type == StitchType.Automatic:
                    raise KeyError("Stitch cannot use Automatic Stitch type")
            elif isinstance(stitch, SimpleStitch):
                square = self.squares[stitch.squareId]
                fromPoint = square.corners[stitch.fro]
                toPoint = square.corners[stitch.to]
                if stitch.type == StitchType.Automatic:
                    if stitch.fro == Corner.TopLeft and stitch.to == Corner.BottomRight:
                        stitch.type = StitchType.FrontOne
                    elif stitch.fro == Corner.BottomRight and stitch.to == Corner.TopRight:
                        stitch.type = StitchType.BackOne
                    elif stitch.fro == Corner.TopRight and stitch.to == Corner.BottomLeft:
                        stitch.type = StitchType.FrontTwo
                    elif stitch.fro == Corner.BottomLeft and stitch.to == Corner.TopLeft:
                        stitch.type = StitchType.BackTwo
                    else:
                        raise KeyError("Unable to decide which stitch to use for given SimpleStitch", stitch)
            else:
                raise KeyError("Unknown Stitch Type", stitch)
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