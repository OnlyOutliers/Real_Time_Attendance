import cv2
import face_recognition
import os
import pickle


#importing students image
folderpath='Images/Students'
modepathlist=os.listdir(folderpath)
# print(modepathlist)
imglist=[]
student_roll=[]
for path in modepathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    student_roll.append(os.path.splitext(path)[0])
print(student_roll)

def findencodeing(imagelist):
    encodelist=[]
    for img in imagelist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("Encoding started....")
encodelist=findencodeing(imglist)
print("Encoding complete")

# print(encodelist)

encodelistwithroll=[encodelist,student_roll]

file=open("Encodefile.p",'wb')
pickle.dump(encodelistwithroll,file)
file.close()
print("file saved")