from direction import Direction
from cart import Cart
from display import Display
import sys
import curses

class Track:    
    def __init__(self,input, using_display=True):
        self.input = input.split("\n")
        self.columns = len(self.input[0])
        self.rows = len(self.input)
        self.field = {}
        for y in range(self.rows):
            for x in range(self.columns):
                self.field[x, y] = " "
        
        self.cart_tokens = ['<','^','>','v']   
        self.carts = []
        self.cart_locs = set()
        self.crash = None
        self.cart_number = 0
        self.using_display = using_display
        self.screen = Display()
    
    def parse(self):
        for y in range(self.rows):
            for x in range(self.columns):
                token = self.input[y][x]
                if token in Cart.track_tokens:
                    self.add_track(token,(x,y))
                if token in self.cart_tokens:
                    cart = self.add_cart(token,(x,y))
                    if cart.get_direction() == Direction.LEFT or \
                            cart.get_direction() == Direction.RIGHT:
                        self.add_track("-",(x,y))
                    else:
                        self.add_track("|",(x,y))
    
    def add_track(self,track,coord):
        self.field[coord[0],coord[1]] = track
    
    def add_cart(self,token,coord):
        self.cart_number += 1
        cart = Cart(token,coord, self.cart_number)
        cart.add_track(self)
        self.carts.append(cart)
        self.cart_locs.add(coord)
        return cart
    
    def get_carts(self):
        return self.carts
        
    def tick(self, screen=None):
        self.crash = None
        for cart in sorted(self.carts, key=lambda x: (x.location[1],x.location[0])):
            if cart.crashed:
                self.carts.remove(cart)
            else:
                self.cart_locs.remove(cart.get_location())
                new_loc = cart.tick()
                if new_loc in self.cart_locs:
                    self.crash = new_loc
                    self.remove_crashed(cart)
                    continue
                self.cart_locs.add(new_loc)
        self.carts = list(filter(lambda x: not x.crashed, self.carts))
        if self.using_display:
            return self.screen.display(self)
    
    def remove_crashed(self, cart):
        self.carts.remove(cart)
        for other_cart in self.carts:
            if other_cart.get_location() == self.crash:
                other_cart.crashed = True
                self.cart_locs.remove(self.crash)
    
    def get_crash(self):
        return self.crash
    
    def run_sim(self, screen=None, part1=True):
        self.screen = Display(screen)
        if part1:
            while not self.get_crash():
                self.tick()
        else:
            while len(self.cart_locs) > 1:
                self.tick()
        if screen:
            self.screen.exit(self.get_crash(), self.carts[0].get_location())
            

if __name__ == "__main__":
    using_display = False
    part1 = True
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0]," filename [part_number] [using_display]")
        print("options: ", sys.argv[0]," filename [1|2] [True|False]")
        exit(1)
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    if len(sys.argv) > 2:
        part1 = sys.argv[2] == "1"
    if len(sys.argv) > 3:
        using_display = sys.argv[3] == "True"
    
    with open(file_name) as f:
        input = f.read()
    
    track = Track(input, using_display)
    track.parse()
    if track.using_display:
        curses.wrapper(track.run_sim, part1)
    else:
        track.run_sim(None, part1)
    if part1:
        print("Crash at ",track.get_crash())
    else:
        print("Last cart at ",track.carts[0].get_location())