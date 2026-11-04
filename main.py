#imports
from aegis_game.stub import *
import heapq
import math

def think() -> None:
    log("Thinking")

    # On the first round, send a request for surrounding information
    # by moving to the center (not moving). This will help initiate pathfinding.
    if get_round_number() == 1:
        set_max_energy()
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
    


###- Energy Management:
RECHARGE_AMOUNT = 5 #energy gained each time the agent calls recharge() on a charging cell
SAFETY_MARGIN = 1     #always keep 1 spare: arriving with 0 energy may kill the agent
 
#The maximum energy = the energy an agent starts with on round 1.
#All agents start with the same amount
max_energy = None

def set_max_energy() -> None: #records agent's max energy at first round
    global max_energy
    if get_round_number() == 1:
        #set the current energy as the maximum.
        max_energy = get_energy_level()

def get_max_energy() -> int:
    return max_energy

#Takes the cost of each cell in a list of paths and outputs the total
def path_cost(path) -> int:
    """Energy to walk a path (list of Locations, starting cell NOT included)."""
    total = 0
    for loc in path: #Visit every cell on the path
        #Entering a cell costs that cell's move_cost.
        total += get_cell_info_at(loc).move_cost
    return total

def energy_needed(agent_loc, dest_loc):
    """Energy to reach dest_loc and do the task there, or None if no path.
 
    For whoever codes the agent action function ---> Compare this to get_energy_level() to help decide which agent should take which task
    task_cost = energy for DIG/SAVE_SURV at the destination (0 if unknown).
    """
    path = find_path(agent_loc, dest_loc) #Finds cheapest path from here to the destination
    if path is None:
        return None
    return path_cost(path) + SAFETY_MARGIN #Safety margin is to ensure the agent has 1 energy when arriving to the cell


def energy_management(agent_loc, dest_loc) -> tuple:
    """Decide whether the agent can afford the trip, and plan charging if not.
    Returns (status, path)
 
      status:         path means:                what the caller should do:
      "ok"            path to dest_loc           walk it (an empty path means the
                                                 agent is already at dest_loc)
      "go_to_charger" path to a charger          walk it; once on the charger the
                                                 next call returns "recharge"
      "recharge"      [] (stay)                        call recharge() right now
      "go_anyway"     path to dest_loc           not enough energy and no charger
                                                 helps: walk it anyway
      "no_path"       None                       dest_loc cannot be reached at all
 
    The safety margin (1) is also the cost of a save(), so an agent that arrives
    with exactly the margin can still use its last energy to rescue a survivor.
    """
    energy = get_energy_level() #How much energy the agent has right now.
    max_energy = get_max_energy() #The most energy this agent can ever hold (its starting amount).
    chargers = get_charging_cells() #Locations of every charging cell on the map.
 
    direct = find_path(agent_loc, dest_loc) #Cheapest path from here straight to the destination.
    
    if direct is None: #No path at all means the destination is unreachable.
        return "no_path", None
    
    direct_cost = path_cost(direct) #Energy to just walk the direct path
    needed = direct_cost + SAFETY_MARGIN #Total energy needed: the walk plus the spare energy we must still have on arrival.
 
    if energy >= needed: #If we already have enough energy, no charging is needed
        return "ok", direct
 
    #On a charger AND (a full charge would be enough OR we are not full yet)?
    if agent_loc in chargers and (needed <= max_energy or energy < max_energy):
        return "recharge", []
 
    best = None  #A charger that lets us finish the trip after one charge
    hop = None   #A charger that just gets us closer

    for charger in chargers: #Try every charging cell as a possible stop.
        to_charger = find_path(agent_loc, charger) #Cheapest path from here to this charger.

        if to_charger is None:#No path to this charger, so it is not an option.
            continue

        cost_to = path_cost(to_charger)#Energy needed just to get to the charger.
       
        if cost_to + SAFETY_MARGIN > energy: #If we cannot afford the walk to the charger
            continue
 
        from_charger = find_path(charger, dest_loc) #Cheapest path from the charger onward to the destination.

        if from_charger is None: #No path from this charger to the destination, so it is not an option.
            continue

        cost_from = path_cost(from_charger)#Energy to walk from the charger to the destination.
        needed_after = cost_from + SAFETY_MARGIN #Energy we must hold when we leave the charger
 
        #Can one full charge at this charger cover the rest of the trip?
        if needed_after <= max_energy:
            #One charger is enough to finish. How many recharge() calls?
            #Calculates the energy we are short by
            deficit = needed_after - (energy - cost_to)
            #Each recharge gives 5, so round up how many are needed (never below 0)
            recharges = max(0, math.ceil(deficit / RECHARGE_AMOUNT))
            #Fewest total rounds wins; ties go to the lower energy spent
            #Calculates the amount of rounds spent to get to destination. Steps to charger + # of recharges + steps after charging
            rounds = len(to_charger) + recharges + len(from_charger)
            #Tuple score compares the # of rounds spent first, if tied it compares the energy spent
            score = (rounds, cost_to + cost_from)
            #Keep this charger if it is the first one, or beats the best so far.
            if best is None or score < best[0]:
                #Remember its score and the path to it.
                best = (score, to_charger)
        
        elif cost_from < direct_cost: #Runs only when charger can't finish a trip
            #prefer the one with the least amount of walking left to the destination, and ties go to the cheaper energy wise
            hop_score = (cost_from, cost_to)
            #Keep it if it is the first hop option, or closer than the best so far.
            if hop is None or hop_score < hop[0]:
                #Remember its score and the path to it.
                hop = (hop_score, to_charger)
 
    #A finishing charger was found: send the agent along the path to it.
    if best is not None:
        #best[1] is the path to that charger.
        return "go_to_charger", best[1]
    #only used when no charger can be found to finish the trip
    if hop is not None:
        #hop[1] is the path to that charger.
        return "go_to_charger", hop[1]
    #Nothing worked: tell agent to try the trip anyway along the direct path.
    return "go_anyway", direct
### end Energy Management

# big function that evaluates available agents, gives them the necessary tasks (task_id function), say assignments and reassign
def agent_coordination():
    pass

# execute agent_coordination task, tasks available will be to move, wait, dig, charge, or save
def agent_action():
    ### Not sure what this function will return yet, but I generally laid out how to use the energy function
    my_loc = get_location()
    status, path = energy_management(my_loc, target_loc)
 
    if status == "no_path":
        return "no_path"
 
    if status == "recharge":
        recharge()
        return "recharged"
 
    #"ok", "go_to_charger" and "go_anyway" all mean: walk the first step of path.
    if not path:
        #An empty path means we are already standing on the target.
        return "arrived"
 
    #path[0] is the cell right next to us; direction_to turns it into a Direction.
    move(my_loc.direction_to(path[0]))
    return "moved"
###
    pass

# used to scan the rubble and maintain requirements and unfinished tasks
def task_id():
    pass
