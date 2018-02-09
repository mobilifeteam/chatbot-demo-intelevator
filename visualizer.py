from util import number_to_day


def weight_table(model, day, total_floor):
    print("%s's weight" % (number_to_day(day)))
    print("        | %s |" % (" | ".join([
        " %02d " % (floor + 1)
        for floor in range(total_floor)
    ])))
    weight = model.daily_weight(day)
    for hour in range(23):
        print("| %02d:00 | %s |" % (hour, " | ".join([
            "%.2f" % (floor)
            for floor in weight[hour]
        ])))


def prediction_table(model, day=None, transpose=False):
    print("Prediction table:")
    if transpose:
        print("      | %s |" % (" | ".join([
            number_to_day(day)[:3] for day in range(7)
        ]) if day is None else number_to_day(day)[:3]))

        for hour in range(24):
            print("%02d:00 | %s |" % (
                hour,
                " | ".join([
                    "%3d" % (model.hourly_prediction(day_number, hour) + 1)
                    for day_number in range(7)
                ])
                if day is None
                else "%3d" % (model.hourly_prediction(day, hour) + 1)
            ))
    else:
        print("          | %s |" % (" | ".join([
            "%02d:00" % (hour) for hour in range(24)
        ])))
    
        def daily_prediction_table(model, day):
            day_text = number_to_day(day)
            print("%9s | %s |" % (day_text, " | ".join([
                " %2d  " % (floor + 1)
                for floor in model.daily_prediction(day)
            ])))
        
        if day is None:
            for day_number in range(7):
                daily_prediction_table(model, day_number)
        else:
            daily_prediction_table(model, day)
