import subprocess
import sys
import os
import glob
import hashlib

def get_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for i in range(100):  # only read the first 100 blocks
            byte_block = f.read(4096)
            if not byte_block:
                break  # break if the file is smaller than 100 * 4K blocks
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def generate_preview(video_path):
    video_file_name = os.path.basename(video_path)
    name, ext = os.path.splitext(video_file_name)
    preview_name = f"{get_md5(video_path)}.png"
    preview_path = os.path.join("/Users/diphia/.cache/dired-preview/", preview_name)
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", "thumbnail,scale=640:-1",  
        "-frames:v", "1",
        "-threads", "4",
        preview_path
    ]
    subprocess.run(command)
    print(f"First frame preview generated: {preview_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py video_path")
        sys.exit(1)
    video_path = sys.argv[1]
    generate_preview(video_path)

if __name__ == "__main__":
    main()
