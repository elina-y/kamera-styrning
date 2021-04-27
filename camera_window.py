import tkinter as tk
import cv2
import PIL.ImageTk
import PIL.Image
import time

#window = tk.Tk()
#greeting = tk.Label(text="Hello, Tkinter")
#greeting.pack()
#captureStor = cv2.VideoCapture('rtsp://root.pass@169.254.203.231/axis-media/media.amp')
captureStor = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')


class App:
    def __init__(self, window, window_title, video_source='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

     # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

         # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

         # Button that lets the user take a snapshot
        self.btn_snapshot=tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
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
         ret, frame = self.vid.get_frame()
         #print(frame)

         if ret:
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             #print(self.photo)
             self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

         self.window.after(self.delay, self.update)


class MyVideoCapture:
     def __init__(self, video_source='rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

 # Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV")
window.mainloop()
