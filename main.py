#imports
from aegis_game.stub import *
import heapq
import math

def think() -> None:
    log("Thinking")

    # On the first round, send a request for surrounding information
    # by moving to the center (not moving). This will help initiate pathfinding.
    if get_round_number() == 1:
        move(Direction.CENTER)
        return

    # Fetch the cell at the agent's current location.
    # If you want to check a different location, use on_map(agent_loc) first
    # to ensure it's within the world bounds. The agent's own location is always valid.
    cell = get_cell_info_at(get_location())

    # Get the top layer at the agent's current location.
    # If a survivor is present, save it and end the turn.
    if isinstance(cell.top_layer, Survivor):
        save()
        return

   
#pathfinding and information
def find_path(agent_loc, rubble_loc):
     #initialize start location, survivor location, discovery heap, and past dict
        discovered_heap = []
        heapq.heappush(discovered_heap, (max(abs(rubble_loc.x - agent_loc.x), abs(rubble_loc.y - agent_loc.y) ), [], agent_loc))
        past_location = {}
    
        #cost so far to reach n
        g_n = {agent_loc: 0}
    
        #total f_score dict
        f_n = {agent_loc: max(abs(rubble_loc.x - agent_loc.x), abs(rubble_loc.y - agent_loc.y) )}
    
        #while we havent discovered everything
        #A* code inspired by pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        while discovered_heap:
    
            #get the smallest next location
            current_record = heapq.heappop(discovered_heap)
            current_node = current_record[2]
    
    
            #check if we already found a better way to reach this node
            node_h = max(abs(rubble_loc.x - current_node.x), abs(rubble_loc.y - current_node.y))
            node_g = current_record[0] - node_h
            if node_g != g_n.get(current_node, math.inf):
                continue
    
            #check if we already found a better equal cost direction priority path for this node
            backtrack_node = current_node
            full_path = [current_node]
            while backtrack_node in past_location.keys():
                backtrack_node = past_location[backtrack_node]
                full_path.insert(0, backtrack_node)
    
            #translate that track into direction priority numbers
            older_directions = []
    
            for i in range(len(full_path) - 1):
                direction = full_path[i].direction_to(full_path[i + 1])  
    
                if direction == Direction.NORTH:
                    older_directions.append(1)
                if direction == Direction.SOUTH:
                    older_directions.append(5)
                if direction == Direction.EAST:
                    older_directions.append(3)
                if direction == Direction.WEST:
                    older_directions.append(7)
                if direction == Direction.NORTHEAST:
                    older_directions.append(2)
                if direction == Direction.NORTHWEST:
                    older_directions.append(8)
                if direction == Direction.SOUTHEAST:
                    older_directions.append(4)
                if direction == Direction.SOUTHWEST:
                    older_directions.append(6)
            if current_record[1] != older_directions:
                continue
            
            #if were at the survivior
            if current_node == rubble_loc:
    
                #reconstruct the full path to the survivor and move one step of the way
                #reconstruction happens every round for version 3, move -> reconstruct -> move -> reconstruct
                full_path = [current_node]
                while current_node in past_location.keys():
                    current_node = past_location[current_node]
                    full_path.insert(0, current_node)
    
                if len(full_path) >= 2 or agent_loc == rubble_loc:
                    return full_path[1:]
    
            directions = []
    
            #checking whether the direction is on the map and that its not a killer cell, then adding that, the total path leading up to it, and a priority number
            if on_map(current_node.add(Direction.NORTH)) and not get_cell_info_at(current_node.add(Direction.NORTH)).is_killer_cell():
                directions.append([current_node.add(Direction.NORTH), 1, current_record[1] + [1]])
            if on_map(current_node.add(Direction.NORTHEAST)) and not get_cell_info_at(current_node.add(Direction.NORTHEAST)).is_killer_cell():
                directions.append([current_node.add(Direction.NORTHEAST), 2, current_record[1] + [2]])
            if on_map(current_node.add(Direction.EAST)) and not get_cell_info_at(current_node.add(Direction.EAST)).is_killer_cell():
                directions.append([current_node.add(Direction.EAST), 3, current_record[1] + [3]])
            if on_map(current_node.add(Direction.SOUTHEAST)) and not get_cell_info_at(current_node.add(Direction.SOUTHEAST)).is_killer_cell():
                directions.append([current_node.add(Direction.SOUTHEAST), 4, current_record[1] + [4]])
            if on_map(current_node.add(Direction.SOUTH)) and not get_cell_info_at(current_node.add(Direction.SOUTH)).is_killer_cell():
                directions.append([current_node.add(Direction.SOUTH), 5, current_record[1] + [5]])
            if on_map(current_node.add(Direction.SOUTHWEST)) and not get_cell_info_at(current_node.add(Direction.SOUTHWEST)).is_killer_cell():
                directions.append([current_node.add(Direction.SOUTHWEST), 6, current_record[1] + [6]])
            if on_map(current_node.add(Direction.WEST)) and not get_cell_info_at(current_node.add(Direction.WEST)).is_killer_cell():
                directions.append([current_node.add(Direction.WEST), 7, current_record[1] + [7]])
            if on_map(current_node.add(Direction.NORTHWEST)) and not get_cell_info_at(current_node.add(Direction.NORTHWEST)).is_killer_cell():
                directions.append([current_node.add(Direction.NORTHWEST), 8, current_record[1] + [8]])
         
            #for all available locations
            for location in directions:
    
                #calculate a new g_score
                new_g_n = g_n[current_node] + get_cell_info_at(location[0]).move_cost
    
                #check if a path to the node has already been constructed and make a track of that path
                backtrack_node = location[0]
                full_path = [backtrack_node]
                while backtrack_node in past_location.keys():
                    backtrack_node = past_location[backtrack_node]
                    full_path.insert(0, backtrack_node)
    
                #translate that track into direction priority numbers
                older_directions = []
    
                for i in range(len(full_path) - 1):
                    direction = full_path[i].direction_to(full_path[i + 1])  
    
                    if direction == Direction.NORTH:
                        older_directions.append(1)
                    if direction == Direction.SOUTH:
                        older_directions.append(5)
                    if direction == Direction.EAST:
                        older_directions.append(3)
                    if direction == Direction.WEST:
                        older_directions.append(7)
                    if direction == Direction.NORTHEAST:
                        older_directions.append(2)
                    if direction == Direction.NORTHWEST:
                        older_directions.append(8)
                    if direction == Direction.SOUTHEAST:
                        older_directions.append(4)
                    if direction == Direction.SOUTHWEST:
                        older_directions.append(6)
    
                # Checking if a g score exists, otherwise get infinity
                # if it does exist, set a g_score if that path is smaller than the old path
                # if the two g_scores are equal, tie break based on the directions
                if (new_g_n < g_n.get(location[0], math.inf)) or ((new_g_n == g_n.get(location[0], math.inf)) and location[2] < older_directions):
                    #initialize that new node and its scores and push it to the heap
                    past_location[location[0]] = current_node
                    g_n[location[0]] = new_g_n
                    f_n[location[0]] = new_g_n + max(abs(rubble_loc.x - location[0].x), abs(rubble_loc.y - location[0].y) )
                    heapq.heappush(discovered_heap, (max(abs(rubble_loc.x - location[0].x), abs(rubble_loc.y - location[0].y)) + new_g_n, current_record[1] + [location[1]], location[0]))
    


# checking whether agent has enough energy for desination, plan charging, likely will use find_path
def energy_management():
    pass

# big function that evaluates available agents, gives them the necessary tasks (task_id function), say assignments and reassign
def agent_coordination():
    pass

# execute agent_coordination task, tasks available will be to move, wait, dig, charge, or save
def agent_action():
    pass

# used to scan the rubble and maintain requirements and unfinished tasks
def task_id():
    pass