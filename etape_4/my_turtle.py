import turtle
import math


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def search_nearest_neighbor(contours, ept):
    distance = []
    for contour in contours:
        distance.append(euclidean_distance(contour[0], ept))
        distance.append(euclidean_distance(contour[-1], ept))
    return distance.index(min(distance)) // 2


class MyTurtle:
    def __init__(self, img, contours):
        self.img = img
        self.contours = contours
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

    def draw(self):
        current_contour = self.draw_contour(self.contours.pop(0))
        while len(self.contours) > 0:
            current_contour = self.draw_contour(self.contours.pop(search_nearest_neighbor(self.contours, current_contour)))
            self.screen.update()
        turtle.exitonclick()

    def draw_contour(self, contour):
        if len(contour) == 1:
            return contour[0]

        self.t.penup()
        rows, columns = self.img.shape
        x = contour[0][0] - columns // 2
        y = rows // 2 - contour[0][1]
        self.t.goto(x, y)
        self.t.pendown()
        for point in contour[1:]:
            x = point[0] - columns // 2
            y = rows // 2 - point[1]
            self.t.goto(x, y)
        return point
