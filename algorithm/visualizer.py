import numpy as np
import matplotlib.pyplot as plt

class TemperatureVisualizer(object):

    def __init__(self, membership_values, crisp_value):
        self.membership_values = membership_values
        self.crisp_value = crisp_value
        self.universe = np.arange(-20, 50.01, 0.01)
        self.terms = {
            'Rất lạnh': {
                'mf': self.trapmf(self.universe, [-20, -20, 5, 10]),
                'color': 'blue'
            },
            'Lạnh': {
                'mf': self.trapmf(self.universe, [5, 10, 15, 20]),
                'color': 'green'
            },
            'Ấm': {
                'mf': self.trapmf(self.universe, [15, 20, 25, 30]),
                'color': 'orange'
            },
            'Nóng': {
                'mf': self.trapmf(self.universe, [25, 30, 51, 51]),
                'color': 'red'
            }
        }
        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1.1])
        self.ax.set_xlim([self.universe.min(),
                          self.universe.max() + 4])

        # Make the plots
        for key, term in self.terms.items():

            self.plots[key] = self.ax.plot(self.universe,
                                           term['mf'],
                                           label=key,
                                           linewidth=1.5,
                                           color=term['color'])

        crisp_value_line = np.arange(0, self.membership_values.max(), 0.01)
        membership_value_line = np.arange(self.universe.min(), self.crisp_value, 0.01)

        self.plots['res'] = self.ax.plot(np.full(crisp_value_line.shape[0], self.crisp_value),
                                        crisp_value_line,
                                        ':',
                                        color='black')
        
        for i in range(self.membership_values.shape[0]):
            if self.membership_values[i] > 0:
                self.plots[i] = self.ax.plot(membership_value_line,
                                                 np.full(membership_value_line.shape[0], self.membership_values[i]),
                                                 ':',
                                                 color=list(self.terms.items())[i][1]['color'])

        plt.yticks([round(j, 2) for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()], [str(round(j, 2)) + "     " for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()])

        # Place legend in upper left
        self.ax.legend(framealpha=0.5, loc='right')

        # Turn off top/right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        # Ticks outside the axes
        self.ax.tick_params(direction='out')

        # Label the axes
        self.ax.set_ylabel('Giá trị thành viên')
        self.ax.set_xlabel('Nhiệt độ (°C)')

        xtick = "\n" + str(round(self.crisp_value, 2))
        plt.xticks([round(self.crisp_value, 2)] + [i for i in range(-20, 51, 10)], [xtick] + [i for i in range(-20, 51, 10)])

        return self.fig, self.ax

    def trimf(self, x, abc):
        a, b, c = np.r_[abc]     # Zero-indexing in Python

        y = np.zeros(len(x))

        # Left side
        if a != b:
            idx = np.nonzero(np.logical_and(a < x, x < b))[0]
            y[idx] = (x[idx] - a) / float(b - a)

        # Right side
        if b != c:
            idx = np.nonzero(np.logical_and(b < x, x < c))[0]
            y[idx] = (c - x[idx]) / float(c - b)

        idx = np.nonzero(x == b)
        y[idx] = 1
        return y

    def trapmf(self, x, abcd):
        a, b, c, d = np.r_[abcd]
        y = np.ones(len(x))

        idx = np.nonzero(x <= b)[0]
        y[idx] = self.trimf(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x >= c)[0]
        y[idx] = self.trimf(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))

        return y
    
class SoilMoistureVisualizer(object):

    def __init__(self, membership_values, crisp_value):
        self.membership_values = membership_values
        self.crisp_value = crisp_value
        self.universe = np.arange(0, 100.01, 0.01)
        self.terms = {
            'Rất khô': {
                'mf': self.trapmf(self.universe, [0, 0, 25, 35]),
                'color': 'red'
            },
            'Khô': {
                'mf': self.trapmf(self.universe, [25, 35, 45, 55]),
                'color': 'orange'
            },
            'Ẩm': {
                'mf': self.trapmf(self.universe, [45, 55, 65, 75]),
                'color': 'green'
            },
            'Rất ẩm': {
                'mf': self.trapmf(self.universe, [65, 75, 101, 101]),
                'color': 'blue'
            }
        }
        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1.1])
        self.ax.set_xlim([self.universe.min(),
                          self.universe.max() + 4])

        # Make the plots
        for key, term in self.terms.items():

            self.plots[key] = self.ax.plot(self.universe,
                                           term['mf'],
                                           label=key,
                                           linewidth=1.5,
                                           color=term['color'])

        crisp_value_line = np.arange(0, self.membership_values.max(), 0.01)
        membership_value_line = np.arange(self.universe.min(), self.crisp_value, 0.01)

        self.plots['res'] = self.ax.plot(np.full(crisp_value_line.shape[0], self.crisp_value),
                                        crisp_value_line,
                                        ':',
                                        color='black')
        
        for i in range(self.membership_values.shape[0]):
            if self.membership_values[i] > 0:
                self.plots[i] = self.ax.plot(membership_value_line,
                                                 np.full(membership_value_line.shape[0], self.membership_values[i]),
                                                 ':',
                                                 color=list(self.terms.items())[i][1]['color'])

        plt.yticks([round(j, 2) for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()], [str(round(j, 2)) + "     " for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()])

        # Place legend in upper left
        self.ax.legend(framealpha=0.5, loc='right')

        # Turn off top/right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        # Ticks outside the axes
        self.ax.tick_params(direction='out')

        # Label the axes
        self.ax.set_ylabel('Giá trị thành viên')
        self.ax.set_xlabel('Độ ẩm (%)')

        xtick = "\n" + str(round(self.crisp_value, 2))
        plt.xticks([round(self.crisp_value, 2)] + [i for i in range(0, 101, 10)], [xtick] + [i for i in range(0, 101, 10)])

        return self.fig, self.ax

    def trimf(self, x, abc):
        a, b, c = np.r_[abc]     # Zero-indexing in Python

        y = np.zeros(len(x))

        # Left side
        if a != b:
            idx = np.nonzero(np.logical_and(a < x, x < b))[0]
            y[idx] = (x[idx] - a) / float(b - a)

        # Right side
        if b != c:
            idx = np.nonzero(np.logical_and(b < x, x < c))[0]
            y[idx] = (c - x[idx]) / float(c - b)

        idx = np.nonzero(x == b)
        y[idx] = 1
        return y

    def trapmf(self, x, abcd):
        a, b, c, d = np.r_[abcd]
        y = np.ones(len(x))

        idx = np.nonzero(x <= b)[0]
        y[idx] = self.trimf(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x >= c)[0]
        y[idx] = self.trimf(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))

        return y
    
class LightIntensityVisualizer(object):

    def __init__(self, membership_values, crisp_value):
        self.membership_values = membership_values
        self.crisp_value = crisp_value
        self.universe = np.arange(0, 1000.01, 0.01)
        self.terms = {
            'Yếu': {
                'mf': self.trapmf(self.universe, [0, 0, 300, 400]),
                'color': 'blue'
            },
            'Trung bình': {
                'mf': self.trapmf(self.universe, [300, 400, 700, 800]),
                'color': 'orange'
            },
            'Mạnh': {
                'mf': self.trapmf(self.universe, [700, 800, 1001, 1001]),
                'color': 'red'
            }
        }
        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1.1])
        self.ax.set_xlim([self.universe.min(),
                          self.universe.max() + 40])

        # Make the plots
        for key, term in self.terms.items():

            self.plots[key] = self.ax.plot(self.universe,
                                           term['mf'],
                                           label=key,
                                           linewidth=1.5,
                                           color=term['color'])

        crisp_value_line = np.arange(0, self.membership_values.max(), 0.01)
        membership_value_line = np.arange(self.universe.min(), self.crisp_value, 0.01)

        self.plots['res'] = self.ax.plot(np.full(crisp_value_line.shape[0], self.crisp_value),
                                        crisp_value_line,
                                        ':',
                                        color='black')
        
        for i in range(self.membership_values.shape[0]):
            if self.membership_values[i] > 0:
                self.plots[i] = self.ax.plot(membership_value_line,
                                                 np.full(membership_value_line.shape[0], self.membership_values[i]),
                                                 ':',
                                                 color=list(self.terms.items())[i][1]['color'])

        plt.yticks([round(j, 2) for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()], [str(round(j, 2)) + "     " for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()])

        # Place legend in upper left
        self.ax.legend(framealpha=0.5, loc='right')

        # Turn off top/right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        # Ticks outside the axes
        self.ax.tick_params(direction='out')

        # Label the axes
        self.ax.set_ylabel('Giá trị thành viên')
        self.ax.set_xlabel('Cường độ ánh sáng PAR (µmol/m²/s)')

        xtick = "\n" + str(round(self.crisp_value, 2))
        plt.xticks([round(self.crisp_value, 2)] + [i for i in range(0, 1100, 100)], [xtick] + [i for i in range(0, 1100, 100)])

        return self.fig, self.ax

    def trimf(self, x, abc):
        a, b, c = np.r_[abc]     # Zero-indexing in Python

        y = np.zeros(len(x))

        # Left side
        if a != b:
            idx = np.nonzero(np.logical_and(a < x, x < b))[0]
            y[idx] = (x[idx] - a) / float(b - a)

        # Right side
        if b != c:
            idx = np.nonzero(np.logical_and(b < x, x < c))[0]
            y[idx] = (c - x[idx]) / float(c - b)

        idx = np.nonzero(x == b)
        y[idx] = 1
        return y

    def trapmf(self, x, abcd):
        a, b, c, d = np.r_[abcd]
        y = np.ones(len(x))

        idx = np.nonzero(x <= b)[0]
        y[idx] = self.trimf(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x >= c)[0]
        y[idx] = self.trimf(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))

        return y
    
class WateringSpeedVisualizer(object):

    def __init__(self, membership_values, crisp_value):
        self.membership_values = membership_values
        self.crisp_value = crisp_value
        self.universe = np.arange(0, 12.01, 0.01)
        self.terms = {
            'Rất chậm': {
                'mf': self.trapmf(self.universe, [0, 0, 2, 3]),
                'color': 'red'
            },
            'Chậm': {
                'mf': self.trapmf(self.universe, [2, 3, 5, 6]),
                'color': 'orange'
            },
            'Nhanh': {
                'mf': self.trapmf(self.universe, [5, 6, 8, 9]),
                'color': 'green'
            },
            'Rất nhanh': {
                'mf': self.trapmf(self.universe, [8, 9, 12, 12]),
                'color': 'blue'
            }
        }
        self.fig, self.ax = plt.subplots()
        self.plots = {}

    def plot(self):
        # Formatting: limits
        self.ax.set_ylim([0, 1.1])
        self.ax.set_xlim([self.universe.min(),
                          self.universe.max() + 1])

        # Make the plots
        for key, term in self.terms.items():
            self.plots[key] = self.ax.plot(self.universe,
                                           term['mf'],
                                           label=key,
                                           linewidth=1.5,
                                           color=term['color'])

        crisp_value_line = np.arange(0, self.membership_values.max(), 0.01)
        membership_value_line = np.arange(self.universe.min(), self.universe.max(), 0.01)

        self.plots['res'] = self.ax.plot(np.full(crisp_value_line.shape[0], self.crisp_value),
                                        crisp_value_line,
                                        ':',
                                        color='black')
        
        for i in range(self.membership_values.shape[0]):
            if self.membership_values[i] > 0:
                self.plots[i] = self.ax.plot(membership_value_line,
                                             np.full(membership_value_line.shape[0], self.membership_values[i]),
                                             ':',
                                             color=list(self.terms.items())[i][1]['color'])

        plt.yticks([round(j, 2) for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()], [str(round(j, 2)) + "     " for j in self.membership_values if j > 0] + [round(j, 2) for j in np.arange(0, 1.2, 0.2).tolist()])

        # Place legend in upper left
        self.ax.legend(framealpha=0.5, loc='right')

        # Turn off top/right axes
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.get_xaxis().tick_bottom()
        self.ax.get_yaxis().tick_left()

        # Ticks outside the axes
        self.ax.tick_params(direction='out')

        # Label the axes
        self.ax.set_ylabel('Giá trị thành viên')
        self.ax.set_xlabel('Tốc độ tưới nước (lít/phút)')

        xtick = "\n" + str(round(self.crisp_value, 2))
        plt.xticks([round(self.crisp_value, 2)] + [i for i in range(0, 14, 2)], [xtick] + [i for i in range(0, 14, 2)])

        return self.fig, self.ax
    
    def trimf(self, x, abc):
        a, b, c = np.r_[abc]     # Zero-indexing in Python

        y = np.zeros(len(x))

        # Left side
        if a != b:
            idx = np.nonzero(np.logical_and(a < x, x < b))[0]
            y[idx] = (x[idx] - a) / float(b - a)

        # Right side
        if b != c:
            idx = np.nonzero(np.logical_and(b < x, x < c))[0]
            y[idx] = (c - x[idx]) / float(c - b)

        idx = np.nonzero(x == b)
        y[idx] = 1
        return y

    def trapmf(self, x, abcd):
        a, b, c, d = np.r_[abcd]
        y = np.ones(len(x))

        idx = np.nonzero(x <= b)[0]
        y[idx] = self.trimf(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x >= c)[0]
        y[idx] = self.trimf(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))

        return y
    
