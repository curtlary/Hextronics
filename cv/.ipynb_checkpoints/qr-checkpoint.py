from matplotlib.pyplot import figure
from sklearn.linear_model import LinearRegression
from PIL import Image
from pyzbar import pyzbar
from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
import time

def show_circles(src):
    src = cv2.imread(src)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    p1, p2 = 70, 30
    edges = cv2.Canny(gray,p1,p2)    

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=p1, param2=p2,
                               minRadius=25, maxRadius=55)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(src, center, 1, (0, 100, 100), 3)
            radius = i[2]
            cv2.circle(src, center, radius, (255, 0, 255), 3)
    plt.figure(figsize=(24, 24))
    plt.imshow(src)
    plt.show()
    
def get_circles(im):
    rows = im.shape[0]
    p1, p2 = 70, 30
    circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=p1, param2=p2,
                               minRadius=25, maxRadius=55)
    if circles is not None:
        circles = np.around(circles)
    return circles
        
def matching_circle_center(circles, qr_center):
    possible = []
    for circle in circles[0]:
        dist = np.linalg.norm(qr_center - circle[:2])
        if (163 < dist < 193) and (30 < circle[2] < 67): # TODO: Too much handpicking values, make this automatic with training images maybe?
            possible.append(circle[:2])
    if len(possible) > 1:
        print(f"More than one circle possible {possible}, returning center for first one")
    if len(possible) ==0:
        print(f"Did not find true button circle")
        return None
    
    return possible[0]

def theta(circle_center, qr_center):
    vec = qr_center - circle_center.astype(float)
    # 87 is the offset to align with gauntry TODO: make this better? Lol
    return np.degrees(np.arctan(vec[1]/vec[0])) + 87 

def locate_drone(img):
    img = process_img(img)
    decoded_objs = decode(thres)
    
    ######## REMOVE BELOW WHEN POSSIBLE ######### 
    xys = np.array([[134.25, 232.75],[64.5, -23.25], [84.75, -110.75], [-35.25, 43.75]])
    offsets = np.array([[-30, 30], [0, -20],[0, -40], [20,0]])

    linreg = LinearRegression().fit(xys, offsets)

    ######## REMOVE ABOVE WHEN POSSIBLE ######### 
    
    if len(decoded_objs) == 0:
        return False, 0, 0, 0
    
    qr_center = get_qr_center(decoded_objs)
    
    pred_offset = linreg.predict([seek_center - qr_center])[0].round()
    
    circle_center = matching_circle_center(circles, qr_center)
    
    angle = 404 # value for not found circle center
    
    if circle_center is not None:
        angle = theta(circle_center, qr_center) % 360
    return True, pred_offset[0], pred_offset[1], angle

def process_img(img):
    """ Applies transforms to the image to make it good
        - Histogram Equalization (Still experimenting)
        - Image dewarping (Planning)
        - thresholding to make QR code more contrastive
        - Dilation + Erosion (Still experimenting)
    """
    thres = cv2.adaptiveThreshold(
        im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,65,2 
    )
    thres = ~thres
    kernel = np.ones((1,1),np.uint8)
    thres = cv2.dilate(thres, kernel, iterations = 1)
    thres = cv2.erode(thres, kernel, iterations = 1)
    thres = ~thres
    return thres


def get_qr_center(objs)
    for obj in objs: 
        points = obj.polygon

    if len(points) > 4: 
        hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
        hull = list(map(tuple, np.squeeze(hull)))
    else: 
        hull = points
    
    n = len(hull)
    hull = np.array([(p.x, p.y) for p in hull])
    center = hull.mean(axis = 0)
    return center