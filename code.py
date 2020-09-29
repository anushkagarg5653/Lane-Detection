import numpy as np
import cv2

'''image_path = r"D:\Projects\Lane-Detection\Images\test_image.jpg"
image = cv2.imread(image_path)
copy_image = np.copy(image)'''

def make_coord(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5)) 
    x1 = int((y1 - intercept)/slope) 
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])
  



def average_slope_int(image, lines):
    left_fit= []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2= line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1) 
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else: 
            right_fit.append((slope, intercept))
    left_fit_avg = np.average(left_fit, axis = 0)
    right_fit_avg = np.average(right_fit, axis = 0)
    left_line = make_coord(image, left_fit_avg)
    right_line = make_coord(image, right_fit_avg)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
    blur_image = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur_image, 50,150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None: 
       for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image 

def region_of_int(image):
    height = image.shape[0] 
    polygons = np.array([
    [(200,height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask) 
    return masked_image


'''c1 = canny(copy_image)
cropped_image = region_of_int(c1)
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 5)
averaged_lines = average_slope_int(copy_image, lines)
line_image = display_lines(copy_image, averaged_lines)
combo_image = cv2.addWeighted(copy_image, 0.8, line_image, 1, 1)
cv2.imshow("result", combo_image)
cv2.waitKey(0)'''

capture = cv2.VideoCapture(r"D:\Projects\Lane-detection\Lane-Detection\test2.mp4")
while(capture.isOpened()):
    ret, frame = capture.read()
    if ret == True:
        c1 = canny(frame)
        cropped_image = region_of_int(c1)
        lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=5)
        averaged_lines = average_slope_int(frame, lines)
        line_image = display_lines(frame, averaged_lines)
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        cv2.imshow("result", combo_image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
capture.release()
cv2.destroyAllWindows()