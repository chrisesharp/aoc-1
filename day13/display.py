import curses


class Display:
    def __init__(self, screen=None):
        self.screen = screen
        if screen:
            self.screen.clear()
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_RED, curses.COLOR_YELLOW)
            self.screen_width = curses.COLS - 1
            self.screen_height = curses.LINES - 1
            self.screen.timeout(1)
            self.pad_origin = (0,0)
        self.camera = -1
    
    def exit(self, crash_loc, cart_loc):
        width = 25
        height = 6
        y = int(self.screen_height / 2) - int(height / 2)
        x =  int(self.screen_width/2) - int(width / 2) 
        msgpad = curses.newpad(height, width)
        msgpad.bkgd(32, curses.color_pair(7))
        msgpad.box()
        msgpad.addstr(2, 1, "Crash at " + str(crash_loc))
        msgpad.addstr(3, 1, "Last cart at " + str(cart_loc))
        msgpad.addstr(4, 1, "PRESS ANY KEY TO EXIT")
        msgpad.refresh(0,0, y, x, y + height, x + width)
        self.screen.timeout(-1)
        self.screen.getkey()
    
    def display(self, track):
        plain_output = ""
        pad = curses.newpad(track.rows + 1, track.columns + 1) if self.screen else None
        
        self.target_cart = None
        if self.camera >= 0:
            self.set_camera(track, self.camera)
        
        for y in range(track.rows):
            for x in range(track.columns):
                if track.crash == (x, y):
                    plain_output += self.render_crash((x, y), pad)
                    continue
                if (x, y) in track.cart_locs:
                    for cart in track.carts:
                        if cart.get_location() == (x, y):
                            plain_output += self.render_cart(cart, pad)
                            continue
                else:
                    if pad:
                        pad.addch(y, x, ord(str(track.field[x, y])))
                    else:
                        plain_output += track.field[x, y]
            if not pad:
                plain_output += "\n"
        if pad:
            pad.refresh(self.pad_origin[1],self.pad_origin[0], 0, 0, self.screen_height, self.screen_width)
            self.help_window(1, 1)
            self.get_keypress()
        return plain_output
    
    def set_camera(self, track, cart_num):
        if len(track.carts) <= cart_num:
            cart_num = -1
            return
        self.target_cart = track.carts[cart_num]
        (target_cart_x, target_cart_y) = self.target_cart.get_location()
        self.pad_origin = (max(0, target_cart_x - 20), max(0, target_cart_y - 20))

    def render_cart(self, cart, pad):
        x, y = cart.get_location()
        if pad:
            cart_colour = curses.color_pair(cart.colour)
            if self.target_cart and ((x, y) == self.target_cart.get_location()):
                cart_colour |= curses.A_REVERSE
            pad.addch(y, x, ord(str(cart.token)), cart_colour)
            return ""
        else:
            return str(cart.token)

    def render_crash(self, loc, pad):
        x, y = loc
        if pad:
            pad.addch(y, x, ord("X"), curses.color_pair(7))
            return ""
        else:
            return "X"

    def get_keypress(self):
        KEY_ESC = 27
        key = self.screen.getch()
        if key >= 0:
            if key == curses.KEY_DOWN:
                (x,y) = self.pad_origin
                self.pad_origin = (x, y + 1)
                return
            if key == curses.KEY_UP:
                (x,y) = self.pad_origin
                self.pad_origin = (x, max(0, y - 1))
                return
            if key == curses.KEY_LEFT:
                (x,y) = self.pad_origin
                self.pad_origin = (max(0, x - 1), y)
                return
            if key == curses.KEY_RIGHT:
                (x,y) = self.pad_origin
                self.pad_origin = (x + 1, y)
                return
            if chr(key) in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
                self.screen.clear()
                self.camera = int(chr(key), 16)
                return
            if key == KEY_ESC:
                self.camera = -1
                return

    def help_window(self, x, y):
        width = 23
        height = 6
        pad = curses.newpad(height, width)
        pad.bkgd(32, curses.color_pair(7))
        pad.box()
        pad.addstr(1,1,"Keys:")
        pad.addstr(2,1, "0..F: Follow cart")
        pad.addstr(3,1,"Arrows: Move camera")
        pad.addstr(4,1,"Esc: Stop following")
        pad.refresh(0,0 , y, x, y + height, x + width)