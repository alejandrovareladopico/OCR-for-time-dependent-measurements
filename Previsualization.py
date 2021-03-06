import cv2
import funciones
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

name = str(input("Introduce file name(in) "))

video = cv2.VideoCapture(name)
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = int(video.get(cv2.CAP_PROP_FPS))
frame = video.read()
video.release()

plt.close("all")

plt.figure(1)
plt.title("ROI selection instructions")
plt.axhline(0.4, 0, 0.7)
plt.axhline(0.6, 0, 0.7)
plt.axvline(0.3, 0, 0.6)
plt.axvline(0.7, 0, 0.6)
plt.axhspan(0.4, 0.6, 0.3, 0.7)
plt.annotate("ROI", (0.45, 0.49), size=18)
plt.xlim((0, 1))
plt.ylim((0, 1))
plt.xticks((0.3, 0.7), ("x0", "x1"))
plt.yticks((0.4, 0.6), ("y0", "y1"))
plt.show()

gray = cv2.cvtColor(frame[1], cv2.COLOR_BGR2GRAY)

plt.figure(2)
plt.title("First frame of the video\nuse it for select the ROI boundaries\nand the grayscale limits")
plt.imshow(gray, cmap ="gray")
plt.show()

x0 = int(input("x0: "))
x1 = int(input("x1: "))
y0 = int(input("y0: "))
y1 = int(input("y1: "))
lower_bound = int(input("Lower grayscale limit: "))
upper_bound = int(input("Upper grayscale limit: "))

recorte = np.zeros((y1-y0, x1-x0), np.uint8)
frame_ROI = funciones.ROI(gray, x0, x1, y0, y1, recorte)
mask = cv2.inRange(frame_ROI, lower_bound, upper_bound)
res = cv2.bitwise_and(frame_ROI, frame_ROI, mask = mask)

plt.figure(3)
plt.title("ROI selected with grayscale corrections")
plt.imshow(res, cmap="gray")
plt.show()


kernel_blur_size = int(input("Kernel blur size: "))
res_blur = cv2.GaussianBlur(res, (kernel_blur_size, kernel_blur_size), 0)

edgy = str(input("Perform edge detection?[y/n]"))

if edgy == "y":
    edged = cv2.Canny(res_blur, 100, 200)

    plt.figure(4)
    plt.title("Edged image")
    plt.imshow(edged, cmap="gray")
    plt.show()

else:
    edged = res_blur

dilate_iterations = int(input("Dilate iterations: "))
dilated = cv2.dilate(edged, None, iterations = dilate_iterations)
eroded = cv2.erode(dilated, None, iterations = 1)

plt.figure(5)
plt.imshow(eroded, cmap="gray")
plt.show()

ret,newimage = cv2.threshold(eroded,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

plt.figure(6)
plt.title("Thresholded image")
plt.imshow(newimage, cmap="gray")
plt.show()


rot = int(input("Rotate the image?(0 no, 1 yes): "))

if rot == 1:
    frame_ROI_edited = funciones.rotation(newimage)
    plt.figure(5)
    plt.title("Rotated image")
    plt.imshow(frame_ROI_edited, cmap = "gray")
    plt.show()

else:
    pass
inv = str(input("Flip the image? [y/n] "))
if inv == "y":
    axis = int(input("Vertical axis (0), horizontal axis(1): "))
    frame_ROI_edited = funciones.inversion(frame_ROI_edited, axis)
    plt.figure(6)
    plt.title("Flipped image")
    plt.imshow(frame_ROI_edited, cmap = "gray")
    plt.show()
else:
    axis = 0
print("Avaliable languages: ", pytesseract.get_languages(config=""))
language = str(input("Choose one language: "))
string = funciones.lecture(frame_ROI_edited, language)

print("Data read from image:", string)

frequency = float(input("Data adquisition frequency (seconds): "))
param_name = str(input("Parameter file name(out)(.txt): "))


np.savetxt(param_name, (name, num_frames, height, width, fps, x0, x1, y0, y1, lower_bound, upper_bound, kernel_blur_size, edgy, dilate_iterations, rot, inv, axis, frequency, language), fmt = "%20s")
