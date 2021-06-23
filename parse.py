import json
import re
import functools
import math

seconds = re.compile("\d+(\.\d+)?")

def frame_to_box_lookup(frame):
    timeOffset = frame['timeOffset']
    m = time_to_seconds(timeOffset)
    if m is not None:
        seconds = float(m.group())
        frame_number = seconds_to_frame_number(seconds)
        bounding_box = frame['normalizedBoundingBox']
        return (frame_number, bounding_box)
    else: 
        return (None, None)

def merge_lookups(lookup, frame_box):
    (frame_number, bounding_box) = frame_box
    lookup[frame_number] = bounding_box
    return lookup

line_midpoint = lambda start, end: (start + end) / 2

bb_centroid = lambda bb: (line_midpoint(bb['left'], bb['right']), line_midpoint(bb['top'], bb['bottom']))

abs_distance = lambda x1, x2: math.sqrt((x2 - x1) ** 2)

mps_to_khm = lambda mps: round((mps * 3.6), 2)

car_i = 0

def calculate_speed(frames, distance = 15):
    global car_i
    print("CALCULATE_SPEED", car_i)
    start, end= frames[0], frames[-1]
    start_centroid = bb_centroid(start[1])
    end_centroid = bb_centroid(end[1])
    print('start & end centres', start_centroid, end_centroid)
    relative_distance_traveled = abs_distance(start_centroid[0], end_centroid[0])
    print('relative_distance_traveled', relative_distance_traveled, distance * relative_distance_traveled)
    time = frame_number_to_seconds(end[0]) - frame_number_to_seconds(start[0])
    print('time taken', time)
    speed = mps_to_khm((distance * relative_distance_traveled) / time)
    print('speed', speed)
    car_i += 1
    return speed

def parse_annotation(annotation):
    frames = annotation['frames']
    frame_boxes = list(map(frame_to_box_lookup, frames))
    frame_box_lookup = functools.reduce(merge_lookups, frame_boxes, {})
    frame_box_lookup['car_speed'] = calculate_speed(frame_boxes)
    return frame_box_lookup

time_to_seconds = lambda time: seconds.match(time)

seconds_to_frame_number = lambda seconds, frame_rate = 30: int(seconds * frame_rate)

frame_number_to_seconds = lambda frame_number, frame_rate = 30: frame_number / frame_rate

is_car = lambda oa: oa['entity']['description'] == 'car'

def cars():
    with open('output.json') as f:
        input = f.read()
        results = json.loads(input)
        ar = results['response']['annotationResults'][0]['objectAnnotations']
        cars = filter(is_car, ar)
        cars_frame_boxes_lookup = list(map(parse_annotation, cars))
        return cars_frame_boxes_lookup
