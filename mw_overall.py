#!/usr/bin/env python3

from clean_data import clean, experts, positions, num_weeks, points_weights

cost_scalar = 0.0007
eta = 0.8

players = set()

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

        players |= set(true_values)
        for expert in predictions:
            players |= set(predictions[expert])

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
    for expert in experts:
        costs[expert] *= cost_scalar
        weights[expert] *= 1 - eta * costs[expert]
    print("Costs:", costs, weekly_cost)
    cost += weekly_cost

if __name__ == '__main__':
    print("Total cost:", cost)
    #for player in sorted(players):
        #print(player)
