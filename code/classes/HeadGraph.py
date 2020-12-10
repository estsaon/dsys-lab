import logging
from TimeIt import timeit

func_to_time = ["edges2file", "write2file"]
timer = {func:0 for func in func_to_time}
counter = {func:0 for func in func_to_time}

class HeadGraph:
    def __init__(self, total_vertices, num_sample, out_e, out_v):
        self.base_id = 0
        self.total_vertices = total_vertices;
        self.vertices = [set() for _ in range(num_sample)]
        self.edges = set()
        self.out_e = out_e
        self.out_v = out_v
        with open(self.out_e, 'w') as f:
            pass
        with open(self.out_v, 'w') as f:
            pass

    def __del__(self):
        for k, v in timer.items():
            logging.info(f"timer {k} {v}")

        for k, v in counter.items():
            logging.info(f"counter {k}{v}")

    def get_num_sample_vertices(self, sample):
        return len(self.vertices[sample])

    def get_vertices(self):
        return self.vertices

    def add_edge(self, vertex_from, vertex_to, sample, base_id=None):
        if base_id == None:
            base_id = self.base_id
        src = vertex_from + base_id
        dest = vertex_to + base_id
        if sample != None:
            self.vertices[sample].add(src)
            self.vertices[sample].add(dest)
        self.edges.add(f"{src} {dest}")
        self.edges.add(f"{dest} {src}")

    def next_sample(self):
        self.base_id += self.total_vertices
        self.edges2file()
        self.edges = set()

    @timeit(timer=timer, counter=counter)
    def edges2file(self):
        with open(self.out_e, 'a') as f:
            for e in self.edges:
                f.write(f"{e}\n")

    @timeit(timer=timer, counter=counter)
    def write2file(self):
        with open(self.out_e, 'a') as f:
            for e in self.edges:
                f.write(f"{e}\n")

        with open(self.out_v, 'a') as f:
            for sample in self.vertices:
                for v in sample:
                    f.write(f"{v}\n")
