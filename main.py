import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import threading

cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://realtimeattendence-b281a-default-rtdb.firebaseio.com/"
})

def update_attendance(student_id, student_info):
    ref = db.reference(f'Students/{student_id}')
    student_info['total_attendence'] += 1
    ref.child('total_attendence').set(student_info['total_attendence'])
    ref.child('last_attendence_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Webcam width
cap.set(4, 720)   # Webcam height

# Load the background image
imgBackground = cv2.imread('Images/Background/full.jpg')

##extracting different mode 
foldermodepath='Images/state'
modepathlist=os.listdir(foldermodepath)
imgmodelist=[]
for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(foldermodepath,path)))

# print(len(imgmodelist))

#load the encoding file
file=open("Encodefile.p",'rb')
encodinglistwithroll= pickle.load(file)
file.close()
encodelist,roll_list=encodinglistwithroll
# print(roll_list)

modeType=0
counter=0
id=-1
while True:

    success, img = cap.read()
    img_scaled=cv2.resize(img,(0,0),None,0.25,0.25)
    img_scaled=cv2.cvtColor(img_scaled,cv2.COLOR_BGR2RGB)

    face_curr_frame=face_recognition.face_locations(img_scaled)
    encode_curr_frame=face_recognition.face_encodings(img_scaled,face_curr_frame)



    # Get the coordinates of the left rectangle (manually adjust these values as needed)
    x, y, w, h = 50, 140, 600, 460  # adjust accordingly
    x_mode, y_mode, w_mode, h_mode = 800, 90, 300, 500
    # Resize the webcam frame to fit into the rectangle
    img_resized = cv2.resize(img, (w, h))
    mode_img_resized = cv2.resize(imgmodelist[modeType], (w_mode, h_mode))
    # Overlay the resized webcam frame onto the background
    imgBackground[y:y+h, x:x+w] = img_resized
    imgBackground[y_mode:y_mode+h_mode, x_mode:x_mode+w_mode] = mode_img_resized
    
    
    for encodeface,facelocation in zip(encode_curr_frame,face_curr_frame):
        matches=face_recognition.compare_faces(encodelist,encodeface)
        facedis=face_recognition.face_distance(encodelist,encodeface)
        # print("matches ",matches)
        # print("face dis ",facedis)

        matchindex=np.argmin(facedis)
        if matches[matchindex]:
            id=roll_list[matchindex]
            if counter==0:
                counter=1
                modeType=1
        # else:
        #     id="NULL"
        #     if counter==0:
        #         counter=1
        #         modeType=1
    # if id=="NULL":
    #     modeType = 0
    #     counter = 0
    #     x_mode, y_mode, w_mode, h_mode = 800, 90, 300, 500
    #     mode_img_resized = cv2.resize(imgmodelist[modeType], (w_mode, h_mode))
    #     imgBackground[y_mode:y_mode + h_mode, x_mode:x_mode + w_mode] = mode_img_resized
    if counter!=0:
        if counter==1:
            studentinfo=db.reference(f'Students/{id}').get()
            print(studentinfo)
            #updating the attendence
            
            datetimeobject=datetime.strptime(studentinfo['last_attendence_time'],
                                            "%Y-%m-%d %H:%M:%S")
            
            time_second=(datetime.now()-datetimeobject).total_seconds()
            print(time_second)

            if time_second>30:
                threading.Thread(target=update_attendance, args=(id, studentinfo)).start()
            else:
                modeType=3
                counter=0
                x_mode, y_mode, w_mode, h_mode = 800, 90, 300, 500
                mode_img_resized = cv2.resize(imgmodelist[modeType], (w_mode, h_mode))
                imgBackground[y_mode:y_mode+h_mode, x_mode:x_mode+w_mode] = mode_img_resized
        if modeType!=3:

            if 10<counter<20:
                modeType=2
                x_mode, y_mode, w_mode, h_mode = 800, 90, 300, 500
                mode_img_resized = cv2.resize(imgmodelist[modeType], (w_mode, h_mode))
                imgBackground[y_mode:y_mode+h_mode, x_mode:x_mode+w_mode] = mode_img_resized

            
            if counter<=10:    
                cv2.putText(imgBackground,str(studentinfo['total_attendence']),(840,160),
                            cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                
                cv2.putText(imgBackground,str(studentinfo['major']),(945,493),
                            cv2.FONT_HERSHEY_COMPLEX,0.4,(255,255,255),1)
                
                cv2.putText(imgBackground,str(studentinfo['name']),(857,415),
                            cv2.FONT_HERSHEY_COMPLEX,1,(140,100,100),1)
                
                cv2.putText(imgBackground,str(id),(945,447),
                            cv2.FONT_HERSHEY_COMPLEX,0.4,(255,255,255),1)
                
                # cv2.putText(imgBackground,str(studentinfo['starting_year']),(845,155),
                #             cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                
                # cv2.putText(imgBackground,str(studentinfo['standing']),(845,155),
                #             cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

                # cv2.putText(imgBackground,str(studentinfo['last_attendence_time']),(945,447),
                #             cv2.FONT_HERSHEY_COMPLEX,0.4,(100,100,100),1)
                
            counter+=1
            if counter>=20:
                counter=0
                modeType=0
                studentinfo=[]
                x_mode, y_mode, w_mode, h_mode = 800, 90, 300, 500
                mode_img_resized = cv2.resize(imgmodelist[modeType], (w_mode, h_mode))
                imgBackground[y_mode:y_mode+h_mode, x_mode:x_mode+w_mode] = mode_img_resized

    # Display the result
    cv2.imshow("Attendance", imgBackground)
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
