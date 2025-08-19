from manim import *

# Manim CE 0.17+
# Usage examples (from your shell):
#   manim -pqh rnn_bahdanau_attention.py EncoderSetup
#    ffmpeg -i media/videos/rnn_bahdanau_attention/1080p60/EncoderSetup.mp4 \
#       -vf "fps=15,scale=600:-1:flags=lanczos" \
#       -loop 0 /Users/lukesprangers/repos/lsprangers.github.io/static/img/RNNEncoderSetup.gif
       
#   manim -pqh rnn_bahdanau_attention.py DecoderSetup
#   manim -pqh rnn_bahdanau_attention.py Seq2SeqAttentionDiagram
# Replace -pqh with -pqk/-pql for higher quality.

# ------------------------------
# Helper builders
# ------------------------------

def token_box(label: str, width=1.2, height=0.6):
    r = RoundedRectangle(corner_radius=0.1, width=width, height=height)
    t = MathTex(label)
    g = VGroup(r, t)
    t.move_to(r.get_center())
    return g


def rnn_cell(label: str, width=1.2, height=0.8):
    r = RoundedRectangle(corner_radius=0.1, width=width, height=height)
    t = Text(label, font_size=24)
    g = VGroup(r, t)
    t.move_to(r.get_center())
    return g


def tiny_box(tex: str):
    r = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.5)
    t = MathTex(tex)
    g = VGroup(r, t)
    t.move_to(r.get_center())
    return g


def annotation_box(tex: str, width=1.3, height=0.6):
    r = RoundedRectangle(corner_radius=0.1, width=width, height=height)
    r.set_stroke(width=2)
    t = MathTex(tex)
    g = VGroup(r, t)
    t.move_to(r.get_center())
    return g


class EncoderSetup(Scene):
    def construct(self):
        title = Text("Encoder (BiRNN)", font_size=48, weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # input x boxes
        xs = VGroup(*[Square(side_length=0.8).set_stroke(WHITE).set_fill(BLACK,0).add(MathTex(f"x_{i}", font_size=28)) for i in range(5)])
        xs.arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=1)

        # RNN cells
        rnns = VGroup(*[Rectangle(width=1.4, height=0.8).set_stroke(WHITE).set_fill(BLACK,0).add(Text("RNN", font_size=24)) for _ in range(5)])
        for r, x in zip(rnns, xs):
            r.next_to(x, UP, buff=1)

        # hidden states h
        hs = VGroup(*[Rectangle(width=1, height=0.6).set_stroke(WHITE).set_fill(BLACK,0).add(MathTex(f"h_{{{i}}}", font_size=28)) for i in range(5)])
        for h, r in zip(hs, rnns):
            h.next_to(r, UP, buff=1)

        # connections x->rnn->h
        arrows_x_rnn = VGroup(*[Arrow(x.get_top(), r.get_bottom(), buff=0.1) for x, r in zip(xs, rnns)])
        arrows_rnn_h = VGroup()
        for i, (r, h, x) in enumerate(zip(rnns, hs, xs)):
            arrow = Arrow(r.get_top(), h.get_bottom(), buff=0.1)
            arrows_rnn_h.add(arrow)

        # forward arrows and labels (rightward pass)
        forward_arrows = VGroup()
        forward_labels = VGroup()
        forward_up_arrows = VGroup()
        forward_up_labels = VGroup()
        for i in range(4):
            right_arrow = Arrow(rnns[i].get_right(), rnns[i+1].get_left(), buff=0.1)
            forward_arrows.add(right_arrow)
                    
        for i in range(5):
            up_arrow = Arrow(rnns[i].get_top(), hs[i].get_bottom(), buff=0.1)
            forward_up_arrows.add(up_arrow)
            if i == 0:
                hidden_state = '[START]'
            else:
                hidden_state = rf'h_{{{i-1}}}'
            up_label = MathTex(rf"\overrightarrow{{h_{{{i}}}}} = f(x_{{{i}}}, {hidden_state})", font_size=18)
            up_label.next_to(up_arrow, RIGHT, buff=0.1)
            forward_up_labels.add(up_label)

        # backward arrows and labels (leftward pass)
        backward_arrows = VGroup()
        backward_labels = VGroup()
        backward_up_arrows = VGroup()
        backward_up_labels = VGroup()
        
        for i in range(4,0,-1):
            left_arrow = Arrow(rnns[i].get_left(), rnns[i-1].get_right(), buff=0.1)
            backward_arrows.add(left_arrow)
                    
        for i in range(4,-1,-1):
            up_arrow = Arrow(rnns[i].get_top(), hs[i].get_bottom(), buff=0.1)
            backward_up_arrows.add(up_arrow)
            if i == 4:
                hidden_state = '[START]'
            else:
                hidden_state = rf'h_{{{i+1}}}'
            up_label = MathTex(rf"\overleftarrow{{h_{{{i}}}}} = f(x_{{{i}}}, {hidden_state})", font_size=18)
            up_label.next_to(up_arrow, LEFT, buff=0.1)
            backward_up_labels.add(up_label)

        # final concatenation equation
        eq = MathTex(r"h_j = [\overrightarrow{h_j}; \overleftarrow{h_j}]", font_size=36)
        eq.next_to(title, DOWN, buff=0.5)

        # Animate
        self.play(FadeIn(xs))
        self.play(FadeIn(rnns))
        self.play(FadeIn(hs))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_x_rnn], lag_ratio=0.2))

        # Forward pass
        self.play(LaggedStart(*[GrowArrow(a) for a in forward_arrows], lag_ratio=0.3))
        self.play(Write(forward_labels))
        self.wait(1)
        self.play(FadeOut(forward_labels))
        self.play(LaggedStart(*[GrowArrow(a) for a in forward_up_arrows], lag_ratio=0.3))
        self.play(Write(forward_up_labels))
        self.wait(1)
        # remove forward arrows and labels
        self.play(FadeOut(forward_arrows), FadeOut(forward_up_arrows), FadeOut(forward_up_labels))

        # Backward pass
        self.play(LaggedStart(*[GrowArrow(a) for a in backward_arrows], lag_ratio=0.3))
        self.play(Write(backward_labels))
        self.wait(1)
        self.play(FadeOut(backward_labels))
        self.play(LaggedStart(*[GrowArrow(a) for a in backward_up_arrows], lag_ratio=0.3))
        self.play(Write(backward_up_labels))
        # self.play(Write(forward_up_labels))
        self.wait(1)

        # Show final concatenation
        self.play(Write(eq))
        self.wait()


class DecoderSetup(Scene):
    """Shows the decoder RNN receiving previous token y_{i-1} and context c_i to produce y_i with hidden state s_i."""
    def construct(self):
        title = Text("Decoder (RNN with Attention)", weight=BOLD)
        title.to_edge(UP)

        # Previous outputs
        y_prev2 = token_box(r"y_{i-2}")
        y_prev1 = token_box(r"y_{i-1}")
        y_curr  = token_box(r"y_i")
        y_group = VGroup(y_prev2, y_prev1, y_curr).arrange(RIGHT, buff=0.6)
        y_group.to_edge(DOWN, buff=1.2)

        # Decoder cells
        s_im1 = rnn_cell("DecRNN")
        s_i   = rnn_cell("DecRNN")
        s_group = VGroup(s_im1, s_i).arrange(RIGHT, buff=1.5)
        s_group.next_to(y_group, UP, buff=1.2)

        # Hidden state labels
        s_im1_lbl = MathTex(r"s_{i-1}").scale(0.9).next_to(s_im1, UP, buff=0.2)
        s_i_lbl   = MathTex(r"s_i").scale(0.9).next_to(s_i, UP, buff=0.2)

        # Arrows y_{i-1} -> s_i, and recurrence s_{i-1} -> s_i
        a_y_to_si = Arrow(y_prev1.get_top(), s_i.get_bottom(), buff=0.05)
        a_rec     = Arrow(s_im1.get_right(), s_i.get_left(), buff=0.08)

        # Context c_i box and arrow into s_i
        c_i = tiny_box(r"c_i")
        c_i.next_to(s_i, LEFT, buff=1.2)
        a_c_to_si = Arrow(c_i.get_right(), s_i.get_left(), buff=0.08)

        # Output distribution g(y_{i-1}, s_i, c_i)
        soft = tiny_box(r"g(y_{i-1}, s_i, c_i)")
        soft.next_to(s_i, RIGHT, buff=1.2)
        a_si_to_soft = Arrow(s_i.get_right(), soft.get_left(), buff=0.08)
        y_hat = MathTex(r"p(y_i\mid y_{<i}, x)")
        y_hat.next_to(soft, RIGHT, buff=0.6)
        a_soft_to_y = Arrow(soft.get_right(), y_hat.get_left(), buff=0.08)

        self.play(FadeIn(title))
        self.play(FadeIn(y_group))
        self.play(FadeIn(s_group))
        self.play(FadeIn(s_im1_lbl), FadeIn(s_i_lbl))
        self.play(Create(a_rec), Create(a_y_to_si))
        self.play(FadeIn(c_i), Create(a_c_to_si))
        self.play(FadeIn(soft), Create(a_si_to_soft))
        self.play(FadeIn(y_hat), Create(a_soft_to_y))
        self.wait(1)


class Seq2SeqAttentionDiagram(Scene):
    """Full encoder-decoder with attention: annotations h_j, attention weights alpha_{ij}, context c_i, decoder state s_i."""
    def construct(self):
        title = Text("Seq2Seq with Bahdanau Attention", weight=BOLD)
        title.to_edge(UP)

        Tx = 6
        # Encoder annotations on top
        hs = VGroup(*[annotation_box(f"h_{{{j+1}}}") for j in range(Tx)]).arrange(RIGHT, buff=0.7)
        hs.to_edge(UP, buff=1.5)

        # Softmax( a(s_{i-1}, h_j) ) block
        score_box = tiny_box(r"e_{ij}=a(s_{i-1}, h_j)")
        softmax_box = tiny_box(r"\alpha_{ij}=\operatorname{softmax}(e_{ij})")
        score_box.next_to(hs, DOWN, buff=1.0).shift(LEFT*3)
        softmax_box.next_to(score_box, DOWN, buff=0.5)

        # Context vector box c_i
        c_i = tiny_box(r"c_i=\sum_j \alpha_{ij} h_j")
        c_i.next_to(softmax_box, DOWN, buff=0.8)

        # Decoder states at bottom
        s_im1 = rnn_cell("DecRNN")
        s_i   = rnn_cell("DecRNN")
        s_group = VGroup(s_im1, s_i).arrange(RIGHT, buff=2.0)
        s_group.to_edge(DOWN, buff=1.2)
        s_im1_lbl = MathTex(r"s_{i-1}").scale(0.9).next_to(s_im1, UP, buff=0.2)
        s_i_lbl   = MathTex(r"s_i").scale(0.9).next_to(s_i, UP, buff=0.2)

        # Attention lines from s_{i-1} to each h_j (dashed)
        att_lines = VGroup()
        for hj in hs:
            att_lines.add(DashedLine(s_im1.get_top(), hj.get_bottom(), dash_length=0.12))

        # Flow: s_{i-1} -> score -> softmax -> c_i -> s_i
        a_s_to_score = Arrow(s_im1.get_top(), score_box.get_bottom(), buff=0.05)
        a_score_to_soft = Arrow(score_box.get_bottom(), softmax_box.get_top(), buff=0.05)
        a_soft_to_c = Arrow(softmax_box.get_bottom(), c_i.get_top(), buff=0.05)
        a_c_to_si = Arrow(c_i.get_bottom(), s_i.get_top(), buff=0.05)

        # Output layer g(y_{i-1}, s_i, c_i)
        g_box = tiny_box(r"g(y_{i-1}, s_i, c_i)")
        g_box.next_to(s_i, RIGHT, buff=1.2)
        a_si_to_g = Arrow(s_i.get_right(), g_box.get_left(), buff=0.05)
        y_prob = MathTex(r"p(y_i\mid y_{<i}, x)")
        y_prob.next_to(g_box, RIGHT, buff=0.6)
        a_g_to_y = Arrow(g_box.get_right(), y_prob.get_left(), buff=0.05)

        self.play(FadeIn(title))
        self.play(LaggedStart(*[FadeIn(h) for h in hs], lag_ratio=0.08))
        self.play(FadeIn(score_box), FadeIn(softmax_box), FadeIn(c_i))
        self.play(FadeIn(s_group))
        self.play(FadeIn(s_im1_lbl), FadeIn(s_i_lbl))
        self.play(Create(att_lines))
        self.play(Create(a_s_to_score), Create(a_score_to_soft), Create(a_soft_to_c), Create(a_c_to_si))
        self.play(FadeIn(g_box), Create(a_si_to_g))
        self.play(FadeIn(y_prob), Create(a_g_to_y))
        self.wait(1)
