import pygame
import pygame.sprite
from pygame.locals import *

class Sprite(pygame.sprite.DirtySprite):
    sprite_focused = None
    
    def __init__(self, img_file, coord):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load(img_file)
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def update(self):
        if (Click and
            not Sprite.sprite_focused and
            self.rect.collidepoint(pygame.mouse.get_pos())):
            Sprite.sprite_focused = self
        elif Sprite.sprite_focused == self:
            surface_rect = Surface.get_rect()
            self.rect.x += Delta_x
            self.rect.y += Delta_y
            if not surface_rect.contains(self.rect):
                self.rect.x -= Delta_x
                self.rect.y -= Delta_y

def run():
    import json
    from sys import argv
    from getopt import getopt, GetoptError

    global Surface
    global Delta_x, Delta_y, Click
    global Config

    flags =  [ "debug=", "config=", "mode=" ]

    def usage():
        pretty_flags = " ".join([ "--%s [val]" % x.rstrip("=") for x in flags ])
        print "usage: %s" % pretty_flags
        exit(1)

    def load_config(fname):
        with open(fname) as f:
            config = json.load(f)
        return config
    
    try:
        opts, args = getopt(argv[1:], "", flags)
    except GetoptError:
        usage()

    options = dict((x.lstrip("-"), y) for x, y in opts)

    Config = load_config(options["config"]) if "config" in options else usage()

    pygame.init()
    pygame.mouse.set_visible(True)
    
    if not "debug" in options:
        modes = pygame.display.list_modes()
        if "mode" in options:
            x, y = options.get("mode").split(",")
            size = (int(x), int(y))
            if size in modes:
                size = modes[modes.index(size)]
            else:
                print "Invalid mode!  Options are: %s" % modes
                exit(0)
        else:
            size = modes[0]
        Surface = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        x, y = options.get("debug").split(",")
        size = (int(x), int(y))
        Surface = pygame.display.set_mode(size)

    background_image = pygame.image.load(Config["background"])
    # background = pygame.transform.smoothscale(background_image,
    #                                           Surface.get_size())
    # Surface.blit(background, (0, 0))
    Surface.blit(background_image, (0, 0))
    pygame.display.flip()

    sprite_group = pygame.sprite.RenderUpdates()

    for sprites_config in Config["sprites"]:
        img_file = sprites_config["file"]
        coord = sprites_config["coord"]
        sprite = Sprite(img_file, coord)
        sprite_group.add(sprite)

    while True:
        for e in pygame.event.get():
            if ((e.type == QUIT) or
                (e.type == KEYDOWN and (e.mod == KMOD_LCTRL) and (e.key == K_c))):
                print "Exiting ..."
                exit(0)
            elif e.type == KEYDOWN:
                char = e.unicode
                
        Delta_x, Delta_y = pygame.mouse.get_rel()
        
        (left_click, center_click, right_click) = pygame.mouse.get_pressed()
        
        Click = True if left_click or center_click or right_click else False

        if Click: pygame.time.wait(250)

        if Click and Sprite.sprite_focused:
            Sprite.sprite_focused = None
        else:
            sprite_group.clear(Surface, background_image)
            sprite_group.update()
                            
        rects = sprite_group.draw(Surface)
        pygame.display.update(rects)

if "__main__" == __name__:
    run()
