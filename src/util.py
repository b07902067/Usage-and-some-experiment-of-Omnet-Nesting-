from topology import *
import ast

def parse_topology_file(input_file_path):
    with open(input_file_path) as input_file:
        # parse number of vertex
        num_vertex = int(input_file.readline().strip())

        # parse graph
        topology = Topology(num_vertex)
        topology.ini_device()

        for i in range(num_vertex):
            start_vertex, neighbor_util = input_file.readline().strip().split(",")
            neighbor_util = neighbor_util.split(" ")
            for end_vertex, util in zip(neighbor_util[0::2], neighbor_util[1::2]):
                topology.add_links(int(start_vertex), int(end_vertex), float(util))

        # parse input to be routed: type1
        M = int(input_file.readline().strip())
        type1 = {}
        for _ in range(M):
            src, des, util = input_file.readline().strip().split(" ")
            topology.add_type1_streams(src, des, util)
            # type1[int(src), int(des)] = float(util)

        # parse expected utilizations: type2 + edge upper bound constraint
        N = int(input_file.readline().strip())
        type2_util = {}
        type2_edge_constraint = {}
        for _ in range(N):
            src, des, util, edge_constraint = input_file.readline().strip().split(" ")
            topology.add_type2_streams(src, des, util)
            # type2_util[int(src), int(des)] = float(util)
            # type2_edge_constraint[int(src), int(des)] = int(edge_constraint)

        # parse constraint 2: max number of transfer
        num_transfer = int(input_file.readline().strip())

        return topology, N

def parse_rout_file(input_file_path, T):
    with open(input_file_path) as input_file:
        type1_rout = input_file.readline().strip()
        if "type1 paths: " in type1_rout:
            ret = stream_rout()
            type1_rout = ast.literal_eval(type1_rout[13:])
            type2_rout = input_file.readline().strip()
            type2_rout = ast.literal_eval(type2_rout[14:])
            
            for rout1 in type1_rout:
                last = rout1[0][0]

                for dst in rout1[0]:
                    if dst == last:
                        continue
                    ret.add_type1_stream_rout(last, dst, rout1[1], T)
                    last = dst
            for rout2 in type2_rout:
                last = rout2[0][0]
                ret.add_type2_stream()

                for dst in rout2[0]:
                    if dst == last:
                        continue
                    ret.add_type2_stream_rout(last, dst, rout2[1], T)
                    last = dst

            return ret
                



if __name__ == "__main__":
    # T, _ = parse_topology_file("5.in")
    rout = parse_rout_file("5.out")
    if rout:
        rout1 = rout.type1
        rout2 = rout.type2
        for stream in rout1:
            print(stream.src, ", ", stream.dst, ", ", stream.util)
        print('==================================================')
        for streams in rout2:
            print("[type2]")
            for stream in streams:
                print(stream.src, ", ", stream.dst, ", ", stream.util)
                
    else:
        print(rout)
    # print(T.type1_stream_list[0].src)
    # print(T.type1_stream_list[0].dst)