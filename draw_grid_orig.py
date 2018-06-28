    def draw_grid(self, amt, start, width, height, space):
        # the lines are drawn incorrectly, the horiz lines get drawn on top of
        # vertical lines

        # self.main_lines.clear()
        Color(1, 1, 1)
        # lines that are added to main_lines could be put in
        # an InstructionGroup and edited later for line spacing
        for x in range(int(amt)):
            if x % 16 == 0:
                # every 4th line is darker
                # vertical line - thick width
                # Color(.2,.2,.2)
                Color(*get_color_from_hex("#565656"))
                L = Line(points=[start, height, start, 0])
                L.width = 2.5
                self.main_lines.append(L)
            else:
                Color(.2,.2,.2)
                # vertical line - normal width
                L = Line(points=[start, height, start, 0])
                self.main_lines.append(L)
            start+=space

            Color(.2,.2,.2)
            # horizontal line
            L = Line(points=[0, start, width, start])
            self.main_lines.append(L)