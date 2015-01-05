"""
Created on Sat Dec 20 22:33:45 2014

@author: Alnour_
this dirty file proves that there is some speed that is common for me at least
this code is written by help of:
http://scikit-learn.org/stable/auto_examples/svm/plot_oneclass.html
"""
import math
import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import preprocessing

def sqr_dist(p1 , p2):
    return (p1._x-p2._x)**2 + (p1._y-p2._y)**2
    
class vector:
    def __init__(self , x , y):
        self._x = x
        self._y = y
    def abs_val(self):
        return math.sqrt(self._x**2 + self._y**2)
    def dot(self , other):
        return self._x * other._x + self._y * other._y
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
        dx = self._x - another._x;
        dy = self._y - another._y;
        return math.sqrt(dx*dx + dy*dy)
    def get_sp(self , another):
        dist = self.get_dist(another)
        if self._time == another._time:
            self._time += 0.00001 #it means that the speed will be infinity
        sp = dist / abs(self._time - another._time)
        return sp#[dist , sp]
    def get_angle(self , another): #get the angle between two mouse points
        dx = self._x - another._x
        dy = self._y - another._y
        if dx == 0:
            return np.pi / 2.0
        return np.arctan(1.0 * dy/dx)
    def get_ang_speed(self , another):
        if self._time == another._time:
            self._time += 0.00001        
        dt = abs(self._time - another._time)
        return self.get_angle(another) * 1.0 /dt
    def get_curve_ang(self , a , b):
        #self is in the center between a anb b , we have 3 vectors: a-self , b-self,a-b
        AS = vector(a._x - self._x , a._y - self._y)
        BS = vector(b._x - self._x , b._y - self._y)
        N = AS.dot(BS)
        D = AS.abs_val()*BS.abs_val()
        N *= 0.99
        if D == 0:
           return None
        return math.acos(N/D)
    def get_curvature(self , p1 , p2): #get the distance from point self to the line passes by p1,p2
        D_m = p1._x - p2._x
        if D_m == 0:
            D_m = 0.001
        m = (p1._y - p2._y) / D_m
        a = m
        b = -1
        c = -m * p1._x + p1._y 
        x0 = self._x
        y0 = self._y
        N = abs(a*x0 + b*y0 + c)
        D = np.sqrt(a*a + b*b)
        if D == 0:
            D = 0.001
        prepenDist = N/D
        realDist = np.sqrt(sqr_dist(p1 , p2))
        if realDist == 0:
            return None
        return prepenDist / realDist
        
#end of the class mouse_obj
def replicate_paper(mouse_objs):
    res = []
    for i in range(2 , len(mouse_objs)):
        p1 = mouse_objs[i]
        p2 = mouse_objs[i-1]
        p3 = mouse_objs[i-2]
        direction = p1.get_angle(p2)
        curve_ang = p1.get_curve_ang(p2,p3)
        curvature = p2.get_curvature(p1,p3)
        if curve_ang != None and curvature != None:
            res.append([direction , curve_ang , curvature])
    return res
def get_arr(file_name):
    log_file = open(file_name)    
    data = log_file.read()
    lines = data.split("\n")
    objects = []
    for ele in lines:
        if ele == "":
            continue
        comps = ele.split("\t")
        axs = comps[2].split(",")
        objects.append(mouse_obj(comps[0] , comps[1] , axs[0] , axs[1]))
    return objects
def get_clf(data  , user_index , data_size): #returns set of classifiers for user number i
    res = []
    for i in range(0 , len(data)):
        if i == user_index:
            continue
        clf = svm.SVC(kernel = 'rbf')
        learn_data = np.concatenate((data[user_index][0:data_size] , data[i][0:data_size]) , axis = 0) 
        lables = [1]*data_size + [-1]*data_size
        print len(learn_data) , len(lables)
        clf.fit(learn_data , lables)
        res.append(clf)
    return res
def get_lablel(fearure_vector , clf_arr):
    ones = 0    
    for clf in clf_arr:
        if clf.predict(fearure_vector)[0] == 1:
            ones += 1
            if ones*1.0/len(clf_arr) > 0.5:
                return True
    return ones*1.0/len(clf_arr) > 0.5
def get_clfs_prc(data , clfs):
    ones = 0
    for feature_vector in data:
        if get_lablel(feature_vector , clfs):
            ones += 1
    print ones
    return ones*1.0/len(data)
y = []
logs_number = 4
for i in range(logs_number):
    y.append(get_arr("D:\FYP\mouselogs/"+str(i+1)+".txt"))
for i in range(len(y)):
    y[i] = replicate_paper(y[i])
    y[i] = preprocessing.scale(y[i])
clfs = get_clf(y , 0 , 15000)