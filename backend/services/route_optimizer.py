from backend.database import db
from backend.models import Street, Route
import heapq

# Map severity to weights
SEVERITY_WEIGHTS = {
    "normal": 1,
    "alert": 5,
    "severe": 100
}

def get_first_segment(street_name):
    """
    Convert user input to the first segment (_1)
    """
    if street_name.endswith("_1"):
        return street_name
    return f"{street_name}_1"

def find_safest_route(start_street_name, end_street_name):
    """
    Compute safest route using Dijkstra with pre-fetched routes and streets.
    Returns coordinates, severities, and total distance.
    """

    # Convert to first segment names
    start_segment = get_first_segment(start_street_name)
    end_segment = get_first_segment(end_street_name)

    # Fetch all streets into a dictionary for fast lookup
    streets = {s.street_id: s for s in Street.query.all()}
    street_name_map = {s.street_name: s for s in streets.values()}

    # Fetch start and end street objects
    start_street = street_name_map.get(start_segment) or street_name_map.get(start_street_name)
    end_street = street_name_map.get(end_segment) or street_name_map.get(end_street_name)

    if not start_street or not end_street:
        return {"error": "Start or end street not found."}

    # Fetch all routes
    routes = Route.query.all()

    # Build graph with adjacency list
    # Each edge: start and end with weight and distance
    # reverse edge  
    graph = {}
    route_lookup = {}  # {(start_id, end_id): route}
    for r in routes:
        severity = streets[r.start_street_id].current_severity
        weight = SEVERITY_WEIGHTS.get(severity, 1)

        # Forward edge
        graph.setdefault(r.start_street_id, []).append((r.end_street_id, weight, r.distance))
        route_lookup[(r.start_street_id, r.end_street_id)] = r

        # Reverse edge
        graph.setdefault(r.end_street_id, []).append((r.start_street_id, weight, r.distance))
        route_lookup[(r.end_street_id, r.start_street_id)] = Route(
            start_street_id=r.end_street_id,
            end_street_id=r.start_street_id,
            distance=r.distance,
            route_start_lat=r.route_end_lat,
            route_start_lon=r.route_end_lon,
            route_end_lat=r.route_start_lat,
            route_end_lon=r.route_start_lon
        )

    # Dijkstra using heap
    queue = [(0, start_street.street_id, [])]  # (total_weight, current_id, path)
    visited = {}

    while queue:
        total_weight, current_id, path = heapq.heappop(queue)

        if current_id in visited and total_weight >= visited[current_id]:
            continue
        visited[current_id] = total_weight
        path = path + [current_id]

        if current_id == end_street.street_id:
            # Build result
            coords = []
            severities = []
            total_distance = 0

            for i in range(len(path) - 1):
                route = route_lookup.get((path[i], path[i + 1]))
                if route:
                    total_distance += route.distance
                    coords.append({
                        "start_lat": float(route.route_start_lat),
                        "start_lon": float(route.route_start_lon),
                        "end_lat": float(route.route_end_lat),
                        "end_lon": float(route.route_end_lon),
                        "severity": streets[path[i]].current_severity
                    })
                    severities.append(streets[path[i]].current_severity)

            return {
                "coordinates": coords,
                "total_distance": total_distance,
                "severities": severities
            }

        for neighbor_id, weight, distance in graph.get(current_id, []):
            new_weight = total_weight + weight
            if neighbor_id not in visited or new_weight < visited.get(neighbor_id, float('inf')):
                heapq.heappush(queue, (new_weight, neighbor_id, path))

    return {"error": "No route found."}
