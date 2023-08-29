import os
import cv2
# 무기라고 판단되는 항목들의 리스트
weapons = []
weapon_list = []

def add(weapon) :
    weapons.append(weapon)
    
def delete(weapon) :
    weapons.remove(weapon)
    
def show_weapons() :
    print(weapons)

def is_weapon(class_name,frame) :
    if class_name in weapons:
        weapon_list.append((frame.copy(), class_name))
    
def save_weapon(output_path) :
    os.makedirs(output_path, exist_ok=True)
    for i, (frame, class_name) in enumerate(weapon_list):
        image_path = os.path.join(output_path, f"weapon_{i}.jpg")
        cv2.imwrite(image_path, frame)