
import cv2
import numpy as np
import pytesseract
from numba import jit

@jit(nopython = True)
def ROI(frame, x0, x1, y0, y1, recorte):
    recorte = recorte * np.uint8(0)
    for i in range(0, recorte.shape[0], 1):
        for j in range(0, recorte.shape[1], 1):
            recorte[i, j]=frame[y0+i, x0+j]
    return recorte

#@jit(nopython = True)
def rotation(data_in):
    data_in = np.transpose(data_in)
    return data_in

#@jit(nopython = True)
def inversion(data_in, eje):
    data_in = np.flip(data_in, eje)
    return data_in
"""
def edicion(data_in, lower_bound, upper_bound, kernel_blur_size, dilate_iterations):
    mask = cv2.inRange(data_in, lower_bound, upper_bound)
    res = cv2.bitwise_and(data_in, data_in, mask = mask)
    res_blur = cv2.GaussianBlur(res, (kernel_blur_size, kernel_blur_size), 0)
    edged = cv2.Canny(res_blur, 100, 200)
    dilated = cv2.dilate(edged, None, iterations = dilate_iterations)
    eroded = cv2.erode(dilated, None, iterations = 1)
    data_out = cv2.threshold(eroded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return data_out
"""
@jit(nopython=True)
def data_array(data, raw_data, pointer):
    for k in range(data.shape[2]):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                data[i,j,k] = raw_data[pointer]
                pointer = pointer + 1
    return data

def lecture(data_input, language):
    output = pytesseract.image_to_string(data_input, config = "--psm 13 -c tessedit_char_whitelist=0123456789", lang =str(language))
    return output
