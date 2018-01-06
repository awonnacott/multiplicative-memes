#!/usr/bin/env python3

from clean_data import clean
from clean_data import get_true_values

experts = ["espn", "nfl", "fftoday"]
positions = ["QB", "RB", "WR", "TE"]
num_weeks = 17
points_weights = [.04, 4, -2, .1, 6, .1, 6]
cost_scalars = {
    "QB": [0.007, 0.009, 0.020, 0.050, 0.050, 1.000, 1.000],
    "RB": [1.000, 1.000, 1.000, 0.005, 0.008, 0.010, 0.020],
    "WR": [1.000, 1.000, 1.000, 0.250, 0.750, 0.002, 0.004],
    "TE": [1.000, 1.000, 1.000, 2.500, 6.000, 0.010, 0.010],
}
eta = .25

for pos in positions:
    print("Position:", pos)
    for stat in range(len(points_weights)):
        # max_cost = 0
        print("Stat:", stat)
        weights = {}
        cost = 0
        for expert in experts:
            weights[expert] = float(1) / len(experts)
        for week in range(1, num_weeks + 1):
            print("Week:", week)
            print("Weights:", weights)
            weight_sum = 0
            for expert in experts:
                weight_sum += weights[expert]
            weekly_cost = 0
            costs = {}
            for expert in experts:
                costs[expert] = 0
            # true_values = clean(pos, str(week), "true")
            true_values = get_true_values(pos, str(week))
            predictions = {}
            for expert in experts:
                predictions[expert] = clean(pos, str(week), expert)
            for player in list(true_values.keys()):
                guess = 0
                true_score = true_values[player][stat] * points_weights[stat]
                for expert in experts:
                    if player in predictions[expert]:
                        expert_score = predictions[expert][player][stat] * points_weights[stat]
                    else:
                        expert_score = 0
                    guess += expert_score * weights[expert]
                    costs[expert] += abs(expert_score - true_score)
                guess /= weight_sum
                weekly_cost += abs(guess - true_score) * cost_scalars[pos][stat]
            for expert in experts:
                costs[expert] *= cost_scalars[pos][stat]
                # if costs[expert] > max_cost:
                #     max_cost = costs[expert]
                weights[expert] *= 1 - eta * costs[expert]
            print("Costs:", costs, weekly_cost)
            cost += weekly_cost
        # print(max_cost)
