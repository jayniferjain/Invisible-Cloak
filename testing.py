import numpy as np 
import cv2

import time
# this library is required to give some time prior to camera to setup before the code is executed

cap = cv2.VideoCapture(0) # creatinng an object of VideoCapture class in cv2 library

time.sleep(2) # When the camera starts initially the camera o/p is very dark and it improves with time, so i've provided 2 secs of time for camera to adjust itself according to the environment

background = 0 # a variable which contains background image that will be displayed when cloak is pull

# To capture the background 30 times 
for i in range(30):
	ret, background = cap.read()

# This condition means till the capture object isopen or running, this while loop will be executing
while(cap.isOpened()):

	ret, img = cap.read()

	if not ret:
		break

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	# HSV values
	lower_red = np.array([0, 120, 70])
	upper_red = np.array([10, 255, 255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red) # Separating the cloak part

	lower_red = np.array([170, 120, 70])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv, lower_red, upper_red)

	mask1 = mask1 + mask2 # After this any shade of red in the screen will be segmented and stored in mask1

	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,
							np.ones((3,3), np.uint8), iterations=2) # Noise Removal

	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,
							np.ones((3,3), np.uint8), iterations=1) # To provide smoothness of image

	mask2 = cv2.bitwise_not(mask1) # Except the cloak

	res1 = cv2.bitwise_and(background, background, mask=mask1) # Used for segmentation of the color
	res2 = cv2.bitwise_and(img, img, mask=mask2) # Used to substitue the cloak part
	final_output = cv2.addWeighted(res1, 1, res2, 1, 0) # alpha = 1, bita = 1, gamma = 0

	cv2.imshow("Invisible Cloak", final_output)
	k = cv2.waitKey(10)
	if k == 27:
		break


cap.release()
cap.destroyAllWindows()