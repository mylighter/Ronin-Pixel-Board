import colorsys
import tkinter.messagebox as msg_box
import tkinter


def hls2rgb(h, l, s):
    return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))


def rgb2hls(r, g, b):
    return tuple(i for i in colorsys.rgb_to_hls(r / 255, g / 255, b / 255))


def decode(code, pixel_total):
    h_l = [0.0 for x in range(pixel_total)]
    l_l = [1.0 for x in range(pixel_total)]
    s_l = [0.0 for x in range(pixel_total)]
    code_list = code.split('|')
    save_code = code_list[0]
    for index, val in enumerate(save_code):
        if index % 3 == 0:
            i = ord(val) - 30100
            if i >= pixel_total:
                window = tkinter.Tk()
                msg_box.showerror('DecodeError!',
                                  'DecodeError:The program cannot decode the save_code with current settings'
                                  )
                window.destroy()
                return None
            else:
                h = (ord(save_code[index + 2]) - 30100) / 200
                s = (ord(save_code[index + 1]) - 30000) / 200
                h_l[i] = h
                l_l[i] = s
                s_l[i] = 1.0

    color_code = tuple(zip(h_l, l_l, s_l))

    seal_code = []
    for index, val in enumerate(code_list[1]):
        if index % 3 == 0:
            num = int(val) - 1
            x = ord(code_list[1][index + 1]) - 30000
            y = 30240 - ord(code_list[1][index + 2]) + 180
            seal_code.append((num, (x, y)))

    return color_code, seal_code, code_list[2]


def encode(color_code, seal_code, name):
    code = ColorCode(color_code).to_hls()

    color_str = ''
    for index, color in enumerate(code):
        if not color == (0.0, 1.0, 0.0):
            color_str += chr(index + 30100)
            color_str += chr(int(color[1] * 200 + 30000))
            color_str += chr(int(color[0] * 200 + 30100))

    seal_str = ''
    for seal in seal_code:
        seal_str += str(seal[2] + 1)
        x = seal[1].centerx + 30000
        y = 30240 - seal[1].centery + 180
        seal_str += chr(x)
        seal_str += chr(y)

    return '%s|%s|%s' % (color_str, seal_str, name)


class ColorCode(object):
    def __init__(self, code):
        self.code = code

    def to_rgb(self):
        rgb_colors = []
        for h, l, s in self.code:
            changed_color = hls2rgb(h, l, s)
            rgb_colors.append(changed_color)
        return rgb_colors

    def to_hls(self):
        hls_colors = []
        for r, g, b in self.code:
            changed_color = rgb2hls(r, g, b)
            hls_colors.append(changed_color)
        return hls_colors
