import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_name = input('\n enter user name end press <return> ==>  ')
path = "dataset/"+face_name+"/"

print("\n [INFO] Initializing face capture. Look the camera and wait ...")


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


createFolder(path)


# Initialize individual sampling face count
count = 0
while(True):
    ret, img = cam.read(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    count += 1
        # Save the captured image into the datasets folder
        #cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
    #cv2.imwrite(path+str(count) + ".jpg", gray[y:y+h,x:x+w])
    cv2.imwrite(path+str(count) + ".jpg", img)
    color_img = cv2.imread(path+str(count) + ".jpg")
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path+str(count) + ".jpg", gray_img)
    cv2.imshow('image', img)
    # image = path+str(count) + ".jpg"
    # img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(image, img)
    # cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 20: # Take 20 face sample and stop video
        break



# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
