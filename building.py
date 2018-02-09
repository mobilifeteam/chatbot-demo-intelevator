import random


class Building:
    def __init__(self, building_structure):
        self.floors = building_structure["floors"]

        self.ground_level = None
        for index, floor in enumerate(self.floors):
            if floor["type"] == "ground":
                self.ground_level = index
                break

        if self.ground_level is None:
            self.floors = [{
                "type": "ground"
            }] + self.floors
            self.ground_level = 0
    
    def generate_passenger(self, floor):
        org = self.floors[floor]
        from_floor = None
        to_floor = None
        call_time = None

        travel_in = random.choice([True, False])
        on_lunch = random.choice(["lunch-break" in org, False, False, False])

        if travel_in:
            # In
            from_floor = self.ground_level
            to_floor = floor

            if on_lunch:
                # Lunch
                call_times = {
                    str(org["lunch-break"]["to"]): 1
                }
            else:
                # Working
                call_times = org["working-time"]["in"]
        else:
            # Out
            from_floor = floor
            to_floor = self.ground_level

            if on_lunch:
                # Lunch
                call_times = {
                    str(org["lunch-break"]["from"]): 1
                }
            else:
                # Working
                call_times = org["working-time"]["out"]
        
        for hour in call_times:
            probability = call_times[hour]
            if random.randint(1, 100) <= probability * 100:
                call_time = int(hour)
                break

        if org["type"] == "company":
            call_day = random.randint(1, 5)
        elif org["type"] == "offday-company":
            call_day = random.choice([0, 6])
        elif org["type"] == "mall":
            call_day = random.randint(1, 6)
        else:
            call_day = random.randint(0, 6)
        
        return [
            from_floor,
            to_floor,
            call_day,
            call_time
        ]

    def generate_sample(self):
        floor_level = self.ground_level
        while floor_level == self.ground_level:
            floor_level = random.randint(0, len(self.floors) - 1)
        return self.generate_passenger(floor_level)
    
    def total_floor(self):
        return len(self.floors)
    
    def describe_floor(self, floor, indent=0):
        org = self.floors[floor]
        indentation = "  " * (indent + 1)

        output = ""

        org_type = ""
        working_day = "Everyday"
        if org["type"] == "company" or org["type"] == "offday-company":
            org_type = "Company"
            working_day = "Weekdays"
            if org["type"] == "offday-company":
                working_day = "Weekends"
        elif org["type"] == "mall":
            org_type = "Mall"
            working_day = "Everyday except Sunday"
        elif org["type"] == "theatre":
            org_type = "Theatre"
        elif org["type"] == "ground":
            return "Ground"
        else:
            org_type = "Factory"
        output += "%s\n%s%s" % (org_type, indentation, working_day)
        output += "\n%sIn    : %s" % (indentation, ", ".join([
            "%02d:00" % (int(hour))
            for hour in org["working-time"]["in"].keys()
        ]))
        if "lunch-break" in org:
            output += "\n%sLunch : %02d:00 - %02d:00" % (
                indentation,
                org["lunch-break"]["from"],
                org["lunch-break"]["to"]
            )
        output += "\n%sOut   : %s" % (indentation, ", ".join([
            "%02d:00" % (int(hour))
            for hour in org["working-time"]["out"].keys()
        ]))
        return output

    def describe(self):
        for index, floor in enumerate(self.floors):
            print("%sfl. : %s" % (index + 1, self.describe_floor(index)))
