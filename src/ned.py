from topology import *
from util import *
import sys

ned_head = "package nesting.simulations;\nimport ned.DatarateChannel;\nimport nesting.node.ethernet.VlanEtherHostQ;\nimport nesting.node.ethernet.VlanEtherHostSched;\nimport nesting.node.ethernet.VlanEtherSwitchPreemptable;"

def make_ned(T, network_name, out_f):
    with open(out_f, 'w') as of:
        print(ned_head, file=of)
        print('network {}'.format(str(network_name)), file=of)
        print('{\n\t@display(\"bgb=831,521\")\;\n', file=of)
        '''types'''
        print("\ttypes:\n", file=of)
        print("\t\tchannel C extends DatarateChannel\n\t\t{\n\t\t\tdelay = 0.1us;\n\t\t\tdatarate = 1Gbps;\n\t\t}", file=of)
        # for i in range(T.node_n):
        #     for j in range(T.node_n):
        #         if i == j:
        #             continue
        #         if T.links_list[i][j].cap == -1:
        #             continue
        #         print("\tchannel C{}{} extends DatarateChannel".format(i , j), file=of)
        #         print("\t{", file=of)
        #         print("\t\tdatarate = {}Gbps;".format(T.links_list[i][j].cap), file=of)
        #         print("\t}", file=of)
        # print("", file=of)
        
        '''submodules'''
        print("\tsubmodules:\n", file=of)
        
        # host
        for i in range(T.node_n):
            print("\t\thost{}: VlanEtherHostSched ".format(i), file=of)
            print("\t\t{", file=of)
            print("\t\t\t@display(\"p=66,207\");", file=of)
            print("\t\t}", file=of)
            print("\t\tswitch{}: VlanEtherSwitchPreemptable".format(i), file=of)
            print("\t\t{", file=of)
            print("\t\t\tparameters:", file=of)
            print("\t\t\t\t@display(\"p=307.65,94.5\");", file=of)
            print("\t\t\tgates:", file=of)
            print("\t\t\t\tethg[{}];".format(T.switch_list[i].free_port), file=of)
            print("\t\t}", file=of)
            print("", file=of)
        # switch


        '''connections'''
        print("\tconnections:\n", file=of)

        # host <---> switch
        for i in range(T.node_n):
            print("\t\thost{}.ethg <--> C <--> switch{}.ethg[0];".format(i, i), file=of)

        # switch <--> switch
        for i in range(T.node_n):
            for j in range(T.node_n):
                if i == j:
                    continue
                if T.links_list[i][j].cap == -1:
                    continue
                print("\t\tswitch{}.ethg[{}] <--> C <--> switch{}.ethg[{}];".format(i, T.links_list[i][j].src_port, j, T.links_list[i][j].dst_port), file=of)

        print("}", file=of)
    
if __name__ == "__main__":
    T, _ = parse_topology_file("./5.in")
    make_ned(T, "./test.ned")

