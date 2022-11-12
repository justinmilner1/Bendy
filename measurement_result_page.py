import time
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import shutil
from datetime import datetime
import os
import matplotlib as plt
import pandas as pd
import numpy as np
import ipywidgets as widgets
from IPython import display
from tabulate import tabulate
import matplotlib.pyplot as plt

class measurement_result_page(BoxLayout, MDApp, Screen):
    # def __init__(self, **kwargs):
    #     super(measurement_result_page, self).__init__(**kwargs)
    #     print("in constructor")

    def yes_button_click(self, *args):
        '''
        save the images/best_image to past_measurement_images
        save best.csv to past_results.csv (measurement_type, angle, datetime, corresponding_image_path)
        provide a "saved" confirmation popup

        '''
        print("yes button")
        now = datetime.now()
        curr_datetime = now.strftime('%d-%m-%Y')

        #copy the image to past_measurement_images
        day_image_number = 0
        while os.path.isfile('./images/past_measurement_images/' + str(curr_datetime) + str(day_image_number) + '.png'):
            day_image_number += 1
        image_location = './images/past_measurement_images/' + str(curr_datetime) + str(day_image_number) + '.png'
        f = open(image_location, "x")
        shutil.copyfile('./images/best.png', image_location)

        #read the saved angle
        with open('./storage/best.csv', 'r+') as curr_results_file:
            angle = curr_results_file.readline().rstrip()

        #write the measurement results to past_results.csv
        curr_movement_type = self.manager.screens[1].external_name_to_internal_name[self.manager.screens[1].current_movement_type]
        with open('./storage/'+str(curr_movement_type) + '_past_results.csv', 'a') as past_results_file:
            past_results_file.write(str(curr_movement_type) +',' + str(angle) + ',' + str(curr_datetime) + ',' + image_location + '\n')

        #update graph for given measurement_type
        self.update_graph(curr_movement_type)

        #go back to main page
        self.manager.current = "main_page"

    def update_graph(self, curr_movement_type):
        '''
        Iterate through the measurements in ./storage/curr_movement_type_past_results.csv' and create a graph image.
        Save that image in images/Graphs.

        The graph will be a scatterplot with a trendline. There can be multiple measurements per day.
        '''
        curr_movement_file_path = './storage/' + str(curr_movement_type) + '_past_results.csv'
        print("curr type",  curr_movement_type)
        print("path: ", curr_movement_file_path)
        df = pd.read_csv(curr_movement_file_path)
        rows = df.values.tolist()
        date_range = pd.date_range(min(df['date']), max(df['date']))
        dates = [row[1] for row in rows]
        dates_angles = [[row[2], row[1]] for row in rows]

        index = 0
        while index < len(date_range):
            date = date_range[index].strftime('%d-%m-%Y')
            if date not in dates:
                dates_angles.insert(index, [date, np.nan])
            index += 1

        dates_angles.sort()
        df_dates = pd.DataFrame([row[0] for row in dates_angles], columns=['dates'])
        df_angles = pd.DataFrame([row[1] for row in dates_angles], columns=['angles'])
        plt.scatter(df_dates['dates'], df_angles['angles'])
        plt.tick_params(axis='x', labelrotation=30)

        plt.savefig('./images/Graphs/' + str(curr_movement_type) + '.png')


    def no_button_click(self, *args):
        '''
        Delete best.csv, images
        provide a "not saved" confirmation popup
        '''
        print("no button")
        self.manager.current = "main_page"

    def on_pre_leave(self, *args):
        '''
        delete images/best.png, images/curr_measurement_images
        '''
        if os.path.isdir("./images/curr_measurement_images"):
            shutil.rmtree("./images/curr_measurement_images")

        if os.path.isfile("./images/best.png"):
            os.remove("./images/best.png")


#Testing

#
# # plt.plot_date(dates, y)
# # plt.tight_layout()
# # plt.show()
# # curr_movement_type = 'Hip_Abduction'
# # plt.savefig('./images/Graphs/'+str(curr_movement_type) + '.png')
# curr_movement_type = 'Hip_Abduction'
# df = pd.read_csv('./storage/'+str(curr_movement_type) + '_past_results.csv')
# rows = df.values.tolist()
# date_range = pd.date_range(min(df['date']), max(df['date']))
# dates = [row[1] for row in rows]
# dates_angles = [[row[2], row[1]] for row in rows]
#
# index = 0
# while index < len(date_range):
#     date = date_range[index].strftime('%d-%m-%Y')
#     if date not in dates:
#         dates_angles.insert(index, [date, np.nan])
#     index+=1
#
# dates_angles.sort()
# print("dates_angles: ", dates_angles)
# df_dates = pd.DataFrame([row[0] for row in dates_angles], columns = ['dates'])
# df_angles = pd.DataFrame([row[1] for row in dates_angles], columns = ['angles'])
# print("df_dates: ",df_dates)
# print("df_angles: ", df_angles)
#
# plt.scatter(df_dates['dates'], df_angles['angles'])
# plt.tick_params(axis='x', labelrotation=30)
# #plt.ylim(0, max(df_angles['angles'])+30)
#
# plt.show()
#
# # print("initial row count: ", len(df.index))
# # date_range = pd.date_range(min(df['date']), max(df['date']))
# # added_count = 0
# # print(df.dtypes)
# # for date in date_range:
# #     date = date.strftime('%d-%m-%Y')
#
# #     df2 = {'measurement_type': "Hip Abduction",
# #            'angle': np.nan,
# #            'date': date.strftime('%d-%m-%Y'),
# #            'image_location': np.nan
# #             }
# #     print("df2: ", df2)
# #     df = pd.concat([df, df2])
# # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
# #
# # plt.scatter(df['date'], df['angle'])
# #plt.show()
#
#
#     # date = datetime64(date.strftime('%d-%m-%Y'))
#     # print("types: " , df['date'].dtype, date.dtype)
#     # if str(date) not in df['date']:
#     #     added_count += 1
#     #     print("adding: ", date)
#     #     row_df = {'date': date, 'angle': np.nan}
#     # if date not in df['date']:
#     #     add it with Nan value
#
# # print("end added count: ", added_count)
#
#
#
#
#
#
#
#
#
# #x = pd.date_range(min(data['datetime']), max(data['datetime']))
#
#
#
# # data.index = pd.DatetimeIndex(data.index)
# # data = data.reindex(x, fill_value=0)
# # print(data)
#
#
#
# # unique, index = np.unique(dates, return_inverse=True)
# # plt.scatter(data['datetime'], data['angle'])
# # plt.tick_params(axis='x', labelrotation=90)
# # #dates = data['datetime']
# # # angles = data['angle']
# # plt.show()
# # x = pd.date_range(min(dates), max(dates))
# # idx = pd.period_range(min(dates), max(dates))
# # angles = data['angle']
# # plt.scatter(dates, angles)
# # plt.xticks(x)
# # plt.show()
# # curr_movement_type = 'Hip_Abduction'
# # dates = ['2015-12-20', '2015-09-12']
# # PM_25 = [80, 55]
# # dates = [pd.to_datetime(d) for d in dates]
# # plt.pyplot.plot_date(dates, PM_25, c = 'red')
# # # plt.scatter(dates, PM_25, s=100, c='red')
# #
# plt.savefig('./images/Graphs/'+str(curr_movement_type) + '.png')