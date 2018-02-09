import json
import sys
import re
import time
try:
    import readline
except:
    pass
from building import Building
from model import Model
from visualizer import weight_table, prediction_table
from util import day_to_number, number_to_day


number_pattern = re.compile("^\\d+$")
day_pattern = re.compile(
    "^((tues|wednes|thurs|satur)day)|(sun|mon|fri)(day)?|(tue|wed|thu|sat)$"
)


def sample_to_string(sample):
    return "%dfl -> %dfl on %s at %02d:00" % (
        sample[0] + 1,
        sample[1] + 1,
        number_to_day(sample[2]),
        sample[3]
    )


files = sys.argv[1:]

if len(files) < 1:
    print("Building structure file is requied")
    exit(1)

building = Building(json.loads(open(files[0]).read()))
model = Model(building)

report_timer = time.time()
training_epoch = 0
visualize_training = False
while True:
    if training_epoch > 0 and report_timer < time.time():
        print("%s training left..." % (training_epoch))
        report_timer = time.time() + 1
    if training_epoch > 0:
        
        sample = building.generate_sample()
        if visualize_training:
            print("  %s" % (sample_to_string(sample)))
        model.train(sample)

        training_epoch -= 1
        continue

    parts = input("> ").split(" ")
    command, args = parts[0], parts[1:]

    if command == "q" or command == "quit":
        break
    elif command == "h" or command == "help":
        print("usage: command [arguments]...")
        print()
        print("commands:")
        print("  h, help")
        print("        this help message")
        print("  q, quit")
        print("        exit the program")
        print("  d, describe")
        print("        describe building structure")
        print("  p, pt, predict, predict-transpose [day of week]")
        print(
            "        show a prediction table for the whole week " +
            "or on specified day of week"
        )
        print("  s, sample [repeat]")
        print("        output a newly generated sample")
        print(
            "  s, sample <from floor> <to floor> <day of week> " +
            "<hour of day> [repeat]"
        )
        print(
            "        immediately train the model from a specified sample data"
        )
        print("  t, train [repeat]")
        print("        train the model using newly generated samples")
        print("  vt, vtrain [repeat]")
        print("        same as `t, train` but also output generated samples")
    elif command == "d" or command == "describe":
        building.describe()
    elif (
        command == "p" or
        command == "predict" or
        command == "pt" or
        command == "predict-transpose"
    ):
        day = None

        if len(args) >= 1 and day_pattern.match(args[0]) is not None:
            day = day_to_number(args[0])
            
        prediction_table(model, day, (
            command == "pt" or command == "predict-transpose"
        ))
    elif command == "s" or command == "sample":
        if (
            len(args) == 0 or
            (len(args) == 1 and number_pattern.match(args[0]) is not None)
        ):
            times = 1
            if len(args) >= 1:
                times = max(times, int(args[0]))
            print("Generated sample:")
            while times > 0:
                sample = building.generate_sample()
                print("  %s" % (sample_to_string(sample)))
                times -= 1
        elif (
            len(args) >= 4 and
            number_pattern.match(args[0]) is not None and
            number_pattern.match(args[1]) is not None and
            day_pattern.match(args[2]) is not None and
            number_pattern.match(args[3]) is not None
        ):
            from_floor = int(args[0])
            to_floor = int(args[1])
            day = day_to_number(args[2])
            hour = int(args[3])
            total_floor = building.total_floor()
            if (
                day >= 0 and
                hour < 24 and
                from_floor > 0 and
                to_floor > 0 and
                from_floor <= total_floor and
                to_floor <= total_floor
            ):
                times = 1
                if (
                    len(args) >= 5 and
                    number_pattern.match(args[4]) is not None
                ):
                    times = max(times, int(args[4]))
                
                sample = [from_floor - 1, to_floor - 1, day, hour]
                print("Training with %d samples: %s" % (
                    times, sample_to_string(sample)
                ))
                while times > 0:
                    model.train(sample)
                    times -= 1
            else:
                print("Invalid sample")
    elif (
        command == "t" or
        command == "train" or
        command == "vt" or
        command == "vtrain"
    ):
        training_epoch = 1
        if len(args) >= 1 and number_pattern.match(args[0]) is not None:
            training_epoch = int(args[0])
        report_timer = time.time() + 1
        visualize_training = command[0] == "v"
        if not visualize_training:
            print("%s training left..." % (training_epoch))
        else:
            print("training with samples...")
    elif command == "w" or command == "weight":
        if len(args) < 1:
            for day in range(7):
                if day > 0:
                    print()
                weight_table(
                    model,
                    day,
                    building.total_floor()
                )
        elif day_pattern.match(args[0]) is not None:
            day = day_to_number(args[0])
            weight_table(
                model,
                day,
                building.total_floor()
            )
