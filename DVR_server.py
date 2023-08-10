import pickle
import socket
sock_p = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_p.bind(('localhost', 3000))
data = sock_p.recvfrom(1024)[0].decode()
print(data)
sock_p.close()
sock_n = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock_n.sendto('ANANYA PILLAI'.encode(), ('localhost', 3001))
sock_n.close()
class DVR:
    def __init__ (self, router_name, neighbors, server_address=None, server_port=None):
        self.router_name = router_name
        self.routing_table = {}
        self.neighbors = neighbors
        self.server_address = server_address
        self.server_port = server_port
    def initialize_routing_table(self):
        self.routing_table = {}
        for neighbor in self.neighbors:
            self.routing_table[neighbor] = {'cost': float('inf'), 'next_hop': None}
# Set cost to reach directly connected neighbors as 1
        for neighbor in self.neighbors:
            self.routing_table[neighbor]['cost'] = 1
            self.routing_table[neighbor]['next_hop'] = neighbor
    def send_routing_table(self):
        # Create UDP socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # Serialize and send the routing table
        routing_table_data = pickle.dumps(self.routing_table)
        sock.sendto(routing_table_data, (self.server_address, self.server_port))
        # Close the socket
        sock.close()
    def receive_routing_table(self):
        # Create UDP socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# Bind the socket to receive the routing table
        sock.bind(('localhost', self.server_port))
# Receive and deserialize the routing table
        routing_table_data, _ = sock.recvfrom(4096)
        routing_table = pickle.loads(routing_table_data)
# Close the socket
        sock.close()
        return routing_table
    
    def update_routing_table(self, neighbor_router, neighbor_routing_table):
        for destination, neighbor_info in neighbor_routing_table.items():
            # Add cost to reach neighbor
            neighbor_cost = neighbor_info['cost'] + 1
            if destination not in self.routing_table or neighbor_cost <self.routing_table[destination]['cost']:
                if destination != self.router_name:
                    self.routing_table[destination] = {'cost': neighbor_cost, 'next_hop': neighbor_router}
    def print_routing_table(self):
        print("========================================")
        print(f"Routing table for {self.router_name}:")
        print("========================================")
        print("Destination\tCost\t\tNext Hop")
        for destination, info in self.routing_table.items():
            print(f"{destination}\t\t{info['cost']}\t\t{info['next_hop']}")
# Create R2 router with its neighbor routers and server details
R2 = DVR('R2', ['R1', 'A', 'B', 'C'], server_address='localhost', server_port=3000)
# Initialize routing table
R2.initialize_routing_table()
R2.print_routing_table()
# Receive and update routing table
R2.update_routing_table('R1', R2.receive_routing_table())
# Print final routing table
R2.print_routing_table()
R2.send_routing_table()
# Add new nodes to the neighbor list
R2.neighbors.append('C1')
# Reset routing table
R2.initialize_routing_table()
# Receive and update routing table again
R2.update_routing_table('R1', R2.receive_routing_table())
# Print final routing table
R2.print_routing_table()
R2.send_routing_table()
