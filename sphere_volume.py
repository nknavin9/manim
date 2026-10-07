"""
Why is the volume of a sphere (4/3)πR³?

Archimedes' argument: slice a hemisphere, a cylinder and a cone (all of
radius R and height R) at the same height h.  The hemisphere's slice has the
same area as the cylinder's slice minus the cone's slice, so by Cavalieri's
principle  V(hemisphere) = V(cylinder) - V(cone).

Render with:  manimgl sphere_volume.py SphereVolume
"""
from manimlib import *

R = 2.0
SPHERE_COLOR = BLUE
CYL_COLOR = GREEN
CONE_COLOR = RED


class SphereVolume(Scene):
    def construct(self):
        self.intro()
        self.three_solids()
        self.slice_argument()
        self.conclusion()

    # ------------------------------------------------------------------
    def intro(self):
        title = Tex(R"V_{\text{sphere}} = \frac{4}{3}\pi R^3", font_size=72)
        question = Text("...but why?", font_size=48).next_to(title, DOWN, buff=0.6)
        self.play(Write(title))
        self.play(FadeIn(question, shift=0.5 * UP))
        self.wait()

        frame = self.frame
        sphere = Sphere(radius=R, color=SPHERE_COLOR, opacity=0.8)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(17, 9), stroke_width=1, stroke_color=WHITE)
        mesh.set_stroke(opacity=0.4)
        self.play(FadeOut(title, UP), FadeOut(question, UP))
        self.play(
            frame.animate.reorient(20, 70),
            ShowCreation(sphere),
            Write(mesh, lag_ratio=0.01),
            run_time=3,
        )
        self.play(frame.animate.reorient(80, 70), run_time=4)
        idea = Text("Idea: compare a hemisphere to shapes we already know", font_size=36)
        idea.fix_in_frame().to_edge(UP)
        self.play(Write(idea))
        self.wait()
        self.play(FadeOut(Group(sphere, mesh)), FadeOut(idea))
        self.play(frame.animate.to_default_state(), run_time=0.5)

    # ------------------------------------------------------------------
    def three_solids(self):
        """2D profiles of hemisphere, cylinder, cone with radius R and height R."""
        base_y = -2.5
        centers = [LEFT * 4.5, ORIGIN, RIGHT * 4.5]
        scale = 0.9
        r = R * scale

        hemi = Arc(0, PI, radius=r).add_line_to(LEFT * r)
        hemi.set_fill(SPHERE_COLOR, 0.4).set_stroke(SPHERE_COLOR, 3)
        cyl = Rectangle(2 * r, r).set_fill(CYL_COLOR, 0.4).set_stroke(CYL_COLOR, 3)
        cyl.move_to(ORIGIN, DOWN)
        # Cone, point-down: apex at the bottom, opening of radius R at height R
        cone = Polygon(ORIGIN, r * (UP + RIGHT), r * (UP + LEFT))
        cone.set_fill(CONE_COLOR, 0.4).set_stroke(CONE_COLOR, 3)

        shapes = VGroup(hemi, cyl, cone)
        for shape, c in zip(shapes, centers):
            shape.move_to(c + base_y * UP, DOWN)
            shape.shift(UP * 1.0)

        labels = VGroup(
            Text("Hemisphere", font_size=32, color=SPHERE_COLOR),
            Text("Cylinder", font_size=32, color=CYL_COLOR),
            Text("Cone", font_size=32, color=CONE_COLOR),
        )
        for label, shape in zip(labels, shapes):
            label.next_to(shape, DOWN, buff=0.3)

        vols = VGroup(
            Tex("?", font_size=40),
            Tex(R"\pi R^2 \cdot R = \pi R^3", font_size=36),
            Tex(R"\tfrac{1}{3}\pi R^2 \cdot R = \tfrac{1}{3}\pi R^3", font_size=36),
        )
        for v, label in zip(vols, labels):
            v.next_to(label, DOWN, buff=0.25)

        header = Text("All three: radius R, height R", font_size=40).to_edge(UP)

        self.play(Write(header))
        self.play(LaggedStart(*(DrawBorderThenFill(s) for s in shapes), lag_ratio=0.3))
        self.play(LaggedStart(*(FadeIn(l, shift=0.3 * UP) for l in labels), lag_ratio=0.3))
        self.play(LaggedStart(*(Write(v) for v in vols), lag_ratio=0.4))
        self.wait(2)

        self.shapes = shapes
        self.r = r
        self.labels = labels
        self.vols = vols
        self.header = header

    # ------------------------------------------------------------------
    def slice_argument(self):
        hemi, cyl, cone = self.shapes
        r = self.r
        bottom = hemi.get_bottom()[1]

        new_header = Text("Slice all three at the same height h", font_size=40).to_edge(UP)
        self.play(FadeTransform(self.header, new_header))

        h_tracker = ValueTracker(0.6 * r)

        def slice_line(shape, half_width_func, color):
            def get():
                h = h_tracker.get_value()
                w = half_width_func(h)
                cx = shape.get_center()[0]
                y = bottom + h
                line = Line([cx - w, y, 0], [cx + w, y, 0])
                line.set_stroke(color, 6)
                return line
            return always_redraw(get)

        hemi_slice = slice_line(hemi, lambda h: np.sqrt(max(r * r - h * h, 0)), YELLOW)
        cyl_slice = slice_line(cyl, lambda h: r, YELLOW)
        cone_slice = slice_line(cone, lambda h: h, YELLOW)

        dashed = always_redraw(lambda: DashedLine(
            [-7, bottom + h_tracker.get_value(), 0],
            [7, bottom + h_tracker.get_value(), 0],
        ).set_stroke(WHITE, 1, opacity=0.5))

        self.play(ShowCreation(dashed), *(ShowCreation(s) for s in (hemi_slice, cyl_slice, cone_slice)))

        # Show the hemisphere slice's radius via Pythagoras
        cx = hemi.get_center()[0]
        center_pt = np.array([cx, bottom, 0])

        def tri():
            h = h_tracker.get_value()
            w = np.sqrt(max(r * r - h * h, 0))
            top = center_pt + h * UP
            corner = top + w * RIGHT
            return VGroup(
                Line(center_pt, top).set_stroke(WHITE, 3),
                Line(top, corner).set_stroke(YELLOW, 3),
                Line(center_pt, corner).set_stroke(TEAL, 3),
            )

        triangle = always_redraw(tri)
        tri_labels = always_redraw(lambda: VGroup(
            Tex("h", font_size=30).next_to(triangle[0], LEFT, buff=0.08),
            Tex("R", font_size=30, color=TEAL).next_to(triangle[2].get_center(), DR, buff=0.05),
        ))
        self.play(ShowCreation(triangle), FadeIn(tri_labels))
        self.play(h_tracker.animate.set_value(0.85 * r), run_time=1.5)
        self.play(h_tracker.animate.set_value(0.5 * r), run_time=1.5)

        # Slice areas
        self.play(FadeOut(self.vols), FadeOut(self.labels))
        areas = VGroup(
            Tex(R"\pi(R^2 - h^2)", font_size=38, color=SPHERE_COLOR),
            Tex(R"\pi R^2", font_size=38, color=CYL_COLOR),
            Tex(R"\pi h^2", font_size=38, color=CONE_COLOR),
        )
        for a, shape in zip(areas, self.shapes):
            a.next_to(shape, DOWN, buff=0.4)
        area_title = Text("Area of each slice (a disk):", font_size=32)
        area_title.next_to(areas, DOWN, buff=0.4)
        pyth = Tex(R"\text{radius}^2 = R^2 - h^2", font_size=32).next_to(hemi, UP, buff=0.2)

        self.play(Write(pyth))
        self.play(FadeIn(area_title), LaggedStart(*(Write(a) for a in areas), lag_ratio=0.4))
        self.wait()

        key = Tex(
            R"\pi(R^2 - h^2) = \pi R^2 - \pi h^2",
            font_size=56,
        )
        key_parts = [key[R"\pi(R^2 - h^2)"][0], key[R"\pi R^2"][0], key[R"\pi h^2"][0]]
        for part, col in zip(key_parts, [SPHERE_COLOR, CYL_COLOR, CONE_COLOR]):
            part.set_color(col)
        key.next_to(new_header, DOWN, buff=0.35)
        box = SurroundingRectangle(key, buff=0.2).set_stroke(YELLOW, 2)

        self.play(
            *(TransformFromCopy(a, k) for a, k in zip(areas, key_parts)),
            FadeIn(key["="][0]), FadeIn(key["-"][1]),
            run_time=2,
        )
        self.play(ShowCreation(box))
        note = Text("True at EVERY height h", font_size=32, color=YELLOW)
        note.next_to(box, DOWN, buff=0.15)
        self.play(FadeIn(note))

        # Sweep the slice through all heights
        self.play(h_tracker.animate.set_value(0.02 * r), run_time=2)
        self.play(h_tracker.animate.set_value(0.98 * r), run_time=3)
        self.play(h_tracker.animate.set_value(0.5 * r), run_time=1.5)
        self.wait()

        self.play(
            *map(FadeOut, [dashed, hemi_slice, cyl_slice, cone_slice, triangle,
                           tri_labels, pyth, areas, area_title, note, box, key]),
            FadeOut(new_header),
        )
        self.areas = areas

    # ------------------------------------------------------------------
    def conclusion(self):
        hemi, cyl, cone = self.shapes
        cav = Text("Same slices at every height  ⇒  same volume", font_size=36)
        cav.to_edge(UP)
        sub = Text("(Cavalieri's principle)", font_size=26, color=GREY_B).next_to(cav, DOWN, buff=0.15)
        self.play(Write(cav), FadeIn(sub))

        # Visually: cylinder with the cone carved out has the hemisphere's slices
        self.play(
            hemi.animate.set_x(-2.5),
            cyl.animate.set_x(2.5),
            FadeOut(cone),
        )
        hole = cone.copy().move_to(cyl, DOWN).set_fill(BLACK, 1).set_stroke(CONE_COLOR, 3)
        self.play(TransformFromCopy(cone, hole))
        carved_group = VGroup(cyl, hole)
        eq_sign = Tex("=", font_size=72).move_to(
            midpoint(hemi.get_right(), cyl.get_left())
        )
        minus_text = Text("cylinder minus cone", font_size=28).next_to(cyl, DOWN, buff=0.3)
        hemi_text = Text("hemisphere", font_size=28, color=SPHERE_COLOR).next_to(hemi, DOWN, buff=0.3)
        self.play(Write(eq_sign), FadeIn(minus_text), FadeIn(hemi_text))
        self.wait(2)

        self.play(*map(FadeOut, [hemi, carved_group, eq_sign, minus_text, hemi_text, sub]))

        lines = VGroup(
            Tex(R"V_{\text{hemisphere}} = V_{\text{cylinder}} - V_{\text{cone}}"),
            Tex(R"= \pi R^3 - \tfrac{1}{3}\pi R^3"),
            Tex(R"= \tfrac{2}{3}\pi R^3"),
            Tex(R"V_{\text{sphere}} = 2 \times \tfrac{2}{3}\pi R^3 = \tfrac{4}{3}\pi R^3"),
        )
        lines.arrange(DOWN, buff=0.45)
        for line in lines[1:3]:
            line.align_to(lines[0][R"="][0], LEFT)
        lines.next_to(cav, DOWN, buff=0.7)
        lines[3].shift(0.3 * DOWN)

        for line in lines:
            self.play(Write(line))
            self.wait(0.6)
        final_box = SurroundingRectangle(lines[3], buff=0.25).set_stroke(YELLOW, 3)
        self.play(ShowCreation(final_box), lines[3].animate.set_color(YELLOW))
        self.wait(3)
