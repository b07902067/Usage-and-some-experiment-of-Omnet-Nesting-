class hosts():
    def __init__(self, no):
        self.name = "host" + str(no)
        self.rout_addr = "00-00-00-00-00-" + str(no+1).zfill(2)
        self.sche_addr = "00:00:00:00:00:" + str(no+1).zfill(2)

class switches():
    def __init__(self, no):
        self.name = "switch" + str(no)
        self.free_port = 1
        self.connect_device = [no]
        self.output_port = [True]

    def add_connected(self, device, out):
        self.output_port.append(out)
        self.connect_device.append(device)
        self.free_port += 1

    def get_connected(self):
        return self.connect_device
    
    def get_free_port(self):
        return self.free_port

class links():
    def __init__(self, capacity):
        self.src_port = -1
        self.dst_port = -1
        self.cap = capacity
    
    def modify_info(self, s_port, d_port, cap):
        self.src_port = s_port
        self.dst_port = d_port
        self.cap = cap
        


class streams():
    def __init__(self, source, destination, util):
        self.util = util
        self.src = source
        self.dst = destination

class Topology():
    def __init__(self, node_num):
        self.node_n = node_num
        self.host_list = []
        self.switch_list = []
        self.type1_stream_list = []
        self.type2_stream_list = []
        self.links_list = [[links(-1) for i in range(node_num)] for j in range(node_num)]

    def ini_device(self):
        for i in range(self.node_n):
            self.host_list.append(hosts(i))
            self.switch_list.append(switches(i))
    
    def add_links(self, src, dst, capacity):
        src_port = self.switch_list[src].get_free_port()
        dst_port = self.switch_list[dst].get_free_port()
        self.links_list[src][dst].modify_info(src_port, dst_port, capacity)
        self.switch_list[src].add_connected(dst, True)
        self.switch_list[dst].add_connected(src, False)


    def add_type1_streams(self, src, dst, util):
        self.type1_stream_list.append(streams(src, dst, util))

    def add_type2_streams(self, src, dst, util):
        self.type2_stream_list.append(streams(src, dst, util))

class stream_rout():
    def __init__(self):
        self.type1 = []
        self.type2 = []
        self.type2_index = -1
    def add_type1_stream_rout(self, src, dst, util, T):
        link_util = T.links_list[src][dst].cap
        if link_util > 0:
            self.type1.append(streams(src, dst, round(util/link_util, 2)))
    def add_type2_stream(self):
        self.type2.append([])
        self.type2_index += 1
    def add_type2_stream_rout(self, src, dst, util, T):
        link_util = T.links_list[src][dst].cap
        if link_util > 0:
            self.type2[self.type2_index].append(streams(src, dst, round(util/link_util, 2)))
    
        
        
