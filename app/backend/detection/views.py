from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import glob
import numpy as np
import cv2

from animal_detection.app.backend.breed_detection.settings import PERSISTENCE_PATH
from animal_detection.detect.detect_objects import execute as execute_detection

DETECTIONS_PATH = os.path.join(PERSISTENCE_PATH, 'detections')

def get_new_detection_id():
    if not os.path.exists(DETECTIONS_PATH):
        os.makedirs(DETECTIONS_PATH)
    
    existing_detections = glob.glob(os.path.join(DETECTIONS_PATH, '*'))
    detections_ids = sorted([int(os.path.basename(d)) for d in existing_detections])
    if (len(detections_ids) > 0):
        detection_id = detections_ids[-1] + 1
    else:
        detection_id = 1
    return detection_id

@csrf_exempt
def run_detection(request):
    if request.method == 'POST':  
        # TODO parametrize (in frontend and backend) the threshold and the amount of boxes to draw  
        detection_id = get_new_detection_id()
        detection_path = os.path.join(DETECTIONS_PATH, str(detection_id))
        os.makedirs(detection_path)
        
        if not(request.FILES) or not('image' in request.FILES):
            return JsonResponse({"error": 'no image provided'}, status=400)
        
        file = request.FILES['image']
        file_ext = os.path.splitext(file.name)[1]
        original_file_path = os.path.join(detection_path, 'original_image' + file_ext)
        detections_data_path = os.path.join(detection_path, 'detections_data.npy')
        result_image_path = os.path.join(detection_path, 'result_image' + file_ext)
        
        with open(original_file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        detections, result_img = execute_detection(original_file_path)
        np.save(detections_data_path, detections)
        cv2.imwrite(result_image_path, result_img)
        
        return JsonResponse({"dir": PERSISTENCE_PATH}, status=200)
    
# todo for kursach:

# change github repo link!!

# /detection/run
# 	run detection on specified image that we send

# /detection/run-again

# /detection/history
# 	get overview list of all detections that were executed

# /detection/detail/:id

# /detection/delete/:id

# detections are persisted in detections/ folder
# each detection looks like this

# 15 (folder)
# 	result_img.jpg
# 	detection_data.npy
# 	original_img.jpg


