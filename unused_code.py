    def old_check_snap_to_grid(self):
        for line in self.main_lines:
            lineX = line.points[0]
            lineY = line.points[1]
            selShapeX = self.selected_item.shape.pos[0]
            selShapeY = self.selected_item.shape.pos[1]
            # snap to vertical line within spacing px amount
            if selShapeX > lineX and selShapeX <= lineX + self.space:
                self.selected_item.shape.pos = (lineX, selShapeY)
                self.selected_item.text.pos = (self.selected_item.shape.pos[0], selShapeY)
            # snap to horizontal line within spacing px amount
            if selShapeY > lineY and selShapeY <= lineY + self.space:
                self.selected_item.shape.pos = (selShapeX, lineY)
                self.selected_item.text.pos = (self.selected_item.shape.pos[0], selShapeY)


        # def draw_grid(amt, start, width, height, space):
        #     Color(1, 1, 1)
        #     # lines that are added to main_lines could be put in
        #     # an InstructionGroup and edited later for line spacing
        #     for x in range(int(amt)):
        #         if x % 4 == 0:
        #             # every 4th line is darker
        #             # vertical line - thick width
        #             Color(.2,.2,.2)
        #             L = Line(points=[0+start, height, 0+start, 0])
        #             L.width = 2
        #             self.main_lines.append(L)
        #         else:
        #             Color(.2,.2,.2)
        #             # vertical line - normal width
        #             L = Line(points=[0+start, height, 0+start, 0])
        #             self.main_lines.append(L)
        #         start+=space

        #         Color(.2,.2,.2)
        #         # horizontal line
        #         L = Line(points=[0, start, width, start])
        #         self.main_lines.append(L)