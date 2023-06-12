
# Real Time Object Detection Using Deep Learning

Object detection is a technology, combined with computer vision and deep learning, provides advance features in various fields of
automation. These computer vision and object recognition tasks enhances automatic robot machines carrying out large amount of work in a small or no time
reducing human effort.

I’ll be using YOLOv3 in this project, in particular, YOLO trained on the COCO dataset.

The YOLOv3 object detector pre-trained (on the COCO dataset) model files. These were trained by the Darknet team.

## Installation


```bash
    pip install opencv-python
    pip install numpy
    pip install PySimpleGUI
    pip install XlsxWriter
    pip install openpyxl
    pip install pyexcel
    pip install pandas
    pip install argparse
    pip install pymongo
```
    
## Screenshots
### Graphic User Interface 

![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/Screenshot%20(28).png?raw=true)

![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/Screenshot%20(31).png?raw=true)


![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/Screenshot%20(35).png?raw=true)


## Database Server

![App Screenshot](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgiacsoXajIMdRDuY-AECAZk-zoA9Bi2wHQjV3H3XVxAP0F3P-BCqd9BgA51rGG619whs&usqp=CAU)

Store all current Detection Data on database server


![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/Screenshot%20(40).png?raw=true)

## Auto Capture System and Motion Detection

Every movement of object will be get capture by system it works only for single object. Store capture image in image folder.


![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/Screenshot%20(41).png?raw=true)



## To Run the project
```
python try5.py

```
## Limitation

### Arguably the largest limitation and drawback of the YOLO object detector is that:
It does not always handle small objects well
It especially does not handle objects grouped close together
The reason for this limitation is due to the YOLO algorithm itself:
The YOLO object detector divides an input image into an SxS grid where each cell in the grid predicts only a single object. If there exist multiple, small objects in a single cell then YOLO will be unable to detect them, ultimately leading to missed object detections. Therefore, if you know your dataset consists of many small objects grouped close together then you should not use the YOLO object detector.

In terms of small objects, Faster R-CNN tends to work the best; however, it’s also the slowest.

SSDs can also be used here; however, SSDs can also struggle with smaller objects (but not as much as YOLO).

SSDs often give a nice tradeoff in terms of speed and accuracy as well.


## Screenshots

![App Screenshot](https://github.com/NikhilDasgupta123/Real-Time-Object-Detection-System-Using-Deep-Learning/blob/main/Screenshots/75d3fd1f-1610-4183-8131-7950dcd56518.jpg?raw=true)


Just follow☝️ me and Star⭐ my repository
