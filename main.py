import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
import networkx as nx
import math
from grid_tools import GridTools
SIZE = 300

def generate(G,airport, start_node):



    # waether_path = "heat_map/final_weather.npy"
    # grid = np.load(waether_path)
    traj_path = f'airports/{airport}.npy'
    grid = traj = np.load(traj_path)
    # grid = grid + traj

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

    # pos = {(x,y):(y,-x) for x,y in G.nodes()}
    # nx.draw(G, pos=pos, 
    #         node_color = [get_node_color(grid[x][y]) for x,y in G.nodes()],
    #         node_size=20)



    end = (int(SIZE/2),int(SIZE/2))
    path = nx.astar_path(G, start_node, end, weight='cost')

    # nx.draw_networkx_nodes(G, pos=pos, nodelist=path, node_color='blue', node_size=15)
    nodes_cords = []
    for i in path:
        nodes_cords.append(i)

    df = pd.DataFrame(nodes_cords)
    df.to_csv('nodes_cords.csv', index=False, header=False)

    # plt.show()
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

    KIAH_tool = GridTools(airports_cords['KIAH'][0], airports_cords['KIAH'][1], 300)
    KORD_tool = GridTools(airports_cords['KORD'][0], airports_cords['KORD'][1], 300)
    KDFW_tool = GridTools(airports_cords['KDFW'][0], airports_cords['KDFW'][1], 300)
    KDEN_tool = GridTools(airports_cords['KDEN'][0], airports_cords['KDEN'][1], 300)
    KATL_tool = GridTools(airports_cords['KATL'][0], airports_cords['KATL'][1], 300)

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

        if airport == 'KIAH':
            tool = KIAH_tool
        elif airport == 'KORD':
            tool = KORD_tool
        elif airport == 'KDFW':
            tool = KDFW_tool
        elif airport == 'KDEN':
            tool = KDEN_tool
        elif airport == 'KATL':
            tool = KATL_tool
        else:
            continue

        start_node = tool.get_index_from_point(lat, lon)
        output = generate(G,airport, start_node)
        to_save = []
        ctr = 0
        for index, row in output.iterrows():
            lat, lon = tool.get_cords_from_index(row[0], row[1])
            to_save.append((ctr, lat, lon))
            ctr += 1

        df = pd.DataFrame(to_save, columns=['seq_number', 'lat', 'lon'])

        df.to_csv(f'solution/{id}.csv', index=False)

        print(f"Time taken: {time.time() - start_time}")

if __name__ == '__main__':
    main()
