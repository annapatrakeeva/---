import numpy as np
from numpy import log as ln
from math import pi, cos, sin

import random
scattering=5
capture=1
M=101
N=2500
#Границы поглощающего элемента
x_border_1=0.75
x_border_2=0.95
y_border=1.5
#Границы пластины
x0=0
x_max=1.3
y0=0
y_max=3

y = np.zeros(M)
x = np.zeros(M)
#входное сечение
def inlet_section(i):
    departure_points = np.zeros((M, N, 2))
    for j in range(1, M+1):
        #Точки вылета
        y = y0 + ((j-1) * (y_border - y0)) / (M - 1)
        x = x0
        #Создает по одной точке вылета, из которой вылетает N нейтронов
        departure_point = np.zeros((N, 2))
        for k in range(N):
            departure_point[k, :] = [x, y]
        #Заполняет слой вылета точками вылета
        departure_points[j-1] = departure_point
        #Возвращает массив из нейтронов, вылетевших из i точки
    return departure_points[i-1]
#массив для записи туда коэффициентов n для нейтронов, которые пересекли границу пластины
n_stop = []
def proverka(m_c, gamma_list):
    #массив из начальных коффициентов n, которые равны 1
    n = np.ones(len(m_c))
    for i in range(len(m_c)):
        if gamma_list[i]>(scattering/(capture+scattering)):
            n[i] = 0
        #Проверка того, не попал ли нейтрон в область поглащающий элемент

        #Проверяет не вылетел ли нейтрон за границу пластины
        if (m_c[i, 0]<x0) or (m_c[i, 1]>y_max):
            n[i] = 0
        #Если нейтрон пересек правую границу пластины, присваем ему n=3, чтобы записать его в n_stop
        if (m_c[i,0])>=x_max:
            n[i]=3
            n_stop.append(n[i])

    #Находит индексы нейтронов, которые либо вылетели за правую границу пластины, либо поглотились
    zero_indices = np.where((n == 0) | (n == 3))[0]
    return zero_indices,  n_stop

gamma_i=[]
def new_coordinates(massive, tetta):
    gamma_i = []
    for i in range(massive.shape[0]):
        gamma = random.uniform(0, 1)

        teta = tetta + pi / 2 * (2 * gamma - 1)
        ksi_0 = (-ln(gamma)) / (scattering + capture)
        #Новая координата x
        massive[i, 0] += ksi_0 * cos(teta)
        #Новая координата y
        massive[i, 1] += ksi_0 * sin(teta)
        gamma_i.append(gamma)
    index,  n_stop = proverka(massive, gamma_i)
    coordinates1_new = np.delete(massive, index, axis=0)
    return coordinates1_new, teta, n_stop
pj_values = []
#Перебираем все точки M
for i in range(1, M):
    #очищает список для каждой точки
    n_stop=[]
    #Получает координаты нейтронов на входе для i  точки
    p=inlet_section(i+1)

    #Получает x1, y1, для нейтронов i-ой точки
    p1_new,  teta1, n_stop1=new_coordinates(p, 0)

    # Получет x2, y2, для нейтронов i-ой точки
    p2new,  teta2, n_stop2=new_coordinates(p1_new, teta1)

    #Выполняется пока все нейтроны i-ой точки либо не вылетят за правую границу области, либо не поглотятся
    while p2new.shape[0]!=0:
        p3_new,  teta3, n_stop3 = new_coordinates(p2new, teta2)
        p2new=p3_new
    #Верояность нейтрона, вылетевшего из i-ой точки пройти пластину
    pj=(len(n_stop3))/N
    print(pj)






