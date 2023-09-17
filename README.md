# Introduction

This simple Python script allows you to get the average shot length of a video file through FFmpeg's scene change detection. It could be helpful to anyone studying film!

# Prerequisites

1. Install [FFmpeg](https://ffmpeg.org/download.html) and place it on your PATH.
2. Install [Python](https://www.python.org/downloads/).

# Instructions

1. Clone or download the repo.
2. Place a video file in the root directory of the repo.
3. Open `average_shot_length.py` in a code editor.
4. Change the `input_video` variable to the name of your video file.
5. Run the script.
6. Check the cut timings printed by the script against the actual cut timings in the video, and adjust `scene_change_detection_score` if necessary.

# Notes

Using machine learning to detect scene changes may be more accurate, but I haven't looked into this method yet.
