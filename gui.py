import tkinter as tk
import io
from PIL import Image, ImageTk
import check
from urllib import request
from urllib.request import urlopen
import manga

window = tk.Tk()
window.title = '动漫之家'

# window.geometry('300x300')

frm = tk.Frame(window)


def download(self, url):
    self.strvar.set('下载中')
    manga.download_comic(url)
    self.strvar.set('已下载')


class Comic:
    def __init__(self, root, title, chapter, image, url):
        self.frame = tk.Frame(root)
        self.strvar = tk.StringVar()
        self.strvar.set('下载')
        self.label = tk.Label(self.frame, bg='white', image=image, compound='top', text=title + chapter) \
            .grid(row=0, column=1, padx=10, pady=10)
        self.btn = tk.Button(self.frame, textvariable=self.strvar, width=15, height=2,
                             command=lambda: download(self, url)) \
            .grid(row=1, column=1)


def print_comic():
    clear_comic()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'http://www.dmzj.com/category'
    }
    comic_list = check.get_my_rss('', '')  # 输入用户名密码
    row, column = 1, 0
    img_list = []
    for i, item in enumerate(comic_list):
        if column == 3:
            row += 1
            column = 0
        rq = request.Request(item['img'], headers=headers)
        image_bytes = urlopen(rq).read()
        data_stream = io.BytesIO(image_bytes)
        im = Image.open(data_stream).resize((88, 118), Image.ANTIALIAS)
        img_list.append(ImageTk.PhotoImage(im))
        # text = item['title'] + item['chapter']
        print(img_list[i])

        Comic(frm, item['title'], item['chapter'], img_list[i], item['url']).frame.grid(row=row, column=column, padx=10,
                                                                                        pady=10)
        # tk.Label(frm, bg='white', image=img_list[i], compound='top', text=text).grid(row=row, column=column,
        #                                                                              padx=10, pady=10)

        column += 1
    frm.grid(row=1, column=1)
    window.mainloop()


def clear_comic():
    frm.grid_forget()


frm_btn = tk.Frame()
b1 = tk.Button(frm_btn, text='检查更新漫画', width=15, height=2, command=print_comic)
b1.pack()
b1 = tk.Button(frm_btn, text='清除列表', width=15, height=2, command=clear_comic)
b1.pack()
frm_btn.grid(row=0, column=1, padx=10, pady=10)

window.mainloop()
