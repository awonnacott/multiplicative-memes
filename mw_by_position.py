#!/usr/bin/env python3

from clean_data import clean, experts, positions, num_weeks, points_weights

eta = 0.5
max_week_1_cost = 0.8

total_cost = 0
cost_scalars = {"QB": 0, "RB": 0, "WR": 0, "TE": 0}
for pos in positions:
    print("Position:", pos)
    weights = {expert: 1.0 / len(experts) for expert in experts}
    position_cost = 0
    for week in range(1, num_weeks + 1):
        print("Week:", week)
        print("Weights:", weights)
        weight_sum = sum(weights[expert] for expert in experts)
        weekly_cost = 0
        costs = {expert: 0 for expert in experts}
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
            weekly_cost += abs(guess - true_score)
        if week == 1:
            cost_scalars[pos] = max_week_1_cost/max(costs[expert] for expert in experts)
        for expert in experts:
            costs[expert] *= cost_scalars[pos]
            weights[expert] *= 1 - eta * costs[expert]
            if weights[expert] <= 0:
                print("Error: weight not positive.")
                exit(1)
        print("Costs:", costs, weekly_cost)
        position_cost += weekly_cost
    print "Total position cost:", position_cost
    total_cost += position_cost
print "Total cost: ", total_cost
