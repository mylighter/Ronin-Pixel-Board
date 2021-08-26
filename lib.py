from pygame_tool import *
import pygame
import tkinter


class Board(object):
    def __init__(self, screen, width=20, height=11, pixel=20):
        self.board = []
        self.color = []
        self.screen_rect = screen.get_rect()
        self.mouse_flag = False
        for x in range(width * height):
            rect = pygame.rect.Rect(0, 0, pixel, pixel)
            rect.left = self.screen_rect.left + x % width * pixel
            rect.top = self.screen_rect.top + int(x / width) * pixel
            self.board.append(rect)

    def update(self, event, color, method, target_color):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_flag = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_flag = False
        if self.mouse_flag:
            x, y = pygame.mouse.get_pos()
            for index, px in enumerate(self.board):
                if px.collidepoint(x, y):
                    if method == 'e':
                        color[index] = (255, 255, 255)
                    elif method == 'p':
                        color[index] = target_color

    def blit(self, screen, color):
        for index, pixel in enumerate(self.board):
            screen.fill(color[index], pixel)


class ColorConsole(object):
    def __init__(self, height=116, width=480, bg_color=(101, 203, 255), font='STKaiti'):
        self.rect = pygame.rect.Rect(0, 0, width, height)
        self.hue_ctrl = Slipper()
        self.hue_msg = Text('颜色', font=font, size=16)
        self.value_ctrl = Slipper()
        self.value_msg = Text('亮度', font=font, size=16)
        self.eraser_sw = Switch('橡皮', font=font)
        self.seal_sw = Switch('印章', font=font)
        self.view = Text('预览颜色', font=font)
        self.color = bg_color
        self.block = pygame.rect.Rect(0, 0, 24, 16)

    def compose(self, dist=10):
        self.hue_msg.rect.left = self.rect.left + dist
        self.hue_msg.rect.top = self.rect.top + dist
        self.hue_ctrl.rect.left = self.hue_msg.rect.left
        self.hue_ctrl.rect.top = self.hue_msg.rect.bottom + dist
        self.hue_ctrl.compose()

        self.value_msg.rect.left = self.rect.left + dist
        self.value_msg.rect.top = self.hue_ctrl.rect.bottom + dist
        self.value_ctrl.rect.left = self.value_msg.rect.left
        self.value_ctrl.rect.top = self.value_msg.rect.bottom + dist
        self.value_ctrl.compose()

        self.eraser_sw.rect.top = self.rect.top + 20
        self.eraser_sw.rect.left = self.hue_ctrl.rect.right + 60
        self.seal_sw.rect.top = self.eraser_sw.rect.bottom + dist
        self.seal_sw.rect.left = self.eraser_sw.rect.left
        self.view.rect.top = self.seal_sw.rect.bottom + dist
        self.view.rect.right = self.seal_sw.rect.left

        self.block.left = self.view.rect.right
        self.block.centery = self.view.rect.centery

        self.eraser_sw.compose()
        self.seal_sw.compose()

    def update(self, event):
        self.hue_ctrl.update(event)
        self.value_ctrl.update(event)
        self.eraser_sw.update(event)
        self.seal_sw.update(event)

    def blit(self, screen, tc):
        screen.fill(self.color, self.rect)
        screen.fill(tc, self.block)
        self.hue_ctrl.blit(screen)
        self.value_ctrl.blit(screen)
        self.hue_msg.blit(screen)
        self.value_msg.blit(screen)
        self.seal_sw.blit(screen)
        self.eraser_sw.blit(screen)
        self.view.blit(screen)


class Switch(object):
    def __init__(self, prep, texts=('on', 'off'), font='Arial', size=12, color=(200, 200, 200),
                 button_color=(100, 100, 100), height=20, width=40):
        self.button = ActiveButton(texts=texts, size=(height, width*0.6), color=button_color, font=font, text_size=size)
        self.rect = pygame.rect.Rect(0, 0, width, height)
        self.color = color
        self.prep = Text(prep, font=font, size=size)

    def update(self, event):
        self.button.update(event)

    def compose(self):
        if self.button.status:
            self.button.rect.right = self.rect.right
        else:
            self.button.rect.left = self.rect.left
        self.button.rect.top = self.rect.top
        self.button.compose()
        self.prep.rect.right = self.rect.left
        self.prep.rect.top = self.rect.top
        self.prep.rect.centery = self.rect.centery

    def blit(self, screen):
        screen.fill(self.color, self.rect)
        self.button.blit(screen)
        self.prep.blit(screen)


class SealPanel(object):
    def __init__(self):
        self.seal_list = [str(i + 1) for i in range(6)]
        self.seal = 0
        self.panel = []
        for index, seal in enumerate(self.seal_list):
            img = pygame.image.load('resources\\seal\\%s.png' % seal)
            rect = img.get_rect()
            self.panel.append((index, img, rect))

    def blit(self, screen, left, top):
        pixel = 50
        for x, img, rect in self.panel:
            rect.left = left + x % 3 * pixel
            rect.top = top + int(x / 3) * pixel
            screen.blit(img, rect)

    def update(self, event):
        x, y = pygame.mouse.get_pos()
        for i, img, rect in self.panel:
            if rect.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
                self.seal = i


class Seal(object):
    def __init__(self, seal_list):
        self.seals = []
        self.seal_list = seal_list
        self.seal = 0
        self.rect = self.seal_list[self.seal][2]

    def update(self, event):
        x, y = pygame.mouse.get_pos()
        self.rect.center = (x, y)
        if event.type == pygame.MOUSEBUTTONDOWN and y < 264:
            self.create_seal(self.seal, x, y)

    def blit(self, screen):
        for img, rect, i in self.seals:
            screen.blit(img, rect)

    def create_seal(self, num, x, y):
        new_seal = self.seal_list[num][1]
        new_rect = new_seal.get_rect()
        new_rect.center = (x, y)
        self.seals.append((new_seal, new_rect, num))


def ask():
    def get_val():
        f = open('val.vl', mode='w')
        f.write(entry.get())
        f.close()
        window.destroy()

    window = tkinter.Tk()
    window.geometry('200x20')
    entry = tkinter.Entry(window)
    entry.place(anchor='nw')
    submit = tkinter.Button(window, text='Submit', command=get_val)
    submit.pack(side='right')
    window.mainloop()


def ask_and_get_val():
    ask()
    f = open('val.vl')
    val = f.read()
    f.close()
    return val
