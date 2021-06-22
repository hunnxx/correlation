import os
import csv
import re
import numpy as np
import tqdm
import time

from CorrData import CorrData

class Data:
    def __init__(self, DATA_PATH='.', DATA_NAME='cifar100'):
        self.DATA_PATH = DATA_PATH
        self.DATA_NAME = DATA_NAME
        self.__data_dict = dict()
        self.__pre_processing(DATA_PATH, DATA_NAME)

    def __pre_processing(self, DATA_PATH, DATA_NAME):
        dir_name_list = [d_name for d_name in os.listdir(DATA_PATH) if DATA_NAME in d_name]
        bar = tqdm.tqdm(total=len(dir_name_list), desc='Load Data')
        for dir_name in dir_name_list:
            self.__data_dict[dir_name] = dict()
            file_name_list = [f_name for f_name in os.listdir(os.path.join(DATA_PATH, dir_name)) if 'csv' in f_name]
            for file_name in file_name_list:
                self.__data_dict[dir_name][file_name] = CorrData(os.path.join(DATA_PATH, dir_name, file_name))
            time.sleep(0.01)
            bar.update(1)
        bar.close()

    def same_processing(self):
        bar = tqdm.tqdm(total=len(self.__data_dict), desc='Same')
        for dir_name, files_name in self.__data_dict.items():
            for crit_file_name, crit in files_name.items():
                for comp_file_name, comp in files_name.items():
                    if not crit_file_name == comp_file_name:
                        l1_dist, l1_dist_1, l1_dist_2, l1_dist_5 = self.__calc(crit, comp)
                        self.__set_results(crit, 'same', [l1_dist, l1_dist_1, l1_dist_2, l1_dist_5])
            time.sleep(0.01)
            bar.update(1)
        bar.close()

    def others_processing(self):
        bar = tqdm.tqdm(total=len(self.__data_dict), desc='Others')
        for crit_dir_name, crit_files_name in self.__data_dict.items():
            for crit_file_name, crit in crit_files_name.items():
                for comp_dir_name, comp_files_name in self.__data_dict.items():
                    if not crit_dir_name == comp_dir_name:
                        for comp_file_name, comp in comp_files_name.items():
                            l1_dist, l1_dist_1, l1_dist_2, l1_dist_5 = self.__calc(crit, comp)
                            self.__set_results(crit, 'others', [l1_dist, l1_dist_1, l1_dist_2, l1_dist_5])
            time.sleep(0.01)
            bar.update(1)
        bar.close()
                
    def __calc(self, crit, comp):
        crit_corr = np.array(crit.correlation)
        comp_corr = np.array(comp.correlation)
        crit_corr_abs = np.abs(crit_corr)

        diff = np.abs(crit_corr - comp_corr)
        diff = diff[np.argsort(crit_corr_abs)[::-1]]

        percentage_1 = int(len(diff) * 0.01)
        percentage_2 = int(len(diff) * 0.02)
        percentage_5 = int(len(diff) * 0.05)

        l1_dist = np.sum(diff)
        l1_dist_1 = np.sum(diff[:percentage_1])
        l1_dist_2 = np.sum(diff[:percentage_2])
        l1_dist_5 = np.sum(diff[:percentage_5])

        return l1_dist, l1_dist_1, l1_dist_2, l1_dist_5

    def __set_results(self, data, task, results):
        data.set_result_diff(task, 'l1_dist', results[0])
        data.set_result_diff(task, 'l1_dist_1', results[1])
        data.set_result_diff(task, 'l1_dist_2', results[2])
        data.set_result_diff(task, 'l1_dist_5', results[3])

    def write_csv(self, task):
        if task == 'same':
            CSV_PATH = os.path.join(self.DATA_PATH, 'summary_same_all.csv')
        else:
            CSV_PATH = os.path.join(self.DATA_PATH, 'summary_others_all.csv')

        field_name = ['criteria_folder', 'Mean', 'Mean_1', 'Mean_2', 'Mean_5', 
                      'Var', 'Var_1', 'Var_2', 'Var_5', 
                      'Stddev', 'Stddev_1', 'Stddev_2', 'Stddev_5']

        with open(CSV_PATH, 'w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=field_name)
            csv_writer.writeheader()

            for dir_name, files_name in self.__data_dict.items():
                l1_dist_result = []
                l1_dist_1_result = []
                l1_dist_2_result = []
                l1_dist_5_result = []
                dir_num = re.findall("\d+", dir_name.split('_')[-1])[-1]

                for file_name, data in files_name.items():
                    l1_dist_result.extend(data.get_result_diff(task, 'l1_dist'))
                    l1_dist_1_result.extend(data.get_result_diff(task, 'l1_dist_1'))
                    l1_dist_2_result.extend(data.get_result_diff(task, 'l1_dist_2'))
                    l1_dist_5_result.extend(data.get_result_diff(task, 'l1_dist_5'))

                mean = np.mean(l1_dist_result)
                mean_1 = np.mean(l1_dist_1_result)
                mean_2 = np.mean(l1_dist_2_result)
                mean_5 = np.mean(l1_dist_5_result)

                var = np.var(l1_dist_result)
                var_1 = np.var(l1_dist_1_result)
                var_2 = np.var(l1_dist_2_result)
                var_5 = np.var(l1_dist_5_result)

                std = np.std(l1_dist_result)
                std_1 = np.std(l1_dist_1_result)
                std_2 = np.std(l1_dist_2_result)
                std_5 = np.std(l1_dist_5_result)
 
                write_dict = {'criteria_folder' : dir_num, 'Mean' : mean, 'Mean_1' : mean_1, 'Mean_2' : mean_2, 'Mean_5' : mean_5, 
                                'Var' : var, 'Var_1' : var_1, 'Var_2' : var_2, 'Var_5' : var_5,
                                'Stddev' : std, 'Stddev_1' : std_1, 'Stddev_2' : std_2, 'Stddev_5' : std_5}
                csv_writer.writerow(write_dict)