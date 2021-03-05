# OCR-for-time-dependent-measurements
Set of python scripts for numerical recognition in time dependent measurements.

This is a set of three python scripts intended for numerical recognition in time dependent measurements. They are made in a very simple and interactive way, in order to make them confortable for people with not much experience in this topic. The scripts are wrote so that the input file is a video of the display showing the numerical data. For better results, it is recomended to avoid camera movements during the recording time. 

## Dependencies

  python<br> 
  pytesseract<br> 
  openCV<br> 
  numpy<br> 
  numba(optional)<br> 
  mpi4py(optional)<br> 

## Workflow
  Set of instructions in order to use the scripts
### Previsualization
  In order to run this scrip just open a terminal in the script directory and type:<br>
  
  $ python3 Previsualization.py<br>
  
  The script will ask you to introduce the name of the file to analyze, and several factors in order to determine region of interest and some image manipulations. Finally will ask you to select one language to read the data. Since tesseract works as a neural network, it has to be previously trained. The language file contain some pre-trained data that you can use. In the repository are also linked some trained data files for seven-segment-displays. The parameters that you have selected will be saved in a parameter file (.txt)
  
### Frame_Selection
 As in the first script, run in the terminal:<br>
 
 $ python3 Frame_Selection.py<br>
 
 This script will ask you an input parameter file name (The output file of the previous script) and a name for an output file. Basically this script selects the video frames to analyze, matching with the frequency of data adquisition selected in the first script. The code will create a folder and save the selected frames in a png format. I know this is not optimal and quite ugly, but since this is the more time requirement script, saving the frames you will only have to run it once in case the final script fails.
 
 
  
  
