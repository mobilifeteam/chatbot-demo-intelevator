import random
from config import learning_rate
from util import uniform_list, normalize_list


class Model:
    def __init__(self, building):
        self.building = building
        self.weight = [
            [
                uniform_list(self.building.total_floor())
            ] * 24
        ] * 7
    
    def train(self, sample):
        [from_floor, to_floor, call_day, call_time] = sample
        self.weight[call_day][call_time][from_floor] += learning_rate

        self.weight[call_day][call_time] = normalize_list(
            self.weight[call_day][call_time]
        )

    def hourly_prediction(self, day, hour):
        max_index = []
        max_prob = 0

        weights = self.weight[day][hour]

        for index, weight in enumerate(weights):
            if weight > max_prob:
                max_prob = weight
                max_index = [index]
            elif weight == max_prob:
                max_index.append(index)

        if len(max_index) > 0:
            return random.choice(max_index)
        else:
            return None
    
    def daily_prediction(self, day):
        return [self.hourly_prediction(day, hour) for hour in range(24)]
    
    def daily_weight(self, day):
        return self.weight[day]
