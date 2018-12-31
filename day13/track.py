from direction import Direction
from cart import Cart
from time import sleep
import sys

class Track:    
    CLR = "\u001B[H" + "\u001B[2J"
    
    def __init__(self,input):
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
    
    def parse(self):
        for y in range(self.rows):
            for x in range(self.columns):
                token = self.input[y][x]
                if token in Cart.track_tokens:
                    self.add_track(token,(x,y))
                if token in self.cart_tokens:
                    cart = self.add_cart(token,(x,y))
                    if cart.get_direction() == Direction.LEFT or cart.get_direction() == Direction.RIGHT:
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
    
    def tick(self):
        for cart in sorted(self.carts, key=lambda x: (x.location[1],x.location[0])):
            self.cart_locs.remove(cart.get_location())
            new_loc = cart.tick()
            if new_loc in self.cart_locs:
                self.crash = new_loc
                self.cart_locs.add(new_loc)
                break
            self.cart_locs.add(new_loc)
        return self.print_track()
        #return self.print_cart(16)
        
    def tick2(self):
        for cart in sorted(self.carts, key=lambda x: (x.location[1],x.location[0])):
            if cart.crashed:
                self.carts.remove(cart)
            else:
                self.cart_locs.remove(cart.get_location())
                new_loc = cart.tick()
                if new_loc in self.cart_locs:
                    self.carts.remove(cart)
                    for other_cart in self.carts:
                        if other_cart.get_location() == new_loc:
                            other_cart.crashed = True
                            self.cart_locs.remove(new_loc)
                    continue
                self.cart_locs.add(new_loc)    
        
        self.carts = list(filter(lambda x: not x.crashed, self.carts))        
        return self.print_track()
    
    def get_crash(self):
        return self.crash
    
    def print_track(self):
        output = self.CLR
        for y in range(self.rows):
            for x in range(self.columns):
                if (x,y) in self.cart_locs:
                    for cart in self.carts:
                        if cart.get_location() == (x,y):
                            if self.crash == (x,y):
                                output +=  "\u001B[1m" + "X" + "\u001B[0m"
                                break
                            else:
                                output += "\u001B[1m" + cart.token + "\u001B[0m"
                else:
                    output += self.field[x,y]
            output += "\n"
        return output

    def print_cart(self, cart_num):
        target_cart = self.carts[cart_num]
        output = self.CLR
        (target_cart_x,target_cart_y) = target_cart.get_location()
        for y in range(max(0,target_cart_y-20),min(self.rows,target_cart_y+20)):
            for x in range(max(0,target_cart_x-20),min(self.columns,target_cart_x+20)):
                if (x,y) in self.cart_locs:
                    for cart in self.carts:
                        if cart.get_location() == (x,y):
                            if self.crash == (x,y):
                                output +=  "\u001B[1m" + "X" + "\u001B[0m"
                                break
                            else:
                                output += "\u001B[1m" + cart.token + "\u001B[0m"
                else:
                    output += self.field[x,y]
            output += "\n"
        return output
            

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        input = f.read()
    track = Track(input)
    track.parse()
    sleep_time = 30
    if sys.argv[2] == "1":
        while not track.get_crash():
            print(track.tick())
            sleep(1/sleep_time)
        print("Crash at ",track.get_crash())
    else:
        while len(track.cart_locs)>1:
            print(track.tick2())
            sleep(1/sleep_time)
        print("Last cart at ",track.carts[0].get_location())