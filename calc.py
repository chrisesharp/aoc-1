import sys
from array import array

class Calc:
    def __init__(self):
        self.repeat_freq = None
        self.current_freq = 0
        self.shifts = array('i')
        self.known_freqs = set({0})
    
    def main(self, filename):
        file = open(filename, "r")
        print(self.answer(file))
        print(self.repeating_freq())
        
    def answer(self,lines):
        for line in lines:
            shift_freq = int(line)
            self.shifts.append(shift_freq)
            self.current_freq += shift_freq
            if (self.repeat_freq is None):
                if (self.known_freq(self.current_freq)):
                    break
        return self.current_freq
        
    def repeating_freq(self):
        while (self.repeat_freq is None):
            for shift_freq in self.shifts:
                self.current_freq += shift_freq
                if (self.known_freq(self.current_freq)):
                    break
        return self.repeat_freq
    
    def known_freq(self, freq):
        if (freq in self.known_freqs):
            self.repeat_freq = freq
            return True
        else:
            self.known_freqs.add(freq)
        return False
        

if __name__ == "__main__":
    calc = Calc()
    calc.main(sys.argv[1])