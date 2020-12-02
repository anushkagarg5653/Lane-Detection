import os
import streamlit as st
import cv2
from PIL import Image 
import numpy as np
import tempfile
import warnings


warnings.filterwarnings("ignore")

@st.cache
def grayscale(new_img):

	img_array = np.array(new_img.convert('RGB'))

	image =  cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

	return image

@st.cache
def gaussian_blur(new_img):

	grayscaled = grayscale(new_img)
	blur = cv2.GaussianBlur(grayscaled , (5,5), 0)
	return blur

@st.cache
def canny(new_img , min = 50, max = 120):
    
    canny0 = gaussian_blur(new_img)
    canny = cv2.Canny(canny0 ,min , max)
    
    return canny

@st.cache
def region_of_interest_masked_for_video(new_img):

	image =  cv2.cvtColor(new_img, cv2.COLOR_RGB2GRAY)
	blur = cv2.GaussianBlur(image , (5,5), 0)
	canny = cv2.Canny(blur ,40 , 120)
	height = canny.shape[0]
	polygons = np.array([[(200, height),(1100 , height), (550 , 250)]])  #Creating a triangular mask

	mask = np.zeros_like(canny)  #Black pixels

	cv2.fillPoly(mask , polygons , 255) #Fill mask with triangle dimensions as white(255)

	mask = cv2.bitwise_and(canny , mask)

	return mask

@st.cache
def region_of_interest_masked(new_img):
	
	image = canny(new_img , 50 , 120)
	height = image.shape[0]
	polygons = np.array([[(200, height),(1100 , height), (550 , 250)]])  #Creating a triangular mask

	mask = np.zeros_like(image)  #Black pixels

	cv2.fillPoly(mask , polygons , 255) #Fill mask with triangle dimensions as white(255)

	mask = cv2.bitwise_and(image , mask)

	return mask

def display_lines(image, lines):
    
    line_image = np.zeros_like(image)
    
    if lines is not None:
        
        for line in lines:
            
            x1 , y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1) ,(x2,y2), (255,0,0), 10)
               
    return line_image

def make_cordinates(image , line_parameters):
    
    try:
    	slope , intercept = line_parameters    
    except TypeError:
    	slope , intercept = 0.01 , 0.0

    y1 = image.shape[0]
    
    y2  = int(y1*(0.49))
    
    x1 = int((y1 - intercept)/slope)
    
    x2 = int((y2 - intercept)/slope)
    
    return np.array([x1, y1 , x2 , y2])

def average_slope_intercept(image , lines):
    
    left_fit = []
    right_fit = []
    
    for line in lines:
        
        x1, y1 , x2 , y2 = line.reshape(4)
        
        parameters = np.polyfit((x1 , x2), (y1, y2), 1)
        
        slope = parameters[0]
        
        intercept = parameters[1]
        
        if slope < 0:
            
            left_fit.append((slope , intercept))
        else:
            
            right_fit.append((slope , intercept))
            
    left_fit_average = np.average(left_fit , axis = 0)
    right_fit_average = np.average(right_fit , axis = 0)
        
    left_line = make_cordinates(image , left_fit_average)
        
    right_line = make_cordinates(image , right_fit_average)
    
    return np.array([left_line , right_line])


#######################################CODE#####################################################################

st.set_option('deprecation.showfileUploaderEncoding', False)
#st.title("Lane Detection")

html_temp = """
			<body style= "background-color:lightblue;">
			<div style = "background-color:lightblue;padding:10px">
			<h2 style = "color:white;text-align:center;">Lane Detection</h2>
			</div>
			</body>
			"""

#st.markdown(bg , unsafe_allow_html = True)
st.markdown(html_temp , unsafe_allow_html = True)
st.markdown('## Enter desired image')

st.markdown('### Select what result you would like to see')



    
    #st.image(our_image, width = 800)

activities = ['Select Image' , 'Select Video']

choice = st.selectbox('Choose what transformation you would like to see ' , activities)

if choice == 'Select Image':

	image_file = st.file_uploader("Choose an image...", type=["jpeg","jpg","png"])

	if image_file is not None:

		our_image = Image.open(image_file)

		st.text('Original Image')

	options = ['Original','Grayscaling','Gaussian Blur' ,
				'Cannyedge','Masked Image' , 'Final Image']

	types = st.selectbox('Choose What would you like to see', options)

	if types == 'Original':
		
		st.write('Here is your original image - ')

		st.image(our_image, width = 800, caption = 'Fig.')
		st.success('Done!')

	elif types == 'Grayscaling':

		
		st.write('Here is your grayscaled image - ')
		gray_scaled_image =  grayscale(our_image)

		st.image(gray_scaled_image, width = 800, caption = 'Fig.')
		st.success('Done!')

	elif types == 'Gaussian Blur':

		st.write('Here is your Gaussian Blurred image - ')
		gaussian_blurred_image = gaussian_blur(our_image)

		st.image(gaussian_blurred_image, width = 800, caption = 'Fig.')
		st.success('Done!')

	elif types == 'Cannyedge':

		st.write('Pass the Parameters -')
		st.text('Preferably between 40 & 200')
		min_reso = st.number_input('Enter minimum :')
		max_reso = st.number_input('Enter maximum :')

		st.write('Here is your image after performing Canny Edge Detection -')
		cannied_image = canny(our_image , min_reso , max_reso)

		st.image(cannied_image, width = 800, caption = 'Fig.')
		st.success('Done!')

	elif types == 'Masked Image':

		st.write('Here is your masked image -')
		masked_image = region_of_interest_masked(our_image)

		st.image(masked_image , width = 800 , caption = 'Fig.')
		st.success('Done!')
		

	elif types == 'Final Image':

		st.write('Voila! Here is your final image detecting lanes!')

		lane_image = np.copy(our_image) 

		masked_image = region_of_interest_masked(our_image)

		lines = cv2.HoughLinesP(masked_image , 2 , (np.pi)/180 , 100 , np.array([]), minLineLength = 40 , maxLineGap = 5)

		averaged_lines = average_slope_intercept(lane_image , lines)

		line_image = display_lines(our_image , averaged_lines)
		combo_image = cv2.addWeighted(lane_image , 0.8, line_image , 1, 1)

		st.image(combo_image , width = 800 , caption = 'Fig.')
		st.success('Done!')
		st.balloons()

elif choice == 'Select Video':

	video_file = st.file_uploader("Choose a video...", type="mp4")

	if video_file is not None:

		#our_image = Image.open(image_file)

		st.video(video_file)

	tfile = tempfile.NamedTemporaryFile(delete=False) 
	tfile.write(video_file.read())


	vf = cv2.VideoCapture(tfile.name)

	stframe = st.empty()

	while vf.isOpened():
	    ret, frame = vf.read()
	    # if frame is read correctly ret is True
	    if not ret:
	        
	        break
	    
	    masked_image = region_of_interest_masked_for_video(frame)
	    lines = cv2.HoughLinesP(masked_image , 2 , np.pi/180 , 100 , np.array([]), minLineLength = 40 , maxLineGap = 5)
	    averaged_lines = average_slope_intercept(frame , lines)

	    line_image = display_lines(frame, averaged_lines)

	    combo_image = cv2.addWeighted(frame , 0.8, line_image , 1, 1)

	    stframe.image(combo_image, width = 800)


	vf.release()
	
	st.write('Done!')
	st.balloons()