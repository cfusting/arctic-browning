import re
from pyhdf.SD import SD, SDC
from datetime import datetime


class ModisFile:

    def __init__(self, file_name):
        self.file_name = file_name
        file_time = re.search('\d{7}', file_name).group()
        self.datetime = datetime.strptime(file_time, '%Y%j')

    def __eq__(self, other):
        return self.datetime == other.datetime

    def __ne__(self, other):
        return self.datetime != other.datetime

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime

    def __gt__(self, other):
        return self.datetime > other.datetime

    def __ge__(self, other):
        return self.datetime >= other.datetime

    def get_layer_data(self, layer_name):
        dataset = SD(self.file_name)
        data = dataset.select(layer_name).get()
        dataset.end()
        return data
