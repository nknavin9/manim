"""
Why is the volume of a ball (sphere) (4/3)πr³?  An explanation for class 9.

Step 1  Warm-up: cut a circle into thin pizza slices.  Each slice is almost a
        triangle of height r, so  Area = ½ × r × (edge) = ½ × r × 2πr = πr².
Step 2  Same trick in 3D: cut a ball into tiny cones with their tips at the
        centre.  Each cone has height r, so
        Volume = ⅓ × r × (surface) = ⅓ × r × 4πr² = (4/3)πr³.
Step 3  Check with water: a cone and a ball, poured into a cylinder of the same
        width and height, fill it exactly (1 part + 2 parts = 3 parts).

Render with:  manimgl sphere_volume.py SphereVolume -w
"""
from manimlib import *

FONT = "Andika"
BALL_COLOR = BLUE
CONE_COLOR = RED
CYL_COLOR = GREEN
WATER = "#4FC3F7"


def words(text, size=40, **kwargs):
    return Text(text, font=FONT, font_size=size, **kwargs)


def facing_camera(mob):
    """Turn a flat label so it stands upright in the 3D view."""
    return mob.rotate(PI / 2, RIGHT)


class SphereVolume(Scene):
    def construct(self):
        self.hook()
        self.circle_warmup()
        self.ball_into_cones()
        self.add_up_the_cones()
        self.water_check()
        self.summary()

    def caption(self, text, old=None, size=40, fixed=False):
        new = words(text, size)
        new.to_edge(UP, buff=0.4)
        if fixed:
            new.fix_in_frame()
        if old is None:
            self.play(FadeIn(new, shift=0.3 * DOWN))
        else:
            self.play(FadeOut(old, shift=0.3 * UP), FadeIn(new, shift=0.3 * UP))
        return new

    # ------------------------------------------------------------------
    def hook(self):
        frame = self.frame
        frame.reorient(-20, 70)
        R = 2.2

        ball = Sphere(radius=R, color=BALL_COLOR, opacity=0.55)
        ball.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(ball, resolution=(17, 9))
        mesh.set_stroke(WHITE, 1, opacity=0.25)
        radius = Line(ORIGIN, R * RIGHT).set_stroke(YELLOW, 5)
        dot = Dot(ORIGIN, radius=0.06).set_fill(YELLOW)
        r_label = facing_camera(Tex("r", font_size=72, color=YELLOW))
        r_label.move_to(0.5 * R * RIGHT + 0.35 * OUT)

        q = words("How much space is inside a ball of radius r?", 44)
        q.fix_in_frame().to_edge(UP, buff=0.4)

        self.play(FadeIn(q, shift=0.3 * DOWN))
        self.play(ShowCreation(ball), Write(mesh, lag_ratio=0.01), run_time=2)
        self.play(GrowFromPoint(radius, ORIGIN), FadeIn(dot), Write(r_label))
        self.play(frame.animate.reorient(25, 70), run_time=4)

        answer = Tex(R"V = \frac{4}{3}\pi r^3", font_size=80)
        answer.fix_in_frame().to_corner(DR, buff=0.6)
        book = words("Your textbook says:", 32).fix_in_frame()
        book.next_to(answer, UP, buff=0.3)
        self.play(FadeIn(book), Write(answer))
        self.wait()
        why = words("But WHY?  Where does the 4/3 come from?", 44, color=YELLOW)
        why.fix_in_frame().to_edge(UP, buff=0.4)
        self.play(FadeOut(q, shift=UP), FadeIn(why, shift=UP))
        self.wait(1.5)

        self.play(*map(FadeOut, [ball, mesh, radius, dot, r_label, why, book, answer]))
        frame.to_default_state()

        plan_title = words("Let's discover it in 3 steps", 52)
        plan = VGroup(
            words("1.  Warm-up: cut a circle into pizza slices", 38),
            words("2.  Cut the ball into tiny cones", 38),
            words("3.  Check it with water", 38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        plan_title.to_edge(UP, buff=1.2)
        plan.next_to(plan_title, DOWN, buff=0.8)
        self.play(Write(plan_title))
        self.play(LaggedStart(*(FadeIn(p, shift=0.3 * RIGHT) for p in plan), lag_ratio=0.5))
        self.wait(2)
        self.play(FadeOut(plan_title), FadeOut(plan))

    # ------------------------------------------------------------------
    def circle_warmup(self):
        r = 1.3
        N = 24
        center = 1.4 * UP
        cap = self.caption("Step 1:  Warm-up with a circle (radius r)")

        circle = Circle(radius=r).move_to(center)
        circle.set_fill(YELLOW_D, 0.8).set_stroke(WHITE, 2)
        radius = Line(center, center + r * RIGHT).set_stroke(RED, 4)
        r_label = Tex("r", font_size=40, color=RED).next_to(radius, UP, buff=0.05)
        self.play(DrawBorderThenFill(circle))
        self.play(ShowCreation(radius), Write(r_label))
        self.wait()

        slices = VGroup()
        for i in range(N):
            s = Sector(angle=TAU / N, radius=r, start_angle=i * TAU / N)
            s.shift(center)
            s.set_fill(YELLOW_D if i % 2 == 0 else ORANGE, 0.9)
            s.set_stroke(WHITE, 1)
            slices.add(s)

        cap = self.caption("Cut it into many thin slices, like a pizza", cap)
        self.remove(circle)
        self.add(slices, radius, r_label)
        self.play(
            *(s.animate.shift(0.25 * rotate_vector(RIGHT, (i + 0.5) * TAU / N))
              for i, s in enumerate(slices)),
            FadeOut(radius), FadeOut(r_label),
        )
        self.wait(0.5)

        # Each slice is (almost) a triangle
        cap = self.caption("A thin slice is almost a triangle", cap)
        one = slices[0].copy()
        big = one.copy().scale(3.0).rotate(PI / 2 - TAU / N / 2).move_to(4.5 * RIGHT + 1.2 * UP)
        tri_pts = [big.get_bottom(), big.get_corner(UR), big.get_corner(UL)]
        h_line = DashedLine(big.get_bottom(), big.get_top()).set_stroke(RED, 3)
        h_label = Tex(R"\text{height} \approx r", font_size=36, color=RED).next_to(big, RIGHT, buff=0.2)
        b_label = words("tiny piece\nof the edge", 26).next_to(big, UP, buff=0.15)
        self.play(TransformFromCopy(one, big))
        self.play(ShowCreation(h_line), Write(h_label), FadeIn(b_label))
        area_one = Tex(
            R"\text{Area of a triangle} = \frac{1}{2}\times\text{base}\times\text{height}",
            font_size=34,
        ).next_to(big, DOWN, buff=0.4).set_x(3.5)
        self.play(Write(area_one))
        self.wait(2)

        # Unroll the slices into a row
        cap = self.caption("Unroll all the slices into a row", cap)
        base_y = -2.4
        total = TAU * r
        x0 = -total / 2
        w = total / N
        triangles = VGroup()
        for i in range(N):
            left = np.array([x0 + i * w, base_y, 0])
            tri = Polygon(left, left + w * RIGHT, left + (w / 2) * RIGHT + r * UP)
            tri.match_style(slices[i])
            triangles.add(tri)
        self.play(
            FadeOut(VGroup(big, h_line, h_label, b_label, area_one)),
            LaggedStart(*(Transform(s, t) for s, t in zip(slices, triangles)), lag_ratio=0.05),
            run_time=3,
        )
        base_brace = Brace(Line(x0 * RIGHT, -x0 * RIGHT).set_y(base_y), DOWN)
        base_text = Tex(R"\text{all the bases} = \text{edge of circle} = 2\pi r", font_size=36)
        base_text.next_to(base_brace, DOWN, buff=0.15)
        h_brace = Brace(Line(base_y * UP, (base_y + r) * UP).set_x(x0), LEFT)
        h_text = Tex(R"\text{height } r", font_size=36).next_to(h_brace, LEFT, buff=0.1)
        self.play(GrowFromCenter(base_brace), Write(base_text))
        self.play(GrowFromCenter(h_brace), Write(h_text))
        self.wait()

        # Slide the tips together: same base, same height => same area
        cap = self.caption("Slide every tip to the left. Same base, same height = same area!", cap, size=34)
        apex = np.array([x0, base_y + r, 0])
        self.play(*(
            s.animate.become(
                Polygon(t.get_vertices()[0], t.get_vertices()[1], apex).match_style(s)
            )
            for s, t in zip(slices, triangles)
        ), run_time=3)
        self.wait()

        result = Tex(
            R"\text{Area of circle} = \frac{1}{2}\times 2\pi r\times r = \pi r^2",
            font_size=48,
        ).move_to(1.3 * UP)
        box = SurroundingRectangle(result, buff=0.2).set_stroke(YELLOW, 3)
        self.play(Write(result))
        self.play(ShowCreation(box))
        known = words("The formula we already know.  Now the SAME trick with a ball!", 34, color=YELLOW)
        known.next_to(box, DOWN, buff=0.35)
        self.play(FadeIn(known))
        self.wait(2.5)

        self.circle_result = VGroup(result, box)
        self.play(*map(FadeOut, [cap, slices, base_brace, base_text, h_brace, h_text, known, result, box]))

    # ------------------------------------------------------------------
    def make_pyramids(self, R, n_lon=16, n_lat=8):
        def P(u, v):
            return R * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)])

        pyramids = VGroup()
        for i in range(n_lon):
            for j in range(n_lat):
                u0, u1 = i * TAU / n_lon, (i + 1) * TAU / n_lon
                v0, v1 = j * PI / n_lat, (j + 1) * PI / n_lat
                corners = [P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)]
                corners = [
                    c for k, c in enumerate(corners)
                    if get_norm(c - corners[k - 1]) > 1e-6
                ]
                cap = Polygon(*corners)
                sides = [Polygon(ORIGIN, a, b) for a, b in adjacent_pairs(corners)]
                pyr = VGroup3D(cap, *sides)
                color = BLUE_B if (i + j) % 2 == 0 else BLUE_D
                pyr.set_fill(interpolate_color(color, BLACK, 0.35), 1).set_stroke(WHITE, 0.5, 0.5)
                cap.set_fill(color, 1)
                pyr.direction = normalize(P((u0 + u1) / 2, (v0 + v1) / 2))
                pyramids.add(pyr)
        return pyramids

    def ball_into_cones(self):
        frame = self.frame
        frame.reorient(-30, 65)
        R = 2.2
        n_lon, n_lat = 16, 8

        cap = self.caption("Step 2:  Cut the ball into tiny cones", fixed=True)
        ball = Sphere(radius=R, color=BALL_COLOR, opacity=0.9)
        ball.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(ball, resolution=(n_lon + 1, n_lat + 1))
        mesh.set_stroke(WHITE, 1.5, opacity=0.6)
        self.play(ShowCreation(ball), Write(mesh, lag_ratio=0.02), run_time=2)
        cap = self.caption("Divide its surface into many tiny patches", cap, fixed=True)
        self.wait()

        pyramids = self.make_pyramids(R, n_lon, n_lat)
        # Pick the patch that faces the camera best (slightly above the middle)
        to_cam = normalize(frame.get_implied_camera_location())
        chosen = max(
            pyramids,
            key=lambda p: np.dot(p.direction, to_cam) + 0.3 * p.direction[2],
        )
        highlight = chosen.copy().set_fill(YELLOW, 1).set_stroke(YELLOW_E, 1)
        highlight[1:].set_fill(YELLOW_E, 1)
        patch = highlight[0].copy().scale(1.06, about_point=ORIGIN)

        self.play(FadeIn(patch))
        cap = self.caption("Join the corners of one patch to the centre", cap, fixed=True)
        corners = patch.get_vertices()
        edges = VGroup(*(Line(c, ORIGIN).set_stroke(YELLOW, 3) for c in corners))
        # Make the ball see-through (keep only its grid lines)
        self.play(
            FadeOut(ball),
            mesh.animate.set_stroke(opacity=0.25),
            run_time=1,
        )
        self.play(ShowCreation(edges, lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(highlight), FadeOut(patch))

        height = DashedLine(ORIGIN, R * chosen.direction).set_stroke(RED, 4)
        h_label = facing_camera(Tex("r", font_size=72, color=RED))
        h_label.move_to(0.55 * R * chosen.direction + 0.4 * OUT)
        cap = self.caption("A tiny cone!  Its tip is at the centre and its height is r", cap, size=36, fixed=True)
        self.play(ShowCreation(height), Write(h_label))
        self.play(frame.animate.reorient(10, 70), run_time=3)
        self.wait()

        cap = self.caption("Do this for every patch...", cap, fixed=True)
        idx = list(pyramids).index(chosen)
        pyramids.replace_submobject(idx, highlight)
        highlight.direction = chosen.direction
        self.play(
            FadeOut(edges), FadeOut(height), FadeOut(h_label),
            FadeOut(mesh),
            LaggedStart(*(FadeIn(p) for p in pyramids if p is not highlight), lag_ratio=0.01),
            run_time=3,
        )
        self.add(pyramids)

        cap = self.caption("...the whole ball is made of tiny cones, all of height r", cap, size=36, fixed=True)
        frame.add_ambient_rotation(8 * DEG)
        self.play(
            *(p.animate.shift(1.0 * p.direction) for p in pyramids),
            run_time=3,
        )
        self.wait(3)
        self.play(
            *(p.animate.shift(-1.0 * p.direction) for p in pyramids),
            run_time=3,
        )
        self.wait()
        frame.clear_updaters()
        self.play(FadeOut(pyramids), FadeOut(cap))
        frame.to_default_state()

    # ------------------------------------------------------------------
    def add_up_the_cones(self):
        cap = self.caption("Now add up the volumes of all the tiny cones")

        # A small picture of one cone, tip down at the centre
        tip = 5.0 * LEFT + 1.0 * DOWN
        cone = Polygon(tip, tip + 0.8 * LEFT + 2.0 * UP, tip + 0.8 * RIGHT + 2.0 * UP)
        cone.set_fill(YELLOW, 0.8).set_stroke(YELLOW_E, 2)
        base = Ellipse(width=1.6, height=0.35).move_to(tip + 2.0 * UP)
        base.set_fill(YELLOW_B, 1).set_stroke(YELLOW_E, 2)
        h_line = DashedLine(tip, tip + 2.0 * UP).set_stroke(RED, 3)
        h_label = Tex("r", color=RED, font_size=40).next_to(h_line, RIGHT, buff=0.1).shift(0.3 * DOWN)
        base_label = words("base", 28).next_to(base, UP, buff=0.1)
        centre_label = words("centre", 26).next_to(tip, DOWN, buff=0.1)
        picture = VGroup(cone, base, h_line, h_label, base_label, centre_label)
        self.play(FadeIn(picture))

        kw = dict(font_size=40)
        lines = VGroup(
            Tex(R"\text{One tiny cone} = \frac{1}{3}\times\text{base}\times r", **kw),
            Tex(R"\text{Whole ball} = \frac{1}{3}\times r\times(\text{all the bases added up})", **kw),
            Tex(R"\text{All the bases} = \text{surface of the ball} = 4\pi r^2", **kw),
            Tex(R"\text{Whole ball} = \frac{1}{3}\times r\times 4\pi r^2 = \frac{4}{3}\pi r^3", **kw),
        )
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        lines.set_max_width(10)
        lines.next_to(picture, RIGHT, buff=0.6).shift(0.2 * DOWN)

        self.play(Write(lines[0]))
        self.wait(1.5)
        self.play(Write(lines[1]))
        self.wait(2)

        # Surface of a ball = 4 circles of radius r (class 9 string activity)
        self.play(Write(lines[2]))
        circles = VGroup(*(
            Circle(radius=0.35).set_fill(BLUE, 0.7).set_stroke(WHITE, 1)
            for _ in range(4)
        )).arrange(RIGHT, buff=0.15)
        circles.next_to(lines[2], DOWN, buff=0.15).align_to(lines[2], RIGHT)
        hint = words("= 4 circles of radius r", 26).next_to(circles, LEFT, buff=0.2)
        self.play(LaggedStartMap(GrowFromCenter, circles, lag_ratio=0.2), FadeIn(hint))
        self.wait(2)
        self.play(FadeOut(circles), FadeOut(hint))

        self.play(Write(lines[3]))
        box = SurroundingRectangle(lines[3], buff=0.15).set_stroke(YELLOW, 3)
        self.play(ShowCreation(box))
        self.wait(2)

        # Compare circle and ball side by side
        cap = self.caption("Same idea, one step up", cap)
        self.play(FadeOut(VGroup(picture, lines, box)))
        table = VGroup(
            VGroup(
                words("Circle", 40, color=YELLOW),
                words("cut into thin triangles", 30),
                Tex(R"\text{Area} = \frac{1}{2}\times r\times 2\pi r = \pi r^2", font_size=40),
                words("½ because a triangle is half a rectangle", 28, color=GREY_A),
            ).arrange(DOWN, buff=0.35),
            VGroup(
                words("Ball", 40, color=BLUE),
                words("cut into thin cones", 30),
                Tex(R"\text{Volume} = \frac{1}{3}\times r\times 4\pi r^2 = \frac{4}{3}\pi r^3", font_size=40),
                words("⅓ because a cone is a third of a cylinder", 28, color=GREY_A),
            ).arrange(DOWN, buff=0.35),
        ).arrange(RIGHT, buff=1.0).set_max_width(13)
        divider = Line(UP, DOWN).set_height(table.get_height() + 0.4).move_to(table)
        divider.set_stroke(GREY, 2)
        self.play(FadeIn(table[0], shift=RIGHT))
        self.play(ShowCreation(divider), FadeIn(table[1], shift=LEFT))
        self.wait(1.5)
        four_thirds = Tex(R"\frac{4}{3} = 4\ (\text{four circles of surface}) \times \frac{1}{3}\ (\text{cones})", font_size=40)
        four_thirds.next_to(table, DOWN, buff=0.6)
        four_thirds.set_color(YELLOW)
        self.play(Write(four_thirds))
        self.wait(4)
        self.play(FadeOut(VGroup(table, divider, four_thirds, cap)))

    # ------------------------------------------------------------------
    def water_check(self):
        r = 1.0
        floor = -3.2
        cap = self.caption("Step 3:  Check it with water!")
        sub = words("(Archimedes did this over 2000 years ago)  —  side view", 28, color=GREY_A)
        sub.next_to(cap, DOWN, buff=0.15)
        self.play(FadeIn(sub))

        # Glasses: an open cylinder, a cone (tip down) and a hollow ball
        cyl = VMobject().set_points_as_corners([
            [-r, floor + 2 * r, 0], [-r, floor, 0], [r, floor, 0], [r, floor + 2 * r, 0]
        ]).set_stroke(CYL_COLOR, 5)
        cone = VMobject().set_points_as_corners([
            [-r, 2 * r, 0], [0, 0, 0], [r, 2 * r, 0]
        ]).set_stroke(CONE_COLOR, 5)
        cone.move_to(4.5 * LEFT + (floor + r) * UP)
        ball = Circle(radius=r).set_stroke(BALL_COLOR, 5)
        ball.move_to(4.5 * RIGHT + (floor + r) * UP)

        names = VGroup(
            words("Cone", 32, color=CONE_COLOR).next_to(cone, DOWN, buff=0.2),
            words("Cylinder", 32, color=CYL_COLOR).next_to(cyl, DOWN, buff=0.2),
            words("Ball", 32, color=BALL_COLOR).next_to(ball, DOWN, buff=0.2),
        )
        self.play(LaggedStart(ShowCreation(cone), ShowCreation(cyl), ShowCreation(ball), lag_ratio=0.3))
        self.play(FadeIn(names))

        same = words("All three: width 2r and height 2r", 34).move_to(2.1 * UP)
        self.play(FadeIn(same))
        # Show the ball fits snugly inside the cylinder
        ball_home = ball.get_center().copy()
        self.play(ball.animate.move_to(cyl.get_center()), run_time=1.5)
        snug = words("The ball fits exactly inside the cylinder", 30, color=BALL_COLOR)
        snug.next_to(same, DOWN, buff=0.25)
        self.play(FadeIn(snug))
        self.wait()
        self.play(ball.animate.move_to(ball_home), FadeOut(snug), run_time=1.5)

        # Cylinder volume
        cyl_vol = Tex(R"\text{Cylinder} = \pi r^2\times 2r = 2\pi r^3", font_size=40)
        cyl_vol.move_to(same)
        self.play(FadeOut(same), Write(cyl_vol))
        self.wait()

        # Marks for thirds on the cylinder
        marks = VGroup(*(
            DashedLine([-r, floor + k * 2 * r / 3, 0], [r, floor + k * 2 * r / 3, 0]).set_stroke(WHITE, 1.5, 0.7)
            for k in (1, 2)
        ))
        mark_text = words("marked in 3 equal parts", 24, color=GREY_A).next_to(cyl, LEFT, buff=0.2)
        self.play(ShowCreation(marks), FadeIn(mark_text))

        # Water state
        cone_level = ValueTracker(0.0)   # height of water in cone (from its tip)
        ball_level = ValueTracker(0.0)   # height of water in ball (from its bottom)
        cyl_level = ValueTracker(0.0)    # height of water in cylinder

        def cone_water():
            h = max(cone_level.get_value(), 0.01)
            tip = cone.get_bottom()
            w = Polygon(tip, tip + h * UP + (h / 2) * RIGHT, tip + h * UP + (h / 2) * LEFT)
            w.set_fill(WATER, 0.85 if cone_level.get_value() > 0.01 else 0).set_stroke(width=0)
            return w

        def ball_water():
            h = max(ball_level.get_value(), 0.01)
            c = ball.get_center()
            a = np.arcsin(np.clip((h - r) / r, -1, 1))
            thetas = np.linspace(PI - a, TAU + a, 60)
            w = Polygon(*(c + r * np.array([np.cos(t), np.sin(t), 0]) for t in thetas))
            w.set_fill(WATER, 0.85 if ball_level.get_value() > 0.01 else 0).set_stroke(width=0)
            return w

        def cyl_water():
            h = max(cyl_level.get_value(), 0.01)
            w = Rectangle(2 * r, h).move_to(cyl.get_bottom(), DOWN)
            w.set_fill(WATER, 0.85 if cyl_level.get_value() > 0.01 else 0).set_stroke(width=0)
            return w

        self.add(cone_level, ball_level, cyl_level)
        waters = VGroup(always_redraw(cone_water), always_redraw(ball_water), always_redraw(cyl_water))
        self.add(waters)
        self.bring_to_front(cone, ball, cyl, marks)

        fill_text = words("Fill the cone and the ball with water", 34).move_to(2.1 * UP)
        self.play(FadeOut(cyl_vol), FadeIn(fill_text))
        self.play(cone_level.animate.set_value(2 * r), ball_level.animate.set_value(2 * r), run_time=2)
        self.wait()

        def pour(source, outlet_func, source_level, level_from_fraction, start_level, amount, label):
            """Move `source` over the cylinder and pour all its water in."""
            home = source.get_center().copy()
            self.play(source.animate.move_to(cyl.get_top() + (r + 0.5) * UP), run_time=1.5)
            t = ValueTracker(0)

            def stream():
                top = outlet_func()
                bottom = cyl.get_bottom() + cyl_level.get_value() * UP
                line = Line(top, [top[0], bottom[1], 0]).set_stroke(WATER, 8)
                on = 0.0 < t.get_value() < 1.0
                line.set_stroke(opacity=1 if on else 0)
                return line

            s = always_redraw(stream)
            self.add(s)
            self.bring_to_front(source)
            source_level.add_updater(lambda m: m.set_value(level_from_fraction(1 - t.get_value())))
            cyl_level.add_updater(lambda m: m.set_value(start_level + amount * t.get_value()))
            self.play(FadeIn(label), t.animate.set_value(1), run_time=4, rate_func=linear)
            source_level.clear_updaters()
            cyl_level.clear_updaters()
            self.remove(s)
            self.play(source.animate.move_to(home), run_time=1.5)

        def cone_level_from_fraction(f):
            # Cone volume grows like (height)³
            return 2 * r * max(f, 0) ** (1 / 3)

        def ball_level_from_fraction(f):
            # Water in a ball up to height h: h²(3r - h) / (4r³) of the ball
            lo, hi = 0.0, 2 * r
            for _ in range(40):
                mid = (lo + hi) / 2
                if mid ** 2 * (3 * r - mid) / (4 * r ** 3) < f:
                    lo = mid
                else:
                    hi = mid
            return lo

        pour_cone = words("Pour the cone into the cylinder...", 34).move_to(fill_text)
        self.play(FadeOut(fill_text))
        pour(
            cone, lambda: cone.get_bottom(), cone_level, cone_level_from_fraction,
            0.0, 2 * r / 3, pour_cone,
        )
        one_part = words("1 part", 30, color=CONE_COLOR).next_to(cyl, RIGHT, buff=0.3)
        one_part.set_y(floor + r / 3)
        self.play(FadeIn(one_part, shift=LEFT))
        self.wait()

        pour_ball = words("...now pour the ball in", 34).move_to(fill_text)
        self.play(FadeOut(pour_cone))
        pour(
            ball, lambda: ball.get_bottom(), ball_level, ball_level_from_fraction,
            2 * r / 3, 4 * r / 3, pour_ball,
        )
        two_parts = words("2 parts", 30, color=BALL_COLOR).next_to(cyl, RIGHT, buff=0.3)
        two_parts.set_y(floor + 4 * r / 3)
        self.play(FadeIn(two_parts, shift=LEFT))
        full = words("Exactly full!", 40, color=YELLOW).move_to(fill_text)
        self.play(FadeOut(pour_ball), FadeIn(full, scale=1.5))
        self.play(Flash(cyl.get_top(), color=YELLOW, flash_radius=0.8))
        self.wait()

        # Conclusion
        self.play(FadeOut(full), FadeOut(mark_text))
        eqs = VGroup(
            Tex(R"\text{Cone} + \text{Ball} = \text{Cylinder}", font_size=44),
            Tex(R"\text{Ball} = \frac{2}{3}\text{ of the cylinder}", font_size=44),
            Tex(R"= \frac{2}{3}\times 2\pi r^3 = \frac{4}{3}\pi r^3", font_size=44),
        ).arrange(DOWN, buff=0.35)
        eqs[2].align_to(eqs[1], LEFT).shift(1.3 * RIGHT)
        eqs.next_to(sub, DOWN, buff=0.4)
        for eq in eqs:
            self.play(Write(eq))
            self.wait(1)
        box = SurroundingRectangle(eqs[2], buff=0.15).set_stroke(YELLOW, 3)
        tick = words("Same answer as Step 2!", 32, color=YELLOW).next_to(box, RIGHT, buff=0.3)
        self.play(ShowCreation(box), FadeIn(tick))
        self.wait(3)

        self.play(*map(FadeOut, self.mobjects))

    # ------------------------------------------------------------------
    def summary(self):
        title = words("Why is the volume of a ball  4/3 πr³ ?", 48).to_edge(UP, buff=0.6)
        points = VGroup(
            words("•  A ball is made of lots of tiny cones, tips at the centre, height r.", 32),
            words("•  Cone volume = ⅓ × base × height, and the bases cover the surface 4πr².", 32),
            words("•  So:  ⅓ × r × 4πr²  =  4/3 πr³", 32),
            words("•  Water check: cone + ball fill a cylinder of the same size (1 : 2 : 3).", 32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        points.set_max_width(13)
        points.next_to(title, DOWN, buff=0.7)
        final = Tex(R"V = \frac{4}{3}\pi r^3", font_size=80).set_color(YELLOW)
        final.next_to(points, DOWN, buff=0.6)
        self.play(Write(title))
        for p in points:
            self.play(FadeIn(p, shift=0.3 * RIGHT))
            self.wait(1.2)
        self.play(Write(final))
        self.play(FlashAround(final, color=YELLOW))
        self.wait(4)
