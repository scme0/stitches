#!/bin/zsh

if [[ $* == --push ]]; then
    git pull
fi

# remove all videos and gifs
rm -f media/videos/main/1080p60/*.mp4
rm -f animations/*.gif

# regenerate videos
manim -qh -a main.py

# regenerate gifs
for file in media/videos/main/1080p60/*.mp4; do
    name=${$(basename ${file})%.*}
    ffmpeg -i "$file" -f yuv4mpegpipe - | gifski -W 600 -o "animations/$name.gif" -
done

if [[ $* == --push ]]; then
    git lfs track animations/*.gif

    git add .gitattributes
    git add animations/*

    git commit -m "updating animation gifs"

    git push
fi