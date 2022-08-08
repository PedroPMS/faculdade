def two_opt_move(tour, distance, travel_time, service_time, ready_time, due_time):
    best_imp = 0
    node1 = -1
    node2 = -1

    if len(tour) >= 5:
        for i in range(len(tour) - 3):
            for j in range(i + 2, len(tour) - 1):
                new_tour = tour[0:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
                if time_checker(new_tour, travel_time, service_time, ready_time, due_time):
                    imp = distance[tour[i]][tour[j]] + distance[tour[i + 1]][tour[j + 1]] - distance[tour[i]][
                        tour[i + 1]] - distance[tour[j]][tour[j + 1]]
                    if imp < best_imp:
                        node1 = i
                        node2 = j
                        best_imp = imp

    return node1, node2, best_imp


def two_opt_search(sub_tour, distance, travel_time, service_time, ready_time, due_time):
    Best_Imp = 0
    Tour = []
    Position1 = []
    Position2 = []

    for i in range(len(sub_tour)):
        [Node1, Node2, Imp] = two_opt_move(sub_tour[i], distance, travel_time, service_time, ready_time, due_time)

        if Node1 != -1:
            Best_Imp += Imp
            Tour.append(i)
            Position1.append(Node1)
            Position2.append(Node2)
    return Tour, Position1, Position2, Best_Imp