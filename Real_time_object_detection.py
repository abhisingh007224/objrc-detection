from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np 
import argparse,imutils,cv2,time 


ap=argparse.ArgumentParser()
ap.add_argument("-p","--prototxt", required=True,
	help="path to caffe deploy prototxt file")
ap.add_argument("-m","--model", required=True,
	help="path to caffe pretrained model")
ap.add_argument("-c","--confidence",default=0.2,type=float,
	help="min confidence to filter weak detections")

args=vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS=np.random.uniform(0,255,size=(len(CLASSES),3))

print("[INFO] loading models")
net=cv2.dnn.readNetFromCaffe(args["prototxt"],args["model"])

print("[Info] starting video stream")

vs=VideoStream(src=0).start()
time.sleep(2.0)
fps=FPS().start()

while True:
	frame=vs.read()

	frame=imutils.resize(frame,width=400)

	(h,w)=frame.shape[:2]
	blob=cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),
		0.007843, (300, 300), 127.5)

	net.setInput(blob)
	detections=net.forward()

	for i in np.arange(0,detections.shape[2]):

		confidence=detections[0,0,i,2]

		if confidence>args["confidence"]:
			idx= int(detections[0,0,i,1])
			box=detections[0,0,i,3:7] * np.array([w,h,w,h])

			(startX,startY,endX,endY)=box.astype("int")

			label="{} : {:.2f}%".format(CLASSES[idx],confidence*100)

			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	cv2.imshow("frame",frame)
	key=cv2.waitKey(1) & 0xFF

	if key ==ord("q"):
		break

	fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


































