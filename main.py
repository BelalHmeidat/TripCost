def get_raw_list():
    raw_list = [
        # list 1
        # ['start', ['A', 22, 70], ['B', 8, 80], ['C', 12, 80]],
        # ['A', ['D', 8, 50], ['E', 10, 70]],
        # ['B', ['D', 25, 50], ['E', 10, 70]],
        # ['C', ['D', 13, 50], ['E', 13, 70]],
        # ['D', ['F', 25, 50], ['G', 30, 70], ['H', 18, 70], ['I', 27, 60]],
        # ['E', ['F', 12, 50], ['G', 10, 70], ['H', 8, 70], ['I', 7, 60]],
        # ['F', ['J', 26, 50], ['K', 13, 70], ['L', 15, 60]],
        # ['G', ['J', 8, 50], ['K', 10, 70], ['L', 10, 60]],
        # ['H', ['J', 20, 50], ['K', 10, 70], ['L', 10, 60]],
        # ['I', ['J', 15, 50], ['K', 10, 70], ['L', 7, 60]],
        # ['J', ['end', 10, 0]],
        # ['K', ['end', 10, 0]],
        # ['L', ['end', 10, 0]],
        # ['end', ]
        # list 2
        ['a', ['b', 5, 0], ['c', 15, 0], ['d', 10, 0]],
        ['b', ['f', 15, 0], ['c', 5, 0]],
        ['c', ['g', 5, 0]],
        ['d', ['g', 10, 0], ['e', 5, 0]],
        ['e', ],
        ['f', ['i', 10, 0]],
        ['g', ['h', 5, 0]],
        ['h', ['i', 5, 0]],
        ['i']
    ]
    return raw_list


# routes = get_raw_list()
city_list = None

# Method that returns the char of indexes
def get_dict_of_cities(routes):
    char_to_indx = {}
    for i in range(len(routes)):
        char_to_indx[routes[i][0]] = i
    global city_list
    city_list = routes
    return char_to_indx


char_to_indx = None

def map_cities(raw_list):
    l = len(raw_list)
    cost_table = [[-1 for i in range(l)] for j in range(l)]  # -1: empty cell
    label_table = [['0' for i in range(l)] for j in range(l)]

    for i in range(l):
        for j in range(l):
            if (j <= i):
                cost_table[i][j] = 0

    for i in range(len(raw_list)):
        for j in range(1, len(raw_list[i])):
            city = raw_list[i][j][0]
            cost = raw_list[i][j][1] + raw_list[i][j][2]
            label_table[i][char_to_indx[city]] = city
            cost_table[i][char_to_indx[city]] = cost

    return cost_table



# Method that returns the label of the city from it's assigned index
def index_to_char(index):
    return city_list[index][0]


def get_routes_2(cost_map, start, end):
    suggested_routes = []

    start_row = char_to_indx[start]
    end_col = char_to_indx[end]
    clone = []
    for row in cost_map:
        clone.append(row.copy())

    cell_to_empty = (0, 0)
    there_is_more = True
    while there_is_more:
        there_is_more = False
        next_col = end_col
        current_route = [end, ]
        cost = 0
        while next_col != start_row:
            route_count = 0
            j = next_col
            for row in range(start_row, len(clone)):
                if clone[row][j] > 0:
                    route_count += 1
                    # j = next_col
                    next_col = row
            cost += clone[next_col][j]
            current_route.append(index_to_char(next_col))
            if route_count >= 2:
                cell_to_empty = next_col, j
                there_is_more = True
        clone[cell_to_empty[0]][cell_to_empty[1]] = 0
        current_route.append(cost)
        suggested_routes.append(current_route)
    return suggested_routes


# Method that updates the row of the source city in the table of route costs with optimal costs. It takes the cost
# table and returns a vector
def get_route_3(cost_map, src_city, dest_city):
    clone = []
    for row in cost_map:
        clone.append(row.copy())
    label_vector = ['0'] * len(cost_map)  # initializing the label vector
    src = char_to_indx[src_city]  # getting the index of the source city from dictionary
    dest = char_to_indx[dest_city]  # getting the index of the destination city from dictionary
    # There are two nested loops one goes over every destination city and finds the lowest cost and path that leads
    # to that said city and places it in the cell that joins the source with the path
    for j in range(src + 1, dest + 1):
        # looping over each city from source to destination no need to start at source as it
        # will always be zero from source ti itself
        optimal = clone[src][j]
        # variable to store the optimal path it. This is just the initial value of it. It will be compared with every
        # alternative path found after and updated if any shorter one was found
        for i in range(src, j):  # Looping over the cities that lead to that city
            if clone[i][j] == -1 or clone[src][i] == -1:  # -1s are skipped because they represent a no path
                continue
            cost_through = clone[i][j] + clone[src][i]
            # variable to store an alternative path to be compared with the optimal path
            if cost_through > optimal and optimal != -1:
                # Paths that cost more than the optimal or are no paths are skipped
                continue
            # Paths that are less to the optimal in cost are new optimal paths
            optimal = cost_through
            #  Optimal paths are updated in the cell that joins the source with the current city we are at
            clone[src][j] = optimal  # updating cost with source city
            label_vector[j] = index_to_char(i)  # labeling the city that lead to that path
    # for i in clone: print(i)
    path = [dest_city]
    current_city = dest
    while current_city != src:
        path.append(label_vector[current_city])
        current_city = char_to_indx[label_vector[current_city]]
    path.reverse()
    path.append(clone[src][dest])
    return path


def get_all_routes(cost_map, src_city, dest_city):
    clone = []
    for row in cost_map:
        clone.append(row.copy())
    all_routes = []
    start_col = char_to_indx[src_city]
    end_col = char_to_indx[dest_city]
    there_is_more = True
    cell_to_remove = (0, 0)
    while there_is_more:
        curr_col = end_col
        there_is_more = False
        while curr_col != start_col:
            count = 0
            selected = start_col
            j = curr_col
            cost = clone[start_col][j]
            for row in range(start_col, end_col):
                if clone[row][j] == -1 or clone[row][j] == 0: continue
                count += 1
                if count >= 2:
                    there_is_more = True
                    if clone[row][j] < cost:
                        cost = clone[row][j]
                        selected = row
                    cell_to_remove = selected, j
                else:  # always applies but only once per loop
                    selected = row
                    cost = clone[row][j]
            curr_col = selected

        all_routes.append(get_route_3(clone, src_city, dest_city))
        # for row in clone:
        #     print(row)
        clone[cell_to_remove[0]][cell_to_remove[1]] = -1

    return all_routes


def get_all_routes2(cost_map, src_city, dest_city):
    clone = []
    for row in cost_map:
        clone.append(row.copy())

    optimal = get_route_3(cost_map, src_city, dest_city)
    optimals = [optimal]

    for col in optimal[1:-1]:
        j = char_to_indx[col]
        count = 0
        for i1 in range(len(clone)):
            if clone[i1][j] == 0 or clone[i1][j] == -1: continue
            count += 1
            if count >= 2:
                clone[i1][j] = -1
                optimals.append(get_route_3(clone, src_city, dest_city))

    return optimals


def global_find_route(routes, src_city, dest_city):
    global char_to_indx
    char_to_indx = get_dict_of_cities(routes)
    cost_map = map_cities(routes)
    list_of_routes = get_all_routes(cost_map, src_city, dest_city)
    for i in get_routes_2(cost_map, src_city, dest_city):
        cost = i[-1]
        s = slice(0, -1)
        i = i[s]
        i.reverse()
        i.append(cost)
        list_of_routes.append(i)
    unique_data = []
    for item in list_of_routes:
        if item not in unique_data:
            unique_data.append(item)
    unique_data = sorted(unique_data, key=lambda x: x[-1])
    return unique_data


# for item in global_find_route(routes, 'a', 'i'):
#     print(item)

def process_file(file):
    cities = []
    line_no = 0
    cities_num = None
    begin_city = None
    end_city = None
    missing_end_city = None
    city_labels = []
    for line in file:
        line.strip()
        if str.isspace(line):
            continue
        line_no += 1
        if line_no == 1:
            cities_num = int(line)
            continue
        elif line_no == 2:
            line = str.replace(line, ' ', '')
            begin_city = str.split(line, ',')[0]
            end_city = str.split(line, ',')[1].strip()
            continue
        else:
            line = str.replace(line, ' ', '')
            city = str.split(line, ',')[0]
            city_labels.append(city)
            line = line.replace(city + ',', '')
            line = line.replace('],', ':')
            line = line.replace(']', '')
            line = line.replace('[', '')
            adjacents = str.split(line, ':')
            city = [city,]
            for adj in adjacents:
                if str.isspace(adj): continue
                elements = str.split(adj, ',')
                nighbor = [elements[0], int(elements[1]), int(elements[2])]
                if elements[0] not in city_labels:
                    missing_end_city = elements[0]
                city.append(nighbor)
            cities.append(city)
    cities.append([missing_end_city,])
    # for  city in cities: print(city)
    return cities, cities_num, begin_city, end_city



