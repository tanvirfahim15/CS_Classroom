import abc
import pandas as pd
import numpy as np


class HtmlTarget(metaclass=abc.ABCMeta):

    def __init__(self):
        self._adaptee = CsvAdaptee()

    @abc.abstractmethod
    def get_html(self, filename):
        pass


class CsvToHtmlAdapter(HtmlTarget):

    def get_html(self, filename):
        csv = self._adaptee.get_csv(filename)
        ret = ''
        for row in csv:
            ret += '<tr>'
            for col in row:
                ret += '<td>' + str(col) + '</td>'
            ret += '</tr>'
        return ret


class CsvAdaptee:

    def get_csv(self, filename):
        df = pd.read_csv('classes/CodeGenerator/'+filename, sep=',', header=None)
        arr = np.array(df)
        return arr

