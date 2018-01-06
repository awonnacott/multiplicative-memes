#!/usr/bin/env python3

from clean_data import clean
from clean_data import get_true_values

experts = ["espn", "nfl", "fftoday"]
positions = ["QB", "RB", "WR", "TE"]
num_weeks = 17
points_weights = [.04, 4, -2, .1, 6, .1, 6]
cost_scalar = .001
eta = .25

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
    for pos in positions:
        # true_values = clean(pos, str(week), "true")
        true_values = get_true_values(pos, str(week))
        predictions = {}
        for expert in experts:
            predictions[expert] = clean(pos, str(week), expert)
        for player in list(true_values.keys()):
            guess = 0
            true_score = 0
            for i in range(len(points_weights)):
                true_score += true_values[player][i] * points_weights[i]
            for expert in experts:
                expert_score = 0
                if player in predictions[expert]:
                    for i in range(len(points_weights)):
                        expert_score += predictions[expert][player][i] * points_weights[i]
                guess += expert_score * weights[expert]
                costs[expert] += abs(expert_score - true_score)
            guess /= weight_sum
            weekly_cost += abs(guess - true_score) * cost_scalar
    for expert in experts:
        costs[expert] *= cost_scalar
        weights[expert] *= 1 - eta * costs[expert]
    print("Costs:", costs, weekly_cost)
    cost += weekly_cost
