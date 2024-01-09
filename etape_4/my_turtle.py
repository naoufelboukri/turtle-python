import turtle
import math


def calcul_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def search_nearest_neighbor(points, current, visited):
    distances = [(point, calcul_distance(point, current)) for point in points if point not in visited]
    distances.sort(key=lambda x: x[1])
    return distances[0][0] if distances else None

class MyTurtle:
    def __init__(self, img=None):
        self.img = img
        self.t = turtle.Turtle()
        self.screen = turtle.Screen()

    def set_tracer_active(self, tracer_update):
        self.screen.tracer(tracer_update, 0)

    def set_image(self, img):
        self.img = img

    def hide_turtle(self):
        self.t.hideturtle()

    def print(self):
        rows, columns = self.img.shape

        for row in range(rows):
            for column in range(columns):
                x = column - columns // 2
                y = rows // 2 - row
                self.t.penup()
                self.t.goto(x, y)
                if self.img[row, column] == 0:
                    self.t.pendown()
                    self.t.dot(1)
            self.screen.update()

        turtle.done()

    def draw(self):
        rows, columns = self.img.shape
        points = [(row, column) for row in range(rows) for column in range(columns) if self.img[row, column] == 0]

        current_point = points[0]
        visited_points = [current_point]
        path = [current_point]

        while len(visited_points) < len(points):
            current_point = search_nearest_neighbor(points, current_point, visited_points)
            if current_point:
                visited_points.append(current_point)
                path.append(current_point)

        self.t.speed("fastest")  # Régler la vitesse de dessin à la plus rapide
        self.t.penup()  # Commencer sans dessiner
        first_point = path[0]
        self.t.goto(first_point[1] - columns // 2, rows // 2 - first_point[0])
        self.t.pendown()  # Commencer à dessiner

        for point in path:
            column = point[1]
            row = point[0]
            x = column - columns // 2
            y = rows // 2 - row
            self.t.goto(x, y)

        turtle.done()
