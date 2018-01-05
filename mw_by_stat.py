from clean_data import clean
from clean_data import get_true_values

experts = ["espn", "nfl", "fftoday"]
positions = ["QB", "RB", "WR", "TE"]
num_weeks = 17
points_weights = [.04, 4, -2, .1, 6, .1, 6]
cost_scalars = {("QB", 0):.007, ("QB", 1):.009, ("QB", 2):.02, ("QB", 3):.05, ("QB", 4):.05, ("QB", 5):1,("QB", 6):1,
                ("RB", 0):1, ("RB", 1):1, ("RB", 2):1, ("RB", 3):.005, ("RB", 4):.008, ("RB", 5):.01,("RB", 6):.02,
                ("WR", 0):1, ("WR", 1):1, ("WR", 2):1, ("WR", 3):.25, ("WR", 4):.75, ("WR", 5):.002,("WR", 6):.004,
                ("TE", 0):1, ("TE", 1):1, ("TE", 2):1, ("TE", 3):2.5, ("TE", 4):6, ("TE", 5):.01,("TE", 6):.01}
eta = .25

for pos in positions:
    print "Position:", pos
    for stat in range(len(points_weights)):
        #max_cost = 0
        print "Stat:", stat
        weights = {}
        cost = 0
        for expert in experts:
            weights[expert] = float(1)/len(experts)
        for week in range(1, num_weeks + 1):
            print "Week:", week
            print "Weights:", weights
            weight_sum = 0
            for expert in experts:
                weight_sum += weights[expert]
            weekly_cost = 0
            costs = {}
            for expert in experts:
                costs[expert] = 0
            #true_values = clean(pos, str(week), "true")
            true_values = get_true_values(pos, str(week))
            predictions = {}
            for expert in experts:
                predictions[expert] = clean(pos, str(week), expert)
            for player in list(true_values.keys()):
                guess = 0
                true_score = true_values[player][stat] * points_weights[stat]
                for expert in experts:
                    if predictions[expert].has_key(player):
                        expert_score = predictions[expert][player][stat] * points_weights[stat]
                    else:
                        expert_score = 0
                    guess += (expert_score * weights[expert])
                    costs[expert] += abs(expert_score - true_score)
                guess /= weight_sum
                weekly_cost += (abs(guess - true_score) * cost_scalars[(pos, stat)])
            for expert in experts:
                costs[expert] *= cost_scalars[(pos, stat)]
                #if costs[expert] > max_cost:
                    #max_cost = costs[expert]
                weights[expert] *= (1 - eta*costs[expert])
            print "Costs:", costs, weekly_cost
            cost += weekly_cost
        #print max_cost