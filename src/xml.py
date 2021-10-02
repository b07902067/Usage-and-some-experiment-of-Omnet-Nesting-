from topology import *
from util import *


def make_rout_xml(T, out_f):
    with open(out_f, 'w') as of:
        print('<filteringDatabases>', file=of)
        for i in range(T.node_n):
            print('\t<filteringDatabase id="switch{}">'.format(i), file=of)
            print('\t\t<static>', file=of)
            print('\t\t\t<forward>', file=of)
            print(T.switch_list[i].connect_device)
            for j in range(len(T.switch_list[i].connect_device)):
                if T.switch_list[i].output_port[j] :
                    dst = T.switch_list[i].connect_device[j]
                    print('\t\t\t\t<individualAddress macAddress=\"{}\" port=\"{}\" />'.format(T.host_list[dst].rout_addr, j), file=of)
            print('\t\t\t</forward>', file=of)
            print('\t\t</static>', file=of)
            print('\t</filteringDatabase>', file=of)
            
        print('</filteringDatabases>', file=of)
def make_flow_xml(T, rout, index_of_type2, out_f):
    with open(out_f, 'w') as of:
        print('<?xml version=\"1.0\" ?>', file=of)
        print('<schedules>', file=of)
        print('\t<defaultcycle>120us</defaultcycle>', file=of)
        if index_of_type2 < len(rout.type2):
            # print("(make_flow_xml)", rout.type2[index_of_type2])
            rout_now = rout.type1 + (rout.type2[index_of_type2])
        for stream in rout_now:
            # print(T.host_list[int(stream.src)].name, ", ", T.host_list[int(stream.dst)].name)
            print('\t<host name=\"{}\">'.format(T.host_list[int(stream.src)].name), file=of)
            print('\t\t<cycle>10us</cycle>', file=of)
            print('\t\t<entry>', file=of)
            print('\t\t\t<start>0us</start>', file=of)
            print('\t\t\t<queue>7</queue>', file=of)
            print('\t\t\t<dest>{}</dest>'.format(T.host_list[int(stream.dst)].sche_addr), file=of)
            print('\t\t\t<size>{}B</size>'.format(int(float(stream.util)*1250)), file=of)
            print('\t\t\t<flowId>1</flowId>', file=of)
            print('\t\t</entry>', file=of)
            print('\t</host>', file=of)
            # print(stream.src, " ", stream.dst)

        print('</schedules>', file=of)

if __name__ == "__main__":
    T, _ = parse_topology_file("./5.in")
    make_rout_xml(T, "./test_rout.xml")