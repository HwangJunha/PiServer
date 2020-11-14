import cv2
import numpy as np
import os
import DoorLockBluetooth
import time

import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def faceReStart(client_socket_doorLock):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    names = []

    known = 0
    unknown = 0
    knownChk = False;
    unknownChk = False;

    #iniciate id counter
    def search_path(path):
        filenames = os.listdir(path)
        for filename in filenames:
            full_filename = os.path.join(path, filename)
            if os.path.isdir(full_filename):
                names.append(filename)
    def send_mail():
        msg = MIMEMultipart('alternative')
        s = smtplib.SMTP('smtp.gmail.com', 587)
        now = datetime.datetime.now()

        me = ''
        you = ''
        msg['From'] = me
        msg['To'] = you

        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        #TLS 보안 시작
        s.starttls()

        s.login('','')

        htmlText = """\
        <html lang="kr">

        <head>
            <meta charset="UTF-8">
            <title>Document</title>
        </head>
        <body>
            <h3>등록되지 않은 사람이 잠금 해제를 시도하였습니다.</h3>
            <p><a href="#">여기</a>를 눌러 침입자의 정보를 확인하세요.</p>
        </body>

        </html>


        """
        part1 = MIMEText(nowDatetime, 'plain') #보내는 문자열
        part2 = MIMEText(htmlText, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s.ehlo()

        msg['Subject'] = nowDatetime+' 침입자 발생 안내'

        #앞에 이메일이 보내는 이메일 뒤에 이메일이 받는 이메일
        s.sendmail(me, you, msg.as_string())

        s.quit()
    
    id = 0
    search_path("dataset/")
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:
        ret, img =cam.read()
        cam.set(cv2.CAP_PROP_EXPOSURE, 40)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match

            if (confidence < 50):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                #얼굴이 10번 인식되어야 문을 연다.
                #if문의 숫자를 늘릴수록 얼굴이 인식되어야 하는 횟수가 증가함
                if(known<10):
                    if(knownChk==False):
                        known = 0
                        knownChk = True
                    else:
                        known += 1
                        knownChk = True
                        unknownChk = False
                        print("known > ",known)
                else:
                    known = 0
                    knownChk = True
                    #인식 완료 시 코드
                    print("인식 성공")
                    DoorLockBluetooth.openDoorLock(client_socket_doorLock)
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

                #얼굴이 20번 인식되어야 특정 동작 실행
                #if문의 숫자를 늘릴수록 얼굴이 인식되어야 하는 횟수가 증가함
                if(unknown<20):
                    if(unknownChk==False):
                        unknown = 0
                        unknownChk = True
                    else:
                        unknown += 1
                        unknownChk = True
                        knownChk = False
                
                    #sleep를 길게 걸면 딜레이가 너무 심하므로 if문과 sleep을 적절히 사용할 것
                    print("unknown > ",unknown)
                else:
                    unknown = 0
                    knownChk = False
                    print("인식 실패")
                
                    send_mail()
                    #인식 실패 시 특정 동작 코드
   
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            if(unknownChk):
                cv2.putText(img, 'intruder detected!', (x-50,y+h+30), font, 1, (0,0,255), 1)
    
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
# Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()





