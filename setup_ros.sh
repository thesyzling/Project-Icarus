#!/bin/bash
echo "ICARUS ROS 2 Bağımlılıkları Kuruluyor..."

# Gazebo ve ROS Köprüleri
sudo apt install ros-humble-gazebo-ros-pkgs -y

# UR5 / UR5e Robot Kolu Paketleri ve Kontrolcüler (Kinematik)
sudo apt install ros-humble-ur -y
sudo apt install ros-humble-ur-robot-driver -y
sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers -y

# OpenCV ve ROS Görüntü Köprüsü (cv_bridge)
sudo apt install ros-humble-cv-bridge -y

echo "Kurulum Tamamlandı! Lütfen Python kütüphanelerini 'pip install -r requirements.txt' ile kurun."
