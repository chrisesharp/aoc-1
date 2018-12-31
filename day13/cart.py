from direction import Direction, next_location,  left, right, ahead, turn

class Cart:
    track_tokens = {
        "|" : {
            Direction.UP:ahead,
            Direction.DOWN:ahead
            },
        "/" : {
            Direction.UP:right,
            Direction.DOWN:right,
            Direction.LEFT:left,
            Direction.RIGHT:left
            },
        "-" : {
            Direction.LEFT:ahead,
            Direction.RIGHT:ahead
            },
        "\\": {
            Direction.UP:left,
            Direction.DOWN:left,
            Direction.LEFT:right,
            Direction.RIGHT:right
            },
        "+" : {
            Direction.UP: turn,
            Direction.DOWN:turn,
            Direction.LEFT:turn,
            Direction.RIGHT:turn
            }
    }
    tokens = {
        "<" : Direction.LEFT,
        "^" : Direction.UP,
        ">" : Direction.RIGHT,
        "v" : Direction.DOWN,
    }
    token_dirs = {
        Direction.LEFT  : "<" ,
        Direction.UP    : "^",
        Direction.RIGHT : ">",
        Direction.DOWN  : "v",
    }
    def __init__(self, token, coord, number):
        self.token = token
        self.direction = Cart.tokens[token]
        self.location = coord
        self.turn_index = -1
        self.number = number
        self.crashed = False
    
    def get_location(self):
        return self.location
    
    def get_direction(self):
        return self.direction
    
    def add_track(self, track):
        self.track = track
    
    def tick(self):
        loc = self.get_location()
        dir = self.get_direction()
        track =  self.track.field[loc[0],loc[1]]
        dir_func_opts = self.track_tokens[track]

        dir_func = dir_func_opts[dir]
        self.direction = dir_func(self,dir)
        next = next_location(loc,self.direction)

        next_track = self.track.field[next[0],next[1]] 
        
        self.location = next
        self.key = (next[1],next[0])
        self.token = self.token_dirs[self.direction]
        return self.location
    
    def turn(self, direction):
        self.turn_index = (self.turn_index + 1) % 3
        if self.turn_index == 0:
            return left(self, direction)
        if self.turn_index == 1:
            return ahead(self, direction)
        if self.turn_index == 2:
            return right(self,direction)