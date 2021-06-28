import cv2
import logging
from annotations_processor import bb_centroid

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 10

normalised_to_xy = lambda x, y, width, height: (int(x * width), int(y * height))

box_start = lambda box, width, height: normalised_to_xy(box['left'], box['top'], width, height)
box_end = lambda box, width, height: normalised_to_xy(box['right'], box['bottom'], width, height)

def annotate_frames(cars_frame_lookup, input_video, output_video, frame_rate, width, height):
    src = cv2.VideoCapture(input_video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    dest = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    frame_number = 0
    while(True):
        logging.debug('annotating frame #%s', frame_number)
        ret, frame = src.read()
        if ret is False: break
        for idx, car in enumerate(cars_frame_lookup):
            if frame_number in car:
                logging.debug('car #%s = %s', idx, car[frame_number])
                if (car['car_speed'] > 1):
                    frame = cv2.rectangle(frame, box_start(car[frame_number], width, height), box_end(car[frame_number], width, height), color, thickness)
                    frame = cv2.putText(frame, "car " + str(idx) + " speed: " + str(car['car_speed']) + "km/h", box_start(car[frame_number], width, height), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 4)
                    centroid = bb_centroid(car[frame_number])
                    coords = normalised_to_xy(centroid[0], centroid[1], width, height)
                    frame = cv2.circle(frame, coords, radius=10, color=(255, 255, 255), thickness=-1)

        #cv2.imshow('annotated-frame', frame)
        #cv2.waitKey(1)
        dest.write(frame)
        frame_number += 1
        print(".", end="", flush=True)

    src.release()
    dest.release()
    #cv2.destroyAllWindows()
