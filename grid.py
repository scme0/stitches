from enum import Enum
from manim import MovingCameraScene, Graph, Text, MovingCamera, Line, DashedLine, Create
from manim import UP, WHITE, PURPLE, GREEN, YELLOW, RED

class StitchType(Enum):
    FrontOne = 0
    FrontTwo = 1
    BackOne = 2
    BackTwo = 3

class Corner(Enum):
    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3
        
class Point:
    def __init__(self, square: tuple[int, int], corner: Corner):
        self.square = square
        self.corner = corner

class Stitch:
    def __init__(self, fro: Point, to: Point, type: StitchType):
        self.fro = fro
        self.to = to
        self.type = type

class Square:
    def __init__(self, x: int, y: int, visible: bool, count: int):
        self.visible = visible
        self.x = x
        self.y = y
        self.layouts = {}
        self.verticies = []
        self.corners = {
            Corner.TopLeft: [x-.5, y+.5, 0],
            Corner.TopRight: [x+.5, y+.5, 0],
            Corner.BottomLeft: [x-.5, y-.5, 0],
            Corner.BottomRight: [x+.5, y-.5, 0],
        }
        if visible:
            self.verticies = [
                (count*4),
                1+(count*4),
                2+(count*4),
                3+(count*4),
            ]
            self.layouts = {
                self.verticies[0]: self.corners[Corner.BottomLeft],
                self.verticies[1]: self.corners[Corner.BottomRight],
                self.verticies[2]: self.corners[Corner.TopLeft],
                self.verticies[3]: self.corners[Corner.TopRight],
            }
        print("layout:", self.layouts, "count:", count)

class Grid:
    def __init__(self, title: str, x: int, y: int, disabled = {}):
        self.title = title
        self.x = x
        self.y = y
        self.disabled = disabled
        self.squares = {}
        self.stiches: list[Stitch] = []
        for xIdx in range(self.x):
            for yIdx in range(self.y):
                print("check", xIdx, yIdx)
                self.squares[(xIdx,yIdx)] = Square(xIdx, yIdx, not self.disabled.get((xIdx,yIdx), False), len(self.squares))
    
    def addStitch(self, stitch: Stitch):
        self.stiches.append(stitch)
    
    def draw(self, scene: MovingCameraScene):
        verticies = []
        lt = {}
        for square in self.squares.values():
            if square.visible:
                print("hell yeah")
                verticies.extend(square.verticies)
                lt.update(square.layouts)
        print("verts:", verticies)
        print("layout:", lt)
        g = Graph(verticies, [], layout=lt)
        scene.add(g)
        t = Text(self.title, font="Arial", color=WHITE, font_size=24).next_to(g, UP)
        scene.add(t)
        if isinstance(scene.camera, MovingCamera):
            scene.camera.auto_zoom([g,t], margin=2.0, animate=False)

        for stitch in self.stiches:
            fromSquare = self.squares[stitch.fro.square]
            toSquare = self.squares[stitch.to.square]
            fromPoint = fromSquare.corners[stitch.fro.corner]
            toPoint = toSquare.corners[stitch.to.corner]
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