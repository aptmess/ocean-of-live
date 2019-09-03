# -*- coding: utf-8 -*-
"""
Created on Tue Sep 3 09:43:45 2019

@author: shiro
"""

'''
синие квадратики - океан - 0
желтые квадратики - скалы, постоянны - 3
рыбы и креветки - бежевые и серые
рыбы - 1
креветки - 2
'''

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#--------------производится обновление океана-----------------------------

def update(i, shape, current_ocean, ocean):
    updateocean = ocean.copy()
    for i in range(shape):
        for j in range(shape):
            #узнаем значения
            top_left = ocean[(i - 1) % shape, (j - 1) % shape]
            top = ocean[(i - 1) % shape, j]
            top_right = ocean[(i - 1) % shape, (j + 1) % shape]
            left = ocean[i, (j - 1) % shape]
            right = ocean[i, (j + 1) % shape]
            bottom_left = ocean[(i + 1) % shape, (j - 1) % shape]
            bottom = ocean[(i + 1) % shape, j]
            bottom_right = ocean[(i + 1) % shape, (j + 1) % shape]
            dummy = []
            dummy.extend([top_left,top,top_right,left,right,bottom_left,bottom,bottom_right])
            fish=dummy.count(1) # количество рыб
            shellfish=dummy.count(2) # количество креветок
            #рыба умирает
            if ocean[i,j] == 1 and (fish < 2 or fish > 3):
                updateocean[i,j] = 0
            #рыба остается на месте
            elif fish in (2,3) and ocean[i,j]==1:
                updateocean[i,j] = 1
            #креветка умирает
            if ocean[i,j] == 2 and (shellfish < 2 or shellfish > 3):
                updateocean[i,j] = 0
            #креветка остается
            elif shellfish == (2,3) and ocean[i,j]==2:
                updateocean[i,j] = 2
            #если пустая клетка океана и рыб 3, то рождается рыбы
            if ocean[i,j] == 0 and fish==3:
                updateocean[i,j] = 1
            #если пустая клетка океана и креветок 3, то рождается креветка
            if ocean[i,j] == 0 and shellfish==3:
                updateocean[i,j] = 2
            #скалы не обновляются остаются на месте
    current_ocean.set_data(updateocean)
    ocean[:] = updateocean[:] # обновляем картинку, присваиваем гриду новое обновленное значение океана
    return (current_ocean,)

#--------------производится генерация рандомного квадратного поля с заданными вероятностями генерации-------

def generate_ocean(n, fish_probability=0.2,shellfish_probability=0.25,rock_probability=0.01):   
    return np.random.choice([1,2,3,0], n*n, \
                            p=[fish_probability,shellfish_probability,rock_probability,\
                               1 -fish_probability -shellfish_probability-rock_probability]).reshape(n,n)
    
def main_ocean(inputs):
    parser = argparse.ArgumentParser(description="ocean's life")
    parser.add_argument("--size", dest="shape",default=inputs, type=int)
    parser.add_argument("--interval", dest="delta", default=20, type=int)
    parser_arguments = parser.parse_args()
    oceanshape,interval= parser_arguments.shape,parser_arguments.delta
    ocean = generate_ocean(oceanshape)
    #работаем с графикой
    fig, ax = plt.subplots(figsize=(10,10))
    plt.axis("off")
    current_ocean = ax.imshow(ocean,cmap='cividis')
    animate = animation.FuncAnimation(fig,update,fargs=(oceanshape,current_ocean, ocean),frames=500,interval=interval,blit=True)
    plt.show()

if __name__ == "__main__":
    print("ocean shape is:")
    input_shape = input()
    main_ocean(input_shape)

