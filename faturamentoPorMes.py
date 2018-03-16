"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


con = sqlite3.connect('ludopedia.db')
cursor = con.cursor()

cursor.execute("""SELECT dt, total from geralpormes """)

dados = cursor.fetchall()

plotData = list()
xValue = list()

for dado in dados:
    xValue.append(dado[0])
    plotData.append(dado[1])

con.close()

#print len(plotData)
#print range(len(plotData))

#print plotData
#print dados
#print dados[0]
#print dados[0][1]




line = plt.plot(range(len(plotData)), plotData,'k', linewidth = 1 )
line = plt.plot(range(len(plotData)), plotData,'bo', linewidth = 1 )
my_xticks = xValue
plt.xticks(range(len(plotData)), my_xticks, rotation='vertical')

#dashes = [1,2,3,4]  # 10 points on, 5 off, 100 on, 5 off
#line.set_dashes(dashes)
plt.grid(True)
plt.show()
