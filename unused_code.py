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