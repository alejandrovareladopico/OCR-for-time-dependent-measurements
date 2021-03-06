import cv2
import numpy as np
import time

param_file = str(input("Parameter file name(in)(.txt): "))

name, num_frames, height, width, fps, x0, x1, y0, y1, lower_bound, upper_bound, kernel_blur_size, edgy, dilate_iterations, rot, inv, axis, frequency, language = np.loadtxt(param_file, str)

video = cv2.VideoCapture(name)

t0 = time.time()
saved_data = 0
for i in range(int(num_frames)):
    frame = video.read(i)[1]
    if i % (float(frequency)*int(fps)) == 0.:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(str(saved_data)+".png", gray)
        saved_data = saved_data + 1
video.release()

print ("Frame selection completed. Elapsed time:", (time.time()-t0)/60, "minutes")

param_file_out = str(input("Out parameter file name(out)(.txt): "))

np.savetxt(param_file_out, (num_frames, height, width, fps, x0, x1, y0, y1, lower_bound, upper_bound, kernel_blur_size, edgy, dilate_iterations, rot, inv, axis, frequency, language, saved_data), "%20s")
