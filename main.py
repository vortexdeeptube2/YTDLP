import threading
import tkinter as tk
from tkinter import messagebox

from yt_dlp import YoutubeDL


class DownloaderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("YT-DLP Downloader")

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(padx=10, pady=10)

        self.button = tk.Button(root, text="Baixar", command=self.start_download)
        self.button.pack(padx=10, pady=5)

        root.bind("<Return>", self.start_download)
        root.bind("<Escape>", self.clear_entry)
        root.bind("<Control-v>", self.paste_clipboard)

        self.entry.focus()

    def start_download(self, event=None) -> None:
        url = self.entry.get().strip()
        if not url:
            return
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url: str) -> None:
        opts = {"outtmpl": "%(title)s.%(ext)s"}
        try:
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Download concluído!"))
        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror("Erro", str(exc)))
        finally:
            self.root.after(0, self.clear_entry)

    def clear_entry(self, event=None) -> None:
        self.entry.delete(0, tk.END)

    def paste_clipboard(self, event=None) -> None:
        try:
            text = self.root.clipboard_get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text)
        except tk.TclError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
