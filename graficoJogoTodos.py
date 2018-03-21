"""
Demo of a simple plot with a custom dashed line.

A Line object's ``set_dashes`` method allows you to specify dashes with
a series of on/off lengths (in points).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sqlite3
import datetime
import os
import sys


arg = sys.argv[1]

#nomeJogo = 'Ticket To Ride'
#nomeJogo = 'Eldritch Horror'
#nomeJogo = 'Agricola'

con = sqlite3.connect('ludopedia.db')

cursor = con.cursor()

x = """select distinct(jogo) from jogos where  preco > 4
                  and jogo like '""" + arg + """%' order  by jogo asc """

#cursor.execute("""select distinct(jogo) from jogos order by jogo""")
#cursor.execute("""select distinct(jogo) from jogos order by jogo asc LIMIT 10""")
cursor.execute( x )

nomesJogos = cursor.fetchall()

idJogo = 0

for nomeJogo in nomesJogos:
    idJogo = idJogo + 1

    #os.system( 'clear' )
    print str( idJogo ).zfill( 4 ) + ' ' + nomeJogo[0]

    con = sqlite3.connect('ludopedia.db')

    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE ESTADO = 'Lacrado' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotData = list()
    xValue = list()
    avgSeries = list()
    desvPadSup = list()
    desvPadInf = list()
    plotDataFinal = list()
    xValueFinal = list()
    plotMedia = list()

    for dado in dados:
        #xValue.append( dado[3] )
        try:
            xValue.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValue.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotData.append( dado[1] )
        plotMedia.append( np.mean( plotData ) )


    desvPadrao = np.std( plotData )
    media = np.mean( plotData )

    for dado in plotData:
        if (dado > media - 2 * desvPadrao) and (dado < media + 2 * desvPadrao):
            plotDataFinal.append( dado )


    #for dado in plotDataFinal:
        #avgSeries.append( media )
        #desvPadSup.append ( media + desvPadrao )
        #desvPadInf.append ( media - desvPadrao )

    for dado in plotData:
        avgSeries.append( media )
        desvPadSup.append ( media + desvPadrao )
        desvPadInf.append ( media - desvPadrao )

    con.close()
    xValues = range(len(plotData))
    #print len(plotData)
    #print range(len(plotData))

    #print plotData
    #print dados
    #print dados[0]
    #print dados[0][1]

    ##########################################################################
    # DADOS JOGOS USADOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')

    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE  ESTADO = 'Usado' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataU = list()
    xValueU = list()
    plotMediaU = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueU.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueU.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataU.append(dado[1])
        plotMediaU.append( np.mean( plotDataU ) )

    mediaU = np.median( plotDataU )


    con.close()

    ##########################################################################
    # DADOS JOGOS NOVOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')
    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE ESTADO = 'Novo' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataN = list()
    xValueN = list()
    plotMediaN = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueN.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueN.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataN.append(dado[1])
        plotMediaN.append( np.mean( plotDataN ) )

    mediaN = np.median( plotDataN )

    con.close()

    ##########################################################################
    # DADOS JOGOS AVARIADOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')
    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE ESTADO = 'Avariado' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataA = list()
    xValueA = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueA.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueA.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataA.append(dado[1])

    mediaA = np.median( plotDataA )

    con.close()


    ##########################################################################
    # DADOS JOGOS APAGADOS / INATVOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')
    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE (STATUS LIKE '%apagado%' or STATUS LIKE '%inativo')  AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataI = list()
    xValueI = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueI.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueI.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataI.append(dado[1])

    mediaI = np.median( plotDataI )

    con.close()



    ##########################################################################
    # DADOS JOGOS ATIVOS LACRADOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')
    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE STATUS = 'Ativo' AND ESTADO = 'Lacrado' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataAtL = list()
    xValueAtL = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueAtL.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueAtL.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataAtL.append(dado[1])

    mediaAtL = np.median( plotDataAtL )

    con.close()

    ##########################################################################
    # DADOS JOGOS ATIVOS NAO LACRADOS
    ##########################################################################

    con = sqlite3.connect('ludopedia.db')
    cursor = con.cursor()

    cursor.execute("""SELECT JOGO, PRECO, strftime( '%Y%m', validade ) AS dt, VALIDADE FROM JOGOS
                  WHERE STATUS = 'Ativo' AND ESTADO <> 'Lacrado' AND jogo = ? AND preco > 4 ORDER BY validade ASC """, [nomeJogo[0]])

    dados = cursor.fetchall()

    plotDataAt = list()
    xValueAt = list()
    #avgSeries = list()
    #desvPadSup = list()
    #desvPadInf = list()

    for dado in dados:
        try:
            xValueAt.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S' ) )
        except:
            xValueAt.append( datetime.datetime.strptime( dado[3], '%Y-%m-%d %H:%M:%S.%f' ) )
        plotDataAt.append(dado[1])

    mediaAt = np.median( plotDataAt )

    con.close()



    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    #fig.suptitle('Preco Medio dos Jogos Mes-a-Mes', fontsize=12, fontweight='bold')

    #if len(plotDataFinal):
    #    divGrid = max( plotDataFinal ) / 8
    #    # major ticks every 20, minor ticks every 5
    #    major_ticks = np.arange( 0, max( plotDataFinal ) + 1, divGrid )
    #    minor_ticks = np.arange( 0, max( plotDataFinal ) + 1, divGrid / 5 )
    #else:
    #    divGrid = 10
    #    major_ticks = np.arange( 0, 20, divGrid )
    #    minor_ticks = np.arange( 0, 5, divGrid / 5 )

    #ax.set_xticks(major_ticks)
    #ax.set_xticks(minor_ticks, minor=True)
    #ax.set_yticks(major_ticks)
    #ax.set_yticks(minor_ticks, minor=True)

    #ax.tick_params(which = 'both', direction = 'out')

    # and a corresponding grid
    #ax.grid(which='both')

    # or if you want differnet settings for the grids:
    #ax.grid(which='minor', alpha=0.2)
    #ax.grid(which='major', alpha=0.5)

    #line = plt.plot( xValue, avgSeries, 'g', linewidth = 2 )
    #line = plt.plot( xValue, desvPadSup, 'y', linewidth = 2 )
    #line = plt.plot( xValue, desvPadInf, 'y', linewidth = 2 )
    #line = plt.plot( xValue, plotData, 'k',  linewidth=1)
    line = plt.plot( xValue, plotMedia, 'b',  linewidth=1)
    line = plt.plot( xValueN, plotMediaN, 'm',  linewidth=1)
    line = plt.plot( xValueU, plotMediaU, 'r',  linewidth=1)
    line = plt.plot( xValue, plotData, 'bo', linewidth = 2 )
    line = plt.plot( xValueU, plotDataU, 'ro', linewidth = 2 )
    line = plt.plot( xValueN, plotDataN, 'mo', linewidth = 2 )
    line = plt.plot( xValueA, plotDataA, 'yo', linewidth = 2 )
    line = plt.plot( xValueAtL, plotDataAtL, 'o', color='lime', linewidth = 2 )
    line = plt.plot( xValueAt, plotDataAt, 'o', color='pink', linewidth = 2 )
    line = plt.plot( xValueI, plotDataI, 'o', color='grey', linewidth = 2 )
    #my_xticks = xValue

    plt.title('Vendas de: ' + nomeJogo[0] + '')
    plt.grid(True)
    plt.ylabel('Preco Medio (R$)')
    plt.xlabel('Meses')

    #plt.xticks(xValues, my_xticks, rotation='vertical', fontsize=5)

    #dashes = [1,2,3,4]  # 10 points on, 5 off, 100 on, 5 off
    #line.set_dashes(dashes)

    ########################################################################
    # LEGENDAS
    ########################################################################

    red_patch = mpatches.Patch(color='red',   label='Usado: ' + str( round( mediaU, 2) ) + ' ( ' + str( len( plotDataU ) ) + ' )'  )
    blue_patch = mpatches.Patch(color='blue', label='Lacrado: ' + str( round( media, 2) ) + ' ( ' + str( len( plotData ) ) + ' )' )
    purple_patch = mpatches.Patch(color='m',    label='Novo: ' + str( round( mediaN, 2) ) + ' ( ' + str( len( plotDataN ) ) + ' )' )
    yellow_patch = mpatches.Patch(color='y',  label='Avariado: ' + str( round( mediaA, 2) ) + ' ( ' + str( len( plotDataA ) ) + ' )' )
    cyan_patch = mpatches.Patch(color='lime',  label='Ativos (L): ' + str( round( mediaAtL, 2) ) + ' ( ' + str( len( plotDataAtL ) ) + ' )' )
    pink_patch = mpatches.Patch(color='pink',  label='Ativos: ' + str( round( mediaAt, 2) ) + ' ( ' + str( len( plotDataAt ) ) + ' )' )
    grey_patch = mpatches.Patch(color='grey',  label='Inat/Ap: ' + str( round( mediaI, 2) ) + ' ( ' + str( len( plotDataI ) ) + ' )' )
    plt.legend(handles=[blue_patch, purple_patch, red_patch, yellow_patch, cyan_patch, pink_patch, grey_patch])


    #plt.show()
    fig.set_size_inches(18.5, 10.5)
    filename = nomeJogo[0].replace( '/', ' ')
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    #fig.savefig( 'Grafico ' + str( idJogo ).zfill( 4 ) + '.png', dpi=100 )
    fig.savefig( './Graficos/ ' + filename + ' ' + date + '.png', dpi=100 )
