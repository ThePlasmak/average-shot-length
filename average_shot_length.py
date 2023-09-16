import subprocess

input_video = "example.mp4"
scene_change_detection_score = 0.15  # adjust for each video. Increase to make the detection less sensitive, reducing number of shots detected and increasing ASL


def extract_timestamps(output):
    timestamps = []
    lines = output.split("\n")
    for line in lines:
        if "showinfo" in line:
            start_idx = line.find("pts_time:") + len("pts_time:")
            end_idx = start_idx
            while end_idx < len(line) and (
                line[end_idx].isdigit() or line[end_idx] == "."
            ):
                end_idx += 1
            extracted_value = line[start_idx:end_idx]
            if extracted_value:  # Check if the extracted value is non-empty
                try:
                    timestamp = float(extracted_value)
                    timestamps.append(timestamp)
                except ValueError:
                    print(f"Failed to convert '{extracted_value}' to float.")
    return timestamps


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    seconds = int(remaining_seconds)
    frames = int((remaining_seconds - seconds) * FRAME_RATE)
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"


def get_frame_rate(video_file):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_file,
    ]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    frame_rate_str = result.stdout.strip()
    numerator, denominator = map(int, frame_rate_str.split("/"))
    return numerator / denominator


FRAME_RATE = get_frame_rate(input_video)

# Run ffmpeg command to detect shots and capture its output
ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_video,
    "-vf",
    f"select='gt(scene,{scene_change_detection_score})',showinfo",
    "-f",
    "null",
    "-",
]
result = subprocess.run(
    ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
output = result.stderr

# Extract timestamps from the output
shot_times = extract_timestamps(output)

# Format and print the cut times
formatted_cut_times = [format_time(time) for time in shot_times]
print(f"Cut times (HH:MM:SS:FF): {formatted_cut_times}")

# Calculate ASL
number_of_shots = len(shot_times)
total_duration = shot_times[-1]  # Assuming the last timestamp is the end of the video

asl = total_duration / number_of_shots
print(f"Average Shot Length: {asl} seconds")
