# ADC Cocktail-Robot

## Overview
This project is a ROS2-based collaborative Cocktail-Robot system with M0609 model from Doosan Robotics.  
It is designed to control robotic tasks integrated with external systems such as Firebase DB and user interfaces.
you can download it with git as well as docker







---

## ⚙️ Requirements

Make sure your environment meets the following:

- Ubuntu 22.04 (recommended)
- ROS2 (Humble or compatible)
- Python 3.8+
- personal Firebase DB API-Key file(we provide DB Format)
- Doosan-robot2 library(preferable, still available to simulate it in virtual environment without it)
---

## 🚀 Installation

### 1. Clone the Repository
```bash
cd ~/cobot_ws/src
git clone https://github.com/DongSearch/Rokey-Cobot-Proj1.git
```

### 2. Install Dependencies
```
cd ~/cobot_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### 3. Source the environment
```
source install/setup.bash
```

### 4. create firebase apk-key json file and put it in your path
```
source install/setup.bash
```

