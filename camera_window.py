import tkinter as tk
import cv2
import PIL.ImageTk
import PIL.Image
import time
import requests



from requests.auth import HTTPDigestAuth
from camera import tiltCameras, panCameras, getPositionCam1, getVirtualPan, getB, newCalibration, getTilt2, getPan2

R = 0
h =0
B = 1
personHeight =0
tilt20 = 0
pan20 = 0
tilt10 = 0
pan10 = 0

auth = HTTPDigestAuth('root','pass')
captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')
captureLiten = cv2.VideoCapture('rtsp://root.pass@169.254.102.3/axis-media/media.amp')
#rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov


class App:
    def __init__(self, window, window_title, video_source1='rtsp://root.pass@169.254.203.231/axis-media/media.amp', video_source2='rtsp://root.pass@169.254.102.3/axis-media/media.amp'):
        self.window = window
        self.window.title(window_title)
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.window.resizable(0,0)
        self.window.pack_propagate(0)


     # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)


         # Create a canvas that can fit the above video source size
        self.canvas1 = tk.Canvas(window, width=560, height=500)
        self.canvas2 = tk.Canvas(window, width=560, height=500)
        self.canvas1.grid(padx=10, pady=0, columnspan=2, row=0, column=0)
        self.canvas2.grid(padx=10, pady=0, columnspan=2, row=0, column=3)



        #self.canvas1.pack(padx=5, pady=10, side="left")
        #self.canvas2.pack(padx=5, pady=60, side="left")




         # Button that lets the user take a snapshot
        #self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)


        file = open("angles.txt","r")
        angles = file.readlines()
        file.close()
        panCameras(angles[0][:-1],1)
        tiltCameras(angles[1][:-1],1)
        panCameras(angles[2][:-1],2)
        tiltCameras(angles[3][:-1],2)
        print(angles[0][:-1], angles[1][:-1])

        self.scale_pan1 = tk.Scale(window, from_=-180, to=180, orient=tk.HORIZONTAL, command=self.pan1)
        #self.scale_pan1.pack(anchor=tk.SE, expand=True)
        self.scale_pan1.grid(padx=6, pady=0, row=1, column=0, sticky=tk.E, rowspan=2)
        self.label_pan1 = tk.Label(window, text="Rotate")
        self.label_pan1.grid(row=1, column=0, sticky=tk.E, padx=40)

        self.scale_tilt1 = tk.Scale(window, from_=0, to=90, orient=tk.VERTICAL, command=self.tilt1 )
        self.scale_tilt1.grid(padx=5, pady=0, row=1, column=1, sticky=tk.W, rowspan=2)
        self.label_tilt1 = tk.Label(window, text="Tilt")
        self.label_tilt1.grid(row=1, column=1, sticky=tk.W, padx=50, rowspan=2)

        self.scale_focus = tk.Scale(window, from_=10, to=0, orient=tk.VERTICAL, resolution=0.1,command = self.focusHeight)
        self.scale_focus.grid(padx=5, pady=0, row=1, column=1, rowspan=2)
        self.label_focus = tk.Label(window, text="Focus height")
        self.label_focus.grid(row=1, column=1, sticky=tk.E, padx=50, rowspan=2)
        self.scale_focus.grid_remove()
        self.label_focus.grid_remove()

        self.scale_pan2 = tk.Scale(window, from_=-180, to=180, orient=tk.HORIZONTAL, command=self.pan2)
        self.scale_pan2.grid(padx=5, pady=0, row=1, column=3, sticky=tk.E, rowspan=2)
        self.label_pan2 = tk.Label(window, text="Rotate")
        self.label_pan2.grid(row=1, column=3, sticky=tk.E, padx=40)

        self.scale_tilt2 = tk.Scale(window, from_=0, to=90, orient=tk.VERTICAL, command=self.tilt2)
        self.scale_tilt2.grid(padx=5, pady=0, row=1, column=4, sticky=tk.W, rowspan=2)
        self.label_tilt2 = tk.Label(window, text="Tilt")
        self.label_tilt2.grid(row=1, column=4, sticky=tk.W, padx=50, rowspan=2)


        self.entry_height = tk.Entry(window)
        self.entry_height.grid(row=1, column=2, sticky=tk.S)
        self.label_height = tk.Label(window, text = "Camera height")
        self.label_height.grid(pady=20, row=1, column=2, sticky=tk.N)

        self.entry_distance = tk.Entry(window)
        self.entry_distance.grid(pady=0, row=2, column=2, sticky=tk.S)
        self.label_distance = tk.Label(window, text="Distance between cameras")
        self.label_distance.grid(pady=20,row=2, column=2, sticky=tk.N)

        #padiy, padix

        self.button_calibrate = tk.Button(window, text="Calibrate", width=7, command=self.calibrate)
        self.button_calibrate.grid(pady=20, row=3,column=2)
        self.button_reset = tk.Button(window, text="Reset", width=7, command=self.reset)
        self.button_reset.grid(pady=80, padx=43, row=1,column=2, rowspan=3)
        self.button_reset.grid_remove()


        #pan10,tilt10,pan20,tilt20 = newCalibration()
        self.scale_pan1.set(angles[0][:-1])
        self.scale_tilt1.set("-"+angles[1][:-1])
        self.scale_pan2.set(angles[2][:-1])
        self.scale_tilt2.set("-"+angles[3][:-1])
        #print(pan10, tilt10, pan20, tilt20)

         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5
        self.update()

        self.window.mainloop()

    def StartValues(self):
        height = float(self.entry_height.get())
        distance = float(self.entry_distance.get())
        return height,distance;


    def calibrate(self):
         # Calibrate the cameras and make scales for camera two disappear
         self.scale_pan2.grid_remove()
         self.scale_tilt2.grid_remove()
         self.label_pan2.grid_remove()
         self.label_tilt2.grid_remove()
         self.button_calibrate.grid_remove()
         self.button_reset.grid()

         global pan10
         global pan20
         global h
         global R
         pan10,t10,pan20,t20 = newCalibration()
         h, R = self.StartValues()
         print("h",h)

         global B
         B = getB(h,0,0)

         self.scale_focus.config(from_=h)
         self.entry_height.grid_remove()
         self.label_height.grid_remove()
         self.entry_distance.grid_remove()
         self.label_distance.grid_remove()
         self.scale_focus.grid()
         self.label_focus.grid()
         self.scale_pan1.config(command=self.pan1cfg)
         self.scale_tilt1.config(command=self.tilt1cfg)
         file = open("angles.txt","w")
         L=[str(pan10),"\n",str(tilt10),"\n",str(pan20),"\n",str(tilt20),"\n"]
         file.writelines(L)
         file.close()
    def reset(self):
         self.scale_pan2.grid()
         self.scale_tilt2.grid()
         self.label_pan2.grid()
         self.label_tilt2.grid()
         self.button_calibrate.grid()
         self.button_reset.grid_remove()
         self.entry_height.grid()
         self.label_height.grid()
         self.entry_distance.grid()
         self.label_distance.grid()
         self.scale_focus.grid_remove()
         self.label_focus.grid_remove()
         self.scale_pan1.config(command=self.pan1)
         self.scale_tilt1.config(command=self.tilt1)
         tiltCameras(tilt10,1)
         tiltCameras(tilt20,2)
         panCameras(pan10,1)
         panCameras(pan20,2)
    def tilt1(obj,value):

        tiltCameras(value, 1)

    def tilt2(obj,value):

        tiltCameras(value, 2)

    def pan1(obj,value):

        panCameras(value, 1)

    def pan2(obj,value):

        panCameras(value, 2)


    def tilt1cfg(obj,value):
        tiltCameras(value, 1)
        pan1, tilt1 = getPositionCam1()
        virPan = getVirtualPan(pan1,pan10)
        tilt2 = getTilt2(virPan, tilt1,R,B,h,personHeight)
        print("virpan",virPan,"tilt1", tilt1,"R",R,"B",B,"h",h,"personHeight",personHeight,"tilt2",tilt2)
        tiltCameras(tilt2, 2)

    def pan1cfg(obj,value):

        panCameras(value, 1)
        pan1, tilt1 = getPositionCam1()
        virPan = getVirtualPan(pan1,pan10)
        virPan2 = getPan2(virPan, tilt1,R,B)
        pan2 = pan20 - virPan2
        print("virPan",virPan,"tilt1",tilt1,"R",R,"B",B,"pan2",virPan2)
        panCameras(pan2, 2)

    def focusHeight(obj,value):
        pan1, tilt1 = getPositionCam1()
        global B
        B = getB(h,tilt1,value)
        global personHeight
        personHeight = value

        pan1, tilt1 = getPositionCam1()
        virPan = getVirtualPan(pan1,pan10)
        tilt2 = getTilt2(virPan, tilt1,R,B,h,personHeight)
        print("virpan",virPan,"tilt1", tilt1,"R",R,"B",B,"h",h,"personHeight",personHeight,"tilt2",tilt2)
        tiltCameras(tilt2, 2)
        virPan2 = getPan2(virPan, tilt1,R,B)
        pan2 = pan20 - virPan2
        print("virPan",virPan,"tilt1",tilt1,"R",R,"B",B,"pan2",virPan2)
        panCameras(pan2, 2)



    def update(self):
         # Get a frame from the video source

         ret1, frame1, ret2, frame2 = self.vid1.get_frame()


         if ret1 and ret2:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tk.NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=tk.NW)

         self.window.after(self.delay, self.update)


class MyVideoCapture:
    #
     def __init__(self, video_source1, video_source2):
         # Open the video source
         #self.vid = cv2.VideoCapture(video_source)
         self.vid1 = cv2.VideoCapture(video_source1)
         self.vid2 = cv2.VideoCapture(video_source2)
         if not self.vid1.isOpened():
             raise ValueError("Unable to open video source", video_source1)

         # Get video source width and height
         print("Nu ar jag i MyvideoCapture")
         self.width = self.vid1.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid1.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):
         if self.vid1.isOpened() and self.vid2.isOpened():

             ret1, frame1 = self.vid1.read()
             ret2, frame2 = self.vid2.read()
             frame1 = cv2.resize(frame1, (600, 400))
             frame2 = cv2.resize(frame2, (600, 400))
             if ret1 and ret2:
                 # Return a boolean success flag and the current frame converted to BGR
                 return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
             else:
                 return ret1, None, ret2, None
         else:
             return ret1, None, ret2, None

     # Release the video source when the object is destroyed
     def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
        if self.vid2.isOpened():
            self.vid2.release()

 # Create a window and pass it to the Application object
App(tk.Tk(), "Gemensam kamerastyrning")
window.mainloop()
