#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <input.wav> <output.wav> <time_stretch_ratio>"
  exit 1
fi

filename="$1"
new_filename="$2"
stretch_factor="$3"

if [ ! -f "$filename" ]; then
  echo "File not found: $filename, please make sure the file path contains .vaw"
  exit 1
fi

python -c "from sound_transform import time_stretch; time_stretch('$filename', '$new_filename', $stretch_factor)"