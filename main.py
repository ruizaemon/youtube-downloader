import tkinter
import customtkinter
import os
from pytube import YouTube, Playlist

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green") # blue, dark-blue, green

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # App frame
        self.x_dimension = 600
        self.y_dimension = 550
        self.geometry(f"{self.x_dimension}x{self.y_dimension}")
        self.title("Youtube downloader")
        self.minsize(300,300)

        # Grid
        self.total_rows = 4
        self.total_columns = 3
        # self.grid_rowconfigure((0,1,2,3), weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_columnconfigure(2, weight=0)

        # ----- Row 0 ----- #
        # UI elements
        self.title = customtkinter.CTkLabel(self, text="Insert a youtube link (video / playlist)")
        self.title.grid(row=0, column=0, columnspan=self.total_columns, padx=10, pady=(10,0))

        # ----- Row 1 ----- #
        # Link entry box
        self.url_var = tkinter.StringVar() # string variable
        self.link_entryBox = customtkinter.CTkEntry(self, height=40, textvariable=self.url_var)
        self.link_entryBox.grid(row=1, column=0, columnspan=self.total_columns, sticky="ew", padx=20, pady=(5,10))

        # ----- Row 2 ----- #
        # Folder entry box
        self.folder_var = tkinter.StringVar() # string variable
        self.folder_entryBox = customtkinter.CTkEntry(self, height=40, textvariable=self.folder_var)
        self.folder_entryBox.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(20,10))

        # Choose folder button
        self.openFolder_button = customtkinter.CTkButton(self, text="Choose folder", command=self.openFolder)
        self.openFolder_button.grid(row=2, column=2, padx=(0,20), pady=10)

        # ----- Row 3 ----- #
        # Frame
        self.checkbox_frame = customtkinter.CTkFrame(self, height=40)
        self.checkbox_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(20,10), pady=(10,0))

        # Video & Audio checkbox
        self.videoCheck_var = tkinter.StringVar()
        self.video_checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text="Video", command=self.video_checkbox_event, variable=self.videoCheck_var, onvalue="on", offvalue="off")
        self.video_checkbox.deselect() # default "off"
        self.video_checkbox.grid(row=0, column=0, padx=70, pady=10) # idk why checkboxes are not centered in their columns (padx70 for now)

        self.audioCheck_var = tkinter.StringVar()
        self.audio_checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text="Audio-only", command=self.audio_checkbox_event, variable=self.audioCheck_var, onvalue="on", offvalue="off")
        self.audio_checkbox.deselect() # default "off"
        self.audio_checkbox.grid(row=0, column=1, pady=10, sticky="ew")

        # check if song exists in folder checkbox
        # self.existsInFolder_var = tkinter.StringVar()
        # self.existsInFolder_checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text="Check songs in folder", command=self.check_folder_event, variable=self.existsInFolder_var, onvalue="on", offvalue="off")
        # self.audio_checkbox.deselect() # default "off"
        # self.audio_checkbox.grid(row=0, column=1, pady=10, sticky="ew")

        # Download button
        self.download_button = customtkinter.CTkButton(self, text="Download", command=self.startDownload)
        self.download_button.grid(row=3, column=2, padx=(0,20), pady=(10,0))

        # ----- Row 4 ----- #
        # Textbox
        textboxColor = "#03fcfc"
        self.textbox = customtkinter.CTkTextbox(self, wrap="none", text_color=textboxColor)
        self.textbox.grid(row=4, column=0, columnspan=self.total_columns, padx=20, pady=20, sticky="nsew")

        # ----- Row 5 ----- #
        # Progress percentage
        self.pPercentage = customtkinter.CTkLabel(self, text="0%")
        self.pPercentage.grid(row=5, column=2, pady=(0,20))

        # Progress bar
        self.progressBar = customtkinter.CTkProgressBar(self)
        self.progressBar.set(0) # 0 to 1
        self.progressBar.grid(row=5, column=0, columnspan=2, pady=(0,20), padx=20, sticky="ew")


        ## DEBUG BUTTON ##
        # self.debugbutton = customtkinter.CTkButton(self, text="Debug", command=self.debug)
        # self.debugbutton.grid(row=5, column=self.total_columns-1, padx=20, pady=(0,20))

    def debug(self):
        print(self.folder_var.get())
        song_list = os.listdir(self.folder_var.get())
        new_song_list = []
        for song in song_list:
            print(os.path.splitext(song)[0])
    
    def openFolder(self):
        temp_var = tkinter.filedialog.askdirectory() # string
        self.folder_var.set(temp_var) # .set to change StringVar object

    # only allow 1 checkbox to be checked (video/audio)
    def video_checkbox_event(self):
        if self.videoCheck_var.get() == "on": 
            self.audio_checkbox.configure(state="disabled")
        if self.videoCheck_var.get() == "off":
            self.audio_checkbox.configure(state="normal")

    def audio_checkbox_event(self):
        if self.audioCheck_var.get() == "on":
            self.video_checkbox.configure(state="disabled")
        if self.audioCheck_var.get() == "off":
            self.video_checkbox.configure(state="normal")

    def startDownload(self):
        self.linkType = ""
        # if link is invalid, display error msg and return
        # else, set the type of link (playlist or youtube)
        try:
            self.ytLink = self.link_entryBox.get()
            if "playlist" in self.ytLink:
                self.plObject = Playlist(self.ytLink)
                self.linkType = "playlist" # set link type
            else:
                self.ytObject = YouTube(self.ytLink, on_progress_callback=self.on_progress) # for progress bar
                self.linkType = "one_video" # set link type
        except Exception as e:
            self.textbox.insert("0.0", "Youtube link is invalid!\n")
            print("Youtube link is invalid. Error message: ", e) # for debugging
            return

        # if folder is not selected, display error msg and return
        if self.folder_var.get() == '':
            self.textbox.insert("0.0", "Select a folder!\n")
            return
        # if folder path does not exist, display error msg and return
        path = self.folder_var.get()
        if os.path.exists(path) == False:
            self.textbox.insert("0.0", "This path does not exist!\n")

        # if both checkboxes are unchecked, display error msg and return
        if (self.videoCheck_var.get() == "off" and self.audioCheck_var.get() == "off"):
            self.textbox.insert("0.0", "Select a download option (video/audio)\n")
            return

        # check folder for song/video titles that are already downloaded
        songVideos_inFolder = os.listdir(self.folder_var.get())
        self.new_song_list = []
        self.new_song_list.clear()
        for mp4 in songVideos_inFolder:
            nameOnly = os.path.splitext(mp4)[0] # remove .mp4
            self.new_song_list.append(nameOnly)
        
        # if playlist, run playlistDownload
        if self.linkType == "playlist":
            self.playlistDownload()

        # if single video, run youtubeDownload
        if self.linkType == "one_video":
            self.youtubeDownload()
        
    def playlistDownload(self):
        # if audio only
        count = 1
        failed_count = 0
        # self.plObject -> list of youtube links in the playlist
        for link in self.plObject: # self.plObject.videos returns a list of Youtube objects
            video = YouTube(link, on_progress_callback=self.on_progress)

            # reset progress bar and percentage before every video
            self.progressBar.set(0)
            self.pPercentage.configure(text="0%")
            self.pPercentage.update()

            try:
                title = video.title
                if title in self.new_song_list:
                    # skip songs/videos that already exist in the folder
                    self.textbox.insert("0.0", f"*{count}. {title} already exists in this folder\n")
                    count += 1
                    continue
                elif self.audioCheck_var.get() == "on": # audio
                    self.audioDownload(video, count)
                    count += 1   
                elif self.videoCheck_var.get() == "on": # video
                    self.videoDownload(video, count)
                    count += 1

            except Exception as e:
                self.textbox.insert("0.0", f"{count}. Download failed\n")
                print("Video in playlist download failed. Error message: ", e)
                count += 1
                failed_count += 1
                continue
        
        # end of loop, show number of failed downloads
        print(f"Failed downloads: {failed_count}") # debug
        if failed_count >= 1:
            self.textbox.insert("0.0", "-"*100 + "\n")
            self.textbox.insert("0.0", f"{failed_count} download(s) failed. Sorry!\nRetry playlist download or download the failed video on its own.\n")
            self.textbox.insert("0.0", "-"*100 + "\n")
        else:
            self.textbox.insert("0.0", "-"*100 + "\n")
            self.textbox.insert("0.0", f"Download complete!\n")
            self.textbox.insert("0.0", "-"*100 + "\n")

    def youtubeDownload(self):
        try:
            if (self.audioCheck_var.get() == "on"): # audio
                self.audioDownload(self.ytObject, 0) # self.ytObject is a Youtube object (with progress callback)
            elif (self.videoCheck_var.get() == "on"): # video
                self.videoDownload(self.ytObject, 0)
            self.textbox.insert("0.0", f"Download complete!\n")
        except Exception as e:
            self.textbox.insert("0.0", "Single download failed. Please try again.\n")
            print("Single download failed. Error message:", e)
            return

    def audioDownload(self, video, count):
        title = video.title
        audio = video.streams.get_audio_only()
        # audio_streams = video.streams.filter(only_audio=True) # list of audio-only stream objects
        # first_stream = audio_streams.first() # takes the first stream
        audio.download(self.folder_var.get())
        self.textbox.insert("0.0", f"{count}. {title} has been downloaded\n")

    def videoDownload(self, video, count):
        title = video.title
        highRes_video = video.streams.get_highest_resolution()
        highRes_video.download(self.folder_var.get())
        self.textbox.insert("0.0", f"{count}. {title} has been downloaded\n")
    
    # function passed into youtube object 
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        per = str(int(percentage_of_completion))
        # update progress bar
        self.progressBar.set(float(percentage_of_completion)/100)
        # update displayed percentage
        self.pPercentage.configure(text=per + "%")
        self.pPercentage.update()

if __name__ == "__main__":
    app = App()
    app.mainloop()