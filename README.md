# **Lane-Detection**
**Objective:** In this project, we'll be detecting lane lines in videos and images of roads using the Computer Vision. Following lane lines is one of the most important traffic rules, so detecting them is a significant task while building models for autonomous(self-driving) vehicles.
## Requirements:
Python version 3.7.0 <br>
opencv-python==4.4.0.42 <br>
numpy==1.19.2 <br>
matplotlib==3.3.2 <br>

## Concepts Applied
From various techniques that can be used to detect lines, we went with Canny Edge detection algorithm and Hough Transform method. 
This is our original image:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Images/test_image.jpg" width="400" height="250">
</p>
There are some pre-processing required to be done on the video/image, but the Canny edge function does that for you. They are:


### 1. Grayscaling
It is the process of converting the images from RGB,HSV etc. to shades of grey. This process helps in increasing the contrast of the lanes, to be able to distinguish them from the rest of the image. The shades vary from pitch black to some whitish-grey, depending upon the wavelength of the original color.
The resultant image will look like this:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Result%20Images/Grayscaling.jpeg" width="400" height="250">
</p>

### 2. Gaussian Blur Filter
The Gaussian blur function is applied on the grayscaled image. Its purpose is to reduce noise and irrelevant details in the image, which may hinder the process of Canny edge function.
This is what you'll get after applying the Gaussian blur:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Result%20Images/GaussianBlur.jpeg" width="400" height="250">
</p>

###  Canny Edge Function
This function actually detects the edges in the road image/video. After increasing contrast by grayscaling and suppressing noise by Gaussian blur, the lines are detected by change in gradient. It calculates the gradient all over the frame and then represents the strong gradient as one white line. We set the high and low threshold for eliminating and including the required gradients.
The image will look like this:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Result%20Images/CannyEdgeDetection.jpeg" width="400" height="250">
</p>

###  Hough Transform
The final and significant method that allows us to work only with the region of our interest(which we define using a function, and tracing it on black pixel). After tracing the region of interest we'll get the following image:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Result%20Images/FilteredCannyImage.jpeg" width="400" height="250">
</p>
The Hough Transform algorithm maps a line(in x-y plane) as a point(in Hough space) and and a single point(in x-y plane) as a family of lines(in Hough Space).
(For deeper understnding behind the Hough Algorithm, check out - https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549) 
Thus, Hough transform returns us the lines having consistently aligned points, that are edges of our defined region of interest. It also detects curves, circles, etc, based on the same logic. 


After applying all the above concept, we finally get our required edges of lane lines traced on black pixels, which we then merge with our original image by weighted additions, and voila! we have detected the lane lines.
Our final merged image, indicating lane lines will look like this:
<p align="center">
<img src = "https://github.com/sampadabareja/Lane-Detection/blob/master/Result%20Images/Finalimage.jpeg" width="400" height="350">
</p>
<p align="center">  Contributed by: Sampada Bareja @ DS Community SRM 
</p>
<p align="center">
<img src = "https://github.com/Data-Science-Community-SRM/template/blob/master/logo-light.png?raw=true"  height="120" alt="Your Name Here (Insert Your Image Link In Src">
</p>
<p align="center">
<a href = "https://github.com/sampadabareja"><img src = "http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height = "36"/></a>
<a href = "https://www.linkedin.com/in/sampada-bareja-43930818b">
<img src = "http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
</a>
</p>

