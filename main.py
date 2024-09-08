import os
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, Frame
from tkinter import font as tkfont
import yt_dlp
import vlc
class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stylish Media Player")
        self.root.geometry("500x400")
        self.root.configure(bg="#1E1E1E")
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_bg = "#4CAF50"
        self.button_fg = "#FFFFFF"
        self.status_bg = "#333333"
        self.status_fg = "#76FF03"
        self.title_label = Label(root, text="Media Player By OmarNabill", font=self.title_font, bg="#1E1E1E", fg="#FFFFFF")
        self.title_label.pack(pady=15)
        self.input_frame = Frame(root, bg="#1E1E1E")
        self.input_frame.pack(pady=10)
        self.url_label = Label(self.input_frame, text="YouTube URL:", font=self.label_font, bg="#1E1E1E", fg="#FFFFFF")
        self.url_label.grid(row=0, column=0, padx=10, pady=5)
        self.url_entry = Entry(self.input_frame, width=45, font=self.label_font)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)
        self.download_button = Button(root, text="Download", command=self.download_media, bg=self.button_bg,
                                      fg=self.button_fg, font=self.label_font, relief="flat")
        self.download_button.pack(pady=10)
        self.path_button = Button(root, text="Choose Download Path", command=self.choose_download_path,
                                  bg=self.button_bg, fg=self.button_fg, font=self.label_font, relief="flat")
        self.path_button.pack(pady=10)
        self.play_button = Button(root, text="Play Local Media", command=self.play_local_media, bg=self.button_bg,
                                  fg=self.button_fg, font=self.label_font, relief="flat")
        self.play_button.pack(pady=10)
        self.status = StringVar()
        self.status.set("Status: Waiting")
        self.status_label = Label(root, textvariable=self.status, bg=self.status_bg, fg=self.status_fg,
                                  font=self.label_font, padx=10, pady=5)
        self.status_label.pack(pady=15, fill="x")
        self.download_path = r"C:\Users\Dell\PycharmProjects"  # Default download path
        self.player = vlc.MediaPlayer()

    def choose_download_path(self):
        selected_path = filedialog.askdirectory(initialdir=self.download_path, title="Select Download Directory")
        if selected_path:
            self.download_path = selected_path
            self.status.set(f"Status: Download path set to {self.download_path}")

    def download_media(self):
        url = self.url_entry.get()
        if not url:
            self.status.set("Status: Please enter a URL")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                self.media_file = os.path.join(self.download_path, f"{info_dict['title']}.{info_dict['ext']}")
                self.status.set(f"Status: Downloaded {info_dict['title']}")
        except Exception as e:
            self.status.set(f"Status: Error - {str(e)}")

    def play_local_media(self):
        file_path = filedialog.askopenfilename(filetypes=[("Media files", "*.mp4 *.mp3 *.avi *.mov *.wav")])
        if file_path:
            self.media_file = file_path
            self.player.set_media(vlc.Media(file_path))
            self.player.play()
            self.status.set(f"Status: Playing {os.path.basename(file_path)}")
        else:
            self.status.set("Status: No file selected")
if __name__ == "__main__":
    root = Tk()
    media_player = MediaPlayer(root)
    root.mainloop()
