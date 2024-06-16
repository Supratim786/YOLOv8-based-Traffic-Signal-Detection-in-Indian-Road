from ultralytics import YOLO
import cv2
import math
import mysql.connector as mysql
from datetime import datetime
import time
from tkinter import *
import keyboard

# mydb = mysql.connect(host="localhost", port=3306, user="root", passwd="root", database="project")
# if(mydb): 
#     print("Connection to DataBase Successful") 
# else: 
#     print("Connection to DataBase Unsuccessful") 
# mycursor=mydb.cursor(buffered=True) 
# flag=0
# gpsvalue=0

gpsvalue='0'
cap=cv2.VideoCapture(0)
model=YOLO("C:\\Users\\USER\Desktop\\Jadavpur University\\Thesis Study\\yolov8_train_1\\kaggle\\working\\runs\\detect\\train\\weights\\best.pt")
classNames = ['Green Left','Green Right','Green Straight','Red','Yellow']
root = Tk()
root.title("Signal Detection")
root.geometry("900x600")
l=Label(root,text="Welcome to Traffic Signal Detection", borderwidth=10, fg="black", bg="yellow",relief=GROOVE)
l.grid(row=0, column=1)
while (True):
    # def getvals():
    #     global gpsvalue
    #     gpsvalue=a1.get()   
    success, img=cap.read()
    results=model(img,stream=True)
    for r in results:
        boxes=r.boxes
        for box in boxes:
            x1,y1,x2,y2=box.xyxy[0]
            x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
            conf=math.ceil((box.conf[0]*100))/100
            cls=int(box.cls[0])
            class_name=classNames[cls]
            label=f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            if class_name == "Red":
                def getvals():
                    global gpsvalue
                    gpsvalue=a1.get() 
                color=(0, 204, 255)
                print("Red Signal, stop the car !!!")
                print(conf)
                theLabel=Label(root,text="Red Signal, stop the car !!!")
                theLabel.update()
                theLabel.grid()
                a1=StringVar()
                a11=Entry(root, textvariable=a1).grid()
                
                #keyboard.wait('enter')
                if gpsvalue=='1':
                    print("Vehicle has stopped.....")
                    gpsvalue='0'
                    time.sleep(5)
                else:
                    # mycursor.execute("SET time_zone = '+05:30';")
                    # mycursor.execute("Insert into timedetails values(now());")
                    # mycursor.execute("Insert into defaulters Select * from (select S_id,OwnerName, Model_No, Model_Name, Phn_No, D_License, CarLicense, Penalty, Charges, Time from RTO,FineDetails,timedetails where S_id=4 and Penalty='Signal Disobey') as T ;")
                    # mycursor.execute("Truncate table timedetails;")
                    # mydb.commit()
                    pass
                time.sleep(5)
            elif class_name == "Yellow":
                color = (222, 82, 175)
                print("Yellow Signal, please slow down....")
                print(conf)
                theLabel=Label(root,text="Yellow Signal, please slow down.... ")
                theLabel.update()
                theLabel.grid()
                time.sleep(0)    
            elif class_name == "Green Left" or "Green Right" or "Green Straight":
                color = (0, 149, 255)
                print('Green Signal, you can go.....')
                print(conf)
                theLabel=Label(root,text="Green Signal, you can go.....")
                theLabel.update()
                theLabel.grid()
                time.sleep(0)

            if conf>0.25:
                cv2.rectangle(img, (x1,y1), (x2,y2), color,3)
                cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
    
    if cv2.waitKey(1) & 0xFF==ord('1'):
        break
cv2.destroyAllWindows()
root.mainloop()
