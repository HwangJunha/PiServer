import cv2
import numpy as np
from PIL import Image
import os
import dlib




# 이미지 경로 지정
dataset_path = 'dataset/준하/'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml");
names = ['junha']
number_images = 20

dataset_paths = ['dataset/준하/']
knownEncodings = [] 
knownNames = []

predictor_file = './model/shape_predictor_68_face_landmarks.dat'
MARGIN_RATIO = 0.5
OUTPUT_SIZE = (300, 300)
image_type = '.jpg'

predictor = dlib.shape_predictor(predictor_file)
detector2 = dlib.get_frontal_face_detector()
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
EYES = list(range(36, 48))

#/dataset의 하위 디렉터리 찾기
def search_path(path):
    filenames = os.listdir(path)
    for filename in filenames:
        full_filename = os.path.join(path, filename)
        if os.path.isdir(full_filename):
            dataset_paths.append(full_filename+'/')
            names.append(filename)

    #dataset_paths -> ['dataset/key/', 'dataset/minho/', 'dataset/suji/', ... ]

# def getFaceDimension(rect):
#     return (rect.left(), rect.top(), rect.right() - rect.left(), rect.bottom() - rect.top())

# def getCropDimension(rect, center):
#     width = (rect.right() - rect.left())
#     half_width = width // 2
#     (centerX, centerY) = center
#     startX = centerX - half_width
#     endX = centerX + half_width
#     startY = rect.top()
#     endY = rect.bottom() 
#     return (startX, endX, startY, endY)    

# def faceAlign():
    # for (i, dataset_path) in enumerate(dataset_paths):
    #     output_path = dataset_paths[i]
    #     print('-------------'+names[i]+'-------------')
        
    #     for idx in range(number_images):
    #         input_file = dataset_path + str(idx+1) + image_type
            
    #         image = cv2.imread(input_file)
    #         image_origin = image.copy()

    #         h, w, c = image.shape
            
    #         if h > 300 and w > 300: #이미 alignment된 이미지면 제외
    #             print('image alignment')
    #             (image_height, image_width) = image.shape[:2]
    #             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #             rects = detector2(gray, 1)

    #             for (i, rect) in enumerate(rects):
    #                 (x, y, w, h) = getFaceDimension(rect)
    #                 cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #                 points = np.matrix([[p.x, p.y] for p in predictor(gray, rect).parts()])
    #                 show_parts = points[EYES]

    #                 right_eye_center = np.mean(points[RIGHT_EYE], axis = 0).astype("int")
    #                 left_eye_center = np.mean(points[LEFT_EYE], axis = 0).astype("int")

    #                 eye_delta_x = right_eye_center[0,0] - left_eye_center[0,0]
    #                 eye_delta_y = right_eye_center[0,1] - left_eye_center[0,1]
    #                 degree = np.degrees(np.arctan2(eye_delta_y,eye_delta_x)) - 180

    #                 eye_distance = np.sqrt((eye_delta_x ** 2) + (eye_delta_y ** 2))
    #                 aligned_eye_distance = left_eye_center[0,0] - right_eye_center[0,0]
    #                 scale = aligned_eye_distance / eye_distance

    #                 eyes_center = ((left_eye_center[0,0] + right_eye_center[0,0]) // 2,
    #                         (left_eye_center[0,1] + right_eye_center[0,1]) // 2)
                            
    #                 metrix = cv2.getRotationMatrix2D(eyes_center, degree, scale)

    #                 warped = cv2.warpAffine(image_origin, metrix, (image_width, image_height),
    #                     flags=cv2.INTER_CUBIC)

    #                 (startX, endX, startY, endY) = getCropDimension(rect, eyes_center)

    #                 croped = warped[startY:endY, startX:endX]
    #                 output = cv2.resize(croped, OUTPUT_SIZE)
    #                 output1 = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                    
    #                 output_file = dataset_path + str(idx+1) + image_type
    #                 #cv2.imshow(output_file, output)
    #                 cv2.imwrite(output_file, output1)
    #                 # cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])



faceSamples=[]

def getImagesAndLabels(path):
    ids = []
    for (i, dataset_path) in enumerate(dataset_paths):
        index = i
        for idx in range(number_images):
            input_file = dataset_path + str(idx+1) + image_type
            PIL_img = Image.open(input_file).convert('L') 
            img_numpy = np.array(PIL_img,'uint8')
            faces = detector.detectMultiScale(img_numpy)
            print(faces)    #얼굴 몇 번 인식되었는지 확인
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(index)
    return faceSamples, ids

        
    
search_path(dataset_path)
# faceAlign()

faces, idx = getImagesAndLabels(dataset_paths)
print(idx)

recognizer.train(faces, np.array(idx))

# Save the model into trainer/trainer.yml
# recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
recognizer.save('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(idx))))
