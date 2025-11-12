## Manim
Getting manim to work here was great for GIFs!

## Requirements
- `conda install manim`
- `brew install --cask mactex`
- `brew instal ffmpeg`

Activate env:
```
conda activate my-manim-environment
```

Run manim:
```
manim -pql manim/rnn_attention_demo.py RNNSeq2SeqAttention
```

Converting to GIF (use relative output path):
```
ffmpeg -i media/videos/<manim_filename>/480p15/SquareToCircle.mp4 \
       -vf "fps=15,scale=600:-1:flags=lanczos" \
       -loop 0 static/img/SquareToCircle.gif

ffmpeg -i media/videos/vector_scaling_demo/480p15/VectorScalingDemo.mp4 \
       -vf "fps=15,scale=600:-1:flags=lanczos" \
       -loop 0 static/img/VectorScalingDemo.gif
```

Embed in Markdown:
![Vector Scaling Demo](../static/img/VectorScalingDemo.gif)

### Troubleshooting
- "No such file or directory" when writing GIF usually means the output path root doesn't match your username. Use `static/img/...` relative path instead of an absolute `/Users/...`.
- Ensure the source MP4 path exists (render with `-pql` first to get low-quality quick preview).
- If colors look off, add `-pix_fmt rgb24` before `-loop 0`.
- To change size, adjust `scale=600:-1` (first number is width, `-1` preserves aspect ratio).