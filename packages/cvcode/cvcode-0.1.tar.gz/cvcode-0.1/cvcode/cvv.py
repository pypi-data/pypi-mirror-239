class cvcode:
    def __init__(self):
        pass

    def print_code(self, code):
        print(code)

    def cv1(self):
        code = """
import cv2
a=cv2.imread('download.jpeg',0)
cv2.imshow('img',a)
"""
        self.print_code(code)

    def cv2(self):
        code = """
import cv2

# Read an image
image = cv2.imread('download.jpeg')  # Replace with the path to your image
cv2.imshow('Original Image', image)
# Scaling the image
scaled_image = cv2.resize(image, None, fx=0.5, fy=0.5)  # Scale by 0.5 in both dimensions
cv2.imshow('Scaled Image', scaled_image)
cv2.waitKey(0)

# Rotation and Shifting
rows, cols = image.shape[:2]
rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)  # Rotate by 45 degrees
shifted_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
cv2.imshow('Rotated and Shifted Image', shifted_image)
cv2.waitKey(0)

cv2.destroyAllWindows()



        """
        self.print_code(code)

    def cv3(self):
        code = """
import cv2
import numpy as np
array_2d = np.random.randint(0, 256, (200, 200), dtype=np.uint8)  # Example 2D array of shape (200, 200)
cv2.imshow('Original 2D Array', array_2d)
cv2.waitKey(0)
gray_image = cv2.cvtColor(array_2d, cv2.COLOR_GRAY2BGR)
cv2.imshow('Grayscale Image', gray_image)
gray_image = cv2.imread('download.jpeg', cv2.IMREAD_GRAYSCALE)
array_2d = gray_image
print(array_2d)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
        self.print_code(code)

    def cv4(self):
        code = """
import cv2
import matplotlib.pyplot as plt

# Read a grayscale image
image_gray = cv2.imread('download.jpeg',0)
# Calculate histogram
hist_gray = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
# Display the histogram
plt.plot(hist_gray, color='black')
plt.title('Grayscale Image Histogram')
plt.xlabel('Pixel Values')
plt.ylabel('Number of Pixels')
plt.show()
image_color = cv2.imread('download.jpeg')
hist_b = cv2.calcHist([image_color], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([image_color], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([image_color], [2], None, [256], [0, 256])
# Display the histograms
plt.plot(hist_b, color='blue', label='Blue')
plt.plot(hist_g, color='green', label='Green')
plt.plot(hist_r, color='red', label='Red')
plt.title('Color Image Histogram')
plt.xlabel('Pixel Values')
plt.ylabel('Number of Pixels')
plt.legend()
plt.show()
plt.show()
"""
        self.print_code(code)

    def cv5(self):
        code = """
import cv2
import numpy as np

img1 = cv2.imread('download.jpeg')
img2 = cv2.imread('download.jpeg')

# Add the two images
add = cv2.add(img1, img2)

# Subtract img1 from img2
sub = cv2.subtract(img2, img1) 

# Find absolute difference
diff = cv2.absdiff(img1, img2)

# Multiply img1 and img2
mul = cv2.multiply(img1, img2)

# Divide img2 by img1
div = cv2.divide(img2, img1)
cv2.imshow('Image 1', img1)
cv2.imshow('Image 2', img2)
cv2.imshow('Added', add)
cv2.imshow('Subtracted', sub)
cv2.imshow('Difference', diff) 
cv2.imshow('Multiplied', mul)
cv2.imshow('Divided', div)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
        self.print_code(code)

    def cv6(self):
        code = """
import cv2
import numpy as np

img = cv2.imread('download.jpeg')

# Single transformation

# Scaling 
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# Display result
cv2.imshow('Scaled', resized)
cv2.waitKey(0) 

# Multiple transformations

# Rotate image
rows,cols = img.shape[:2]
M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
rotated = cv2.warpAffine(img,M,(cols,rows))

# Shift image 
M = np.float32([[1,0,100],[0,1,50]]) 
shifted = cv2.warpAffine(rotated,M,(cols,rows))

# Flip image horizontally  
flipped = cv2.flip(shifted, 1)

# Display result
cv2.imshow('Multiple Transformed', flipped)
cv2.waitKey(0)  
cv2.destroyAllWindows()

"""
        self.print_code(code)

    def cv7(self):
        code = """
import cv2
import numpy as np

img = cv2.imread('2.jpg')

# Linear transformation
m = 100
c = 50
linear_img = m*img + c

# Non-linear transformation  
power = 1.5
nonlinear_img = np.power(img, power)

# Clipping
clip_img = np.clip(img, 100, 200) 

# Windowing
rows, cols = img.shape[:2]
start_row, start_col = int(rows*0.25), int(cols*0.25)
end_row, end_col = int(rows*0.75), int(cols*0.75)
window_img = img[start_row:end_row, start_col:end_col]

cv2.imshow('Original', img)
cv2.imshow('Linear', linear_img)
cv2.imshow('Non-Linear', nonlinear_img) 
cv2.imshow('Clipped', clip_img)
cv2.imshow('Windowed', window_img)

cv2.waitKey(0)
cv2.destroyAllWindows()"""
        self.print_code(code)

    def cv8(self):
        code = """
import numpy as np 
import cv2

points1 = np.float32([[51,791], [63,143], [444,211], [426,719] ])
points2 = np.float32([[1,900], [1,1], [501,1], [501,900] ])

A = []
for i in range(0, len(points1)):
    x, y = points1[i][0], points1[i][1] 
    u, v = points2[i][0], points2[i][1]
    A.append([x, y, 1, 0, 0, 0, -u*x, -u*y, -u])
    A.append([0, 0, 0, x, y, 1, -v*x, -v*y, -v])
    
A = np.array(A)
    
U, S, Vh = np.linalg.svd(A)
L = Vh[-1,:] / Vh[-1,-1]
H = L.reshape(3,3)

print(H)

# Transform points  
pts = np.float32([[100,200], [300,250]]).reshape(-1,1,2)
transformed = cv2.perspectiveTransform(pts, H)
print(transformed)


#run in colab 
import cv2
import numpy as np
import os
import glob

CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints = []
imgpoints = []
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
images = glob.glob('/content/chess board.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                             cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()
"""
        self.print_code(code)

    def cv9(self):
        code="""
import numpy as np 
import cv2

points1 = np.float32([[51,791], [63,143], [444,211], [426,719] ])
points2 = np.float32([[1,900], [1,1], [501,1], [501,900] ])

A = []
for i in range(0, len(points1)):
    x, y = points1[i][0], points1[i][1] 
    u, v = points2[i][0], points2[i][1]
    A.append([x, y, 1, 0, 0, 0, -u*x, -u*y, -u])
    A.append([0, 0, 0, x, y, 1, -v*x, -v*y, -v])
    
A = np.array(A)
    
U, S, Vh = np.linalg.svd(A)
L = Vh[-1,:] / Vh[-1,-1]
H = L.reshape(3,3)

print(H)

# Transform points  
pts = np.float32([[100,200], [300,250]]).reshape(-1,1,2)
transformed = cv2.perspectiveTransform(pts, H)
print(transformed)



import cv2

# Load the image
image = cv2.imread("2.jpg")

# Draw a line
cv2.line(image, (50, 50), (200, 200), (0, 0, 255), 2)

# Draw text
cv2.putText(image, "OpenCV", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Draw a circle
cv2.circle(image, (150, 150), 10, (0, 255, 0), 2)

# Draw a rectangle
cv2.rectangle(image, (100, 50), (50, 100), (255, 0, 255), 2)

# Draw an ellipse
cv2.ellipse(image, (50, 55), (65, 50), 30, 0, 360, (255, 255, 0), 2)

# Display the annotated image
cv2.imshow("Annotated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
        self.print_code(code)

    def cv10(self):
        code="""
import cv2

# Load the image
image = cv2.imread("2.jpg", cv2.IMREAD_GRAYSCALE)

# Apply Sobel edge detection
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
sobel_edges = cv2.magnitude(sobel_x, sobel_y)

# Apply Canny edge detection
canny_edges = cv2.Canny(image, 100, 200)

# Apply gradient edge detection
gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)
gradient_edges = cv2.threshold(gradient_magnitude, 50, 255, cv2.THRESH_BINARY)[1]

# Display the original image and the edge detection results
cv2.imshow("Original Image", image)
cv2.imshow("Sobel Edges", sobel_edges.astype('uint8'))
cv2.imshow("Canny Edges", canny_edges)
cv2.imshow("Gradient Edges", gradient_edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""
        self.print_code(code)

    def cv11(self):
        code="""
import cv2

# Load the image
image = cv2.imread("2.jpg")

# Crop the image
cropped_image = image[100:300, 200:400]

# Resize the image
resized_image = cv2.resize(image, (500, 500))

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Blob detection
params = cv2.SimpleBlobDetector_Params()
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(thresholded_image)

# Display the results
cv2.imshow("Original Image", image)
cv2.imshow("Cropped Image", cropped_image)
cv2.imshow("Resized Image", resized_image)
cv2.imshow("Thresholded Image", thresholded_image)
cv2.imshow("Contour Image", cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2))
cv2.imshow("Blob Image", cv2.drawKeypoints(image.copy(), keypoints, None, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
        self.print_code(code)

    def cv12(self):
        code="""
import cv2
import numpy as np

# Load the image
image = cv2.imread("2.jpg")

# Convert the image to different color spaces
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

# Perform histogram equalization on the grayscale image
equalized_image = cv2.equalizeHist(gray_image)

# Define a kernel for convolution
kernel = np.ones((5, 5), np.float32) / 25

# Apply convolution on the grayscale image
convolved_image = cv2.filter2D(gray_image, -1, kernel)

# Apply image smoothing using Gaussian blur
smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)

# Display the results
cv2.imshow("Original Image", image)
cv2.imshow("Grayscale Image", gray_image)
cv2.imshow("HSV Image", hsv_image)
cv2.imshow("LAB Image", lab_image)
cv2.imshow("Equalized Image", equalized_image)
cv2.imshow("Convolved Image", convolved_image)
cv2.imshow("Smoothed Image", smoothed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
        self.print_code(code)

    def cv13(self):
        code="""
import cv2
from google.colab.patches import cv2_imshow
import numpy as np
from matplotlib import pyplot as plt
image = cv2.imread('/content/umberala.jpeg', cv2.IMREAD_COLOR)
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_image1, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image1, (x1, y1), (x2, y2), (0, 0, 255), 2)

    plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    plt.title('Hough Transform')
    plt.show()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
fourier = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
fourier_shift = np.fft.fftshift(fourier)
magnitude = 20*np.log(cv2.magnitude(fourier_shift[:,:,0],fourier_shift[:,:,1]))
magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
cv2_imshow(magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()
image1 = cv2.imread('/content/umberala.jpeg', cv2.IMREAD_COLOR)
image2 = cv2.imread('/content/foot ball.jpg', cv2.IMREAD_COLOR)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)
matches = sorted(matches, key=lambda x: x.distance)
matching_result = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.imshow(cv2.cvtColor(matching_result, cv2.COLOR_BGR2RGB))
plt.title('Matching Keypoints')
plt.show()"""

        self.print_code(code)
    def cv14(self):
        code="""
import cv2
import numpy as np
from matplotlib import pyplot as plt
image1 = cv2.imread('/content/umberala.jpeg', cv2.IMREAD_COLOR)
image2 = cv2.imread('/content/foot ball.jpg', cv2.IMREAD_COLOR)
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(gray_image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(gray_image2, None)
keypoints_image1 = cv2.drawKeypoints(image1, keypoints1, None, color=(0, 255, 0), flags=0)
keypoints_image2 = cv2.drawKeypoints(image2, keypoints2, None, color=(0, 255, 0), flags=0)
plt.subplot(121), plt.imshow(cv2.cvtColor(keypoints_image1, cv2.COLOR_BGR2RGB))
plt.title('ORB Keypoints Image 1'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(cv2.cvtColor(keypoints_image2, cv2.COLOR_BGR2RGB))
plt.title('ORB Keypoints Image 2'), plt.xticks([]), plt.yticks([])
plt.show()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)
matches = sorted(matches, key=lambda x: x.distance)
matching_result = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.imshow(cv2.cvtColor(matching_result, cv2.COLOR_BGR2RGB))
plt.title('Matching Keypoints')
plt.show()
src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
homography, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
aligned_image = cv2.warpPerspective(image1, homography, (image2.shape[1], image2.shape[0]))
plt.imshow(cv2.cvtColor(aligned_image, cv2.COLOR_BGR2RGB))
plt.title('Aligned Image')
plt.show()
"""
        self.print_code(code)
    def cv15(self):
        code="""
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
def graphcut_segmentation(img, rect):
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    segmented_img = img * mask2[:, :, np.newaxis]
    return segmented_img
def main():
    img = cv2.imread("/content/umberala.jpeg")
    rect = (10, 10, 170, 100)
    segmented_img = graphcut_segmentation(img, rect)
    print("INPUT IMAGE")
    cv2_imshow(img)
    print("GRAPH IMAGE")
    cv2_imshow(segmented_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()






import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('/content/chess board.png')
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (100,120,470,350)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img_cut = img*mask2[:,:,np.newaxis]
plt.subplot(211),plt.imshow(img)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(212),plt.imshow(img_cut)
plt.title('Grab cut'), plt.xticks([]), plt.yticks([])
plt.show()

"""
        self.print_code(code)
    def cv16(self):
        code="""
import cv2
import numpy as np
import os
import glob

CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints = []
imgpoints = []
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
images = glob.glob('/content/chess board.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                             cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()




import cv2
from google.colab.patches import cv2_imshow
import numpy as np
width, height = 640, 480
color = (255, 0, 0)
color_image = np.zeros((height, width, 3), dtype=np.uint8)
color_image[:, :] = color
cv2_imshow(color_image)
cv2.waitKey(0)
cv2.imwrite('color_image.jpg', color_image)
loaded_image = cv2.imread('color_image.jpg')
cv2_imshow(loaded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
        self.print_code(code)
    def cv17(self):
        code="""
!pip install mediapipe
import cv2
import mediapipe as mp
from google.colab.patches import cv2_imshow
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
image = cv2.imread('/content/man.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
pose_results = pose.process(image_rgb)
image_with_landmarks = image.copy()
mp_drawing.draw_landmarks(image_with_landmarks, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
cv2_imshow(image_with_landmarks)




import cv2
from google.colab.patches import cv2_imshow
image=cv2.imread("umberala.jpeg")
reflected_image = cv2.flip(image, 1)  # 1 indicates horizontal reflection
cv2_imshow(image)
cv2_imshow(reflected_image)
cv2.imwrite('reflected_image.jpg', reflected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
        self.print_code(code)
    def cv18(self):
        code="""
import cv2
from google.colab.patches import cv2_imshow
import numpy as np
def remove_projective_distortion(distorted_image):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(distorted_image, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des1)
    matches = sorted(matches, key=lambda x: x.distance)
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp1[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    undistorted_image = cv2.warpPerspective(distorted_image, H, (distorted_image.shape[1], distorted_image.shape[0]))
    return undistorted_image
if __name__ == "__main__":
    distorted_image = cv2.imread("/content/book image.jpeg", 0)
    undistorted_image = remove_projective_distortion(distorted_image)
    cv2_imshow( distorted_image)
    cv2_imshow( undistorted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




import cv2
from google.colab.patches import cv2_imshow
import numpy as np
from IPython.display import Image
def compute_disparity_map(left_image_path, right_image_path, output_image_path):
    imgL = cv2.imread(left_image_path, cv2.IMREAD_GRAYSCALE)
    imgR = cv2.imread(right_image_path, cv2.IMREAD_GRAYSCALE)
    imgL = cv2.resize(imgL, (imgR.shape[1], imgR.shape[0]))
    stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)
    disparity = stereo.compute(imgL, imgR)
    disparity_normalized = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imwrite(output_image_path, disparity_normalized)
if __name__ == "__main__":
    left_image_path = "/content/Picture1.jpg"
    right_image_path = "/content/Picture2.jpg"
    output_image_path = "disparity.png"
    compute_disparity_map(left_image_path, right_image_path, output_image_path)
    disparity_image = cv2.imread(output_image_path, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(output_image_path, disparity_image)
    Image(filename=output_image_path)"""
        self.print_code(code)
    def cv20(self):
        code="""
from google.colab.patches import cv2_imshow
import cv2
image = cv2.imread("/content/umberala.jpeg", 0)
_,thresholded_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
cv2_imshow(thresholded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("THRESHOLD IMAGE")



import numpy as np
import cv2
from google.colab.patches import cv2_imshow
image = cv2.imread('/content/umberala.jpeg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
block_size = 2
ksize = 3
k = 0.04
corner_response = cv2.cornerHarris(gray, blockSize=block_size, ksize=ksize, k=k)
threshold = 0.01
corner_response_thresholded = (corner_response > threshold * corner_response.max()).astype(np.uint8)
image[corner_response_thresholded > 0] = [0, 0, 255]
cv2_imshow (image)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
        self.print_code(code)
    def cv21(self):
        code="""
import cv2
import numpy as np

# Create a blank image with the desired dimensions
height = 500
width = 500
image = np.zeros((height, width, 3), np.uint8)

# Draw the woman's face
center_x = int(width / 2)
center_y = int(height / 2)
radius = 150
color = (255, 255, 255)
thickness = -1
cv2.circle(image, (center_x, center_y), radius, color, thickness)





# Display the image
cv2.imshow("Generated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()




import cv2
import numpy as np

# Create a blank image with the desired dimensions
height = 500
width = 500
image = np.ones((height, width, 3), np.uint8) * 255

# Define the size and position of the black boxes
box_size = 50
margin = 20

# Draw the black boxes in the four corners
cv2.rectangle(image, (margin, margin), (margin + box_size, margin + box_size), (0, 0, 0), -1)
cv2.rectangle(image, (margin, height - margin - box_size), (margin + box_size, height - margin), (0, 0, 0), -1)
cv2.rectangle(image, (width - margin - box_size, margin), (width - margin, margin + box_size), (0, 0, 0), -1)
cv2.rectangle(image, (width - margin - box_size, height - margin - box_size), (width - margin, height - margin), (0, 0, 0), -1)

# Display the image
cv2.imshow("Generated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()



import cv2
import numpy as np

# Create a blank image with the desired dimensions
height = 500
width = 500
image = np.ones((height, width, 3), np.uint8) * 255

# Define the number of rows and columns for the grid
rows = 5
cols = 5

# Calculate the spacing between gridlines
row_spacing = (height - 100) // rows
col_spacing = (width - 100) // cols

# Draw horizontal gridlines
for i in range(1, rows):
    y = i * row_spacing + 50
    cv2.line(image, (50, y), (width - 50, y), (0, 0, 0), 2)

# Draw vertical gridlines
for j in range(1, cols):
    x = j * col_spacing + 50
    cv2.line(image, (x, 50), (x, height - 50), (0, 0, 0), 2)

# Display the image
cv2.imshow("Generated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
        self.print_code(code)
    def cv19(self):
        code="""
import cv2
import numpy as np

# Initialize Kalman Filter
def kalman_filter_init(state_dim, measurement_dim):
    kalman = cv2.KalmanFilter(state_dim, measurement_dim)
    kalman.transitionMatrix = np.eye(state_dim, dtype=np.float32)
    kalman.measurementMatrix = np.eye(measurement_dim, state_dim, dtype=np.float32)
    kalman.processNoiseCov = 1e-5 * np.eye(state_dim, dtype=np.float32)
    kalman.measurementNoiseCov = 1e-2 * np.eye(measurement_dim, dtype=np.float32)
    kalman.errorCovPost = 1 * np.eye(state_dim, dtype=np.float32)
    return kalman

# Camshift Tracking
def camshift_track(frame, roi_hist, roi):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    ret, track_window = cv2.CamShift(dst, roi, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    return pts

def main():
    cap = cv2.VideoCapture('test.mp4')
    ret, frame = cap.read()
    
    # Define Kalman Filter and Camshift parameters
    state_dim, measurement_dim = 4, 2
    kalman = kalman_filter_init(state_dim, measurement_dim)
    
    # Initialize Camshift parameters
    roi = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi_mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    roi_hist = cv2.calcHist([hsv_roi], [0], roi_mask, [180], [0, 180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    
    while ret:
        ret, frame = cap.read()

        if not ret:
            break

        # Kalman Filter Prediction
        prediction = kalman.predict()
        predicted_x, predicted_y = prediction[0], prediction[1]

        # Camshift Tracking
        tracked_points = camshift_track(frame, roi_hist, roi)
        (x, y), (w, h), angle = cv2.minAreaRect(tracked_points)

        # Kalman Filter Update
        measurement = np.array([[x + w / 2], [y + h / 2]], dtype=np.float32)
        kalman.correct(measurement)

        # Draw the tracked object on the frame
        cv2.polylines(frame, [tracked_points], True, (0, 255, 0), 2)
        cv2.imshow('Object Tracking', frame)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
"""
        self.print_code(code)
    def cvques(self):
        code="""
List of Questions:

1. a. OpenCV Installation and working with Python
b. To create a program to display grayscale image using read and write
operation

2. Construct a program to perform the following operations using OpenCV

a. Read an image
b. Scaling
c. Rotation and shifting operation.

3. a. Create a program to convert a 2D array into a grayscale image
b. Create program to convert gray images into an array of numbers.
c. To create a program to rotate an image.

4. Construct a program to find histogram value and display histograph of a
grayscale and color image in OpenCV.
5. Write a program to perform the following operation

 Image addition
 Image Subtraction
 Image Difference
 Image Multiplication
 Image Division

6. Write a program to perform the following operation

a) Single transformation
b) Multiple transformations are allowed

7. Write a program to perform the following transformation function

a) Linear
b) Non-linear
c) Clipping
d) Windowing

8. a) Compute the Homography matrix for a given 4 data points without
SVD and transformed the point using the computed homography
matrix.
(51,791) --→ (1,900)
(63,143) - → (1,1)
(444,211) -→ (501,1)
(426,719) --→ (501,900)
b) Develop a program to perform Camera Calibration with circular grid
9. a) Compute the Homography matrix for a given 4 data points using DLT
and transformed the point using the computed homography matrix.
(51,791) - → (1,900)
(63,143) - → (1,1)
(444,211) --→ (501,1)
(426.719) --→ (501,900)

b) Construct a program to perform Image Annotation – Drawing lines,
text circle, rectangle, ellipse on images

Develop a program to determine the edge detection of an image using
i. Sobel
ii. Canny Edge Detector
iii. Gradient Edge Detector

11. Write a program to perform the basic image processing

i. Loading images,
ii. Cropping,
iii. Resizing,
iv. Thresholding,
v. Contour analysis,
vi. Bolb detection

12. Develop a python program to perform image enhancement

i. Color spaces,
ii. Color space conversion,
iii. Histogram equalization,
iv. Convolution,
v. Image smoothing,

13. Develop a program to perform Image Features and Image Alignment

i. Fourier
ii. Hough
iii. Feature matching-based image alignment

14. Develop a program to perform Image Features and Image Alignment

i. Extract ORM Image features
ii. Feature matching,
iii. Cloning

15. Write a python program to perform an image segmentation using

i. Graphcut
ii. Grabcut

16. a) Construct a python program to perform a camera calibration with

circular grid
b) To create a color image and perform read and write operation.
17. a) Develop a python code to perform the pose estimation.
b) Construct a code to perform image reflection on an image using
OpenCV ().

18. a) Develop a code to remove the projective distortion in the image using

Homography
b) Construct a python program to perform 3D Reconstruction
i. Creating Depth map from stereo images
19. Construct a python program to perform the following

i. Object Detection
ii. Tracking using Kalman Filter
iii. Camshift

20. a) Construct a program to perform thresholding-based segmentation

technique.
b) Write a program to determine corner detection using harris corner
detector algorithm.

21)Write 3 different Python functions that can create the images given below.
Code them in such so that the size of the image itself, size of boxes, size of
lines, and a number of horizontal and vertical lines are entered by the user."""
        self.print_code(code)






        

        
        


                                                                   












