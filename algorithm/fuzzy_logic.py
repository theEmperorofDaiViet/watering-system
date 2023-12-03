import numpy as np

class FuzzyLogic():

    def __init__(self):
        self.membership_values_of_temperature = np.array([0., 0., 0., 0.])
        self.membership_values_of_soil_moisture = np.array([0., 0., 0., 0.])
        self.membership_values_of_light_intensity = np.array([0., 0., 0.])
        self.membership_values_of_watering_speed = np.array([0., 0., 0., 0.])

    RULES_SET = {
        '001': 0,
        '100': 2,
        '101': 2,
        '102': 3,
        '110': 1,
        '111': 1,
        '112': 2,
        '121': 0,
        '122': 1,
        '200': 3,
        '201': 3,
        '202': 3,
        '210': 2,
        '211': 2,
        '212': 3,
        '220': 1,
        '221': 1,
        '222': 2,
        '300': 3,
        '301': 3,
        '302': 3,
        '310': 2,
        '311': 2,
        '312': 3,
        '320': 1,
        '321': 2,
        '322': 2
    }

    def do_fuzzification_of_temperature(self, temperature):
        if temperature < 5:
            self.membership_values_of_temperature[0] = 1
        elif temperature >= 5 and temperature < 10:
            self.membership_values_of_temperature[0] = (-1/5) * temperature + 2
            self.membership_values_of_temperature[1] = (1/5) * temperature - 1
        elif temperature >= 10 and temperature < 15:
            self.membership_values_of_temperature[1] = 1
        elif temperature >= 15 and temperature < 20:
            self.membership_values_of_temperature[1] = (-1/5) * temperature + 4
            self.membership_values_of_temperature[2] = (1/5) * temperature - 3
        elif temperature >= 20 and temperature < 25:
            self.membership_values_of_temperature[2] = 1
        elif temperature >= 25 and temperature < 30:
            self.membership_values_of_temperature[2] = (-1/5) * temperature + 6
            self.membership_values_of_temperature[3] = (1/5) * temperature - 5
        else:
            self.membership_values_of_temperature[3] = 1
        print(self.membership_values_of_temperature)

    def do_fuzzification_of_soil_moisture(self, soil_moisture):
        if soil_moisture < 25:
            self.membership_values_of_soil_moisture[0] = 1
        elif soil_moisture >= 25 and soil_moisture < 35:
            self.membership_values_of_soil_moisture[0] = (-1/10) * soil_moisture + (7/2)
            self.membership_values_of_soil_moisture[1] = (1/10) * soil_moisture - (5/2)
        elif soil_moisture >= 35 and soil_moisture < 45:
            self.membership_values_of_soil_moisture[1] = 1
        elif soil_moisture >= 45 and soil_moisture < 55:
            self.membership_values_of_soil_moisture[1] = (-1/10) * soil_moisture + (11/2)
            self.membership_values_of_soil_moisture[2] = (1/10) * soil_moisture - (9/2)
        elif soil_moisture >= 55 and soil_moisture < 65:
            self.membership_values_of_soil_moisture[2] = 1
        elif soil_moisture >= 65 and soil_moisture < 75:
            self.membership_values_of_soil_moisture[2] = (-1/10) * soil_moisture + (15/2)
            self.membership_values_of_soil_moisture[3] = (1/10) * soil_moisture - (13/2)
        else:
            self.membership_values_of_soil_moisture[3] = 1
        print(self.membership_values_of_soil_moisture)

    def do_fuzzification_of_light_intensity(self, light_intensity):
        if light_intensity < 300:
            self.membership_values_of_light_intensity[0] = 1
        elif light_intensity >= 300 and light_intensity < 400:
            self.membership_values_of_light_intensity[0] = (-1/100) * light_intensity + 4
            self.membership_values_of_light_intensity[1] = (1/100) * light_intensity - 3
        elif light_intensity >= 400 and light_intensity < 700:
            self.membership_values_of_light_intensity[1] = 1
        elif light_intensity >= 700 and light_intensity < 800:
            self.membership_values_of_light_intensity[1] = (-1/100) * light_intensity + 8
            self.membership_values_of_light_intensity[2] = (1/100) * light_intensity - 7
        else:
            self.membership_values_of_light_intensity[2] = 1
        print(self.membership_values_of_light_intensity)

    def do_fuzzy_inference(self):
        for i in range(self.membership_values_of_temperature.shape[0]):
            combination = ''
            if self.membership_values_of_temperature[i] > 0:
                combination += str(i)
                for j in range(self.membership_values_of_soil_moisture.shape[0]):
                    if self.membership_values_of_soil_moisture[j] > 0:
                        combination += str(j)
                        for k in range(self.membership_values_of_light_intensity.shape[0]):
                            if self.membership_values_of_light_intensity[k] > 0:
                                combination += str(k)
                                if combination in self.RULES_SET:
                                    [a, b, c] = [int(i) for i in list(combination)]
                                    temperature = self.membership_values_of_temperature[a]
                                    soil_moisture = self.membership_values_of_soil_moisture[b]
                                    light_intensity = self.membership_values_of_light_intensity[c]
                                    new_value = min(temperature, soil_moisture, light_intensity)
                                    old_value = self.membership_values_of_watering_speed[self.RULES_SET[combination]]
                                    self.membership_values_of_watering_speed[self.RULES_SET[combination]] = new_value if (new_value > old_value) else old_value

                                combination = combination[0:2]
                        combination = combination[0:1]
        print(self.membership_values_of_watering_speed)

    def do_defuzzification_of_watering_speed(self):
        max_y = max(self.membership_values_of_watering_speed)
        max_index = self.membership_values_of_watering_speed.argmax()


        max_x1, max_x2 = 0, 0
        if self.membership_values_of_watering_speed[0] == max_y:
            if max_y == 1:
                max_x2 = 2
            else:
                max_x2 = 3 - max_y
        elif self.membership_values_of_watering_speed[1] == max_y:
            if max_y == 1:
                if max_x1 == 0:
                    max_x1 = 3
                max_x2 = 5
            else:
                if max_x1 == 0:
                    max_x1 = max_y + 2
                max_x2 = 6 - max_y
        elif self.membership_values_of_watering_speed[2] == max_y:
            if max_y == 1:
                max_x1 = 6
                max_x2 = 8
            else:
                max_x1 = max_y + 5
                max_x2 = 9 - max_y
        elif self.membership_values_of_watering_speed[3] == max_y:
            if max_y == 1:
                if max_x1 == 0:
                    max_x1 = 9
                max_x2 = 12
            else:
                if max_x1 == 0:
                    max_x1 = max_y + 8
                max_x2 = 12
        res = (max_x1 + max_x2) / 2
        print(max_x1, max_x2, res)
    