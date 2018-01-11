#!/usr/bin/env python3

from clean_data import clean, experts, positions, num_weeks, points_weights
import math

eta = (math.log(len(experts)) / num_weeks) ** 0.5
margin = 1.3

players = set()

weights = {expert: 1.0 / len(experts) for expert in experts}
cost = 0
cost_scalar = 0
cost_constant = 0
print("eta: ", eta)
for week in range(1, num_weeks + 1):
    print("Week:", week)
    print("Weights:", weights)
    weight_sum = sum(weights[expert] for expert in experts)
    if week == 17 and "nfl" in weights:
        weight_sum -= weights["nfl"]
    weekly_cost = 0
    costs = {expert: 0 for expert in experts}
    for pos in positions:
        true_values = clean(pos, str(week), "truevalues")
        predictions = {expert: clean(pos, str(week), expert) for expert in experts}

        players |= set(true_values)
        for expert in predictions:
            players |= set(predictions[expert])

        for player in true_values:
            guess = 0
            true_score = sum(value * weight for value, weight in zip(true_values[player], points_weights))
            for expert in experts:
                if not(week == 17 and expert == "nfl"):
                    expert_score = 0
                    if player in predictions[expert]:
                        expert_score += sum(value * weight for value, weight in zip(predictions[expert][player], points_weights))
                    guess += expert_score * weights[expert]
                    costs[expert] += abs(expert_score - true_score)
            guess /= weight_sum
            weekly_cost += abs(guess - true_score)
    if week == 1:
        min_cost = min(costs[expert] for expert in experts)
        max_cost = max(costs[expert] for expert in experts)
        cost_scalar = 2 / (max_cost * margin - min_cost / margin)
        cost_constant = 1 - cost_scalar * max_cost * margin
    for expert in experts:
        costs[expert] = cost_scalar * costs[expert] + cost_constant
        weights[expert] *= 1 - eta * costs[expert]
        if weights[expert] <= 0:
            print("Error: weight not positive.")
            exit(1)
    print("Costs:", costs, weekly_cost)
    cost += weekly_cost

if __name__ == '__main__':
    print("Total cost:", cost)
