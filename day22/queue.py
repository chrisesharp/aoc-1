import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        (priority, item) = heapq.heappop(self.elements)
        return (priority, item)
    
    def get_item(self):
        (priority, item) = heapq.heappop(self.elements)
        return item