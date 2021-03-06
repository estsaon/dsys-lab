"""
Discription: 
    Class for LDBC graph data parser.  
"""

import re
from functools import singledispatch
from pathlib import Path

METIS_N_LINES_OF_METADATA = 1

@singledispatch
def get_value_from_line(pos, line):
    raise TypeError


@get_value_from_line.register(int)
def _(pos, line):
    return int(line.strip().split(" ")[pos])


@get_value_from_line.register(slice)
def _(pos, line):
    return [int(x) for x in line.strip().split(" ")[pos]]


class GraphParser:
    def __init__(self, name):
        self.name = name
        self.path_to_graph = f"data/{self.name}/{self.name}"

        # get #vertice and #edges
        with open(f"{self.path_to_graph}.properties", 'r') as fp:
            for line in fp:
                if "meta.vertices" in line:
                    self.n_vertices = get_value_from_line(-1, line)
                if "meta.edges" in line:
                    self.n_edges = get_value_from_line(-1, line)

    def lines_in_edge_file(self):
        with open(f"{self.path_to_graph}.e", 'r') as fp:
            for line in fp:
                yield get_value_from_line(slice(0, 2), line)

    def lines_in_vert_file(self):
        with open(f"{self.path_to_graph}.v", 'r') as fp:
            for metis_id, ldbc_id in enumerate(fp):
                yield metis_id, int(ldbc_id)

    def lines_in_part_file(self, n_part):
        with open(f"{self.path_to_graph}.m.{n_part}p", 'r') as fp:
            for vert_id, rank_id in enumerate(fp): 
                yield vert_id, int(rank_id)

    def get_rank_by_metis_vert(self, n_part):
        rank_by_metis_vert = dict()
        for metis_vert_id, rank_id in self.lines_in_part_file(n_part): 
            rank_by_metis_vert[metis_vert_id] = rank_id
        return rank_by_metis_vert

    def get_metis_by_ldbc(self):
        metis_by_ldbc = dict()
        for metis_id, ldbc_id in self.lines_in_vert_file():
            metis_by_ldbc[ldbc_id] = metis_id
        return metis_by_ldbc

    def get_ldbc_by_metis(self):
        ldbc_by_metis = []
        for metis_id, ldbc_id in self.lines_in_vert_file():
            ldbc_by_metis.append(ldbc_id)
        return ldbc_by_metis
