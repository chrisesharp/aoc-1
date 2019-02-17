import sys
from datetime import date
from dateutil.parser import isoparse
import collections

class Logger:
    def __init__(self):
        self.sorted_log = collections.OrderedDict()
        self.guards = {}
        self.sleeps = {}
    
    def parse(self, input):
        logs = {}
        for line in input:
            timestring = line[1:17]
            entry = line[19:]
            timestamp = isoparse(timestring)
            logs.update({timestamp : entry})
            if entry[:5] == "Guard":
                rest = entry[7:]
                guard = rest[0:rest.index(" ")]
                self.guards.update({guard:timestamp})
        
        for key in sorted(logs.keys()):
            self.sorted_log[key] = logs[key]
    
    def last(self):
        return next(reversed(self.sorted_log))
    
    def guard_list(self):
        return list(self.guards.keys())
    
    def guard_sleep(self, guard):
        sleep_time=0
        our_guard=False

        sleeps = self.sleeps.get(guard, {})
        for entry in self.sorted_log:
            event = self.sorted_log[entry]
            our_guard = self.is_guard(event, guard, our_guard) 
            if our_guard:
                if event[:5]=="falls":
                    start=entry
                if event[:5]=="wakes":
                    sleep_time+= self.update_minutes_asleep(sleeps, start, entry)
        self.sleeps.update({guard:sleeps})
        return sleep_time
    
    def update_minutes_asleep(self, sleeps, start, entry):
        sleep=abs(start.minute-entry.minute)
        for minute in range(start.minute, entry.minute):
            count = sleeps.get(minute,-1) + 1
            sleeps.update({minute:count})
        return sleep
        
    def is_guard(self, event, guard, default):
        our_guard = default
        guard_entry="Guard #"
        if event.find(guard_entry)>-1:
            if event.find(guard_entry+str(guard))>-1:
                our_guard=True
            else:
                our_guard=False
        return our_guard
    
    def find_minute(self,guard):
        sleeps = self.sleeps.get(guard, False)
        longest = 0
        longest_minute = 0
        most_frequent = 0
        if sleeps:
            for minute in sleeps:
                if sleeps[minute] > longest:
                    longest=sleeps[minute]
                    longest_minute=minute

        count = collections.Counter(sleeps)
        if len(count)>0:
            (most_frequent,_) = count.most_common(1)[0]
        return (longest_minute, most_frequent)
        
            
    def main(self, filename):
        file = open(filename, "r")
        self.parse(file)
        longest = 0
        sleepiest_guard = 0
        sleepiest_guard_time = 0
        freq_guard = 0
        freq_minute = 0
        for guard in self.guard_list():
            sleep = self.guard_sleep(guard)
            (long_min, freq_min) = self.find_minute(guard)
            if sleep > longest:
                longest = sleep
                sleepiest_guard=guard
                sleepiest_guard_time = long_min
            if freq_min > freq_minute:
                freq_minute = freq_min
                freq_guard = guard
        print("Sleepiest guard is ",sleepiest_guard)
        print("Minute asleep most is ", sleepiest_guard_time)
        print("Answer is ", int(sleepiest_guard)*sleepiest_guard_time)
        print("Most frequent guard is ", freq_guard," and minute is ", freq_minute)
        print("Answer is ", int(freq_guard) * freq_minute)

if __name__ == "__main__":
    logs = Logger()
    logs.main(sys.argv[1])