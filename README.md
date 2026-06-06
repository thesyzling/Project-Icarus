# Project ICARUS: Vision-Language-Action (VLA) Robotic Framework

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Classic-FF7D00?logo=gazebo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-00FFFF?logo=yolo&logoColor=black)

Project ICARUS is a next-generation robotic simulation framework designed to bridge Large Language Models (LLMs), deep learning-based Computer Vision, and physical kinematic simulations. The ultimate goal is to create an autonomous system that "understands" abstract human intents, "perceives" its 3D environment, and "acts" accordingly.

## ✅ Current Achievements (Phase 3 Completed)
* **Physical Embodiment:** Spawns a UR5e manipulator in Gazebo with active `joint_trajectory_controller`.
* **Cognitive Bridge:** Built `eve_bridge.py` allowing natural language prompts to dictate robotic states.
* **3D Perception (ICARUS EYE):** Engineered a custom RGB-D (Depth) camera.
* **Spatial Awareness:** Developed `vision_node.py` which utilizes YOLOv8 to detect objects and calculates precise target distance (Z-axis in meters) in real-time.

## 📌 Next Action (Phase 4)
* **Hand-Eye Coordination:** We need to capture the Z-axis depth and XY pixel data, convert it to the robot's base coordinate frame, and send it to the EVE (Gemini) node so the robot can physically reach the detected object.
