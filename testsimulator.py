import math
import random
import joblib, warnings
import pygame as pg
import csv
pg.init()
win = ''
x_pos = []
x_pos.extend([i for i in range(340, 350)])
y_pos = []
y_pos.extend([j for j in range(240,260)])
nodes = []
count = 0
residual_energies= []
def avg(lis):
    return sum(lis)/len(lis)
class Node:
    def __init__(self, node_id, intrusion_detection_model, is_ch, ch):
        self.node_id = node_id
        self.intrusion_detection_model = intrusion_detection_model
        self.neighbors = []
        self.time = random.randint(0, 2000)
        self.is_ch = is_ch
        self.is_intruder = False
        if is_ch:
            self.dis_to_ch = 0
            self.join_s = 0
            self.join_r = random.randint(0, 100)
            self.sch_s = 1
            self.sch_r = 0
            self.data_s = 0
            self.data_r = 0
            self.data_sent_to_bs = random.randint(0, 100)
            self.dist_to_bs = random.uniform(0, 100)
            self.pos = (350,250)
            self.expend_energy = (self.join_s+self.join_r+self.sch_r+self.sch_s+self.data_r+self.data_s+self.data_sent_to_bs)*self.dist_to_bs
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
        self.residual_energy = 5000 - self.expend_energy
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expend_energy]]
        self.commun_cost = self.expend_energy*((self.dis_to_ch*self.data_s) + self.dist_to_bs*(self.data_r+self.data_sent_to_bs))/100

    def run(self):
        global nodes 
        
        if not self.intrusion_detection_model.is_normal(self.client_data):
            self.color = (255, 0, 0)
            self.is_intruder = True
        else:
            data = self.generate_data()
            self.ch.data_r += data


    def generate_data(self):
        return self.data_s
    
    def update(self):
        self.client_data = [[self.time, self.is_ch, self.dis_to_ch, self.join_s, self.join_r, self.sch_r, self.sch_s,
                             self.data_r, self.data_s, self.data_sent_to_bs, self.dist_to_bs, self.expend_energy]]
class IntrusionDetectionModel:
    def __init__(self):
        # Load intrusion detection model
        self.knn_model = joblib.load("knn_model2.joblib")

    def is_normal(self, client_data):
        # Generate client data for the node
        # Use intrusion detection model to predict
        prediction = self.knn_model.predict(client_data)
        return prediction[0] == "Normal" or prediction[0] == "TDMA"
ch = ''
nodes = []
residual_avg_before = []
residual_avg_after = []
pack_R_b = []
pack_R_a = []
commun_cost_b = []
commun_cost_a = []
end_to_end_b = []
end_to_end_a = []

def network_simulation(num_nodes):
    global nodes, count, ch, win, x_pos, y_pos, residual_avg, pack_R_a, pack_R_b, commun_cost_b, commun_cost_a, end_to_end_b, end_to_end_a
    count_before_after = 1
    packet_s = 0
    residual_avg = []
    commun_c_avg = []
    end_to_end = 0
    x_pos = []
    x_pos.extend([i for i in range(340, 350)])
    y_pos = []
    y_pos.extend([j for j in range(240,260)])
    pg.init()
    win = pg.display.set_mode((700, 500))
    pg.display.set_caption("Wireless Sensor Network")
    warnings.filterwarnings("ignore")
    
    intrusion_detection_model = IntrusionDetectionModel()
    ch = Node(0, intrusion_detection_model, 1, "")
    nodes = [Node(node_id, intrusion_detection_model, 0, ch) for node_id in range(1, num_nodes+1)]
    i = 0
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
                break
        if i < len(nodes):
            if not nodes[i].is_intruder:
                draw(nodes, nodes[i].node_id)
                nodes[i].run()
                packet_s += nodes[i].data_s
                residual_avg.append(nodes[i].residual_energy)
                commun_c_avg.append(nodes[i].commun_cost)
                end_to_end += nodes[i].time
                #pg.time.delay(nodes[i].time)
            i += 1
        else:
            if count_before_after < 2:
                residual_avg_before.append(sum(residual_avg))
                commun_cost_b.append(sum(commun_c_avg))
                pack_R_b.append(ch.data_r/packet_s)
                end_to_end_b.append(end_to_end)
                end_to_end = 0
                i = 0
                ch.data_r = 0
                packet_s = 0
                count_before_after += 1
                residual_avg = []
                commun_c_avg = []
                nodes = [node for node in nodes if not node.is_intruder]
            else:
                residual_avg_after.append(sum(residual_avg))
                commun_cost_a.append(sum(commun_c_avg))
                pack_R_a.append(ch.data_r/packet_s)
                end_to_end_a.append(end_to_end)
                pg.quit()
                break
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
NUM_NODES = 500
while count < 10:
    count += 1
    network_simulation(NUM_NODES)
    print(count)
    

plr_b = []
for i in pack_R_b:
    plr_b.append(1-i)
plr_a = []
for i in pack_R_a:
    plr_a.append(1-i)
print("Residual Energy: ", residual_avg_before, residual_avg_after, len(residual_avg_after), len(residual_avg_before))
print("Packet Delivery Ratio: ", pack_R_b, pack_R_a, len(pack_R_a), len(pack_R_b))
print("Communication Cost: ", commun_cost_b, commun_cost_a, len(commun_cost_a), len(commun_cost_b))
print("Packet Loss Rate: ", plr_b, plr_a)
print("End-to-End delay: ", end_to_end_b, end_to_end_a, len(end_to_end_a), len(end_to_end_b))
header = ['Simulation', 'Before', 'After']

#Residual Energy
with open('Residual_Energy.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for i in range(len(residual_avg_before)):
        csv_writer.writerow(['Simulation '+str(i+1), residual_avg_before[i], residual_avg_after[i]])

#Packet Delivery Ratio
with open('Packet_Delivery_Ratio.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for i in range(len(pack_R_a)):
        csv_writer.writerow(['Simulation '+str(i+1), pack_R_b[i], pack_R_a[i]])

#Packet Loss Rate
with open('Packet_Loss_Rate.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for i in range(len(plr_a)):
        csv_writer.writerow(['Simulation '+str(i+1), plr_b[i], plr_a[i]])

#Communication_Cost
with open('Communication_Cost.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for i in range(len(commun_cost_a)):
        csv_writer.writerow(['Simulation '+str(i+1), commun_cost_b[i], commun_cost_a[i]])

#End-To-End
with open('End-to-End_Delay.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header)
    for i in range(len(end_to_end_a)):
        csv_writer.writerow(['Simulation '+str(i+1), end_to_end_b[i], end_to_end_a[i]])

