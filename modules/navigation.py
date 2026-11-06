"""
Alliance University - Campus Navigation Module
Module 1: Pathfinding & Interactive Wayfinding Engine
Algorithms: A* (A-Star) Pathfinding and Dijkstra Shortest Path
"""

import math
from typing import List, Dict, Any, Tuple, Optional
import networkx as nx
from PIL import Image, ImageDraw, ImageFont

from data.seed_data import CAMPUS_NODES, CAMPUS_EDGES, ASSEMBLY_POINTS_MAPPING


class CampusNavigator:
    """Intelligent Wayfinding and Route Calculation Engine."""

    def __init__(self):
        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self):
        """Constructs the spatial graph with node coordinates and weighted edges."""
        for name, data in CAMPUS_NODES.items():
            self.graph.add_node(name, **data)

        for u, v, weight in CAMPUS_EDGES:
            self.graph.add_edge(u, v, weight=weight)

    @staticmethod
    def _euclidean_heuristic(u: str, v: str) -> float:
        """Heuristic function for A* pathfinding using 2D coordinates."""
        u_data = CAMPUS_NODES.get(u, {})
        v_data = CAMPUS_NODES.get(v, {})
        ux, uy = u_data.get("x", 0), u_data.get("y", 0)
        vx, vy = v_data.get("x", 0), v_data.get("y", 0)
        return math.hypot(ux - vx, uy - vy)

    def find_route(
        self, start: str, destination: str, algorithm: str = "A*"
    ) -> Dict[str, Any]:
        """Calculates optimal walking route between two campus locations."""
        if start not in self.graph or destination not in self.graph:
            return {
                "success": False,
                "error": "Start or destination location not recognized.",
                "path": [],
                "distance": 0,
                "estimated_time_mins": 0,
                "steps": []
            }

        if start == destination:
            return {
                "success": True,
                "path": [start],
                "distance": 0,
                "estimated_time_mins": 0,
                "steps": ["You are already at your chosen destination!"]
            }

        try:
            if algorithm == "A*":
                path = nx.astar_path(
                    self.graph, start, destination,
                    heuristic=self._euclidean_heuristic, weight="weight"
                )
            else:
                path = nx.dijkstra_path(
                    self.graph, start, destination, weight="weight"
                )

            # Calculate total distance along path
            total_distance = sum(
                self.graph[path[i]][path[i+1]]["weight"]
                for i in range(len(path) - 1)
            )

            # Average walking speed ~ 1.4 m/s (~84 meters/minute)
            time_mins = max(1, round(total_distance / 84.0))

            # Turn-by-turn navigation instructions
            steps = []
            for i in range(len(path) - 1):
                cur = path[i]
                nxt = path[i+1]
                leg_dist = self.graph[cur][nxt]["weight"]
                nxt_info = CAMPUS_NODES.get(nxt, {})
                fl = nxt_info.get("floor", "Ground")
                steps.append(
                    f"Walk {leg_dist}m from **{cur}** to **{nxt}** ({fl})"
                )

            return {
                "success": True,
                "start": start,
                "destination": destination,
                "algorithm_used": algorithm,
                "path": path,
                "distance": total_distance,
                "estimated_time_mins": time_mins,
                "steps": steps,
                "node_count": len(path)
            }

        except nx.NetworkXNoPath:
            return {
                "success": False,
                "error": f"No accessible walking path found between {start} and {destination}.",
                "path": [],
                "distance": 0,
                "estimated_time_mins": 0,
                "steps": []
            }

    def find_nearest_assembly_point(self, current_location: str) -> Dict[str, Any]:
        """Identifies nearest emergency assembly point from current location."""
        min_dist = float("inf")
        best_pt = None
        best_route = None

        cur_data = CAMPUS_NODES.get(current_location)
        if not cur_data:
            first_pt = list(ASSEMBLY_POINTS_MAPPING.keys())[0]
            return {
                "assembly_point": first_pt,
                "distance": 150,
                "time_mins": 2,
                "info": ASSEMBLY_POINTS_MAPPING[first_pt]
            }

        for pt_name, pt_info in ASSEMBLY_POINTS_MAPPING.items():
            # Estimate distance to assembly point coords
            px, py = pt_info["coords"]
            dist = math.hypot(cur_data["x"] - px, cur_data["y"] - py) * 0.8
            if dist < min_dist:
                min_dist = dist
                best_pt = pt_name

        time_mins = max(1, round(min_dist / 84.0))
        return {
            "assembly_point": best_pt,
            "distance": round(min_dist),
            "time_mins": time_mins,
            "info": ASSEMBLY_POINTS_MAPPING.get(best_pt, {})
        }

    def render_dynamic_map(
        self,
        active_path: Optional[List[str]] = None,
        width: int = 1000,
        height: int = 560
    ) -> Image.Image:
        """
        Dynamically renders the Alliance University Campus Navigation Map with
        walking routes, building footprints, and point-of-interest markers.
        """
        img = Image.new("RGB", (width, height), "#0d1117")
        draw = ImageDraw.Draw(img)

        # 1. Background grid & lawn areas
        # Outer lawns
        draw.polygon([(0, 0), (width, 0), (width, 100), (0, 100)], fill="#111923")
        draw.polygon([(650, 380), (width, 380), (width, height), (650, height)], fill="#122319")
        # Central green lawn
        draw.rectangle([(420, 240), (620, 360)], fill="#16291e", outline="#234230", width=2)
        draw.text((475, 290), "Central Campus Lawn\n(Primary Assembly Area)", fill="#4ade80")

        # 2. Draw all walking paths
        for u, v, weight in CAMPUS_EDGES:
            u_pt = (CAMPUS_NODES[u]["x"], CAMPUS_NODES[u]["y"])
            v_pt = (CAMPUS_NODES[v]["x"], CAMPUS_NODES[v]["y"])
            draw.line([u_pt, v_pt], fill="#21262d", width=8)
            draw.line([u_pt, v_pt], fill="#30363d", width=4)

        # 3. Draw active calculated route (if provided)
        if active_path and len(active_path) > 1:
            route_coords = [
                (CAMPUS_NODES[node]["x"], CAMPUS_NODES[node]["y"])
                for node in active_path if node in CAMPUS_NODES
            ]
            # Glowing shadow effect
            draw.line(route_coords, fill="#047857", width=12)
            # Main high-visibility walking path
            draw.line(route_coords, fill="#10b981", width=6)

        # 4. Draw buildings & POI nodes
        for name, data in CAMPUS_NODES.items():
            x, y = data["x"], data["y"]
            cat = data.get("category", "Academic")

            # Determine color by category
            if cat == "Academic":
                fill_col = "#1e293b"
                border_col = "#38bdf8"
            elif cat == "Laboratories":
                fill_col = "#1e293b"
                border_col = "#a855f7"
            elif cat == "Library":
                fill_col = "#1e293b"
                border_col = "#f59e0b"
            elif cat == "Dining":
                fill_col = "#1e293b"
                border_col = "#f97316"
            elif cat == "Hostels":
                fill_col = "#1e293b"
                border_col = "#ec4899"
            elif cat == "Emergency":
                fill_col = "#2a1517"
                border_col = "#ef4444"
            else:
                fill_col = "#1e293b"
                border_col = "#64748b"

            # Draw building block badge
            b_width, b_height = 130, 42
            x0, y0 = x - b_width // 2, y - b_height // 2
            x1, y1 = x + b_width // 2, y + b_height // 2

            draw.rectangle([(x0, y0), (x1, y1)], fill=fill_col, outline=border_col, width=2)
            
            # Shortened label
            short_name = name.split(" - ")[0].replace("Alliance University ", "")
            if len(short_name) > 17:
                short_name = short_name[:16] + ".."
            draw.text((x0 + 8, y0 + 6), short_name, fill="#f8fafc")
            draw.text((x0 + 8, y0 + 22), f"• {cat}", fill=border_col)

        # 5. Highlight Start & Destination Pins
        if active_path and len(active_path) > 0:
            # Start pin (Red)
            s_name = active_path[0]
            if s_name in CAMPUS_NODES:
                sx, sy = CAMPUS_NODES[s_name]["x"], CAMPUS_NODES[s_name]["y"]
                draw.ellipse([(sx - 12, sy - 38), (sx + 12, sy - 14)], fill="#ef4444", outline="#ffffff", width=2)
                draw.polygon([(sx - 8, sy - 18), (sx + 8, sy - 18), (sx, sy - 6)], fill="#ef4444")
                draw.text((sx - 4, sy - 34), "A", fill="#ffffff")

            # Destination pin (Green Flag)
            d_name = active_path[-1]
            if d_name in CAMPUS_NODES:
                dx, dy = CAMPUS_NODES[d_name]["x"], CAMPUS_NODES[d_name]["y"]
                draw.ellipse([(dx - 12, dy - 38), (dx + 12, dy - 14)], fill="#10b981", outline="#ffffff", width=2)
                draw.polygon([(dx - 8, dy - 18), (dx + 8, dy - 18), (dx, dy - 6)], fill="#10b981")
                draw.text((dx - 4, dy - 34), "B", fill="#ffffff")

        # 6. Map UI Overlays
        # Map Title banner
        draw.rectangle([(20, 16), (360, 52)], fill="#161b22", outline="#30363d", width=1)
        draw.text((32, 24), "ALLIANCE UNIVERSITY CAMPUS MAP (A* Wayfinding)", fill="#58a6ff")

        # Map Scale indicator
        draw.line([(width - 150, height - 25), (width - 50, height - 25)], fill="#e2e8f0", width=3)
        draw.text((width - 120, height - 42), "100 metres", fill="#94a3b8")

        return img

