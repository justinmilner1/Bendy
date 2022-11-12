import cv2
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import math
from math import atan2, pi
from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh
import logging
import time
import os
from os import listdir

class loading_page(BoxLayout, MDApp, Screen):
    logger = logging.getLogger('TfPoseEstimator-WebCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def on_enter(self):
        self.process_images()

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")


    def process_images(self):
        '''
        Iterate through each image in ./images/curr_measurement_images, compute the angle for each. Write values to storage/curr_results.csv (angle_1, angle_2, ...)
        Do postprocessing: outlier removal, sliding window averaging
        Select image with largest result - write that image to images/best.png and write best measurement to storage/best.csv
        :return:
        '''
        print("doing image processing")
        angles_imagepath_human = self.measure_angles()
        print("angles_imagepath_human: ", angles_imagepath_human)
        best_angle_position = self.get_best_angle_and_path(angles_imagepath_human)
        print("best_angle_acheived: ", angles_imagepath_human[best_angle_position][0])

        #overlay the image
        print("path: ", './images/curr_measurement_images/' + angles_imagepath_human[best_angle_position][1])
        image = cv2.imread('./images/curr_measurement_images/' + angles_imagepath_human[best_angle_position][1])
        print("image: ", image)
        humans = angles_imagepath_human[best_angle_position][2]
        print("humans: ", humans)
        best_image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        #save the overlay of the image in best.png
        best_image_path = './images/best.png'
        if os.path.exists(best_image_path):
            os.remove(best_image_path)
        cv2.imwrite(best_image_path, best_image)


        # with open('./storage/curr_results.csv', 'r+') as curr_results:
        #         curr_results.truncate()
        #         curr_results.write("100,50,80")

        with open('./storage/best.csv', 'r+') as curr_results:
                curr_results.truncate()
                curr_results.write(str(int(angles_imagepath_human[best_angle_position][0])))

        self.manager.current = "measurement_result_page" #this will go to measurement_result page

    def get_best_angle_and_path(self, angles_and_image_path):
        '''
        Post processing. Do window slide.

        Temporarily just returning max no post processing
        '''
        max_angle = float('-inf')
        max_position = None
        curr_position = 0
        for angle_and_path in angles_and_image_path:
            if angle_and_path[0] > max_angle:
                max_angle = angle_and_path[0]
                max_position = curr_position
            curr_position+=1
        return max_position

    def measure_angles(self):
        angles_and_image_path = []
        e = TfPoseEstimator('./models/graph/mobilenet_v2_small/graph_opt.pb', target_size=(432, 368),
                            trt_bool=self.str2bool("False"))
        w, h = model_wh('0x0')
        folder_dir = "./images/curr_measurement_images"
        for image_path in sorted(os.listdir(folder_dir)):
            image = cv2.imread(folder_dir + '/' + image_path)
            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
            bp1, bpcenter, bp2, joint_name = self.get_joint_points(1)
            if len(humans) > 1:
                print("only one person in frame please")
            else:
                if len(humans) == 1:
                    angle = self.get_joint_angle(image, humans[0], bp1, bpcenter, bp2, input)
                    if angle is not None:
                        angles_and_image_path.append([angle, image_path, humans])
        return angles_and_image_path



    def getAngle(self, a, b, c):
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
        return ang + 360 if ang < 0 else ang

    def angle(A, B, C, /):
        Ax, Ay = A[0] - B[0], A[1] - B[1]
        Cx, Cy = C[0] - B[0], C[1] - B[1]
        a = atan2(Ay, Ax)
        c = atan2(Cy, Cx)
        if a < 0: a += pi * 2
        if c < 0: c += pi * 2
        return (pi * 2 + c - a) if a > c else (c - a)

    def get_joint_angle(self, image, human, bp1, bpcenter, bp2, input):
        try:
            center_x = human.body_parts[bpcenter].x * image.shape[1]
            center_y = human.body_parts[bpcenter].y * image.shape[0]
            bp1_x = human.body_parts[bp1].x * image.shape[1]
            bp1_y = human.body_parts[bp1].y * image.shape[0]
            bp2_x = human.body_parts[bp2].x * image.shape[1]
            bp2_y = human.body_parts[bp2].y * image.shape[0]
            angle = self.getAngle([bp1_x, bp1_y], [center_x, center_y], [bp2_x, bp2_y])
            if angle > 185:
                return 360 - angle
            else:
                return angle
        except KeyError:
            return None


    def get_joint_points(self, joint):
        bp1 = None
        bpcenter = None
        bp2 = None
        joint_name = None

        joint = int(joint)
        if joint == 1:
            bp1 = 10
            bpcenter = 8
            bp2 = 13
            joint_name = 'Side Splits'
        elif joint == 2:
            bp1 = 10
            bpcenter = 8
            bp2 = 13
            joint_name = 'Front Splits'
        elif joint == 3:
            bp1 = 5
            bpcenter = 6
            bp2 = 7
            joint_name = 'Elbow'
        elif joint == 4:
            bp1 = 2
            bpcenter = 3
            bp2 = 4
            joint_name = 'Elbow'
        elif joint == 5:
            bp1 = 12
            bpcenter = 13
            bp2 = 14
            joint_name = 'Knee'
        elif joint == 6:
            bp1 = 9
            bpcenter = 10
            bp2 = 11
            joint_name = 'Knee'
        return bp1, bpcenter, bp2, joint_name