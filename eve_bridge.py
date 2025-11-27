import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState, Image
from cv_bridge import CvBridge
import cv2
import PIL.Image
import numpy as np
import google.generativeai as genai
import json
import threading
import re

# --- EVE v8.0 (GÖREN UR5) ---
API_KEY = "AIzaSyAKb83rdTQ1d60CQyygozJPGLH25ESbQQE"

TOPIC_ARM = '/joint_trajectory_controller/joint_trajectory'
TOPIC_CAMERA = '/wrist_camera/image_raw'

ARM_JOINTS = [
    'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
    'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'
]

class EveBridge(Node):
    def __init__(self):
        super().__init__('eve_bridge_node')
        
        # 1. Kol Kontrolü
        self.publisher_ = self.create_publisher(JointTrajectory, TOPIC_ARM, 10)
        
        # 2. Kamera (Göz)
        self.create_subscription(Image, TOPIC_CAMERA, self.image_callback, 10)
        self.bridge = CvBridge()
        self.latest_image = None
        
        # 3. Beyin
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.get_logger().info('👁️ ICARUS GÖRSEL UR5 MODU AKTİF.')
        threading.Thread(target=self.start_interface, daemon=True).start()

    def image_callback(self, msg):
        try:
            self.latest_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except: pass

    def start_interface(self):
        print("\n--- 🦾 GÖREN NAIM (UR5) ---")
        print("Komutlar: 'Ne görüyorsun?', 'Kutuya bak', 'Kolu yere indir'")
        
        while rclpy.ok():
            try:
                user_input = input("\nKomutan > ")
                if user_input.lower() == 'q':
                    rclpy.shutdown()
                    break
                
                if "görüyorsun" in user_input.lower() or "analiz" in user_input.lower():
                    self.analyze_vision()
                else:
                    self.process_movement(user_input)
            except Exception as e:
                print(f"Hata: {e}")

    def analyze_vision(self):
        if self.latest_image is None:
            print("⚠️ Görüntü yok! (Gazebo Play butonuna bastın mı?)")
            return
        
        print("📸 Fotoğraf çekildi, Gemini inceliyor...", end="\r")
        pil_img = PIL.Image.fromarray(cv2.cvtColor(self.latest_image, cv2.COLOR_BGR2RGB))
        
        try:
            response = self.model.generate_content(["Kameram robotun bileğinde. Şu an ne görüyorum? Detaylı anlat.", pil_img])
            print(f"\n👁️ RAPOR: {response.text}")
        except Exception as e:
            print(f"❌ Görme Hatası: {e}")

    def process_movement(self, text):
        print("🤖 Hareket planlanıyor...", end="\r")
        
        prompt = f"""
        Sen UR5 robot kolunu yönetiyorsun.
        GÖREV: "{text}"
        
        UR5 AÇILARI (6 Eksen, Radyan):
        - Ev (Dik): [0, -1.57, 0, -1.57, 0, 0]
        - Yere Bak (Kamera aşağı): [0, -1.57, 1.57, -1.57, -1.57, 0]
        - Sağa Bak: [-1.57, -1.57, 0, -1.57, 0, 0]
        
        ÇIKTI: Sadece JSON listesi: [j1, j2, j3, j4, j5, j6]
        """
        
        try:
            response = self.model.generate_content(prompt)
            match = re.search(r'\[.*\]', response.text, re.DOTALL)
            
            if match:
                angles = json.loads(match.group(0))
                traj_msg = JointTrajectory()
                traj_msg.joint_names = ARM_JOINTS
                point = JointTrajectoryPoint()
                point.positions = [float(x) for x in angles]
                point.time_from_start.sec = 3
                traj_msg.points.append(point)
                self.publisher_.publish(traj_msg)
                print(f"✅ Hareket: {angles}")
            else:
                print("❌ Anlaşılamadı.")
        except Exception as e:
             print(f"❌ Hata: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = EveBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
