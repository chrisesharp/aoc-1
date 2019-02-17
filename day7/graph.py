import sys

class Graph:
    def __init__(self):
        self.nodes = {}
        self.all_nodes = set()
        self.end_node = None
        self.latency = 0
    
    def main(self, file):
        input = open(file, "r").readlines()
        self.parse(input)
        self.latency = 60
        done, time = self.find_with_workers(5)
        answer = ''.join(done)
        print("Done: ",answer,time)
    
    def find_with_workers(self, num):
        done = []
        elapsed = -1
        workers = [['_',0] for x in range(num)]
        
        self.print_headers(workers)
        while (self.get_avail()):
            elapsed += 1
            for i in range(len(workers)):
                workers[i], done = self.update_work(workers[i], done)
            todo = self.get_avail()
            for i in range(len(todo)): 
                workers, todo, done = self.dispatch_work(i, workers, todo, done)
            self.print_status(elapsed, workers, done)
        return done, elapsed
    
    def secs(self, node):
        return ord(node) - 64 + self.latency
    
    def update_work(self, worker, done):
        node, time = worker
        if node != '_':
            if time == 1:
                done = done + [node]
                self.remove_dependency(node)
                worker=['_',0]
            else:
                time -= 1
                worker = [node,time]
        return worker, done
    
    def dispatch_work(self, i, workers, todo, done):
        if todo:
            next = todo[i]
            if self.available(next):
                avail = self.next_free(next,workers)
        return self.assign_work(avail, next, workers, todo, done)
    
    def next_free(self, task, workers):
        if task not in map(lambda y: y[0], workers):
            for i in range(len(workers)):
                node, time = workers[i]
                if time==0:
                    return i, node
        return -1, task
    
    def assign_work(self, avail, next, workers, todo, done):
        if avail:
            (idx, task) = avail
            if idx > -1:
                workers[idx] = [next, self.secs(next)]
                if task != "_":
                    done = done + [task]
                    self.remove_dependency(task)
                    todo = todo[1:]
        return workers, todo, done
        
    def available(self, next):
        return len(self.nodes.get(next, [])) == 0
    
    def print_headers(self, workers):
        sys.stdout.write("Second\t")
        for i in range(len(workers)):
            sys.stdout.write("W {}\t".format(i))
        sys.stdout.write("Done\n")
        
    def print_status(self, elapsed, workers, done):
        sys.stdout.write("{}\t".format(elapsed))
        for i in range(len(workers)):
            sys.stdout.write("{}\t".format(workers[i][0]))
        sys.stdout.write("{}\n".format(''.join(done)))
    
    def find_ordered_path(self):
        done = []
        todo = self.get_avail()
        while (todo):
            next = todo[0]
            next_deps = self.nodes.get(next, [])
            if len(next_deps) == 0:
                done = done + [next]
                todo = todo[1:]
                self.remove_dependency(next)
            todo = self.get_avail()
        return done
        
    def remove_dependency(self, dep):
        nodes = list(self.nodes)
        for node in nodes:
            deps = sorted(filter(lambda x: x != dep, self.nodes.get(node)))
            self.nodes.update({ node : deps })
        self.all_nodes = list(filter(lambda x: x != dep, self.all_nodes))
        
    def parse(self, input):
        for line in input:
            node = str(line[5])
            dependent = str(line[36])
            depends_on = self.nodes.get(dependent, [])
            depends_on.append(node)
            self.nodes.update({ dependent : depends_on})
            self.all_nodes.add(node)
            self.all_nodes.add(dependent)

        for node in self.nodes:
            deps = sorted(self.nodes[node])
            self.nodes.update({ node : deps })
            print(node,deps)
        
    def get_avail(self):
        return sorted(filter(lambda x: len(self.nodes.get(x,[]))==0, self.all_nodes))
    
if __name__ == "__main__":
    graph = Graph()
    graph.main(sys.argv[1])