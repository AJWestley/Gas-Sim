class Button:

    def __init__(self, x, y, width, height, text, border_thickness=0, font_size=24, fill_colour=(192, 244, 255),
                 border_colour=(5, 5, 5), hover_colour=(200, 170, 170), text_mult=0.23):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.fill = fill_colour
        self.border = border_colour
        self.hover = hover_colour
        self.active_fill = fill_colour
        self.tm = text_mult

    def check_over(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.active_fill = self.hover
            return True
        self.active_fill = self.fill
        return False

    def draw(self, pg, screen):
        pg.draw.rect(screen, self.border, (self.x, self.y, self.width, self.height))
        pg.draw.rect(screen, self.active_fill,
                     (self.x + self.border_thickness, self.y + self.border_thickness,
                      self.width - 2 * self.border_thickness, self.height - 2 * self.border_thickness))
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.border)
        screen.blit(text, (self.x + self.tm * self.width, self.y + 0.35 * self.height))


class CheckBox:

    def __init__(self, x, y, height, text, border_thickness=0, font_size=24, fill_colour=(192, 244, 255),
                 border_colour=(5, 5, 5), hover_colour=(200, 170, 170), text_mult=0.23):
        self.x = x
        self.y = y
        self.height = height
        self.text = text
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.fill = fill_colour
        self.border = border_colour
        self.hover = hover_colour
        self.active_fill = fill_colour
        self.tm = text_mult
        self.checked = True

    def check_over(self, x, y):
        if self.x <= x <= self.x + self.height and self.y <= y <= self.y + self.height:
            self.active_fill = self.hover
            return True
        self.active_fill = self.fill
        return False

    def draw(self, pg, screen):
        pg.draw.rect(screen, self.border, (self.x, self.y, self.height, self.height))
        pg.draw.rect(screen, self.active_fill,
                     (self.x + self.border_thickness, self.y + self.border_thickness,
                      self.height - 2 * self.border_thickness, self.height - 2 * self.border_thickness))
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.border)
        screen.blit(text, (self.x - self.tm * self.height, self.y + 0.3 * self.height))
        st = "x" if self.checked else ""
        text = font.render(st, True, self.border)
        screen.blit(text, (self.x + 0.35 * self.height, self.y + 0.15 * self.height))

class TextInput:
    
    def __init__(self, x, y, width, height, text, border_thickness=0, font_size=24, fill_colour=(192, 244, 255),
                 border_colour=(5, 5, 5), hover_colour=(200, 170, 170), text_mult=0.23):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.value = "500"
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.fill = fill_colour
        self.border = border_colour
        self.hover = hover_colour
        self.active_fill = fill_colour
        self.tm = text_mult
        self.active = False
        
    def check_over(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.active_fill = self.hover
            return True
        self.active_fill = self.fill
        return False
    
    def draw(self, pg, screen):
        pg.draw.rect(screen, self.border, (self.x, self.y, self.width, self.height))
        pg.draw.rect(screen, self.active_fill,
                     (self.x + self.border_thickness, self.y + self.border_thickness,
                      self.width - 2 * self.border_thickness, self.height - 2 * self.border_thickness))
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.value, True, self.border)
        screen.blit(text, (self.x + self.tm * self.width, self.y + 0.35 * self.height))
        text = font.render(self.text, True, self.border)
        screen.blit(text, (self.x- 0.5 * self.width, self.y - 0.7 * self.height))
        
    def add(self, text: str):
        digit = text[0]
        if not digit.isdigit() or len(self.value) >= 4: return
        if self.value == '0': 
            self.value = digit
            return
        l = list(self.value)
        l.append(digit)
        self.value = ''.join(l)
        
    def backspace(self):
        if len(self.value) <= 1: self.value = '0'
        else: 
            self.value = self.value[:len(self.value)-1]
            
class IntensityButton:
    
    def __init__(self, x, y, width, height, text, values, displays, border_thickness=0, font_size=24, fill_colour=(192, 244, 255),
                 border_colour=(5, 5, 5), hover_colour=(200, 170, 170), text_mult=0.23):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        l = min(len(values), len(displays))
        self.values = values[:l]
        self.displays = displays[:l]
        self.current_val = 0
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.fill = fill_colour
        self.border = border_colour
        self.hover = hover_colour
        self.active_fill = fill_colour
        self.tm = text_mult

    def check_over(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.active_fill = self.hover
            return True
        self.active_fill = self.fill
        return False
    
    def increment(self):
        self.current_val += 1
        if self.current_val >= len(self.values): self.current_val = 0

    def draw(self, pg, screen):
        pg.draw.rect(screen, self.border, (self.x, self.y, self.width, self.height))
        pg.draw.rect(screen, self.active_fill,
                     (self.x + self.border_thickness, self.y + self.border_thickness,
                      self.width - 2 * self.border_thickness, self.height - 2 * self.border_thickness))
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.border)
        screen.blit(text, (self.x - self.tm * self.width, self.y + 0.3 * self.height))
        st = self.displays[self.current_val]
        text = font.render(st, True, self.border)
        screen.blit(text, (self.x + 0.2 * self.width, self.y + 0.18 * self.height))