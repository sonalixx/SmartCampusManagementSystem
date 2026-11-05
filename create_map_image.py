"""
Generates clean local assets:
1. campus_navigation_map.png (Matching Implementation Screenshot 1 in PPT)
2. navigation_icon.png (For the sidebar Navigation section)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_navigation_map():
    width, height = 960, 480
    img = Image.new("RGB", (width, height), "#f2efe9")
    draw = ImageDraw.Draw(img)

    # Campus grounds (light green areas)
    draw.polygon([(180, 0), (width, 0), (width, height), (320, height)], fill="#e1eed9")
    draw.polygon([(0, 200), (120, 180), (100, height), (0, height)], fill="#e8f2e2")

    # Major road: Anekal Main Road (angled on left)
    road_pts = [(240, 0), (280, 0), (420, height), (380, height)]
    draw.polygon(road_pts, fill="#ffffff")
    draw.line([(240, 0), (380, height)], fill="#d1cbbf", width=2)
    draw.line([(280, 0), (420, height)], fill="#d1cbbf", width=2)

    # Campus interior roads / walking paths
    paths = [
        # Path from main road into campus
        [(330, 260), (480, 280), (620, 270), (780, 250), (920, 240)],
        # North connector
        [(480, 280), (450, 120), (560, 90), (750, 80)],
        # South road
        [(400, 370), (520, 390), (700, 400), (880, 410)],
        # Parking lot loop
        [(450, 120), (470, 70), (530, 60), (560, 90)]
    ]
    for p in paths:
        draw.line(p, fill="#ffffff", width=12)
        draw.line(p, fill="#dcd6cb", width=14)
        draw.line(p, fill="#ffffff", width=10)

    # Campus Buildings (light beige with subtle border)
    buildings = [
        [(520, 140), (640, 200)], # Academic Block
        [(680, 130), (780, 190)], # Central Library
        [(580, 310), (720, 360)], # Food Court & SAC
        [(760, 300), (880, 370)], # Hostel Block A
        [(480, 30), (550, 55)],   # Security & Gate
    ]
    for b in buildings:
        draw.rectangle(b, fill="#ded6cc", outline="#c4baa9", width=2)

    # The Calculated Walking Route (Green Line - exactly matching PPT Screenshot 1!)
    route = [
        (350, 300),  # Alliance University Start
        (420, 290),
        (470, 280),
        (450, 160),
        (465, 100),
        (470, 80),   # Alliance University Car Parking
    ]
    draw.line(route, fill="#15803d", width=5)

    # Start Point Marker (Circle)
    start_pt = route[0]
    draw.ellipse([(start_pt[0]-7, start_pt[1]-7), (start_pt[0]+7, start_pt[1]+7)], fill="#b91c1c", outline="#ffffff", width=2)

    # Destination Marker (Green Flag & Parking Icon P)
    dest_pt = route[-1]
    # Pin circle
    draw.ellipse([(dest_pt[0]-14, dest_pt[1]-30), (dest_pt[0]+14, dest_pt[1]-2)], fill="#16a34a", outline="#ffffff", width=2)
    draw.ellipse([(dest_pt[0]-10, dest_pt[1]-26), (dest_pt[0]+10, dest_pt[1]-6)], fill="#2563eb")
    # P text
    draw.text((dest_pt[0]-4, dest_pt[1]-23), "P", fill="#ffffff")

    # Destination Label Box
    label_box = [(dest_pt[0]-75, dest_pt[1]+6), (dest_pt[0]+75, dest_pt[1]+34)]
    draw.rectangle(label_box, fill="#ffffff", outline="#16a34a", width=1)
    draw.text((dest_pt[0]-70, dest_pt[1]+8), "Alliance University", fill="#1f2937")
    draw.text((dest_pt[0]-70, dest_pt[1]+20), "Car Parking", fill="#15803d")

    # Start Label Box
    start_box = [(start_pt[0]-60, start_pt[1]+10), (start_pt[0]+60, start_pt[1]+26)]
    draw.rectangle(start_box, fill="#ffffff", outline="#b91c1c", width=1)
    draw.text((start_pt[0]-54, start_pt[1]+12), "Alliance University", fill="#b91c1c")

    # Road Name Label (Anekal-Main-Road along road angle)
    draw.text((275, 180), "Anekal-Main-Road", fill="#6b7280")

    # Zoom controls (+ / - buttons on top left, exactly matching Leaflet/OSM in PPT)
    draw.rectangle([(20, 20), (52, 52)], fill="#ffffff", outline="#9ca3af", width=1)
    draw.text((31, 26), "+", fill="#374151")
    draw.rectangle([(20, 52), (52, 84)], fill="#ffffff", outline="#9ca3af", width=1)
    draw.text((33, 58), "-", fill="#374151")

    # Scale indicator at bottom
    draw.line([(30, height-25), (110, height-25)], fill="#374151", width=3)
    draw.text((50, height-42), "50 m", fill="#374151")

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "campus_navigation_map.png")
    img.save(out_path)
    print(f"Saved {out_path}")


def generate_navigation_icon():
    width, height = 120, 120
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Circular dark badge
    draw.ellipse([(10, 10), (110, 110)], fill="#1f2937", outline="#8b0000", width=3)
    draw.ellipse([(20, 20), (100, 100)], fill="#111827")

    # Compass needle
    # North (Red)
    draw.polygon([(60, 25), (48, 60), (60, 54)], fill="#ef4444")
    draw.polygon([(60, 25), (72, 60), (60, 54)], fill="#b91c1c")
    # South (Silver)
    draw.polygon([(60, 95), (48, 60), (60, 66)], fill="#9ca3af")
    draw.polygon([(60, 95), (72, 60), (60, 66)], fill="#d1d5db")

    # Center pin
    draw.ellipse([(55, 55), (65, 65)], fill="#ffffff", outline="#8b0000", width=2)

    out_path = os.path.join(os.path.dirname(__file__), "navigation_icon.png")
    img.save(out_path)
    print(f"Saved {out_path}")

if __name__ == "__main__":
    generate_navigation_map()
    generate_navigation_icon()

