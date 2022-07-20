import json, sys, matplotlib.pyplot as plt

class BoundingBox:
    def __init__(self, x_center=0, y_center=0, width=0, height=0, iou=0):
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.iou = iou


def read_lean_map_of_bboxes(input_json_file_path: str):
    try:
        with open(input_json_file_path, 'r') as json_stream: # Open the file
            raw_object = json.load(json_stream) # Load the file into a python object
        return {k: [BoundingBox(**item) for item in v] for k, v in raw_object.items()}# Unpacking the dictionary from the json file to a class object
    except Exception as e:
        print(f"{e}\nPlease check the input and run again")
        exit(0)


def get_minimum_and_maximum_height(boxes: dict, iou: int):
    input_validation(boxes, iou) # Input validation
    min_height, max_height = sys.float_info.max, sys.float_info.min # Initialize the min and max numbers in python
    for box in boxes:
        for box_details in boxes[box]: 
            if box_details.iou > iou:
                if box_details.height > max_height:
                    max_height = box_details.height # Increment the amount of iou's that bigger than the givven iou
                elif box_details.height < min_height:
                    min_height = box_details.height# Increacment the sum of the iou's that bigger than the givven iou
    return min_height, max_height


def input_validation(boxes: dict, iou: int):
    if type(boxes) is not dict or not(type(iou) is int or type(iou) is float): # Input validation
        print("Input is not of the right type\nPlease check the input and run again")
        exit(1)
   
    
def create_historgram(boxes: dict, iou_threshold: int):
    input_validation(boxes, iou_threshold) # Input validation
    bigger_ious = [] # The list of iou's that are bigger than the given iou 
    for box in boxes:
        for box_details in boxes[box]: 
            if box_details.iou > iou_threshold:
                bigger_ious.append(box_details.iou)
    plt.hist(bigger_ious, bins=100) # Create a histogram of the iou's that are bigger than the given iou
    plt.xlabel('IOU')
    plt.ylabel('Occurrences')
    plt.show()


def calculate_average_iou(boxes: dict, iou: int):
    input_validation(boxes, iou_threshold) # Input validation
    amount_of_iou = sum_of_bigger_ious = 0
    if type(boxes) is dict and (type(iou) is int or type(iou) is float): # Input validation   
        for box in boxes: 
            for box_details in boxes[box]: 
                if box_details.iou > iou:
                    amount_of_iou += 1 # Increment the amount of iou's that bigger than the givven iou
                    sum_of_bigger_ious += box_details.iou # Increacment the sum of the iou's that bigger than the givven iou
        try:
            return sum_of_bigger_ious / amount_of_iou
        except ZeroDivisionError:
            return 0


def calculate_iou_for_2_boxes(box1: BoundingBox, box2: BoundingBox):
    if type(box1) is not BoundingBox or type(box2) is not BoundingBox:
        print("Input is not of the right type\nPlease check the input and run again")
        exit(1)
    else:
        # Two points of rectangle 1 
        right_point_box1 = {"x" : box1.x_center + box1.width,
                            "y": box1.height + box1.y_center }  #                   ___(right_point_box1)
        left_point_box1 = {"x" : box1.x_center,                 #                  |   |
                            "y": box1.y_center }                # (left_point_box1)|___| 
                                                                #                                                          
        # Two points of rectangle 2                             #                   
        right_point_box2 = {"x" : box2.x_center + box2.width,   #
                            "y": box2.height + box2.y_center }  #                   ___(right_point_box2)
        left_point_box2 = {"x" : box2.x_center,                 #                  |   |
                            "y": box2.y_center }                # (left_point_box2)|___| 
        
        overlap_width = min(right_point_box1["x"], right_point_box2["x"]) - max(left_point_box1["x"], left_point_box2["x"]) # Calculate the width of the overlap between the two rectangles
        overlap_height = min(right_point_box1["y"], right_point_box2["y"]) - max(left_point_box1["y"], left_point_box2["y"]) # Calculate the height of the overlap between the two rectangles
        
        if overlap_width > 0 and overlap_height > 0: # There is overlap
            area_box1= box1.width * box1.height 
            area_box2= box2.width * box2.height
            area_overlap = overlap_width *overlap_height
            two_boxes_area = (area_box1 + area_box2) - area_overlap # Because the overlap is in both boxes
            iou = area_overlap / two_boxes_area # Calculate the iou
        else: # There is no overlap between the two rectangles 
            iou = 0 
            
        return iou         

if __name__ == '__main__':
    path_detection_boxes_json = "system_output.json" # path to system output file
    path_groundtruth_boxes_json = "Labels.json" # path to gt file
    iou_threshold = 0.5 # iou threshold for testing

    detection_boxes = read_lean_map_of_bboxes(path_detection_boxes_json) # Read the system output file can be change by user
    ground_truth_boxes = read_lean_map_of_bboxes(path_groundtruth_boxes_json) # Read the gt file can be change by user

    for name, detection_bounding_box_list in detection_boxes.items():
        ground_truth_bounding_box_list = ground_truth_boxes[name]
        for det_box in detection_bounding_box_list:
            for gt_bbox in ground_truth_bounding_box_list:
                iou = calculate_iou_for_2_boxes(det_box, gt_bbox)
                # saving the highest iou for a detection bounding box
                if iou > getattr(det_box, 'iou', 0):
                    det_box.iou = iou 
                    # print(iou)

    # calculate average iou for the boxes that pass > iou_threshold
    average_iou = calculate_average_iou(detection_boxes, iou_threshold)
    print(f"\nThe average_iou is: {average_iou}\n")

    # create histogram for the boxes that pass iou_threshold.
    # x_axis: iou, y_axis: occurrences
    create_historgram(detection_boxes, iou_threshold)


    # find the minimum and the maximum height for the boxes that pass > iou_threshold
    min_height, max_height = get_minimum_and_maximum_height(detection_boxes, iou_threshold)
    print(f"The min_height is: {min_height} and the max_height is: {max_height}")


