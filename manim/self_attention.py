from manim import *

class RNNWithAttention(Scene):
    def construct(self):
        # Input sentence
        words = ["I", "love", "machine", "learning"]
        word_mobs = [Text(w).scale(0.7) for w in words]
        word_boxes = [SurroundingRectangle(w, color=BLUE) for w in word_mobs]

        # Arrange words horizontally
        word_group = VGroup(*[VGroup(box, mob) for box, mob in zip(word_boxes, word_mobs)]).arrange(RIGHT, buff=0.7)
        self.play(*[FadeIn(mob) for mob in word_mobs], *[Create(box) for box in word_boxes])
        self.wait(0.5)

        # Encoder RNN hidden states
        h_states = [Circle(radius=0.3, color=GREEN).next_to(box, DOWN, buff=0.7) for box in word_boxes]
        h_labels = [MathTex(f"h_{i+1}").scale(0.7).move_to(h.get_center()) for i, h in enumerate(h_states)]
        for h, l in zip(h_states, h_labels):
            self.play(Create(h), FadeIn(l), run_time=0.3)
        self.wait(0.5)

        # Draw arrows from words to hidden states (encoding)
        for box, h in zip(word_boxes, h_states):
            arr = Arrow(box.get_bottom(), h.get_top(), buff=0.05, color=YELLOW)
            self.play(Create(arr), run_time=0.2)
        self.wait(0.5)

        # Decoder hidden state
        decoder = Circle(radius=0.4, color=RED).shift(DOWN*2.5 + RIGHT*2)
        decoder_label = MathTex("s_t").scale(0.8).move_to(decoder.get_center())
        self.play(Create(decoder), FadeIn(decoder_label))
        self.wait(0.5)

        # Attention arrows (from decoder to all encoder hidden states)
        attn_arrows = []
        for h in h_states:
            arr = CurvedArrow(decoder.get_top(), h.get_bottom(), angle=-PI/2, color=ORANGE)
            attn_arrows.append(arr)
            self.play(Create(arr), run_time=0.2)
        self.wait(0.5)

        # Context vector
        context = Rectangle(width=0.7, height=0.4, color=PURPLE).next_to(decoder, RIGHT, buff=0.7)
        context_label = MathTex("c_t").scale(0.7).move_to(context.get_center())
        self.play(Create(context), FadeIn(context_label))
        self.wait(0.5)

        # Arrow from attention to context
        self.play(Create(Arrow(decoder.get_right(), context.get_left(), buff=0.05, color=PURPLE)))
        self.wait(0.5)

        # Decoder output (predicted word)
        output_word = Text("output: 'AI'").scale(0.7).next_to(context, RIGHT, buff=0.7)
        self.play(Write(output_word))
        self.wait(1.5)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])
