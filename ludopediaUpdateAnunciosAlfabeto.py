# -*- coding: utf-8 -*-
from lxml import html
from time import sleep
from datetime import datetime
import requests
import os
import sqlite3
import sys

# No terminal usar ~: python ludopedia.py [idIni] [regs]
# por ex. ~: python ludopedia.py 451 3000
#
#idIni = int(sys.argv[1])
#regs  = int(sys.argv[2])
#
#idMax = idIni + regs
#
try:
	maxItems = int(sys.argv[1])
except:
	maxItems = 0


current = 0

con = sqlite3.connect('ludopedia.db')
cursor = con.cursor()

cursor.execute("""
SELECT anuncio from jogos where tipo = 'ANUNCIO' and Status = 'Ativo' order by jogo, preco asc;
""")

jogoCount = 0
jogosAtulizados = 0
jogosApagados = 0
for id in cursor.fetchall():
	jogoCount = jogoCount + 1
	# 'http://www.ludopedia.com.br/anuncio?id_anuncio='+str(id)
	#url = 'http://www.ludopedia.com.br/anuncio?id_anuncio=' % id
	try:
		page = requests.get('http://www.ludopedia.com.br/anuncio?id_anuncio='+str(id[0]))
		tree = html.fromstring(page.content)
	except:
		print 'nova tentativa em 10s'
		sleep(10)
		page = requests.get('http://www.ludopedia.com.br/anuncio?id_anuncio='+str(id[0]))
		tree = html.fromstring(page.content)

	#jogoNome = tree.xpath('//div[@class="col-xs-10"]/h3/a/text()')
	jogoNome = tree.xpath('//*[@id="page-content"]/div/div/div/div[2]/h3/a/text()')
	#jogoFlavor = tree.xpath('//div[@class="col-xs-10"]/h3/span/text()')
	jogoFlavor = tree.xpath('//*[@id="page-content"]/div/div/div/div[2]/h3/span/text()')

	if len(jogoFlavor):
		detalhes = jogoFlavor[0]
	else:
		detalhes = 'NA'

	jogoPreco = tree.xpath('//span[@class="negrito proximo_lance"]/text()')

	if len(jogoPreco):
		jogoPreco =jogoPreco[0].split()
		jogoPreco[1] = jogoPreco[1].replace('.','')
		preco = float( jogoPreco[1].replace( ',','.' ) )
	else:
		preco = 0.0

	status = tree.xpath('//td/span/text()')

	validadeAnuncio = tree.xpath('//td/text()')

	if len(validadeAnuncio):
		validadeAnuncio[4] = validadeAnuncio[4].replace(',',' ')

		data = validadeAnuncio[4].split()
		ano = data[0].split('/')
		hora = data[1].split(':')
		data = datetime( int(ano[2]), int(ano[1]),int(ano[0]), int(hora[0]), int(hora[1]))

		if ( data > datetime.now() and status[1] == 'Vendido'):
			data = datetime.now()

	else:
		data = datetime( 1979, 8, 10 )

	pessoa = tree.xpath('//td/a/text()')
	#pessoa = tree.xpath('//*[@id="page-content"]/div/div/div/div[2]/table/tbody/tr[10]/td[2]/a/text()')



	if len(pessoa):
		vendedor = pessoa[1]

	if len(pessoa) < 3:
		comprador = 'NA'
	else:
		comprador = pessoa[2]

	#os.system('clear')

	current += 1
	#print 'Registro: ' + str(current)
#	total = idMax-idIni
#	progress = (current/float(total))*100
#
#	print str(current) + ' / ' + str(total) + " : " +  "%.2f" % round(progress,2) + "%"

	#print 'Id:       ', id[0]

	if  len(jogoNome) :

		if ( len(status[1]) > 15 ):
			status[1] = 'Ativo'

		#print 'Jogo:     ', jogoNome[0]
		#print 'Detalhes  ', detalhes
		#print 'Preco:    ', str(preco)
		#print 'Status:   ', status[1]
		#print 'Validade: ', data
		#print 'Estado:   ', validadeAnuncio[6]
		#print 'Local:    ', validadeAnuncio[8]
		#print 'Vendedor: ', vendedor
		#print 'Comprador:', comprador
		#print ' '


		formatedRow = "{0:4} {1:7} {2:16} {3:12}  {4:7}  {5}".format( str( jogoCount ).zfill( 4 ),
		                                                  str( id[0] ),
														  status[1],
														  validadeAnuncio[6],
														  str(preco),
														  jogoNome[0] )

		print  formatedRow  


		if ( comprador != 'Comprar'):
			jogosAtulizados = jogosAtulizados + 1

			con = sqlite3.connect('ludopedia.db')
			cursor = con.cursor()

			cursor.execute("""UPDATE JOGOS SET  STATUS = ?, COMPRADOR = ?, PRECO = ?, VALIDADE = ? where ANUNCIO = ? """,
		 					(status[1], comprador, preco, data, id[0] ) )
			try:
	  			con.commit()
			except:
				print 'Falha no Commit, tentando novamente em 10s.'
				sleep(10)
				con.commit()

			con.close()
	else:
		print str( jogoCount ).zfill( 4 ) + ' ' +  str( id[0] ) + '\t ' + '-------' + '   \t ' + '-------' + '     \t ' + '------' + '\t ' + '---'
		jogosApagados = jogosApagados + 1

		con = sqlite3.connect('ludopedia.db')
		cursor = con.cursor()

		status = 'Anuncio Apagado'
		comprador = 'NA'
		cursor.execute("""UPDATE JOGOS SET  STATUS = ?, COMPRADOR = ? where ANUNCIO = ? """,
		 				(status, comprador, id[0] ) )
		try:
	  		con.commit()
		except:
			print 'Falha no Commit, tentando novamente em 10s.'
			sleep(10)
			con.commit()

		con.close()

	sleep(0.0675)

#os.system('clear')
print '--------------------------------------------'
print 'Jogos Atualizados: ' + str( jogosAtulizados )
print 'Jogos Apagados:    ' + str( jogosApagados )
print '--------------------------------------------'
########################################################################

#sTable = sorted( table, key = getKey )

#print tabulate(sTable, tablefmt="plain" )

#f = open ( 'LudopediaLeaks %s-%s.csv' % ( idIni, idMax) , 'w' )

#for x in range ( 0, len( sTable ) ):

#	row =  "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % ( sTable[x][0],
#						sTable[x][1].encode('utf8'),
#						sTable[x][2].encode('utf8'),
#						sTable[x][3],
#						sTable[x][4].encode('utf8'),
#						sTable[x][5],
#						sTable[x][6].encode('utf8'),
#						sTable[x][7].encode('utf8'),
#						sTable[x][8].encode('utf8'),
#						sTable[x][9].encode('utf8') )
#	print row
#	f.write(row + '\n' )

#f.close()
