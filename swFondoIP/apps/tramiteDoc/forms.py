#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Autor: Nolasco Bonilla, Francisco 
# Email: fnolasco124@gmail.com	

from django import forms
from django.contrib.auth.models import User
from .models import *
import datetime
FECHA = datetime.datetime.today()

class MTablaForm(forms.ModelForm):
	class Meta:
		model = MTabla

class DTablaForm(forms.ModelForm):
	class Meta:
		model = DTabla

class MClienteForm(forms.ModelForm):
	class Meta:
		model = MCliente


class MProyectoForm(forms.ModelForm):
	#Estado: Probado
	bancos = DTabla.objects.filter(IdMTab__IdMTabla = '007')
	sectores = DTabla.objects.filter(IdMTab__IdMTabla = '010')
	l_bancos = (('','(Seleccione Banco)'),)
	l_sectores = (('','(Seleccione Sector)'),)
	
	for b in bancos:
		dato = ((b.pk, b.NomDTab),)
		l_bancos  += dato
	for s in sectores:
		dato = ((s.pk, s.NomDTab),)
		l_sectores  += dato
	
	CONVOCATORIA = (('', '(Selec. convoc.)'),('2007','2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('20012', '2012'), ('2013', '2013'), ('2014', '2014'))
	
	IdMProy = forms.CharField(required = False, widget = forms.TextInput(attrs={'class':'hide form-control'}))
	IdCFMProy = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código'}))
	IdConv = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control', 'placeholder': 'Convocatoria'}), choices = CONVOCATORIA)
	NomMProy = forms.CharField(widget = forms.TextInput(attrs= {'class': 'form-control', 'placeholder': 'Nombre del Convenio'}))
	IdSector = forms.ChoiceField(widget = forms.Select(attrs= {'class': 'form-control'}), choices = l_sectores)
	#IdSector = forms.ModelChoiceField(queryset = DTabla.objects.filter(IdMTab__IdMTabla = '010'), empty_label= '(Seleccione Sector)..',widget = forms.Select(attrs= {'class': 'form-control'}))
	IdBanco = forms.ChoiceField(widget = forms.Select(attrs= {'class': 'form-control'}), choices = l_bancos)
	NumCtaInterMProy = forms.CharField(widget = forms.TextInput(attrs= {'class': 'form-control text-right', 'placeholder': 'Nro de cuenta interbancaria'}))
	FecIngMProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	MontInvCliMProy = forms.DecimalField(initial = '0.00', max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	MontInvFipMProy = forms.DecimalField(initial = '0.00', max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	MontTotMProy = forms.DecimalField(initial = '0.00', max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	#MontInvOtrMProy = forms.DecimalField(initial = '0.00', max_digits = 15, decimal_places = 2, widget = forms.NumberInput(atts = {'class': 'form-control'})))
	FecIniMProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	FecFinMProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	RutaPDFMProy = forms.FileField(required = False)
	RutaPDFConvMProy = forms.FileField(required = False)
	RutaPDFACMProy = forms.FileField(required = False)

	class Meta:
		model = MProyecto
		fields = ('IdMProy', 'IdCFMProy', 'IdConv', 'NomMProy', 'IdSector', 'IdBanco', 'NumCtaInterMProy', 'RutaPDFMProy', \
			'RutaPDFConvMProy', 'RutaPDFACMProy', 'FecIngMProy', 'MontInvCliMProy', 'MontInvFipMProy', 'FecIniMProy', 'FecFinMProy')


class MProtocoloForm(forms.ModelForm):
	# Estado: Probado
	NomMProt = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'proyecto'}))
	EmpMProt = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'empresa'}))
	RespMProt = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'responsable'}))
	DescMProt = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'descripcion'}))
	FecEntMProt = forms.DateField(required = True, initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs = {'class': 'form-control text-right', 'id': 'fecha'}))
	
	class Meta:
		model = MProtocolo
		fields = ('NomMProt', 'EmpMProt', 'RespMProt', 'DescMProt', 'FecEntMProt')


"""
class MProtocoloForm(forms.ModelForm):
	class <Meta:></Meta:>
		model = MProtocolo
"""
class DProtocoloForm(forms.ModelForm):
	# Estado: Probado
	NomDProt = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class': 'form-control', 'id': 'asunto'}))
	class Meta:
		model = DProtocolo
		fields = ('RutaPdfDProt', 'NomDProt')

class DProyectoForm(forms.ModelForm):
	
	FecIniDProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	FecFinDProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	FecFirmaDProy = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	MontAportFIPDProy = forms.DecimalField(initial = 0.00, max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control text-right'}))
	MontAportCliDProy = forms.DecimalField(initial = 0.00, max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control text-right'}))
	MontAportOtrDProy = forms.DecimalField(initial = 0.00, max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control text-right'}))
	DescDProy = forms.CharField(required = True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'[Breve descripcion de la adenda]'}))
	RutaPDFDProy = forms.FileField(required = True)
	
	class Meta:
		model = DProyecto
		fields =('FecIniDProy', 'FecFinDProy', 'FecFirmaDProy', 'MontAportFIPDProy', 'MontAportCliDProy', 'MontAportOtrDProy', 'IdTipDocDProy', 'DescDProy', 'RutaPDFDProy')

class MColaboradorForm(forms.ModelForm):

	#IdMPer = models.ForeignKey(MPersonal, db_column = 'IdMPer', verbose_name = "Personal", blank = True, null = True)
	#IdMProy = models.ForeignKey(MProyecto,db_column = 'IdMProy', verbose_name = "Proyecto", blank = True, null = True)
	#IdTipoCargoProy = forms.CharField(required = True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'[Breve descripcion de la adenda]'}))
	FecIniMCol = forms.DateField(required = False, initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	FecFinMCol = forms.DateField(required = False, initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	#FecFirmaMCol = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget = forms.DateInput(attrs= {'class': 'form-control text-right'}))
	#TiempoMCol = models.CharField(max_length = 50, blank=True, verbose_name = "Tiempo", null = True, default = 0)
	MontoMCol = forms.DecimalField(required = False, initial = 0.00, max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control text-right'}))
	MontoMenMCol = forms.DecimalField(required = False, initial = 0.00, max_digits = 15, decimal_places = 2, widget = forms.NumberInput(attrs = {'class': 'form-control text-right'}))
	#EstMCol = models.BooleanField(default = True, verbose_name = 'Estado')
	#EstActMCol = models.CharField(max_length =2, blank = True, verbose_name = "Estado actual", null = True)
	RutaPDFMCol = forms.FileField(required = False)
	#RutaOCRMCol = models.FileField(upload_to = urlOcr, verbose_name = "Ruta OCR", blank = True, null = True)
	class Meta:
		model = MColaborador
		fields =('FecIniMCol', 'FecFinMCol', 'MontoMCol', 'MontoMenMCol','RutaPDFMCol')		

class CargaForm(forms.ModelForm):
	class Meta:
		model = CargaPresupuesto
		fields = ('doc_temp',)


class UsuarioForm(forms.ModelForm):

	NIVEL_USUARIO = (('','Seleccione nivel de Usuario'),('0','Administrador'),('1','Usuario FIP'),('2','Supervisor'),('3','Unidad Ejecutora'))
	#lista_personal = MPersonal.objects.all().order_by("ApePMPer")
	#lista_clientes = MCliente.objects.all().order_by("NomMCli")
	FECHA = datetime.datetime.today()
	"""
	PERSONAL = (('','Seleccione Personal'),)
	CLIENTE = (('','Seleccione UE'),('0','NO ES UE'))
	
	for p in lista_personal:
		dato = ((p.IdMPer, p.ApePMPer+" "+p.ApeMMPer+", "+p.NomMPer),)
		PERSONAL += dato
	for c in lista_clientes:
		dato = ((c.IdMCli,c.NomMCli),)
		CLIENTE += dato
	"""
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de Usuario'}))
	password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'Password'}))
	fecIngreso = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), required=False, widget=forms.DateInput(attrs={'class':'form-control','type':'date', 'placeholder':'Fecha de ingreso'}))
	tipoUsuario = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=NIVEL_USUARIO)
	#idMCli = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}),choices=CLIENTE)
	#idMPer = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}),choices=PERSONAL)

	class Meta:
		model = User
		fields = ('username','password','fecIngreso','tipoUsuario')
		
class MPersonalForm(forms.ModelForm):
	lista_tipo_doc = DTabla.objects.filter(IdMTab__IdMTabla = '011')
	lista_areas = DTabla.objects.filter(IdMTab__IdMTabla = '008')
	lista_tipo_per = DTabla.objects.filter(IdMTab__IdMTabla = '022')
	FECHA = datetime.datetime.today()
	TIPO_PER = (('','Seleccione tipo personal'),)
	TIPO_DOC = (('','Seleccione tipo documento'),)
	AREAS = (('','Seleccione área'),)
	for p in lista_tipo_per:
		dato = ((p.pk, p.NomDTab),)
		TIPO_PER  += dato
	for p in lista_tipo_doc:
		dato = ((p.pk, p.NomDTab),)
		TIPO_DOC  += dato
	for p in lista_areas:
		dato = ((p.pk, p.NomDTab),)
		AREAS  += dato

	ApePMPer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el apellido paterno'}))
	ApeMMPer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el apellido materno'}))
	NomMPer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese los nombres'}))
	FechNacMPer = forms.DateField(required=False,initial = FECHA.strftime('%Y-%m-%d'), widget=forms.DateInput(attrs={'class':'form-control','type':'date', 'placeholder':'Fecha de nacimiento'}))
	IdTipPerMPer = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}),choices=TIPO_PER)
	IdTipDocMPer = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}),choices=TIPO_DOC)
	NDocMPer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese número de documento'}))
	FecIngMPer = forms.DateField(initial = FECHA.strftime('%Y-%m-%d'), widget=forms.DateInput(attrs={'class':'form-control','type':'date', 'placeholder':'Fecha de ingreso'}))
	Tel1MPer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese telefono'}))
	Tel2MPer = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese telefono(opcional)'}))
	Email1MPer = forms.CharField(widget=forms.TextInput(attrs={'type':'email','class':'form-control','placeholder':'Ingrese email'}))
	Email2MPer = forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'email','class':'form-control','placeholder':'Ingrese email(opcional)'}))
	IdArea = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class':'form-control'}),choices=AREAS)
	class Meta:
		model = MPersonal
		fields = ('ApePMPer','ApeMMPer','NomMPer','FechNacMPer','IdTipPerMPer','IdTipDocMPer','NDocMPer','FecIngMPer','Tel1MPer','Tel2MPer','Email1MPer','Email2MPer','IdArea')

class PresupuestoForm(forms.ModelForm):
	class Meta:
		model = PProyectos
		
