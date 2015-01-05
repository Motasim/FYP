"""
Created on Sat Dec 20 22:33:45 2014

@author: Alnour_
this dirty file proves that there is some speed that is common for me at least
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


class vector:
    def __init__(self , x , y):
        self._x = x
        self._y = y
    def abs_val(self):
        return math.sqrt(self._x**2 + self._y**2)
    def dot(self , other):
        return vector(self._x * other._x , self._y * other._y)
    def show(self):
        print '(' , self._x , ',' , self._y , ')'
class mouse_obj:
    def __init__(self , mouse_type , time  , x , y):
        self._type = mouse_type;
        self._time = int(time);
        self._x = int(x);
        self._y = int(y);
    def show(self):
        print ">>" , self._time , self._type , self._x , self._y
    def get_dist(self , another):
        x_res = self._x - another._x;
        y_res = self._y - another._y;
        return math.sqrt(x_res*x_res + y_res*y_res)
    def get_sp(self , another):
        dist = self.get_dist(another)
        if self._time == another._time:
            self._time += 1
        sp = dist / abs(self._time - another._time)
        return sp#[dist , sp]
    def get_angle(self , another):
        dx = abs(self._x - another._x)
        dy = abs(self._y - another._y)
        if dx == 0:
            return np.pi / 2.0
        return np.arctan(1.0 * dy/dx)
    def get_ang_speed(self , another):
        if self._time == another._time:
            self._time += 1
        dt = abs(self._time - another._time)
        return self.get_angle(another) * 1.0 /dt
    def get_3rd_dir(self , sec , third):
        dx1 = abs(sec._x - self._x)
        dy1 = abs(sec._y - self._y)
        
        dx2 = abs(sec._x - third._x)
        dy2 = abs(sec._y - third._y)
        theta_1 = np.pi/2
        if dx1  !=  0:
            theta_1 = np.arctan(dy1 * 1.0/ dx1)
        theta_2 = np.pi/2
        if dx2  !=  0:
            theta_2 = np.arctan(dy2 * 1.0/ dx2)
        return theta_1 + theta_2
    def get_curve_ang(self , a , b):
        #self is in the center between a anb b , we have 3 vectors: a-self , b-self,a-b
        AS = vector(a._x - self._x , a._y - self._y)
        BS = vector(b._x - self._x , b._y - self._y)
        return math.acos(AS.dot(BS)/(AS.abs_val()*BS.abs_val()))
#end of the class mouse_obj
        
def get_dis_sp(mouse_objs):
    dis_sp = []
    for i , ele in enumerate(mouse_objs):
        if i == 0:
            continue
        dis_sp.append(ele.get_ang_speed(mouse_objs[i-1]))
    return dis_sp
def get_3rd_angle(mouse_objs):
    res = []
    for i in xrange(2,len(mouse_objs)-2):
        res.append(mouse_objs[i].get_3rd_dir(mouse_objs[i-1] , mouse_objs[i-2]))
    return res
def get_arr(file_name):
    log_file = open(file_name)    
    data = log_file.read()
    lines = data.split("\n")
    objects = []
    for ele in lines:
        comps = ele.split("\t")
        if(comps[0] == 'MOUSEMOVE'):
            axs = comps[2].split(",")
            objects.append(mouse_obj(comps[0] , comps[1] , axs[0] , axs[1]))
    return get_dis_sp(objects)
    
y1 = get_arr("D://FYP/7oota.txt")
y2 = get_arr("D://FYP/bashir_mo.txt")
print  int(len(y1)*0.05)
y1_test = y1[0 : int(len(y1)*0.1)]
y2_test = y2[0 : int(len(y2)*0.1)]
t1 = np.arange(0, len(y1))
t2 = np.arange(0, len(y2))
plt.subplot(2,1,1)
plt.plot(t1,y1)
plt.subplot(2,1,2)
plt.plot(t2,y2)
