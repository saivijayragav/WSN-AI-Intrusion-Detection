import math
import random
import joblib, warnings
import pygame as pg
pg.init()
win = pg.display.set_mode((700, 500))
pg.display.set_caption("Wireless Sensor Network")
warnings.filterwarnings("ignore")
x_pos = []
x_pos.extend([i for i in range(340, 350)])
y_pos = []
y_pos.extend([j for j in range(240,260)])
class Node:
    def __init__(self, node_id, intrusion_detection_model, is_ch, ch):
        self.node_id = node_id
        self.intrusion_detection_model = intrusion_detection_model
        self.neighbors = []
        self.time = random.randint(0, 2000)
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
            self.pos = (350,250)
        else:
            self.ch = ch
            
            self.join_s = 1
            self.join_r = 0
            self.sch_s = 0
            self.sch_r = 1
            self.data_s = random.randint(0,100)
            self.data_r = 0     
            self.data_sent_to_bs = 0
            self.dist_to_bs = 0
            self.expaned_energy = random.uniform(0,2)
            x = random.randint(5, 690)
            y = random.randint(5, 490)
            while x in x_pos:
                x = random.randint(5, 695)
            while y in y_pos:
                y = random.randint(5, 495)    
            x_pos.extend([i for i in range(x-10, x+10)])
            y_pos.extend([i for i in range(y-10, y+10)])
            self.x_pos = x
            self.y_pos = y
            self.dis_to_ch = math.sqrt((x-self.ch.pos[0])**2 + (y-self.ch.pos[1])**2)/10
            
            self.color = (255,255,255)
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expaned_energy]]
    def run(self):
        data = self.generate_data()
        self.ch.data_r += data 
        if not self.intrusion_detection_model.is_normal(self.client_data):
            self.color = (255, 0, 0)
            print(f"Node {self.node_id} detected as an intruder and removed.")

    def generate_data(self):
        # Generate data to send
        print(f"Node {self.node_id} sent {self.data_s} data packets to Cluster Head")
        return self.data_s
    
    def update(self):
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expaned_energy]]
class IntrusionDetectionModel:
    def __init__(self):
        # Load intrusion detection model
        self.knn_model = joblib.load("knn_model2.joblib")

    def is_normal(self, client_data):
        # Generate client data for the node
        # Use intrusion detection model to predict
        prediction = self.knn_model.predict(client_data)
        return prediction[0] == "Normal"

def network_simulation(num_nodes):
    # Create intrusion detection model
    intrusion_detection_model = IntrusionDetectionModel()

    # Create nodes
    ch = Node(0, intrusion_detection_model, 1, "")
    nodes = [Node(node_id, intrusion_detection_model, 0, ch) for node_id in range(1, num_nodes+1)]

    # Simulate network events
    i = 0
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
                break
        if i < len(nodes):
            draw(nodes, nodes[i].node_id)
            nodes[i].run()
            pg.time.delay(nodes[i].time)
        draw(nodes, 0)
        i += 1
        ch.update()
        

def draw(nodes, id):   
    win.fill((0, 0, 0))
    for i in nodes:
        
        if i.node_id == id:
            pg.draw.line(win, (255, 170, 51), i.ch.pos, (i.x_pos, i.y_pos), 3)
        else:
            pg.draw.line(win, (128,128,128), i.ch.pos, (i.x_pos, i.y_pos), 1)
        pg.draw.circle(win, (255, 255, 255), i.ch.pos, 20)
        pg.draw.circle(win, i.color, (i.x_pos, i.y_pos), 10)
    
        
    pg.display.update()

# Simulation parameters
NUM_NODES = 30
network_simulation(NUM_NODES)

