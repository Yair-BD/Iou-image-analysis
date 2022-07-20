# Iou-image-analysis
I want to analyze the output of two detection files

1. Labels file, which contains boxes labeled by humans. These describe the real
location of the relevant objects in a frame.

2. A Detection file, which contains the system’s output - predicted boxes

Files Format:

‘image_name.png’
  - "x_center":,
  - "y_center":,
  - "width":,
  - "height":,
  
# The Pipeline methods:
Calculate iou for 2 boxes
- Takes 2 boxes as input and returns the calculation of the intersection over union between the 2 Boxes

Calculate average iou :
- Returns the average IoU of all the boxes that pass the givven iou_threshold.

Create historgram :
  - x_axis: iou that pass the givven 
  - iou_threshold , y_axis: occurrences

Get minimum and maximum height:
- Return the minimum height and the maximum height of all the boxes
that pass the givven iou_threshold. 
