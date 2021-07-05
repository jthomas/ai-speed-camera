import argparse
import json
import logging

logging.basicConfig(level=logging.INFO)

from annotations_processor import extract_cars
from video import annotate_frames

parser = argparse.ArgumentParser(description='Estimate speed of cars in video file.')

parser.add_argument('--video', help='the video file to process', required=True, type=argparse.FileType('r'))
parser.add_argument('--output', help='the processed output video file', required=True)
parser.add_argument('--annotations', help='annotation response JSON file from Google Cloud Video API', required=True, type=argparse.FileType('r'))
parser.add_argument('--distance', help='horizontal distance (metres) captured by video', required=True, type=int)
parser.add_argument('--frame-rate', help='frame rate for video file', type=int, default=30)
parser.add_argument('--width', help='width for input video file', type=int, default=1920)
parser.add_argument('--height', help='heightfor input video file', type=int, default=1080)
parser.add_argument('--min-speed', help='ignore cars travelling slower than threshold (kmph)', type=int, default=1)
parser.add_argument('--min-distance', help='ignore cars travelling  minimum relative distance across frame (0..1)', type=float, default=0)

args = parser.parse_args()

input = args.annotations.read()
results = json.loads(input)
cars_frame_lookup = extract_cars(results, args.frame_rate, args.distance, args.min_speed, args.min_distance)

annotate_frames(cars_frame_lookup, args.video.name, args.output, args.frame_rate, args.width, args.height)
