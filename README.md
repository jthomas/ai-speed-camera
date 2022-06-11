
![Tests](https://github.com/jthomas/ai-speed-camera/actions/workflows/tests.yml/badge.svg)

# AI-Powered Speed Camera 🚗📸

This repository contains the source for an AI-powered digital speed camera. It can detect vehicles in video files and calculate their speeds. It will produce an annotated version of the source video where cars are labelled with their speeds. The car speed statistics can also be exported to a CSV file.

![AI Speed Camera Example](ai-speed-camera.gif)

The project uses the [Google Cloud Video AI API](https://cloud.google.com/video-intelligence) to track moving cars in video source files. API results from this service are used to calculate speeds based on a known fixed distance of video frame. [FFMPEG](https://ffmpeg.org/) is used to produce an annotated video file with cars labelled with their speeds.

*If you want to learn more about this project - please see this blog post here: https://jamesthom.as/2022/05/ai-powered-speed-camera/*

## Requirements

- Google Cloud Platform Account
- Python3 with Numpy, CV2 and tqdm libraries installed
- Source video file of cars. Video must be from a fixed position. Camera should be parallel to the road.
- Measured real-world distance covered by video frame.

## Usage

### TLDR - Run Demo
1. Install requirements via [poetry](https://pypi.org/project/poetry/)
    - `poetry install`
2. Run as below
```
# uses existing video with pre-generatated annotations from google cloud video ai api
python -m ai_speed_camera --video sample_data/dene_road.mp4 --output dest.mp4 --annotations sample_data/output.json --distance 32
```

### Process Source Video File with Cloud Video AI API

- Upload the video file to a [Google Cloud Storage Bucket](https://cloud.google.com/storage).

- Create `request.json` file with JSON file containing video file bucket name.

  ```json
  {
    "inputUri": "gs://<BUCKET_NAME>/<VIDEO_FILE>.mp4",
    "features": ["OBJECT_TRACKING"]
  }
  ```

- Send HTTP request to Google Cloud Video AI API.

  ```
  curl -X POST \
  -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @request.json \
  https://videointelligence.googleapis.com/v1/videos:annotate
  ```

- HTTP response will contain URL of the API results. Poll this URL until the results are ready.

```
https://videointelligence.googleapis.com/v1/projects/<X>/locations/<REGION>/operations/<Y>
```

- Save output from API result (when it is available) to a JSON file.

```
curl -X GET \
-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
https://videointelligence.googleapis.com/v1/projects/<X>/locations/<REGION>/operations/<Y> > results.json
```

### Run Python Script To Annotate Video

```shell
python -m ai_speed_camera --video input.mp4 --output dest.mp4 --annotations results.json --distance 32

# try it out with pregenerated annotations
python -m ai_speed_camera --video sample_data/dene_road.mp4 --output dest.mp4 --annotations sample_data/output.json --distance 32
```

The Python script to calculate speeds and annotate the video file takes the following parameters (mandatory parameters in bold).

- **` --annotations`: Video AI API output results file**
- **`--video`: Source video file (MP4 format)**
- **`--output`: Annotated video destination file (MP4 format)**
- **`--distance`: Real-world distance covered by video frame (metres)**
- `--frame-rate`: Source video frame rate (default :15)
- `--width`: Source video width (pixels - default: 1920)
- `--height`: Source video height (pixels - default: 1080)
- `--min-speed`: Ignore cars with speed lower than this value. Used to ignore fixed vehicles in frame or anomolous cars detected (kmph - default: 1).
- `--min-distance`: Ignore cars which travel less than this relative distance in the frame. Used to remove anomolous cars detected (relative distance between 0 & 1 - default: 0).
- `--export-to-csv`: Export car speed statistics to CSV file (output filename)

The Python script will produce the output below whilst running. It prints the number of cars detected in the AI API result set and the number of valid cars (in reference to minimum speeds and distances). A progress bar will be shown during the video processing stage with estimated time left.

```
INFO:root:Discovered 50 total cars in annotation response
INFO:root:Discovered 12 valid cars in annotation response: 6, 7, 11, 13, 14, 21, 24
INFO:root:Exporting valid car statistics to csv file
INFO:root:Processing source video file
100%|█████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.71it/s]
```

## Limitations

- Camera frame must be parallel to road. Code assumes cars detected are travelling along a straight horizontal line. Direction of travel does not matter.
- Car detection algorithm will produce anomalies, i.e. phantom "cars" will only exist for a short number of frames in different locations. The code attempts to strip these out by removing those with unrealistic speeds.

## Future Ideas

- Make it real-time?
- Mobile app?
- Detect other objects?
