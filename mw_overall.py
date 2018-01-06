#!/usr/bin/env python3

from clean_data import clean

experts = ["espn", "nfl", "fftoday"]
positions = ["QB", "RB", "WR", "TE"]
num_weeks = 17
points_weights = [.04, 4, -2, .1, 6, .1, 6]
cost_scalar = .001
eta = .25

weights = {expert: 1.0 / len(experts) for expert in experts}
cost = 0
for week in range(1, num_weeks + 1):
    print("Week:", week)
    print("Weights:", weights)
    weight_sum = sum(weights[expert] for expert in experts)
    weekly_cost = 0
    costs = {expert: 0 for expert in experts}
    for pos in positions:
        true_values = clean(pos, str(week), "truevalues")
        predictions = {expert: clean(pos, str(week), expert) for expert in experts}
        for player in true_values:
            guess = 0
            true_score = sum(value * weight for value, weight in zip(true_values[player], points_weights))
            for expert in experts:
                expert_score = 0
                if player in predictions[expert]:
                    expert_score += sum(value * weight for value, weight in zip(predictions[expert][player], points_weights))
                guess += expert_score * weights[expert]
                costs[expert] += abs(expert_score - true_score)
            guess /= weight_sum
            weekly_cost += abs(guess - true_score) * cost_scalar
    for expert in experts:
        costs[expert] *= cost_scalar
        weights[expert] *= 1 - eta * costs[expert]
    print("Costs:", costs, weekly_cost)
    cost += weekly_cost
