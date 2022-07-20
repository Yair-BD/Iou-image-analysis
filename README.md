# Iou-image-analysis
We want to analyze the output of two detection files (containing bounding boxes) - 1. A 
GT(ground truth) file, which contains boxes labeled by humans. These describe the real
location of the relevant objects in a frame(‘Q1_gt.tsv’).
2. A Detection file, which contains the system’s output - predicted boxes
(‘Q1_system_output.tsv’).
File Format - Sample Line:
‘image_name.png’
{
"x_center":,
"y_center":,
"width":,
"height":,
},]
