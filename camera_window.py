import tkinter as tk
import cv2
import PIL.ImageTk
import PIL.Image
import time


#captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')
captureStor = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
kameraLiten='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'
kameraStor='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'


class App:
    def __init__(self, window, window_title, video_source1=kameraLiten, video_source2=kameraStor):
        self.window = window
        self.window.title(window_title)
        self.video_source1 = video_source1
        self.video_source2 = video_source2


     # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)


         # Create a canvas that can fit the above video source size
        self.canvas1 = tk.Canvas(window, width=600, height=400)
        self.canvas2 = tk.Canvas(window, width=600, height=400)
        self.canvas1.grid(padx=10, pady=10, columnspan=2, row=0, column=0)
        self.canvas2.grid(padx=10, pady=10, columnspan=2, row=0, column=3)

        #self.canvas1.pack(padx=5, pady=10, side="left")
        #self.canvas2.pack(padx=5, pady=60, side="left")




         # Button that lets the user take a snapshot
        #self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.scale_pan1 = tk.Scale(window, from_=-180, to=180, orient=tk.HORIZONTAL)
        #self.scale_pan1.pack(anchor=tk.SE, expand=True)
        self.scale_pan1.grid(padx=6, pady=10, row=1, column=0, sticky=tk.E, rowspan=2)
        self.label_pan1 = tk.Label(window, text="Pan")
        self.label_pan1.grid(row=1, column=0, sticky=tk.E, padx=40)

        self.scale_tilt1 = tk.Scale(window, from_=0, to=90, orient=tk.VERTICAL, command=self.tilt("tilt1"))
        self.scale_tilt1.grid(padx=5, pady=10, row=1, column=1, sticky=tk.W, rowspan=2)
        self.label_tilt1 = tk.Label(window, text="Tilt")
        self.label_tilt1.grid(row=1, column=1, sticky=tk.W, padx=50, rowspan=2)

        self.scale_pan2 = tk.Scale(window, from_=-180, to=180, orient=tk.HORIZONTAL)
        self.scale_pan2.grid(padx=5, pady=10, row=1, column=3, sticky=tk.E, rowspan=2)
        self.label_pan2 = tk.Label(window, text="Pan")
        self.label_pan2.grid(row=1, column=3, sticky=tk.E, padx=40)

        self.scale_tilt2 = tk.Scale(window, from_=0, to=90, orient=tk.VERTICAL)
        self.scale_tilt2.grid(padx=5, pady=10, row=1, column=4, sticky=tk.W, rowspan=2)
        self.label_tilt2 = tk.Label(window, text="Tilt")
        self.label_tilt2.grid(row=1, column=4, sticky=tk.W, padx=50, rowspan=2)

        self.button_calibrate = tk.Button(window, text="Calibrate", width=7, command=self.calibrate)
        self.button_calibrate.grid(row=1,column=2)
        self.button_reset = tk.Button(window, text="Reset", width=7, command=self.reset)
        self.button_reset.grid(row=2,column=2)
        self.button_reset.grid_remove()
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5
        self.update()

        self.window.mainloop()

    def snapshot(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
                cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def calibrate(self):
         # Calibrate the cameras and make scales for camera two disappear
         self.scale_pan2.grid_remove()
         self.scale_tilt2.grid_remove()
         self.label_pan2.grid_remove()
         self.label_tilt2.grid_remove()
         self.button_calibrate.grid_remove()
         self.button_reset.grid()

    def reset(self):
         self.scale_pan2.grid()
         self.scale_tilt2.grid()
         self.label_pan2.grid()
         self.label_tilt2.grid()
         self.button_calibrate.grid()
         self.button_reset.grid_remove()

    def tilt(value, title_scale):
        print(value)
        print(title_scale)

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
         print("Nu är jag i MyvideoCapture")
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
