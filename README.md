# Wireless Sensor Network Simulation with AI Intrusion Detection

## Overview
This project simulates a wireless sensor network (WSN) and utilizes AI to detect and remove intruders. The simulation is visualized using Pygame, and the intrusion detection is performed using a k-Nearest Neighbors (kNN) model.

## Features
- **Dynamic Node Creation**: Nodes with attributes like energy, data transmission, and distances.
- **Cluster Heads**: Certain nodes act as cluster heads, managing data collection within their clusters.
- **AI Intrusion Detection**: Detects and removes intruder nodes using a kNN model.
- **Energy Management**: Tracks and manages energy consumption for each node.
- **Pygame Visualization**: Visual representation of the network, showing the state before and after intrusion detection.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/saivijayragav/WSN-AI-Intrusion-Detection.git
    cd WSN-AI-Intrusion-Detection
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Download the dataset**:
    - Download the dataset from [https://www.kaggle.com/datasets/bassamkasasbeh1/wsnds].
    - Extract the dataset and place the files in the appropriate directory.
    - This dataset is used to train the model in the modeltraining.py script.

4. **Run the simulation**:
    ```bash
    python main.py
    ```

## File Structure
- `simulatormain.py`: The main simulation script.
- `modeltraining.py`: Script to train the kNN model.
- `requirements.txt`: Required Python packages.
- `README.md`: Project overview and setup instructions.
- `testsimulator.py`: Script to get the network data

## Usage
1. **Train the kNN Model**:
    - Run the `modeltraining.py` script to train the kNN model.
    - The trained model will be saved in the `model/` directory.

    ```bash
    python modeltraining.py
    ```

2. **Run the Simulation**:
    - Execute the `simulatormain.py` script to start the WSN simulation.
    - The simulation window will display the network's state and visualize the nodes before and after intrusion detection.


## Visualization
The simulation visualizes the network using Pygame:
- **White Nodes**: Normal member nodes.
- **Yellow Nodes**: Cluster heads.
- **Red Nodes**: Detected intruder nodes.

The state of the network is shown before and after the intrusion detection model is applied.

## Contributions
Contributions are welcome! If you have any improvements or new features to suggest, please create an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
- Pygame for visualization.
- scikit-learn for the kNN model implementation.
- Kaggle for prov8ding the dataset to train the model
