import cv2
import numpy as np
import time
import imutils
import time
import os
import PySimpleGUI as sg
import xlsxwriter
from openpyxl import Workbook
import datetime
import pyexcel
from pyexcel_xls import get_data
import json
import pandas as pd
import requests
import json
import imutils
import argparse
from collections import deque
import pyttsx3
import pymongo


def main():
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    db=client['Objects']
    collection=db['sample']
    db2=client['Images']
    collection2=db2['sample2']
    
    engine = pyttsx3.init()
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=32,help="max buffer size")
    args = vars(ap.parse_args())
    
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""

    sg.theme('Black')
    df1 = pd.read_excel('detections.xlsx')
    table_detections = pd.DataFrame(df1)
    values = table_detections.values.tolist()
    toprow = ['Object','Time']
    table_detections.reset_index(inplace=True)
    table_detections_dict=table_detections.to_dict("records")
    collection.insert_many(table_detections_dict)
    
    df2 = pd.read_csv('Time_of_movements.csv')
    table_movements = pd.DataFrame(df2)
    values2 = table_movements.values.tolist()
    toprow2 = ['','Initial','Final','Start','End']
    

    # df2=pd.read_csv('Time_of_movements.csv')
    # table_Time_of_movements = pd.DataFrame(df2)
    # values2 = table_Time_of_movements.values.tolist()
    # define the window layout
    file_types = [("JPEG (*.jpg)", "*.jpg"),("All files (*.*)", "*.*")]
    layout_column = [[sg.Text("View Image File"),sg.FileBrowse(file_types=file_types),],[sg.Text('Object Detection', size=(100, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='',key='image')],
              [sg.Button('Record', size=(10, 1),font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Capture', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14')],[sg.Table(values = values, headings=toprow,auto_size_columns=True,col_widths=list, expand_x=True,expand_y=True,justification='center')],
               [sg.Table(values = values2, headings=toprow2,auto_size_columns=True,col_widths=list, justification='center')]]

    static_back = None
    motion_list = [ None, None ]
    time = []
    df = pd.DataFrame(columns = ["Initial", "Final"])

    layout = [[sg.Column(layout_column, element_justification='center')]]
    

    # create the window and show it without the plot
    window = sg.Window('Object Detection',layout, location=(1000, 600),finalize=True)
    # window = sg.Window('Window Title', layout, no_titlebar=True, location=(0,0), size=(800,600), keep_on_top=True)
    window.maximize()

    # Load the YOLO model
    net = cv2.dnn.readNet('yolov3_training_last.weights','yolov3_testing.cfg')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    layer_names = net.getLayerNames()
    #Determine the output layer names from the YOLO model
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    cap = cv2.VideoCapture(0)
    recording = False
    font = cv2.FONT_HERSHEY_SIMPLEX
    # starting_time = time.time()
    frame_id = 0

    book = Workbook()
    sheet = book.active
    i=0
    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Record':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
        
        elif event=='Capture':
            recording = True
            # cv2.imwrite(filename='saved_img.jpg', img=frame)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join('C:/Users/Nikhil/Desktop/ObjectDetect/image',f"image{timestamp}.png")
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE))
            # frame.release()
            # img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            # img_new = cv2.imshow("Captured Image", img_new)
            # cv2.waitKey(1650)
            


        if recording:
            # ret, frame = cap.read()
            # imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            # window['image'].update(data=imgbytes)
            _, frame = cap.read()
            motion=0
            frame_id += 1
            height, width, channels = frame.shape
            cnt=1
            # fg_mask = back_sub.apply(frame)

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

            net.setInput(blob)
            outs = net.forward(output_layers)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            if static_back is None:
                static_back = gray
                continue

            # Visualising data
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.1:
                        # Object detected
                        time_ref = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                        sheet.append((classes[class_id], time_ref ))
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        motion = 1
                        

            
            book.save('detections.xlsx')
            
            
            
            

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.10, 0.5)
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    percent = str(round(confidence, 2)*100) + "%"
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + percent, (x, y-5), font, 1/2, color, 2)
                    x2 = x + int(w/2)
                    y2 = y + int(h/2)
                    (dirX, dirY) = ("", "")
                    if  np.abs(x2) > 300:
                        dirX = "Left" if (x2) == 2 else "Right"
                    if np.abs(y2) > 300:
                        dirY = "Up" if np.sign(dY) == 2 else "Down"
                    if dirX != "" and dirY != "":
                        direction = "{}-{}".format(dirY, dirX)
                    else:
                        direction = dirX if dirX != "" else dirY
                    cv2.circle(frame,(x2,y2),4,(0,255,0),-1)
                    text = "x: " + str(x2) + ", y: " + str(y2)
                    cv2.putText(frame, text, (x2 - 10, y2 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 3)
              
            

            motion_list.append(motion)       
            motion_list = motion_list[-2:]  
             # Appending Start time of motion
            if motion_list[-1] == 1 and motion_list[-2] == 0:
                time.append(datetime.datetime.now())
                cv2.imwrite('C:/Users/Nikhil/Desktop/ObjectDetect/image/Frame'+str(i)+'.jpg', frame)
                i += 1
                engine.say("Movement has been detected")
                engine.runAndWait()

            # Appending End time of motion
            if motion_list[-1] == 0 and motion_list[-2] == 1:
                time.append(datetime.datetime.now())
                cv2.imwrite('C:/Users/Nikhil/Desktop/ObjectDetect/image/Frame'+str(i)+'.jpg', frame)
                i += 1
                engine.say("Movement has been detected")
                engine.runAndWait()

            key = cv2.waitKey(1)
            # if q entered whole process will stop
            if key == ord('q'):
            # if something is movingthen it append the end time of movement
                if motion == 1:
                    time.append(datetime.datetime.now())
                    cv2.imwrite('C:/Users/Nikhil/Desktop/ObjectDetect/image/Frame'+str(i)+'.jpg', frame)
                    i += 1
                engine.say("Movement has been detected")
                engine.runAndWait()

                break
            
            for i in range(0, len(time), 2):
                df = df.append({"Start":time[i], "End":time[i]}, ignore_index = True)
            df.to_csv("Time_of_movements.csv")
            # elapsed_time = time.time() - starting_time
            # fps = frame_id / elapsed_time
            # cv2.putText(frame, "FPS: " + str(round(fps, 2)), (40, 670), font, .7, (0, 255, 255), 1)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  
            window['image'].update(data=imgbytes)
            # elapsed_time = time.time() - starting_time
            # fps = frame_id / elapsed_time
            # cv2.putText(frame, "FPS: " + str(round(fps, 2)), (40, 670), font, .7, (0, 255, 255), 1)
            # imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            # window['image'].update(data=imgbytes)

        

main()