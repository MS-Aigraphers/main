
def check_crossing_line(prev_bboxes, curr_bboxes, line_y):
    crossed_above_to_below = False
    crossed_below_to_above = False
    
    for prev_bbox, curr_bbox in zip(prev_bboxes, curr_bboxes):
        prev_x1, prev_y1, prev_x2, prev_y2, prev_label = prev_bbox
        curr_x1, curr_y1, curr_x2, curr_y2, curr_label = curr_bbox
        
        if prev_label == 0 and curr_label == 0:  # Check only for objects with label 0
            prev_center_y = (prev_y1 + prev_y2) / 2
            curr_center_y = (curr_y1 + curr_y2) / 2
            
            # Check if the object crosses the line from above to below
            if prev_center_y < line_y and curr_center_y >= line_y:
                crossed_above_to_below = True
            
            # Check if the object crosses the line from below to above
            if prev_center_y > line_y and curr_center_y <= line_y:
                crossed_below_to_above = True
    
    return crossed_above_to_below, crossed_below_to_above
