import cv2
import numpy as np

# capturing video through webcam
cap = cv2.VideoCapture(0)
while 1:
    _, img = cap.read()
    # converting frame(img i.e BGR)to HSV(hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining the range of red
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # defining the range of blue
    blue_lower = np.array([99, 115, 150], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # defining the range of yellow
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # finding the range of red,blue and yellow color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # morpological transformation,Dilation
    kernal = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernal)
    res = cv2.bitwise_and(img, img, mask=red)

    blue = cv2.dilate(blue, kernal)
    res1 = cv2.bitwise_and(img, img, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    res2 = cv2.bitwise_and(img, img, mask=yellow)

    # tracking the red color
    (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "RED color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

            # tracking the blue
    (contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Blue color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

            # tracking the yellow1
    (contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "yellow color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

            # cv2.imshow("Redcolor",red)
            cv2.imshow("Color Tracking ", img)
            # cv2.imshow("red",res)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break

            import datetime
            import imutils
            import time
            import cv2

            # if the video arg is none,then we r reading frm webcam
            camera = cv2.VideoCapture(0)
            time.sleep(0.25)

            # otherwise,we r reading frm vdo file
            # initialize the first frame in the vdo stream
            firstFrame = None
            i = 0
            t_data = ""
            min_area = 500
            while True:
                # grab the current frame and initialize the occupied/unoccupied
                # text
                (grabbed, frame) = camera.read()
                text = "not detected"

                # if the frame could not be grabed,then we hav reached the end
                # of the vdo
                if not grabbed:
                    break

                # resize the frame,convert it to grayscale,and blur it
                frame = imutils.resize(frame, width=500)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                # time.sleep(1)

                # if the first frame is none,initialize it
                if firstFrame is None:
                    firstFrame = gray
                    continue
                # compute the absolute difference betnnthe current frame and
                # first frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
                # dilate the thresholded img tofill in holes, then find contours
                # on thresholded img
                thresh = cv2.dilate(thresh, None, iterations=2)
                (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # loop over the contours
                for c in cnts:
                    # if the contour is too small ignr it
                    if cv2.contourArea(c) < min_area:
                        continue
                    # compute the bounding box for the contour draw it on frame
                    # & update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w + y + h), (0, 255, 0), 2)
                    text = "Detected"
                    t_data = datetime.datetime.now()
                    f = open("time.txt", "a+")
                    f.write(str(t_data) + "\n")  # str()converts to string
                    f.close()
                    cv2.imwrite('detect' + str(i) + '.png', frame)
                    time.sleep(0.5)
                    i = i + 1
                    # draw the text and timestamp on the frame
                    cv2.putText(frame, "Motion:{}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.putText(frame, datetime.datetime.now().strftime("%A%d%B%Y%l:%M:%S%P"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    # show the frame nd record if the user presses key
                    cv2.imshow("Security Feed", frame)
                    # cv2.imshow("Thresh",thresh)
                    # cv2.imshow("frame delta",frameDelta)
                    key = cv2.waitKey(1) & 0xFF

                    # if d 'q' key is pressed, brk from the lop
                    if key == ord("q"):
                        break

                        # cleanup the camera and close any opn windows
                    camera.release()
                    cv2.destroyAllWindows()
