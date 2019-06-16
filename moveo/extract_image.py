import cv2 
import numpy as np
import csv
import os
import subprocess
  
from os.path import isfile, join
# Function to extract frames 
def FrameCapture(video_file_path, params): 
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
  # Path to video file 
	vidObj = cv2.VideoCapture(video_file_path)
	fps = vidObj.get(cv2.CAP_PROP_FPS)
	print("FPS : ")
	print(fps)
	audio_path = "audio.mp3"
	if os.path.exists(audio_path):
		os.remove(audio_path)
	command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video_file_path, audio_path)
	FNULL = open(os.devnull, 'w')
	subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

	# Used as counter variable 
	count = 0
	num_params = np.shape(params)[0]
	print(num_params)
	i=0
  # checks whether frames were extracted 
	success = 1
    
	while success:
  
		# vidObj object calls read 
		# function extract frames 
		success, image = vidObj.read()
		if(success!=1):
			print("break here : {}".format(count))
			break
		# Saves the frames with frame-count 
		# cv2.imwrite("sample_video_photos/frame%d.jpg" % count, image)

		if(count==0):
			center_x = int(image.shape[1]/2)
			center_y = int(image.shape[0]/2)
			print(image.shape)
			lside = center_x-10

		if(i<num_params and count>params[i][1]):
			i += 1

		if(i<num_params and count>params[i][0] and count<params[i][1]):
			if(lside < center_x+params[i][2] < image.shape[1] - lside):
				center_x += params[i][2]
				# print("count : {}  |  X,Y: {},".format(count, center_x), end = '')
			if(lside < center_y+params[i][3] < image.shape[0] - lside):	
				center_y += params[i][3]
				# print(center_y)


		image = image[center_y-lside:center_y+lside,center_x-lside:center_x+lside]
		path = "/home/atman/work/moviecrop/sample_video_photos/CroppedDance1/"
		cv2.imwrite("{}frame{}.jpg".format(path, count), image)
		count += 1
	tempPath = path+"new_video.mp4"
	
	if os.path.exists(tempPath):
		os.remove(tempPath)
	print("Starting convert_frames_to_video function :")
	convert_frames_to_video(path,tempPath,fps)


	if os.path.exists("/home/atman/work/moviecrop/output.mp4"):
		os.remove("/home/atman/work/moviecrop/output.mp4")
	command = "ffmpeg -i {}/new_video.mp4 -i audio.mp3 -c copy -map 0:v -map 1:a output.mp4".format(path)
	subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
	print(count)


#convertovideo
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    print("but couldn't reach here")
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        # print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        
        #inserting the frames into an image array
        frame_array.append(img)


    
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()


# Driver Code 
if __name__ == '__main__': 
  
	# Calling the function

	with open('/home/atman/work/moviecrop/parameters.csv', 'r') as f:
	    reader = csv.reader(f)
	    params = list(reader)
	params = [[int(i) for i in row] for row in params ]
	# params = [[50,80,-5,-5]]
	# params.append([160,200,10,0])
	print(params)
	
	video_file_path = "/home/atman/work/moviecrop/dance1.mp4"
	FrameCapture(video_file_path, params) 
