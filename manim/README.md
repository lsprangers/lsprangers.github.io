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

Converting to GIF:
```
ffmpeg -i media/videos/<manim_filename>/480p15/SquareToCircle.mp4 \
       -vf "fps=15,scale=600:-1:flags=lanczos" \
       -loop 0 /Users/lukesprangers/repos/lsprangers.github.io/static/img/SquareToCircle.gif
```

Embed in Markdown:
![Square to Circle](../static/img/SquareToCircle.gif)