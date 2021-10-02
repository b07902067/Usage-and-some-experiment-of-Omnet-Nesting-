from topology import *
from util import *

def make_ini(T, network_name, sim_time, out_f):
    with open(out_f, 'w') as of:
        print("[General]", file=of)
        print("network = {}".format(network_name), file=of)
        print("record-eventlog = false", file=of)
        print("result-dir = results_strict_priority", file=of)
        print("sim-time-limit = {}s".format(sim_time), file=of)
        print('', file=of)
        print("**.displayAddresses = true", file=of)
        print("**.verbose = true", file=of)
        print('', file=of)
        
        # mac address
        for i in range(T.node_n):
            print('**.host{}.eth.address = \"{}\"'.format(i, T.host_list[i].rout_addr), file=of)
        print('', file=of)

        # parameter of switch
        print("**.switch*.processingDelay.delay = 1us", file=of)
        print("**.filteringDatabase.database = xmldoc(\"XML/demo_rout.xml\", \"/filteringDatabases/\")", file=of)
        print('', file=of)
        for i in range(8):
            print("**.switch*.eth[*].queue.tsAlgorithms[{}].typename = \"StrictPriority\"".format(i), file=of)
        print("**.queues[*].bufferCapacity = 363360b", file=of)
        print('', file=of)

        # specify flow creation file
        for i in range(T.node_n):
            print("**.host{}.trafGenSchedApp.initialSchedule = \
    xmldoc(\"XML/demo_sched.xml\")".format(i), file=of)

if __name__ == "__main__":
    T = parse_topology_file("./5.in")
    make_ini(T, "./test_ini")


