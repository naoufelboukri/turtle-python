import turtle


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

    def draw(self):
        rows, columns = self.img.shape
        for row in range(rows):
            for column in range(columns):
                x = column - columns // 2
                y = rows // 2 - row
                self.t.penup()
                self.t.goto(x, y)
                if self.img[row, column] == 0:
                    self.t.pendown()
                    self.t.forward(1)
            self.screen.update()

        turtle.done()
