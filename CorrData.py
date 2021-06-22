import csv

class CorrData:
    def __init__(self, path):
        self.__data_dict = dict()
        self.__result_dict = dict()

        self.__data_dict['layers'] = []
        self.__data_dict['ch1'] = []
        self.__data_dict['ch2'] = []
        self.__data_dict['correlation'] = []

        self.__result_dict['same'] = dict()
        self.__result_dict['others'] = dict()
        self.__result_dict['same']['l1_dist'] = []
        self.__result_dict['same']['l1_dist_1'] = []
        self.__result_dict['same']['l1_dist_2'] = []
        self.__result_dict['same']['l1_dist_5'] = []
        self.__result_dict['others']['l1_dist'] = []
        self.__result_dict['others']['l1_dist_1'] = []
        self.__result_dict['others']['l1_dist_2'] = []
        self.__result_dict['others']['l1_dist_5'] = []

        self.__extract_correlation(path)

    def __extract_correlation(self, path):
        # print(path)
        f = open(path, 'r')
        csv_reader = csv.reader(f)
        for idx, line in enumerate(csv_reader):
            if not idx == 0:
                self.__data_dict['layers'].append(line[0])
                self.__data_dict['ch1'].append(int(line[1]))
                self.__data_dict['ch2'].append(int(line[2]))
                self.__data_dict['correlation'].append(float(line[3]))

    @property
    def correlation(self):
        return self.__data_dict['correlation']

    def get_result_diff(self, task, type):
        return self.__result_dict[task][type]

    def set_result_diff(self, task, type, data):
        self.__result_dict[task][type].append(data)