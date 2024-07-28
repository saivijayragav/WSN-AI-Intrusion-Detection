import math
import random
import joblib, warnings
import pygame as pg

pg.init()
win = pg.display.set_mode((700, 500))
pg.display.set_caption("Wireless Sensor Network")
warnings.filterwarnings("ignore")
nodes = []
font = pg.font.Font('freesansbold.ttf', 32)
text = font.render('Before', True, (255, 255, 255))

# Class to create a node in the Network
class Node:
    def __init__(self, node_id, intrusion_detection_model, is_ch, ch):
        self.node_id = node_id
        self.intrusion_detection_model = intrusion_detection_model # Initialising the IDS model
        self.time = random.randint(0, 2000) # 10^-5 seconds
        self.is_ch = is_ch  # Assigning whether the node is a cluster head or not
        self.is_intruder = False # Assuming the node is not a intruder initially

        # Attributes of a Cluster Head
        if is_ch: 
            self.dis_to_ch = 0
            self.join_s = 0
            self.join_r = random.randint(0, 100)
            self.sch_s = 1
            self.sch_r = 0
            self.data_s = 0
            self.data_r = 0
            self.data_sent_to_bs = self.data_r
            self.dist_to_bs = random.uniform(0, 100)
            self.pos = (random.randint(5, 690), random.randint(5, 490))
            self.expend_energy = (self.join_s+self.join_r+self.sch_r+self.sch_s+self.data_r+self.data_s+self.data_sent_to_bs)*self.dist_to_bs
            self.initial_energy = 5000
            self.residual_energy = self.initial_energy - self.expend_energy
            self.nodes = []
            self.color = (220, 220, 0)

        # Attributes of a Member Node
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
            x = random.randint(5, 690)
            y = random.randint(5, 490)
            self.x_pos = x
            self.y_pos = y
            self.dis_to_ch = math.sqrt((x-self.ch.pos[0])**2 + (y-self.ch.pos[1])**2)/10
            self.color = (255,255,255)
            self.expend_energy = (self.join_s+self.join_r+self.sch_r+self.sch_s+self.data_r+self.data_s+self.data_sent_to_bs)*self.dis_to_ch 
            self.initial_energy = 5000
            self.residual_energy = self.initial_energy - self.expend_energy
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expend_energy]]
        self.commun_cost = self.expend_energy*((self.dis_to_ch*self.data_s) + self.dist_to_bs*(self.data_r+self.data_sent_to_bs))/100

    #Runs the node
    def run(self):
        global nodes 
        if not self.intrusion_detection_model.is_normal(self.client_data):
            self.color = (255, 0, 0)
            print('CH', self.ch.node_id, 'Node', self.node_id, "is detected as an intruder\n")
            self.is_intruder = True
        else:
            data = self.generate_data()
            self.ch.data_r += data

    # generate data
    def generate_data(self):
        return self.data_s
    
    #u pdates the node data
    def update(self):
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expend_energy]]
        
class IntrusionDetectionModel:
    def __init__(self):
        # Load intrusion detection model
        self.knn_model = joblib.load("model/knn_model2.joblib")

    def is_normal(self, client_data):
        # Use intrusion detection model to predict
        prediction = self.knn_model.predict(client_data)
        if prediction[0] != 'Normal':
            print("Attack type: ", prediction[0], end=' ')
        return prediction[0] == "Normal"

#Main Function
def network_simulation(num_nodes, num_ch):
    global nodes, text
    count_before_after = 1 #Variable to check before and after implementing the IDS model
    intrusion_detection_model = IntrusionDetectionModel()
    cluster_head = []

    #Loop to create nodes and form cluster heads
    for i in range(num_ch):
        ch = Node(i+1, intrusion_detection_model, 1, "")
        nodes_ch = [Node(node_id, intrusion_detection_model, 0, ch) for node_id in range(1, (num_nodes//num_ch)+1)]
        nodes.extend(nodes_ch)
        ch.nodes = nodes_ch[:]
        cluster_head.append(ch)

    for i in range(num_nodes%num_ch):
        node = Node(len(cluster_head[i].nodes)+1, intrusion_detection_model, 0, cluster_head[i])
        cluster_head[i].nodes.append(node)
        nodes.append(node)

    i = 0
    run = True
    #Main Loop
    while run:

        #Pygame event listener to quit the simulation
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
                break
        
        #Condition to run the nodes
        if i < len(cluster_head[-1].nodes):
            for ch in cluster_head:
                if i < len(ch.nodes) and ch.nodes[i] in nodes:
                    draw(nodes, ch.nodes[i].node_id)
                    print("CH", ch.node_id, "node ", ch.nodes[i].node_id, " is running ")
                    ch.nodes[i].run()
            pg.time.delay(nodes[i].time)
            i += 1

        else:
            #Condition to check before or after implementing the IDS model
            if count_before_after < 2:
                print('Intruders are removed')
                nodes = [node for node in nodes if not node.is_intruder]
                i = 0
                count_before_after += 1
                text = font.render('After', True, (255,255,255))

            else:
                pg.quit()
                break
        ch.update()
         

#Visualisation
def draw(nodes, id):   
    win.fill((0, 0, 0))
    win.blit(text, (0,0))
    for i in nodes:
        if i.node_id == id:
            pg.draw.line(win, (255, 170, 51), i.ch.pos, (i.x_pos, i.y_pos), 3)
        else:
            pg.draw.line(win, (128,128,128), i.ch.pos, (i.x_pos, i.y_pos), 1)
        pg.draw.circle(win, i.ch.color, i.ch.pos, 20)
        pg.draw.circle(win, i.color, (i.x_pos, i.y_pos), 10)
    
    pg.display.update()

num_nodes = 200 # number of member nodes
num_ch = 7 # number of cluster heads
network_simulation(num_nodes, num_ch)
