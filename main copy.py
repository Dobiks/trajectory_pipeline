import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import networkx as nx
import math
import geopy.distance
from grid_tools import GridTools
SIZE = 300
def generate(G,airport, start_node, id):

    DRAW = 0
    weather_path = f"weather_matrices/{id}.npy"
    #check if exists
    airport_cord = airport
    airports_cords = {
        'KIAH': (29.97762,-95.31953),
        'KORD': (38.17409, -85.73649),
        'KDFW': (32.8571,-97.05491),
        'KDEN': (39.83613,-104.64165),
        'KATL':(33.6367, -84.42786)
    }
    # for key, value in airports_cords.items():
    #     if (round(float(value[0]),1),round(float(value[1]),1)) == (round(float(airport[0]),1),round(float(airport[1]),1))  :
    #         airport = key
    
    traj_path = f'airports/KORD.npy'

    if os.path.exists(weather_path):
        weather = np.load(weather_path)
        grid = np.load(traj_path)
        grid = grid + weather
        DRAW = 0
        # print("drawing")
    else:
        grid = np.load(traj_path)
        DRAW = 0



    for i in range(SIZE):
        for j in range(SIZE):
            G.nodes[(i,j)]['value'] = grid[i][j]

    d = {(i,j): int(G.nodes[i]['value']) for i,j in G.edges}

    # print("unique:",np.unique(list(d.values())))



    nx.set_edge_attributes(G, d, 'cost')

    def get_node_color(value):
        if value == 0:
            return 'yellow'
        elif value == 1:
            return 'black'
        else:
            return 'red'

    if DRAW:
        pos = {(x,y):(y,-x) for x,y in G.nodes()}
        nx.draw(G, pos=pos, 
                node_color = [get_node_color(grid[x][y]) for x,y in G.nodes()],
                node_size=20)



    end = (int(SIZE/2),int(SIZE/2))
    path = nx.astar_path(G, start_node, end, weight='cost')

    if DRAW:
        nx.draw_networkx_nodes(G, pos=pos, nodelist=path, node_color='blue', node_size=15)
    nodes_cords = []
    for i in path:
        nodes_cords.append(i)

    df = pd.DataFrame(nodes_cords)
    df.to_csv('nodes_cords.csv', index=False, header=False)

    if DRAW:
        plt.show()
    return df


def nodes_to_lat_lon(df: pd.DataFrame):
    pass


def main():

    G = nx.grid_2d_graph(SIZE,SIZE)
    #add diagonal edges
    for i in range(SIZE):
        for j in range(SIZE):
            if i != SIZE - 1 and j != SIZE - 1:
                G.add_edge((i,j), (i+1,j+1))
                G.add_edge((i+1,j), (i,j+1))

    airports_cords = {
        'KIAH': (29.97762,-95.31953),
        'KORD': (41.96584,-87.85868),
        'KDFW': (32.8571,-97.05491),
        'KDEN': (39.83613,-104.64165),
        'KATL':(33.6367, -84.42786)
    }

    # KIAH_tool = GridTools(airports_cords['KIAH'][0], airports_cords['KIAH'][1], 300)
    # KORD_tool = GridTools(airports_cords['KORD'][0], airports_cords['KORD'][1], 300)
    # KDFW_tool = GridTools(airports_cords['KDFW'][0], airports_cords['KDFW'][1], 300)
    # KDEN_tool = GridTools(airports_cords['KDEN'][0], airports_cords['KDEN'][1], 300)
    # KATL_tool = GridTools(airports_cords['KATL'][0], airports_cords['KATL'][1], 300)

    file_path = 'test_flights.csv'
    df = pd.read_csv(file_path)
    tmp_itr = 0
    for index, row in df.iterrows():
        start_time = time.time()
        tmp_itr += 1
        print(tmp_itr)
        airport = row['destination_airport_id']
        id = row['id']
        timestamp = row['start_position_timestamp']
        lat = row['start_position_lat']
        lon = row['start_position_lon']
        waypoints = pd.read_csv(f"../hackathon/trajectory_challenge/routes/{id}.csv")
        to_save = []
        ctr = 0

        for index, row in waypoints.iterrows():
            airport_lat = waypoints.values[-1][1]
            airport_lat = waypoints.values[-1][2]
            if geopy.distance.distance((airport_lat,airport_lat), (row['lat'],row['lon'])).miles > 150:
                last_waypoint =  (row['lat'], row['lon'])
                continue

            tool = GridTools(row['lat'], row['lon'], 300)
            start_node = tool.get_index_from_point(row['lat'], row['lon'])
            if index > 0:
                output = generate(G,last_waypoint, start_node, id)
            else:
                output = generate(G,airport, start_node, id)
            for index, row1 in output.iterrows():
                lat, lon = tool.get_cords_from_index(row1[1], row1[0])
                to_save.append((ctr, lat, lon))
                ctr += 1
            last_waypoint =  (row['lat'], row['lon'])
        df = pd.DataFrame(to_save, columns=['seq_number', 'lat', 'lon'])

        df.to_csv(f'{id}_6.csv', index=False)
            # df.to_csv(f'{id}.csv', index=False)

        print(f"Time taken: {time.time() - start_time}")
        break

if __name__ == '__main__':
    main()
