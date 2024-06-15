
import pygame
pygame.init()

class Button():
    def __init__(self, x, y, image, hover_image, scale):
        self.original_image = image
        self.hover_image = hover_image
        self.scale = scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.is_hovered = False
        self.current_scale = scale

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

        # Smoothly resize the button
        if self.is_hovered:
            if self.current_scale < self.scale * 1.1:
                self.current_scale += 0.01
        else:
            if self.current_scale > self.scale:
                self.current_scale -= 0.01

        # Ensure scale stays within bounds
        self.current_scale = min(self.scale * 1.1, max(self.scale, self.current_scale))

        # Update the image size based on current scale
        self.image = pygame.transform.scale(self.hover_image if self.is_hovered else self.original_image, 
                                            (int(self.original_image.get_width() * self.current_scale), 
                                             int(self.original_image.get_height() * self.current_scale)))
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Draw the button
        surface.blit(self.image, self.rect.topleft)

        # Check for button click
        if self.is_hovered and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
    
#text buttons
class TextButton():
    def __init__(self, x, y, text, font, normal_color, hover_color, scale):
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.scale = scale  # Initial scale
        self.scale_speed = 0.02  # Rate of scaling
        self.image_normal = self.font.render(self.text, True, self.normal_color)
        self.image_hover = self.font.render(self.text, True, self.hover_color)
        self.rect = self.image_normal.get_rect()
        self.rect.topleft = (x, y)
        self.is_hovered = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            self.is_hovered = True
            # Scale up when hovered
            self.scale = min(1.1, self.scale + self.scale_speed)
        else:
            self.is_hovered = False
            # Reset scale when not hovered
            self.scale = max(1.0, self.scale - self.scale_speed)

        # Render button with appropriate scale and color
        image_scaled = pygame.transform.scale(self.image_hover if self.is_hovered else self.image_normal,
                                               (int(self.image_normal.get_width() * self.scale),
                                                int(self.image_normal.get_height() * self.scale)))
        self.rect = image_scaled.get_rect(center=self.rect.center)
        surface.blit(image_scaled, self.rect)

        # Check for button click
        if self.is_hovered and pygame.mouse.get_pressed()[0] == 1:
            action = True

        return action