import json
import pathlib

from ai_speed_camera.annotations_processor import extract_cars
from ai_speed_camera.video import annotate_frames

SAMPLE_DIR = pathlib.Path(__file__).absolute().parent.parent / "sample_data"


def test_main():
    """
    Runs example from README

    No assertions, just checking no errors for code coverage
    """
    cars_frame_lookup = extract_cars(
        annotations_response=json.load(open(SAMPLE_DIR / "output.json")),
        frame_rate=15,
        distance=32,
        min_speed=1,
        min_rdt=0,
    )

    annotate_frames(
        cars_frame_lookup=cars_frame_lookup,
        input_video=str(SAMPLE_DIR / "dene_road.mp4"),
        output_video=str(SAMPLE_DIR / "dest.mp4"),
        frame_rate=15,
        width=1920,
        height=1080,
    )
