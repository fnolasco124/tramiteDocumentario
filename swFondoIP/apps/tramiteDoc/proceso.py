#! /usr/bin/env python
# -*- coding:utf-8 -*-

""" Script para modulo de Finanzas """
import sys
import xlrd
class Presupuesto:
	
	def inicio(self, nombre_archivo):
		isValid = True
		if nombre_archivo == '':
			isValid = False
		else:
			self.fileName = nombre_archivo
		return isValid

			
	def procesar_pres(self):
		""" METODO PARA PROCESAR EL PRESUPUESTO """
		import commands
		a = commands.getoutput('chmod 777 /var/www/appfip.com/swFondoIP/swFondoIP/media/presup/'+ self.fileName +'')
		self.cb = xlrd.open_workbook("/var/www/appfip.com/swFondoIP/swFondoIP/media/presup/" + self.fileName)
		try:
			self.cs = self.cb.sheet_by_index(3)	
		except IndexError as ie:
			self.cs = self.cb.sheet_by_index(0)
		except IOError as ioe:
			print "No existe ningun archivo con el nombre : %s" %(self.fileName)

		self.lista_errores = [] # Lista de errores encontrados en la hoja
		self.ind_i = 10 # Indice inicial para obtener valores de los meses
		self.ind_f = 10 # Indice final para obtener valores de los meses
		self.numCols = 0 # Obtiene la  duracion del proyecto
		self.tiempo_proy = self.duracion_proyecto()
		self.pos_fni = 5 # Gurada la ultima posicion no iterable
		self.lista_fni = [] # Guarda posiciones de las filas que poseen totales y subtotales para no ser iteradas
		self.pos_pp = self.get_pos_pp() # Obtenemos el indice de la primera partida
		self.dic_dp = {} # Cotiene los datos de las partidas
		self.verifica_fni()
		self.datos_presp = []
		self.datos_resultados = {}
		self.valido = True
		for x in range(self.pos_pp,self.pos_fni):	
			if (self.lista_fni.__contains__(x) == False):
				self.datos_presp.append(self.get_datos_partida(x))
			else:
				self.get_datos_resultado(x)
		if len(self.lista_errores) > 2:
			self.valido = False
			
		return self.valido, self.datos_presp, self.lista_errores
	
	def get_nivel_partida(self,partida):
		"""" METODO PARA OBTENER EL NIVEL DE LA PARTIDA """
		nivel = len(partida.split('.'))
		if nivel == 1:
			nivel = str(nivel) 
		elif nivel == 2:
			nivel = str(nivel) 
		elif nivel == 3:
			nivel = str(nivel) 
		elif nivel == 4:
			nivel = str(nivel) 
		else :
			nivel = str(nivel) 
		return nivel
		
	def verifica_fni(self):
		""" METODO PARA VERIFICAR LAS FILAS NO ITERABLES """
		self.val_st_res = self.get_fni() # Verifica la ubicacion de la sumatoria de resultados
		self.val_co_ad = self.get_fni() # Verifica la ubicacion de costos de administracion directa
		try:
			self.porc_cad_st = self.val_co_ad / self.val_st_res
		except ZeroDivisionError as zd:
			self.porc_cad_st = 0
		
		self.pos_fni = (self.lista_fni[-1])+1
		self.lista_fni.append(self.pos_fni) # Agrega la ubicacion del porcentaje de adm directa vs resultado
		self.val_cos_dir = 0.0
		self.val_cos_dir = self.val_st_res + self.val_co_ad 
		self.pos_fni = (self.lista_fni[-1])+1
		self.lista_fni.append(self.pos_fni) # Agrega la ubicacion de costo directo
		self.pos_fni = (self.lista_fni[-1])+1
		self.lista_fni.append(self.pos_fni) # Agrega la fila en blanco
		self.pos_fni = (self.lista_fni[-1])+1
		self.lista_fni.append(self.pos_fni) # Agrega la fila en blanco
		self.val_cos_ind = self.get_fni()
		self.pos_fni = (self.lista_fni[-1])+1
		self.lista_fni.append(self.pos_fni) # Agrega la ubicacion de costos directos vs indirectos
		self.pos_fni = (self.lista_fni[-1])+2
		self.lista_fni.append(self.pos_fni) # Agrega la ubicacion de imprevistos vs costo directo
				
	def get_pos_pp(self):
		pos = 0
		while True:
			try:
				valorCelda = self.cs.cell_value(rowx=pos,colx=0)
				if valorCelda == '01':
					break
				pos += 1
			except Exception, e:
				print "ERROR EN  METODO GET_POS_PP :: %s" %(e)
				pass
		return pos
			
	def duracion_proyecto(self):
		band = True
		pos = 0
		
		while band:
			try:
				valorCelda = self.cs.cell_value(rowx=pos,colx=0)
				#print valorCelda
				nivel = len(valorCelda.split('.'))
				pos += 1
				if nivel == 4:
					break
			except Exception, e:
				pass
		
		while band:
			try:				
				valorCelda = self.cs.cell_value(rowx=pos,colx=self.ind_f)
				self.ind_f += 1
				self.numCols += 1
			except IndexError as ie:
				self.numCols -= 1
				self.ind_f -= 1
				band = False
		return self.numCols/2

	def get_datos_resultado(self, fila):
		
		titulo = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,1))
		monto_total = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,6))																																																																																																																																																					
		self.datos_resultados[titulo] = monto_total	

	def get_lista_resultados(self):
		#print self.datos_resultados
		return self.datos_resultados
		
	def get_datos_partida(self,fila):
		dic_dp = {}																																																																																						
		partida = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,0))
		titulo = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,1))
																																																																																														
		descripcion = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,2))
		if descripcion == '':
			descripcion = titulo
		medida = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,3))
		cantidad = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,4))
		costo_unitario = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,5))
		monto_total = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,6))
		fip = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,7))
		ue = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,8))
		otros = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,9))
		
		try:
			if fip == '' and ue == '' and otros == '':
				pifip,piue,piotros = 0.0,0.0,0.0
			else:
				pifip = (float(fip)*100)/float(monto_total)
				piue = (float(ue)*100)/float(monto_total)
				piotros = (float(otros)*100)/float(monto_total)
		except ValueError as ve:
			pifip = 0.0
			piue = 0.0
			piotros = 0.0
		
		dic_dp['partida'] = partida
		dic_dp['nivel'] = self.get_nivel_partida(partida)
		dic_dp['tit'] = titulo.encode('ascii','ignore')
		dic_dp['desc'] = descripcion.encode('ascii','ignore')
		dic_dp['um'] = medida
		dic_dp['cant'] = cantidad
		dic_dp['cu'] = costo_unitario
		dic_dp['ct'] = monto_total
		dic_dp['ifip'] = fip
		dic_dp['iue'] = ue
		dic_dp['iotros'] = otros
		dic_dp['pifip'] = pifip
		dic_dp['piue'] = piue
		dic_dp['piotros'] = piotros
		dic_dp['cant_meses'] = self.get_datos_fila(fila)

		
		return dic_dp

		
	def get_datos_fila(self,fila):
				
		lista_valores = []
		suma_valores = 0.0
		
		for n in range(self.ind_i,self.ind_f):
			valor_celda = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,n))
			
			if (valor_celda == ''):
				lista_valores.append(0.0)
			else:
				try:
					lista_valores.append(float(valor_celda))
					suma_valores += float(valor_celda)
					
				except ValueError as ve:
					x,y = fila+1,n+1
					self.lista_errores.append('Existen valores no numericos en la celda (%s,%s)' %(x,y))
					self.presupuesto_valido = False
					break
		pos_suma = self.ind_f
		tfila = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,self.ind_f))
		tfip = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,7))
		tue = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,8))
		totros = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,9))
		
		if (tfila == '' and tfip == '' and tue == ''and totros == ''):
			tfila, tfip, tue, totros = 0.0, 0.0, 0.0, 0.0
			
		self.verifica_suma(lista_valores, tfila,tfip,tue,totros,fila)
		valor_celda = eval('self.cs.cell_value(rowx=%s,colx=%s)' %(fila,self.ind_f))	
		lista_valores.append(suma_valores)
		return lista_valores
	
	def get_fni(self,pos_col=6):
		#Verificamos la posicion de la sumatoria de los resultados
		self.pos_fni += 1
		band = True
		total  = 0.0
		i = 0
		pos_st_res = 0
		valor_celda = 0
		while band:
			try:
				valor_celda = float(eval('self.cs.cell_value(rowx=%s,colx=%s)' %(self.pos_fni,pos_col)))
			except ValueError as ve:
				valor_celda = 0.0
			except IndexError as ie:
				self.lista_errores.append("La sumatoria de los componentes, resultados, actividades y partidas no es igual al valor de la Suma de Resultados")
				band = False
				
			if (total == valor_celda and i>2):
				self.lista_fni.append(self.pos_fni)
				band = False
			else:
				total += valor_celda
				self.pos_fni += 1
			i+= 1
		return total
		
		
	def verifica_suma(self,lista,tfila,tfip,tue,totros,fila):
		s_fip, s_ue, s_tot = 0.0, 0.0, 0.0
		t_ue = 0.0
		if (tue == '' and tfip == '' and totros == ''):
			tue, tfip, totros = 0.0, 0.0, 0.0
		try:
			t_ue = float(tue) + float(totros)
		except ValueError as ve:
			t_ue = 0.0
			
		for n in lista[::2]: #Suma de valores para montos FIP
			 s_fip += float(n)
			 s_tot += float(n)
		for n in lista[1::2]:  #Suma de valores para montos UE + Otros
			s_ue += float(n)
			s_tot += float(n)
		
		if float(tfip) != float(s_fip):
			self.lista_errores.append('La inversion total de FIP no concuerda con la distribucion de meses[FILA %s]' %(fila)) 
		if float(t_ue) != float(s_ue):
			self.lista_errores.append('La inversion total de UE + Otros no concuerda con la distribucion de meses[FILA %s]' %(fila))
		if float(s_tot) != float(tfila):
			self.lista_errores.append('La suma de los montos por meses no concuerda con el total[FILA %s]' %(fila))
	
	def imprimir_presupuesto(self):
		for item in self.datos_presp:
			print "Partida \t: %s" %(item['partida'])
			print "Nivel \t: %s" %(item['nivel'])
			print "Titulo \t: %s" %(item['tit'])
			print "Descripcion \t: %s" %(item['desc'])
			print "Unidad de Medida \t: %s" %(item['um'])
			print "Cantidad \t: %s" %(item['cant'])
			print "Costo Unitario \t: S/. %s" %(item['cu'])
			print "Costo Total \t: %s" %(item['ct'])
			print "Inversion Fip \t: S/. %s  --  %s" %(item['ifip'],item['pifip'])
			print "Inversion UE \t: S/. %s  --  %s " %(item['iue'],item['piue'])
			print "Inversion Otros \t: S/. %s  --  %s" %(item['iotros'],item['piotros'])
			print "Valores \t: %s" %(item['cant_meses'][:10])
			print "Cantidad de valores \t:  %s " %(len(item['cant_meses']))
			print "*"*80
	
	def imprimir_errores(self):
		print "El archivo no puede ser procesado por que contiene los siguiente errores:"
		for error in self.lista_errores[:-2]:
			print error

	def get_lista_fni(self):
		return self.lista_fni
		
		
		


