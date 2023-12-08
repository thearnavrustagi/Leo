cd mappings
ffmpeg \
  -framerate 2 \
  -pattern_type glob \
  -i '*.png' \
  -vf scale=512:-1 \
  out.gif;
cd ..
scp -r mappings satvik@172.20.10.2:~/Desktop/result
