import pygame
import os

version = 'Alpha 3'
absolute_path = os.path.dirname(os.path.abspath(__file__))


class Text(object):
    def __init__(self, text, color=(0, 0, 0), font='Arial', size=12):
        pygame.font.init()
        self.color = color
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect()

    def set_center(self, screen_rect):
        self.rect.centerx = screen_rect.centerx

    def blit(self, screen):
        screen.blit(self.text, self.rect)


class ActiveText(object):
    def __init__(self, color=(0, 0, 0), font='Arial', size=12):
        pygame.font.init()
        self.color = color
        self.font = pygame.font.SysFont(font, size)
        self.text = None
        self.rect = None

    def set_text(self, text):
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect()

    def blit(self, screen):
        screen.blit(self.text, self.rect)


class Button(object):
    def __init__(self, prep, prep_size=12, font='Arial', color=(200, 200, 200), size=(10, 20)):
        self.rect = pygame.rect.Rect(0, 0, size[1], size[0])
        self.prep = Text(prep, size=prep_size, font=font)
        self.status = False
        self.color = color

    def update(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
            self.status = not self.status

    def compose(self):
        self.prep.rect.center = self.rect.center

    def blit(self, screen):
        screen.fill(self.color, self.rect)
        self.prep.blit(screen)


class ActiveButton(object):
    def __init__(self, texts=('on', 'off'), text_size=12, font='Arial', color=(200, 200, 200), size=(10, 20)):
        self.rect = pygame.rect.Rect(0, 0, size[1], size[0])
        self.text = ActiveText(size=text_size, font=font)
        self.status = False
        self.texts = texts
        self.color = color

    def update(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
            self.status = not self.status
        if self.status:
            self.text.set_text(self.texts[0])
        else:
            self.text.set_text(self.texts[1])

    def compose(self):
        self.text.rect.center = self.rect.center

    def blit(self, screen):
        screen.fill(self.color, self.rect)
        self.text.blit(screen)


class TriggerButton(Button):
    def update(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
            self.status = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.status = False


class List(object):
    def __init__(self, values, font='arial'):
        self.list = values
        self.font = pygame.font.SysFont(font, 20)

    def blit(self, screen, start_pos=(0, 0)):
        for cont in self.list:
            text = self.font.render(cont, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.centerx = start_pos[0]
            text_rect.centery = start_pos[1] + self.list.index(cont) * 20
            screen.blit(text, text_rect)


class DataRect(object):
    def __init__(self, data, total, width=100, height=20, color=(48, 112, 255), background=(240, 240, 240),
                 percentage=True):
        self.rect = pygame.Rect(0, 0, width, height)
        self.bg_color = background
        self.ratio = round(data / total * 100) / 100
        self.data_rect = pygame.Rect(0, 0, int(self.ratio * width), height)
        self.color = color
        if percentage:
            self.info = '%0.1f (%0.1f%s)' % (float(data), self.ratio*100, '%')
        else:
            self.info = '%0.1f' % float(data)
        self.text = Text(self.info)

    def compose(self):
        self.data_rect.centery = self.rect.centery
        self.data_rect.left = self.rect.left
        self.text.rect.centery = self.rect.centery
        self.text.rect.left = self.rect.right + 15

    def blit(self, screen, show_info=True):
        screen.fill(self.bg_color, rect=self.rect)
        screen.fill(self.color, rect=self.data_rect)
        if show_info:
            self.text.blit(screen)


class BarChart(object):
    def __init__(self, data: dict, font='Arial', size=12, color=(0, 0, 0), columns_limit=12):
        self.data = data
        if len(self.data.items()) > columns_limit:
            self.data = dict(tuple(self.data.items())[:columns_limit])
        self.font = pygame.font.SysFont(font, size)
        self.data_lines = []
        self.total = data[max(data, key=lambda a:data[a])]
        for prep, datum in self.data.items():
            msg = self.font.render(prep, True, color)
            self.data_lines.append(
                (msg, msg.get_rect(), DataRect(datum, self.total, width=400, height=25, percentage=False)))

    def compose(self, top, left):
        i = 0
        for prep, prep_rect, rect in self.data_lines:
            rect.rect.top = top + 32 * i
            rect.rect.left = left + 72
            rect.compose()
            prep_rect.centery = rect.rect.centery
            prep_rect.left = left
            i += 1

    def blit(self, screen):
        for prep, prep_rect, rect in self.data_lines:
            screen.blit(prep, prep_rect)
            rect.blit(screen)


class PercentageBarChart(BarChart):
    def __init__(self, data: dict, total, font='Arial', size=12, color=(0, 0, 0)):
        self.data = data
        self.font = pygame.font.SysFont(font, size)
        self.data_lines = []
        for prep, datum in data.items():
            msg = self.font.render(prep, True, color)
            self.data_lines.append((msg, msg.get_rect(), DataRect(datum, total, width=400, height=25)))


class Slipper(object):
    def __init__(self, width=100, height=10, bg_color=(100, 100, 100), color=(200, 200, 200)):
        self.width = width
        self.height = height
        self.color = bg_color
        self.slipper_color = color
        self.rect = pygame.rect.Rect(0, 0, width, height)
        self.slipper = pygame.rect.Rect(0, 0, 5, 20)
        self.value = 0
        self.flag = False

    def update(self, event):
        x, y = pygame.mouse.get_pos()
        if self.slipper.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.flag = False
        if self.flag:
            if self.rect.left < x < self.rect.right:
                self.slipper.centerx = x

        self.value = (self.slipper.centerx - self.rect.left) / self.width

    def compose(self):
        self.slipper.centerx = self.rect.left + self.value * self.width
        self.slipper.centery = self.rect.centery

    def blit(self, screen):
        screen.fill(self.color, self.rect)
        screen.fill(self.slipper_color, self.slipper)
