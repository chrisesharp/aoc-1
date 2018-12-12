import sys

class Marble:
    def __init__(self, players, last_marble):
        self.circle = [0]
        self.current = 0
        self.players = [0]  * (players+1)
        self.last = last_marble
        
    def play(self):
        player = 1
        for marble in range(1,self.last+1):
            if marble%23 != 0:
                self.place(marble)
            else:
                self.current = self.pos3()
                popped = self.circle.pop(self.current)
                score = self.players[player]
                score += marble + popped
                self.players[player] = score
            player = max(1, (player + 1) % (len(self.players)))
        high_score = 0
        winner = 0
        for player in range(len(self.players)):
            score = self.players[player]
            if score > high_score:
                high_score = score
                winner = player
        print ("Winner:", winner)
        print ("High:", high_score)
        return winner, high_score
    
    def place(self, marble):
        pos1 = self.pos1()
        pos2 = self.pos2()
        if pos2>pos1:
            if pos2 <= len(self.circle):
                self.current= pos1+1
            else:
                self.current= max(1,pos1)
        else:
            self.current = max(1,pos1+1)
        self.circle.insert(self.current,marble)
        return self.current

    def pos1(self):
        return (self.current + 1) % (len(self.circle))
    
    def pos2(self):
        return (self.current + 2) % (len(self.circle)+1)
    
    def pos3(self):
        circ = len(self.circle)
        return (self.current - 7 + circ) % (circ)


        