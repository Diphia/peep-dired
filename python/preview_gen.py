import subprocess
import sys
import os
import glob
import hashlib

def get_video_info(video_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=nb_frames,duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    total_frames, duration = map(float, result.stdout.split())
    return total_frames, duration

def extract_frames(video_path, frame_numbers):
    expressions = '+'.join([f'eq(n\\,{num})' for num in frame_numbers])
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"select='{expressions}'",
        "-vsync", "vfr",
        "-threads", "4",
        "/tmp/output_frame_%04d.png"
    ]
    subprocess.run(command)

def get_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def generate_preview(video_path):
    video_file_name = os.path.basename(video_path)
    name, ext = os.path.splitext(video_file_name)
    preview_name = f"{get_md5(video_path)}.png"
    preview_path = os.path.join("/Users/diphia/.cache/dired-preview/", preview_name)
    command = [
        "ffmpeg",
        "-i", "/tmp/output_frame_%04d.png",
        "-vf", "tile=2x2",
        preview_path
    ]
    subprocess.run(command)
    print(f"Preview generated: {preview_path}")

def clean_up():
    for filename in glob.glob('/tmp/output_frame_*.png'):
        os.remove(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py video_path")
        sys.exit(1)
    video_path = sys.argv[1]
    total_frames, duration = get_video_info(video_path)
    frame_interval = total_frames / 5
    frame_numbers = [int(frame_interval * i) for i in range(1, 5)]
    extract_frames(video_path, frame_numbers)
    generate_preview(video_path)
    clean_up()
