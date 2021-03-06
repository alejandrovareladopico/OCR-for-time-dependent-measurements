import numpy as np
import funciones
from mpi4py import MPI
import cv2
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


if rank == 0:
    param_name = str(input("Param file name(in)(.txt): "))
    data_out = str(input("Read data file name(out)(.txt): "))
    t0 = time.time()
else:
    param_name = None


param_name = comm.bcast(param_name, root = 0)

num_frames, height, width, fps, x0, x1, y0, y1, lower_bound, upper_bound, kernel_blur_size, edgy, dilate_iterations, rot, inv, axis, frequency, language, saved_data = np.loadtxt(param_name, str)
recorte = np.zeros((int(y1)-int(y0), int(x1)-int(x0)), np.uint8)

lectures = []

local_start = rank*int(int(saved_data)/size)
local_end = (rank + 1)*int(int(saved_data)/size)
if rank == (size - 1):
    local_end = local_end + (int(saved_data) % size)

for i in range(local_start, local_end, 1):
    frame = cv2.imread("Frames/"+str(i)+".png")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_ROI = funciones.ROI(gray, int(x0), int(x1), int(y0), int(y1), recorte)
    mask = cv2.inRange(frame_ROI, int(lower_bound), int(upper_bound))
    res = cv2.bitwise_and(frame_ROI, frame_ROI, mask = mask)
    res_blur = cv2.GaussianBlur(res, (int(kernel_blur_size), int(kernel_blur_size)), 0)
    if edgy == "y":
        edged = cv2.Canny(res_blur, 100, 200)
    else:
        edged = res_blur
    dilated = cv2.dilate(edged, None, iterations = int(dilate_iterations))
    eroded = cv2.erode(dilated, None, iterations = 1)
    ret,data = cv2.threshold(eroded,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if int(rot) == 1:
        data_rot = funciones.rotation(data)
    else:
        data_rot = data
    if inv == "y":
        data_rot = funciones.inversion(data_rot, int(axis))
    else:
        pass
    lectures.append(funciones.lecture(data_rot, language))


if rank == 0:
    for i in range(1, size):
        data_recv = comm.recv(data, source = i)
        lectures += data_recv

    timer = np.zeros(int(saved_data), float)
    data_float = np.zeros(len(lectures), float)
    for i in range(len(lectures)):
        data_float[i] = float(lectures[i])
        timer[i] = i*float(frequency)

    final_data = np.array([timer, data_float])
    t1 = time.time()
    file = open(data_out, "w")
    np.savetxt(file, final_data.T, "%.3f")
    file.close()
    print("Done, elapsed time:", (t1-t0)/60, "minutes")
else:
    data = comm.send(lectures, dest=0)


comm.Disconnect()
