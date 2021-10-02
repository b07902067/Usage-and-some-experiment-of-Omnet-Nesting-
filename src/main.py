from topology import *
from ini import *
from ned import *
from util import *
from xml import *
import os
import argparse


def main(args):
    # args : input file, output directory(relative to working directory)
    T, num_of_type2 = parse_topology_file(args.topology_file_path)
    R = parse_rout_file(args.routing_file_path, T)

    # create output directory(files)
    # path = args[1]
    working_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = working_dir + "/" + args.output_directory_path
    print(output_dir)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        os.makedirs(output_dir+"/xml")
    make_ini(T, args.network_name, args.simulation_time, output_dir+"/sim.ini")
    make_ned(T, args.network_name, output_dir+"/sim.ned")
    make_rout_xml(T, output_dir+"/xml/rout.xml")
    for i in range(num_of_type2):
        make_flow_xml(T, R, i, output_dir+"/xml/sched{}.xml".format(i))
    

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("topology_file_path")
    parser.add_argument("routing_file_path")
    parser.add_argument("output_directory_path")
    parser.add_argument("network_name")
    parser.add_argument("simulation_time")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args)
    main(args)
