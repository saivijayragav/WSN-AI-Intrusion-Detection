import simpy
import random
import joblib, warnings
warnings.filterwarnings("ignore")
class Node:
    def __init__(self, node_id, intrusion_detection_model, is_ch):
        self.env = env
        self.node_id = node_id
        self.intrusion_detection_model = intrusion_detection_model
        self.neighbors = []
        self.time = random.randint(1, 100)
        self.is_ch = is_ch
        if is_ch:
            self.dis_to_ch = 0
            self.join_s = 0
            self.join_r = random.randint(0, 100)
            self.sch_s = 1
            self.sch_r = 0
            self.data_s = 0
            self.data_r = random.randint(1, 200)
            self.data_sent_to_bs = random.randint(0, 100)
            self.dist_to_bs = random.uniform(0, 100)
            self.expaned_energy = 1000
        else:
            self.ch = ""
            self.dis_to_ch = random.uniform(0, 100)
            self.join_s = 1
            self.join_r = 0
            self.sch_s = 1
            self.sch_r = 0 
            self.data_s = random.randint(0, 50)
            self.data_r = 0      
            self.data_sent_to_bs = 0
            self.dist_to_bs = 0
            self.expaned_energy = random.uniform(0,2)
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expaned_energy]]
    def run(self):
        data = self.generate_data()
        self.ch.data_r += data 
        if not self.intrusion_detection_model.is_normal(self.client_data):
            print(f"Node {self.node_id} detected as an intruder and removed.")
        self.update()
    def generate_data(self):
        # Generate data to send
        return self.data_s
    
    def update(self):
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expaned_energy]]
class IntrusionDetectionModel:
    def __init__(self):
        # Load intrusion detection model
        self.knn_model = joblib.load("e:/knn/knn_model2.joblib")

    def is_normal(self, client_data):
        # Generate client data for the node
        # Use intrusion detection model to predict
        prediction = self.knn_model.predict(client_data)
        return prediction[0] == "Normal"

def network_simulation(env, num_nodes):
    # Create intrusion detection model
    intrusion_detection_model = IntrusionDetectionModel()

    # Create nodes
    ch = Node(0, intrusion_detection_model, 1)
    nodes = [Node(node_id, intrusion_detection_model, 0) for node_id in range(1, num_nodes+1)]

    # Simulate network events
    i = 0
    while i < len(nodes):
        nodes[i].ch = ch
        nodes[i].run()
        # Simulate network events indefinitely
        i += 1
        ch.update()
        yield env.timeout(nodes[i-1].time)  # Simulate 1 time unit
    print(ch.data_r)
    print(ch.intrusion_detection_model.is_normal(ch.client_data))

# Simulation parameters
NUM_NODES = 500
SIMULATION_TIME = 60*60*60

# Run simulation
env = simpy.Environment()
env.process(network_simulation(env, NUM_NODES))

env.run(until=SIMULATION_TIME)

n = Node(0, IntrusionDetectionModel(), 1)
print(n.intrusion_detection_model.is_normal(client_data=n.client_data))
