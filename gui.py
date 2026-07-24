import pygame

# This file contains all the gui related stuff to create buttons, boxes and labels used throughout the game

# Converts a hexadecimal colour string (e.g. "#FF0000")
# to an RGB tuple (255, 0, 0) as pygames relies on RGB tuple color values
def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Returns a darker shade of an RGB colour
# Used for hover and disabled button effects
def darken(color, amount=0.75):
    return tuple(max(0, int(c * amount)) for c in color)

# Default callback function used when no function is supplied to a button
def noop():
    pass

# Custom button widget supporting:
# - Hover effects
# - Click callbacks
# - Disabled state
# - Rounded corners
# - Borders
class Button:
    def __init__(self, x, y, width=50, height=50, color="#FFFFFF", hover_color=None, border_radius=0, border_width=0, border_color="#FFFFFF"):
        # If no hover colour is specified,
        # automatically generate a darker version
        # of the button colour

        self.border_radius = border_radius
        self.color = hex_to_rgb(color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.disabled = False
        self.border_color = hex_to_rgb(border_color)
        self.border_width = border_width

        if hover_color is None:
            self.hover_color = darken(self.color)
        else:
            self.hover_color = hex_to_rgb(hover_color)
        self.rect = pygame.Rect(x, y, width, height)

    # Draws the button using its current state
    # (normal, hovered or disabled)

    def draw(self, screen):
        color = self.hover_color if self.is_hovered() else darken(self.color, amount=0.8) if self.disabled else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)

    # Returns True if the mouse is currently
    # hovering over the button
    def is_hovered(self):
        if not self.disabled:
            mouse_pos = pygame.mouse.get_pos()
            return self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.disabled:
            return self.rect.collidepoint(event.pos)
        return False

    # Executes the supplied callback function
    # when the button is clicked
    def on_click(self, event, func=noop):
        if self.is_clicked(event):
            func()

# Simple rectangular container.
# Used for decorative UI elements
class Box:
    def __init__(self, x, y, width=50, height=50, color="#FFFFFF", border_radius=0, border_width=0, border_color="#FFFFFF"):
        self.border_radius = border_radius
        self.color = hex_to_rgb(color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.border_color = hex_to_rgb(border_color)
        self.border_width = border_width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=self.border_radius)

# Custom text label.
# Can optionally centre itself inside
# another GUI object (Button/Box)
class Label:
    def __init__(self, x=0, y=0, obj=None, text="", font="Segoe UI Symbol", font_size=26, smooth_edge=True, color="#000000", bold=False, center_to_object=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.font_size = font_size
        self.smooth_edge = smooth_edge
        self.obj = obj
        self.c2o = center_to_object
        self.color = hex_to_rgb(color)
        self.ft = pygame.font.SysFont(self.font, self.font_size)
        self.ft.set_bold(bold)
        self.txt = self.ft.render(self.text, self.smooth_edge, self.color)

    def draw(self, screen):
        # Recalculate the text position each frame
        # so the label always stays centred.
        if self.c2o:
            obj_x_cen = (self.obj.width)/2
            obj_y_cen = (self.obj.height)/2
            self.x = (self.obj.x+obj_x_cen)-(self.txt.get_width()/2)
            self.y = (self.obj.y+obj_y_cen)-(self.txt.get_height()/2)

        screen.blit(self.txt, (self.x, self.y))

    # Updates the displayed text by
    # re-rendering the font surface
    def set_text(self, text):
        self.text = text
        self.txt = self.ft.render(self.text, self.smooth_edge, self.color)