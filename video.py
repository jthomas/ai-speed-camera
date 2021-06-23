import numpy as np
import cv2

cap = cv2.VideoCapture('dene_road.mp4')

current_state = False
annotation_list = []

# Starting coordinate, here (100, 100)
# Represents the top left corner of rectangle
starting_point = (0, 0)

# Ending coordinate, here (400, 400)
# Represents the bottom right corner of rectangle
# w(x) x h(y)
ending_point = (1920, 1080)

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 10

video_dimensions = (1920, 1080)
width = 1920
height = 1080
#(628, 778) (918, 1015)
# Draw a rectangle with blue line borders of thickness of 2 px
left = 0.7212495
top = 0.32746944
right = 0.9405163
bottom = 0.47839144

normalised_to_xy = lambda x, y: (int(x * width), int(y * height))

box_start = lambda box: normalised_to_xy(box['left'], box['top'])
box_end = lambda box: normalised_to_xy(box['right'], box['bottom'])

#box_end = lambda box: (int(box['right'] * width), int(box['bottom'] * height))

#box_start = (int(left * width), int(top * height))
#box_end = (int(right * width), int(bottom * height))

frame_number = 0

from parse import cars, bb_centroid

cars_frame_lookup = cars()
print(len(cars_frame_lookup))

# Work out speed for cars that move from centroid of first and last frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30, (width,height))

while(True):
    print('next frame')
    ret, frame = cap.read()
    if ret is False: break
    #print(frame)
    #print((int(top * 1080), int(left * 1080)), (int(bottom * 1920), int(right * 1080)))
    #image = cv2.rectangle(frame, (int(top * 1080), int(left * 1920)), (int(bottom * 1080), int(right * 1920)), color, thickness)
    for idx, car in enumerate(cars_frame_lookup):
        if frame_number in car:
            print(frame_number, idx, car[frame_number])
            if (car['car_speed'] > 1):
                frame = cv2.rectangle(frame, box_start(car[frame_number]), box_end(car[frame_number]), color, thickness)
                frame = cv2.putText(frame, "car " + str(idx) + " speed: " + str(car['car_speed']) + "km/h", box_start(car[frame_number]), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 4)
                centroid = bb_centroid(car[frame_number])
                coords = normalised_to_xy(centroid[0], centroid[1])
                print(centroid, coords)
                frame = cv2.circle(frame, coords, radius=10, color=(255, 255, 255), thickness=-1)

    #image = cv2.rectangle(frame, box_start, box_end, color, thickness)
    cv2.imshow('annotated-frame', frame)
    cv2.waitKey(1)
    out.write(frame)
    frame_number += 1

cap.release()
out.release()
cv2.destroyAllWindows()
