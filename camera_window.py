import tkinter as tk
import cv2
import PIL.ImageTk
import PIL.Image
import time

#window = tk.Tk()
#greeting = tk.Label(text="Hello, Tkinter")
#greeting.pack()
#captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')
captureStor = cv2.VideoCapture('http://169.254.203.231')


class App:
    def __init__(self, window, window_title, video_source1='rtsp://root.pass@169.254.203.231/axis-media/media.amp', video_source2='rtsp://root.pass@169.254.135.93/axis-media/media.amp'):
        self.window = window
        self.window.title(window_title)
        self.video_source1 = video_source1
        self.video_source2 = video_source2

     # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)


         # Create a canvas that can fit the above video source size
        self.canvas1 = tk.Canvas(window, width=600, height=400)
        self.canvas2 = tk.Canvas(window, width=600, height=400)
        self.canvas1.pack(padx=5, pady=10, side="left")
        self.canvas2.pack(padx=5, pady=60, side="left")

        #self.canvas = tk.Canvas(window, width = self.vid1.width+self.vid2.width, height = self.vid1.height)
        #self.canvas.pack()

         # Button that lets the user take a snapshot
        #self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 5
        self.update()

        self.window.mainloop()

    def snapshot(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
                cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
         # Get a frame from the video source
         #print("Nu är jag i update")
         ret1, frame1, ret2, frame2 = self.vid1.get_frame()
         #ret, frame1 = self.vid1.get_frame()
         #ret, frame2 = self.vid2.get_frame()
         #print(frame)

         if ret1 and ret2:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tk.NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=tk.NW)

             #self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame1))
             #self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
             #print(self.photo)
             #self.canvas.create_image(0, 0, image = self.photo1, anchor = tk.NW)
             #self.canvas.create_image(0, 0, image = self.photo2, anchor = tk.NE)

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
App(tk.Tk(), "Tkinter and OpenCV")
window.mainloop()
