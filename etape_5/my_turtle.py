import turtle
import math
from sklearn.cluster import KMeans
import cv2
import numpy as np  

def color_image(image, contours):
    number_of_clusters = 10
    pixel_tab = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=number_of_clusters, n_init=1)
    kmeans.fit(pixel_tab)
    strong_colors = kmeans.cluster_centers_.astype(int)
    for i, _ in enumerate(pixel_tab):
        pixel_tab[i] = strong_colors[kmeans.labels_[i]]
    image_reshape = pixel_tab.reshape(image.shape)
    masks = [np.zeros(image.shape[:2], dtype=np.uint8) for x in contours]
    for i, ctr in enumerate(contours):
        cv2.fillPoly(masks[i], [ctr], 255)
    for i, mask in enumerate(masks):
        x, y = contours[i][0]  
        image_reshape[np.where(mask == 255)] = tuple(strong_colors[kmeans.labels_[y * image.shape[1] + x]])
    result = [[] for _ in range(10)]
    for y in range(image_reshape.shape[1]):
        for x in range(image_reshape.shape[0]):
            for i in range(len(strong_colors)):
                if strong_colors[i][0] == image_reshape[x][y][0] and strong_colors[i][1] == image_reshape[x][y][1] and strong_colors[i][2] == image_reshape[x][y][2]:
                    result[i].append([[x,y],image_reshape[x,y]])
                    break
    return result

def normalize_color(color):
    return tuple(component / 255 for component in color)

def color_normalized(color):
    color = tuple(int(max(0, min(255, c))) for c in color)
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def search_nearest_neighbor(contours, ept):
    distance = []
    for contour in contours:
        distance.append(euclidean_distance(contour[0], ept))
        distance.append(euclidean_distance(contour[-1], ept))
    return distance.index(min(distance)) // 2


def search_nearest_neighbor_background(points, ept):
    crayon = []
    last_point =  None
    i = 0
    while i < len(points):
        distance = euclidean_distance(points[i][0], ept[0])
        if distance <= 20:
            last_point = points[i]          
            crayon.append(last_point)
            points.pop(i)
        else:
            i = i + 1
    if last_point != None:
        points.append(last_point)        
    return crayon, points



class MyTurtle:
    def __init__(self, img, contours):
        self.img = img
        self.contours = contours
        self.t = turtle.Turtle()
        self.screen = turtle.Screen()

    def set_tracer_active(self, tracer_update):
        self.screen.tracer(0, tracer_update)

    def set_image(self, img):
        self.img = img

    def hide_turtle(self):
        self.t.hideturtle()

    def print(self,original_image):
        rows, columns = self.img.shape
        for row in range(rows):
            for column in range(columns):
                x = column - columns // 2
                y = rows // 2 - row
                self.t.penup()
                self.t.goto(x, y)
                if self.img[row, column] == 0:
                    self.t.pendown()
                    original_color = color_normalized(tuple(original_image[y,x]))
                    self.t.pencolor(original_color)
                    self.t.dot(1)
            self.screen.update()

    def draw(self,original_image, formatted_contours):
        current_contour = self.draw_contour(self.contours.pop(0),original_image)
        background =  color_image(original_image,formatted_contours)
        while len(self.contours) > 0:
            current_contour = self.draw_contour(self.contours.pop(search_nearest_neighbor(self.contours, current_contour)), original_image)
            self.screen.update()       
        self.draw_background(background)
        turtle.exitonclick()

    def draw_contour(self, contour, original_image):
        if len(contour) == 1:
            return contour[0]
        self.t.penup()
        rows, columns = self.img.shape
        x = contour[0][0] - columns // 2
        y = rows // 2 - contour[0][1]
        self.t.goto(x, y)
        self.t.pendown()
        original_color = color_normalized(tuple(original_image[contour[0][1],contour[0][0]]))
        self.t.pencolor(original_color)
        for point in contour[1:]:
            x = point[0] - columns // 2
            y = rows // 2 - point[1]
            self.t.goto(x, y)
        return point

    def draw_background(self, background):
        rows, columns = self.img.shape
        for i in range(len(background)):
            actual_background = background[i]
            index = 0
            current_point = actual_background[index]
            while len(actual_background) > 0:            
               y = current_point[0][1] - columns // 2
               x = rows // 2 - current_point[0][0]
               self.screen.update() 
               self.t.goto(y, x)
               self.t.pendown()
               original_color = color_normalized(tuple(current_point[1]))
               self.t.pencolor(original_color)
               self.t.forward(1)
               self.t.penup()
               crayon , actual_background = search_nearest_neighbor_background(actual_background,actual_background.pop(index))
               for j in range(len(crayon)-1) :
                   current_point = crayon[j]
                   y = current_point[0][1] - columns // 2
                   x = rows // 2 - current_point[0][0]
                   self.t.goto(y, x)
                   self.t.pendown()
                   self.t.forward(1)
                   self.t.penup()
               index = len(actual_background)-1
               if len(actual_background) > 0:
                   current_point = actual_background[index]  
    
