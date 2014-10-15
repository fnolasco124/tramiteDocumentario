#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys
from django.db import models
from django.contrib.auth.models import User
import datetime

# Agregamos los campos a la tabla usuario
TIPO_USUARIO = (
		('0', 'Administrador'),
		('1', 'Supervisor'),
		('2', 'Unidad Ejecutora'),
		('3', 'Usuario Fip'),
	)
User.add_to_class('IdMPer',models.CharField(max_length=30))
User.add_to_class('TipoUsuario',models.CharField(max_length=2,choices=TIPO_USUARIO))
User.add_to_class('FecIngreso',models.DateField(default='2014-01-01'))
User.add_to_class('IdMCli',models.CharField(max_length=30, default='0', blank=True))



class MTabla(models.Model):

	IdMTabla = models.CharField(max_length = 4, blank = True, primary_key = True)
	NomMTabla = models.CharField(max_length = 80, blank = True)
	AbrMTabla = models.CharField(max_length = 5, blank = True)
	PropMTabla = models.CharField(max_length = 2, blank = True)
	EstMTabla = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s - %s' %(self.IdMTabla, self.NomMTabla)

	def natural_key(self):
		return u'%s' %(self.NomMTab)

	def delete(self):
		self.EstMTabla = False
		detalles = DTabla.objects.filter(IdMTab__IdMTabla = self.IdMTabla)
		for d in detalles:
			d.delete()
		self.save()
		return True


class DTabla(models.Model):
	
	IdDTab = models.CharField(max_length = 5, blank = True, verbose_name = "Código")
	IdMTab = models.ForeignKey(MTabla, db_column ='IdMTabla', verbose_name = "Tabla Maestro")
	NomDTab = models.CharField(max_length = 80, blank = True, verbose_name = "Nombre")
	AbrDTab = models.CharField(max_length = 5, null = True, blank = True, verbose_name = "Abreviatura")
	AbrOpDTab = models.CharField(max_length = 5, null = True, blank = True, verbose_name = "Abreviatura Opcional")
	FactDTab = models.IntegerField(blank = True, verbose_name = "Factor")
	IndDTab = models.IntegerField(blank = True, verbose_name = "Indicador")
	IdRefDTab = models.CharField(max_length = 5, blank = True,verbose_name = "Referencia")
	PropDTab = models.CharField(max_length = 2,blank = True, verbose_name = "Prop")
	EstDTab = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s' %(self.NomDTab)

	def natural_key(self):
		return u'%s' %(self.NomDTab)

	def delete(self):
		self.EstDTab = False
		self.save()
		return True

class MPersonal(models.Model):

	IdMPer = models.CharField(max_length= 30,verbose_name = "Codigo", primary_key = True)
	ApePMPer = models.CharField(max_length = 80, verbose_name = "Apellido Paterno", blank = True)
	ApeMMPer = models.CharField(max_length = 80, verbose_name = "Apellido Materno", blank = True)
	NomMPer = models.CharField(max_length = 80, verbose_name = "Nombres", blank = True)
	FechNacMPer = models.DateField(verbose_name = "Fecha de Nacimiento", blank = True, null = True)
	IdTipPerMPer = models.CharField(max_length = 5, verbose_name = "Tipo Personal", blank = True)
	IdTipDocMPer = models.CharField(max_length = 5, verbose_name = "Tipo Documento", blank = True)
	NDocMPer = models.CharField(max_length = 20, verbose_name ="Numero de Documento", blank = True)
	EstMPer	= models.BooleanField(default = True, verbose_name = 'Estado')
	FecIngMPer = models.DateField(verbose_name = "Fecha de Ingreso", blank = True)
	Tel1MPer = models.CharField(max_length = 20, blank = True,verbose_name = "Telefono 1",)
	Tel2MPer = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 2(Opc)")
	Email1MPer = models.EmailField(max_length = 254, blank = True, verbose_name = "Email 1")
	Email2MPer = models.EmailField(max_length = 254, blank = True, verbose_name = "Email 2(Opc)")
	IdArea = models.CharField(max_length = 5, verbose_name = "Area", blank = True)

	def __unicode__(self):
		return u'%s %s, %s' %(self.ApePMPer, self.ApeMMPer, self.NomMPer)

	def natural_key(self):
		return u'%s %s' %(self.NomMPer, self.ApePMPer)

	def delete(self):
		self.EstMPer = False
		usuarios = User.objects.filter(IdMPer = self.IdMPer)
		for u in usuarios:
			u.delete()
		self.save()
		return True

class MCliente(models.Model):
	
	IdMCli = models.CharField(max_length = 30, verbose_name = "Código", primary_key = True)
	NomMCli= models.CharField(max_length = 300, blank = True, verbose_name = "Nombre",null = True)
	IdTipMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Tipo",null = True)
	IdTipInstMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Tip. Insitución",null = True)
	DirMCli = models.CharField(max_length = 100, blank = True, verbose_name = "Dirección", null = True)
	IdPaisMCli = models.CharField(max_length = 5, blank = True, verbose_name = "País", null = True)
	IdRegMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Región", null = True)
	IdDepMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Departamento",null = True)
	IdProvMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Provincia", null = True)
	IdDistMCli = models.CharField(max_length = 5, blank = True, verbose_name = "Distrito", null = True)
	RefMCli = models.CharField(max_length = 200, blank = True, verbose_name = "Referencia", null = True)
	Tel1MCli = models.CharField(max_length = 20, blank = True, verbose_name = "Teléfono 1", null = True)
	Tel2MCli = models.CharField(max_length = 20, blank = True, verbose_name = "Teléfono 2", null = True)
	Tel3MCli = models.CharField(max_length = 20, blank = True, verbose_name = "Teléfono 3", null = True)
	Email1MCli = models.EmailField(max_length = 300, blank = True, verbose_name = "Email Institucional", null = True)
	FecIngMCli = models.DateField(blank = True, verbose_name = "Fecha de Ingreso", null = True)
	EstMCli = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s' %(self.NomMCli)

	def natural_key(self):
		return u'%s' %(self.NomMCli)

	def delete(self):
		self.EstMCli = False
		self.save()
		return True

class MProyecto(models.Model):

	def urlPdf(self, filename):
		ruta = 'protocolos/%s.pdf' %(self.IdMProy)
		return ruta

	def urlOcr(self, filename):
		ruta = 'ocr/%s.pdf' %(self.IdMProy)
		return ruta

	def urlPDFAC(self, filename):
		ruta = 'acPdf/%s.pdf' %(self.IdMProy)
		return ruta

	def urlOCRAC(self, filename):
		ruta = 'acOcr/%s.pdf' %(self.IdMProy)
		return ruta

	def urlPdfConv(self, filename):
		ruta = 'convPdf/%s.pdf' %(self.IdMProy)
		return ruta

	def urlOcrConv(self, filename):
		ruta = 'convOcr/%s.pdf' %(self.IdMProy)
		return ruta


	IdMProy = models.CharField(max_length = 30, verbose_name = "Código", primary_key = True)
	IdMCli = models.ForeignKey(MCliente, db_column = 'IdMCli', verbose_name = "Cliente", null = True, blank = True)
	NomMProy = models.CharField(max_length = 700, blank = True, verbose_name = "Convenio", null = True)
	FecEntMProy = models.DateField(blank = True, verbose_name = "Fecha de Entrega" , null = True)
	FecEntRealMProy = models.DateField(blank = True, verbose_name = "Fecha de Entrega Real", null = True)
	FecIniMProy = models.DateField(blank = True, verbose_name = "Fecha de Inicio" , null = True)
	FecIniRealMProy = models.DateField(blank = True, verbose_name = "Fecha de Inicio Real", null = True)
	FecFinMProy = models.DateField(blank = True, verbose_name = "Fecha Fin", null = True)
	FecFinRealMProy = models.DateField(blank = True, verbose_name = "Fecha Fin Real", null = True)
	MontInvCliMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Inversión Cliente", null = True, default = 0)
	MontInvFipMProy = models.DecimalField(max_digits = 15, decimal_places =2, blank = True,verbose_name = "Inversión FIP", null = True, default = 0)
	MontTotMProy = models.DecimalField(max_digits = 15, decimal_places=2, blank = True, verbose_name = "Inversión Total", null = True, default = 0)
	MontTInvRealCliMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Inversión Real Cliente", null = True, default = 0)
	MontTInvRealFipMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Inversión Real FIP", null = True, default = 0)
	MontTInvRealOtrMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Inversión Real Asociados", null = True, default = 0)
	MontTotRealMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank =  True, verbose_name = "Inversión Real Total", null = True, default = 0)
	IdTipProMProy = models.CharField(max_length = 5, blank = True, verbose_name = "Tipo Proyecto", null = True, default = '0')
	EstMProy = models.BooleanField(default = True, verbose_name = 'Estado')
	FecIngMProy = models.DateField(blank = True, verbose_name = "Fecha de Ingreso", null = True)
	IdEstMProy = models.CharField(max_length = 5, blank = True, verbose_name="Estado", null = True, default = '0') 
	IdSector = models.CharField(max_length = 5,blank = True, verbose_name = "Sector", null = True, default = '0')
	IdBanco = models.CharField(max_length = 5,blank = True, verbose_name = "Banco", null = True, default = '0')
	NumCtaInterMProy = models.CharField(max_length = 50, blank = True, verbose_name = "Cuenta Corriente", null = True)
	MontTotAdeCliMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Monto Adendas Cliente", null = True, default = 0)
	MontTotAdeFipMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Monto Adendas FIP", null = True, default = 0)
	MontTotAdeOtrMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Monto Adendas Asociados", null = True, default = 0)
	MontTotAdeTotMProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Monto Total Adendas", null = True, default = 0)
	IdConv = models.CharField(max_length = 5, blank = True, verbose_name = "Convocatoria", null = True)
	TiempoMProy = models.CharField(max_length = 50, blank = True, verbose_name = "Tiempo", null = True)
	PorcTotAdeMProy = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, verbose_name="Porcentaje de Adelanto", null=True)
	RutaPDFMProy = models.FileField(upload_to = urlPdf, verbose_name="PDF PROYECTO", null = True, blank = True)
	RutaPDFConvMProy = models.FileField(upload_to = urlPdfConv, verbose_name = "PDF PROYECTO", null = True, blank = True)
	RutaOCRConvMProy = models.FileField(upload_to = urlOcrConv, verbose_name = "PDF PROYECTO", null = True, blank = True)
	RutaOCRMProy = models.FileField(upload_to = urlOcr, verbose_name = "OCR PROYECTO", null = True, blank = True)
	RutaPDFACMProy = models.FileField(upload_to = urlPDFAC, verbose_name = "PDF AC", null = True, blank = True)
	RutaOCRACMProy = models.FileField(upload_to = urlOCRAC, verbose_name = "OCR AC", null = True, blank = True)
	EstCierreMProy = models.CharField(max_length = 2, blank = True, default = "0")
	IdCFMProy = models.CharField(max_length = 30, blank = True, null = True)

	def __unicode__(self):
		return u'%s - %s' %(self.IdMProy, self.NomMProy)

	def natural_key(self):
		return u'%s, %s' %(self.NomMProy, self.IdMCli)

	def delete(self):
		self.EstMProy = False
		protocolos = MProtocolo.objects.filter(IdMProy__IdMProy = self.IdMProy)
		modificatorias = DProyecto.objects.filter(IdMProy__IdMProy = self.IdMProy)
		colaboradores = MColaborador.objects.filter(IdMProy__IdMProy = self.IdMProy)
		for p in protocolos:
			p.delete()
		for m in modificatorias:
			m.delete()
		for c in colaboradores:
			c.delete()
		self.save()
		return True

class MProtocolo(models.Model):
	
	IdMProt = models.CharField(max_length = 30, verbose_name = "Código",primary_key = True)
	IdMProy = models.ForeignKey(MProyecto, db_column = "IdMProy", verbose_name = "Convenio", null = True, blank = True)
	NomMProt = models.CharField(max_length = 450, blank = True, verbose_name = "Nombre")
	EmpMProt = models.CharField(max_length = 200, verbose_name = "Empresa", blank = True)
	RespMProt = models.CharField(max_length = 100, verbose_name = "Responsable", blank = True)
	DescMProt = models.CharField(max_length = 450, blank = True, verbose_name = "Descripción")
	FecEntMProt = models.DateField(blank = True, verbose_name = "Fecha de Entrega")
	FecEntRealMProt = models.DateField(blank = True, verbose_name = "Fecha de Entrega Real")
	IdTipFormEntMProt = models.CharField(max_length = 5,blank = True, verbose_name = "Formato de Entrega") # Puede ser digital, fisico o ambos
	IdRefMProt = models.CharField(max_length = 30, blank = True, verbose_name = "Referencia")
	IdTipDocGen = models.CharField(max_length = 5,blank = True, verbose_name = "Documento Generado") # Informe, etc
	EstMProt = models.BooleanField(default = True, verbose_name = 'Estado')
	DocInter = models.CharField(max_length = 5, default = "0", verbose_name = "Documento Interno")
	
	def __unicode__(self):
		return u'%s - %s' %(self.IdMProt, self.NomMProt)

	def save(self, *args, **kwargs):
		codigo_protocolo = self.IdMProt
		# Convertimos a mayusculas los datos ingresados
		self.NomMProt = self.NomMProt.upper()
		self.EmpMProt = self.EmpMProt.upper()
		self.RespMProt = self.RespMProt.upper()
		self.DescMProt = self.DescMProt.upper()
		super(MProtocolo, self).save(*args, **kwargs)
		item = Bandeja.objects.last()
		item.IdMProt = MProtocolo.objects.get(IdMProt = codigo_protocolo)
		item.save()

	def natural_key(self):
		return u'%s' %(self.NomMProt)

	def delete(self):
		self.EstMProt = False
		detalles = DProtocolo.objects.filter(IdMProt__IdMProt = self.IdMProt)
		bandejas = Bandeja.objects.filter(IdMProt__IdMProt = self.IdMProt)
		for d in detalles:
			d.delete()
		for b in bandejas:
			b.delete()
		self.save()
		return True

class DProtocolo(models.Model):
	
	def urlPdf(self, filename):
		ruta = 'protocolos/%s.pdf' %(self.IdDProt)
		return ruta

	def urlOcr(self, filename):
		ruta = 'ocr/%s' %(filename)
		return ruta

	IdDProt = models.CharField(max_length = 35, verbose_name = "Código", primary_key = True)
	IdMProt = models.ForeignKey(MProtocolo, db_column = 'IdMProt', verbose_name = "Protocolo")
	NomDProt = models.CharField(max_length = 600, blank = True, verbose_name = "Nombre")
	IdTipDocDProt = models.CharField(max_length = 5, blank = True, verbose_name = "Tipo Documento")
	UbLogDProt = models.CharField(max_length = 20, blank = True, verbose_name = "Ubicación Lógica")
	UbiFisDProt = models.CharField(max_length = 20, blank = True, verbose_name = "Ubicación Física")
	RutaPdfDProt = models.FileField(upload_to = urlPdf, verbose_name = "Ruta PDF", null = True, blank=True)
	RutaOcrDProt = models.FileField(upload_to = urlOcr, verbose_name = "Ruta OCR", null = True, blank= True)
	EstDProt = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s' %(self.NomDProt)

	def save(self, *args, **kwargs):
		self.NomDProt = self.NomDProt.upper()
		super(DProtocolo, self).save(*args, **kwargs)

	def natural_key(self):
		return u'%s' %(self.NomDProt)

	def delete(self):
		self.EstDProt = False
		self.save()
		return True

class DProyecto(models.Model):

	def urlPdf(self, filename):
		ruta = 'adendasPDF/%s.pdf' %(self.IdDProy)
		return ruta

	def urlOcr(self, filename):
		ruta = 'adendasOCR/%s.txt' %(self.IdDProy)
		return ruta

	IdDProy = models.CharField(max_length = 30, verbose_name = "Código", primary_key = True)
	IdMProy = models.ForeignKey(MProyecto, db_column = 'IdMProy', verbose_name = "Proyecto")
	FecIniDProy = models.DateField(blank = True, verbose_name = "Fecha de Inicio")
	FecFinDProy = models.DateField(blank = True, verbose_name = "Fecha Final")
	FecFirmaDProy = models.DateField(blank = True, verbose_name = "Fecha de Firma")
	MontAportFIPDProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Aporte FIP")
	MontAportCliDProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Aporte Cliente")
	MontAportOtrDProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Aporte Asociados")
	IdTipDocDProy = models.CharField(max_length = 5, blank = True, null = True, verbose_name = "Tipo de documento")
	DescDProy = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Descripción")
	RutaPDFDProy = models.FileField(upload_to = urlPdf, verbose_name = "Ruta PDF", blank = True, null = True)
	RutaOcrDProy =  models.FileField(upload_to = urlOcr, verbose_name = "Ruta OCR", blank = True, null = True)
	EstDProy = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s' %(self.IdDProy)

	def save(self, *args, **kwargs):
		instancia = self.IdMProy
		instancia.MontTotAdeCliMProy = float(instancia.MontTotAdeCliMProy) + float(self.MontAportCliDProy)
		instancia.MontTotAdeFipMProy = float(instancia.MontTotAdeFipMProy) + float(self.MontAportFIPDProy)
		instancia.MontTotAdeOtrMProy = float(instancia.MontTotAdeOtrMProy) + float(self.MontAportOtrDProy)
		total = instancia.MontTotAdeCliMProy + instancia.MontTotAdeFipMProy + instancia.MontTotAdeOtrMProy
		instancia.MontTotAdeTotMProy = total
		instancia.save()
		super(DProyecto, self).save(*args, **kwargs)
		

	def natural_key(self):
		return u'%s' %(self.DescDProy)

	def delete(self):
		self.EstDProy = False
		self.save()
		return True

class MColaborador(models.Model):
	
	def urlPdf(self, filename):
		ruta = 'colaborador/%s.pdf' %(filename)
		return filename

	def urlOcr(self, filename):
		ruta = 'ocr/%s.txt' %(filename)
		return ruta

	IdMPer = models.ForeignKey(MPersonal, db_column = 'IdMPer', verbose_name = "Personal", blank = True, null = True)
	IdMProy = models.ForeignKey(MProyecto,db_column = 'IdMProy', verbose_name = "Proyecto", blank = True, null = True)
	IdTipoCargoProy = models.CharField(max_length = 5, blank = True, verbose_name = "Cargo", null = True)
	FecIniMCol = models.DateField(blank = True, verbose_name = "Fecha de Inicio", null = True, default = datetime.datetime.today())
	FecFinMCol = models.DateField(blank = True, verbose_name = "Fecha Final", null = True, default = datetime.datetime.today())
	FecFirmaMCol = models.DateField(blank = True, verbose_name = "Fecha Firma", null = True, default = datetime.datetime.today())
	TiempoMCol = models.CharField(max_length = 50, blank=True, verbose_name = "Tiempo", null = True, default = 0)
	MontoMCol = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Pago Total", null = True, default = 0)
	MontoMenMCol = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, verbose_name = "Pago Mensual", null = True, default = 0)
	EstMCol = models.BooleanField(default = True, verbose_name = 'Estado')
	EstActMCol = models.CharField(max_length =2, blank = True, verbose_name = "Estado actual", null = True)
	RutaPDFMCol = models.FileField(upload_to = urlPdf, verbose_name = "Ruta PDF", blank = True, null = True)
	RutaOCRMCol = models.FileField(upload_to = urlOcr, verbose_name = "Ruta OCR", blank = True, null = True)
	
	def __unicode__(self):
		return u'%s' %(self.IdMPer)

	def natural_key(self):
		return u'%s' %(self.IdMPer.NomMPer)

	def delete(self):
		self.EstMCol = False
		self.save()
		return True

class Bandeja(models.Model):

	IdBandeja = models.CharField(max_length = 50, verbose_name = "Codigo", primary_key = True)
	IdMProt = models.ForeignKey(MProtocolo, db_column = "IdMProt", verbose_name = "Protocolo", blank = True, null = True)
	IdMUsuEnv = models.ForeignKey('auth.User', related_name = "Enviado_Por", verbose_name = "Enviado Por", blank = True, null = True)
	IdMUsuRec = models.ForeignKey('auth.User', related_name = "Recepcionado_Por/Recepcionado_Por", verbose_name = "Recepcionado Por", blank = True, null = True)
	FecEnv = models.DateField(blank = True, verbose_name = "Fecha de Envio")
	FecRec = models.DateField(blank = True, verbose_name = "Fecha de Recepcion")
	FecSist = models.DateField(blank = True, verbose_name = "Fecha del sistema")
	MenBProt = models.CharField(max_length = 850, blank = True, verbose_name = "Mensaje")
	EstBProt = models.BooleanField(default = True, verbose_name = 'Estado')
	EstAccion = models.CharField(max_length = 6, blank = True, verbose_name = "Accion")
	EstObservado = models.CharField(max_length = 2, blank = True, verbose_name = "Observado")
	ObsProt = models.CharField(max_length = 200, blank = True, verbose_name = "Observación")
	IdProtRef = models.CharField(max_length = 30, blank = True, verbose_name = "Referencia")
	
	def __str__(self):
		return u'IdBandeja %s' %(self.IdBandeja)

	def natural_key(self):
		return u'%s' %(self.IdMUsuEnv.username,self.IdMUsuRec.username)

	def finalizar(self, estado = False):
		self.EstBProt = estado
		self.save()

	def delete(self):
		self.EstBProt = False
		self.save()
		return True

class FProtocolo(models.Model):

	IdDProt = models.ForeignKey(DProtocolo, verbose_name = "DProtocolo_id")
	IdMPerE = models.ForeignKey(MPersonal, related_name = "Transferido_por", db_column = "IdMPerE", verbose_name = "Enviado por")
	IdMPerR = models.ForeignKey(MPersonal, related_name = "Transferido_a", db_column = "IdMPerR", verbose_name = "Recepcionado por")
	FecFProt = models.DateTimeField(auto_now = True)
	EstFProt = models.BooleanField(default = True)

	def __unicode__(self):
		return u"%s" %(self.IdDProt)
	def delete(self):
		self.EstFProt = False
		self.save()
		return True

class CClientes(models.Model):

	IdCCli = models.CharField(max_length = 30, verbose_name = "Codigo", primary_key = True)
	IdMCli = models.ForeignKey(MCliente, db_column = 'IdMCli', blank = True, verbose_name = "Codigo Cliente")
	ApePCCli = models.CharField(max_length = 80, blank = True, verbose_name = "Apellido Paterno")
	ApeMCCli = models.CharField(max_length = 80, blank = True, verbose_name = "Apellido Materno")
	NomCCli = models.CharField(max_length = 80, blank = True, verbose_name = "Nombres")
	IdTipDocCCli = models.CharField(max_length = 5, blank = True, verbose_name = "Tipo de Documento")
	NumDocCCli = models.CharField(max_length = 20, blank = True, verbose_name = "Numero de Documento")
	EstCCli = models.BooleanField(default = True, verbose_name = 'Estado')
	Tel1CCli = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 1")
	Tel2CCli = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 2(opc)")
	Email1CCli = models.EmailField(max_length = 254, blank = True, verbose_name = "Email 1")
	Email2CCli = models.EmailField(max_length = 254, blank = True, verbose_name = "Email 2(Opc)")

	def __unicode__(self):
		return u'%s - %s -%s ' %(self.IdMCli, self.IdCCli, self.NomCCli)

class SClientes(models.Model):

	IdSCli = models.CharField(max_length = 30, verbose_name = "Codigo", primary_key = True) 
	IdMCli = models.ForeignKey(MCliente, db_column = 'IdMCli',max_length = 30, blank = True, verbose_name = "Codigo Cliente")
	NomSCli = models.CharField(max_length = 100, blank = True, verbose_name = "Nombre")
	IdTipSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Tipo")
	DirSCli = models.CharField(max_length = 100, blank = True, verbose_name = "Direccion")
	IdPaisSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Pais")
	IdRegSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Region")
	IdDepSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Departamento")
	IdProvSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Provincia")
	IdDistSCli = models.CharField(max_length = 5, blank = True, verbose_name = "Distrito")
	RefSCli = models.CharField(max_length = 200, blank = True, verbose_name = "Referencia")
	Tel1SCli = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 1")
	Tel2SCli = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 2(opc)")
	Tel3SCli = models.CharField(max_length = 20, blank = True, verbose_name = "Telefono 3(opc)")
	Email1SCli = models.EmailField(max_length = 254, blank = True, verbose_name = "Email")
	EstSCli = models.BooleanField(default = True, verbose_name = 'Estado')

	def __unicode__(self):
		return u'%s %s' %(self.IdSCli, self.NomSCli)

class PProyectos(models.Model):

	IdPProy = models.CharField(max_length = 30, primary_key = True, verbose_name = "Codigo del Presupuesto", help_text = "Ingrese codigo del presupuesto")
	IdMProy = models.ForeignKey(MProyecto, blank = True, null =True, verbose_name = "Seleccione Convenio", help_text = "Seleccione el convenio")
	NroPartPProy = models.CharField(max_length = 40, blank = True, null = True, verbose_name = "Numero de Partida", help_text = "Ingrese el numero de partida")	
	IdNivPartPProy	= models.CharField(max_length = 4, blank = True, null = True, verbose_name = "Nivel de Partido", help_text = "Seleccione el  nivel de partida")
	DescPProy = models.CharField(max_length = 300, blank =True, null = True, verbose_name = "Descripcion de la partida", help_text = "Ingrese la descripción de la partida")
	TitPProy = models.CharField(max_length = 300, blank = True, null = True, verbose_name = "Descripcion de la partida", help_text = "Ingrese el título de la partida")
	NroPartPerPProy = models.CharField(max_length = 40, blank = True, null = True, verbose_name = "Pertenece a ", help_text = "Seleccione a que partida pertenece")
	IdUnidMed = models.CharField(max_length = 4, blank = True, null = True, verbose_name = "Unidad de medida", help_text = "Seleccione unidad de medida")
	CantPProy = models.IntegerField(blank = True, null = True, verbose_name = "Cantidad", help_text = "Ingrese la cantidad")
	CostUnitPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null=True, verbose_name = "Cantidad", help_text = "Ingrese la cantidad")
	CostTotPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null= True, verbose_name = "Costo total", help_text = "Costo total")
	FFFipPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null=True,verbose_name = "Financiamiento FIP", help_text = "Financiamiento FIP")
	FFCliPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null=True, verbose_name = "Financiamiento UE", help_text = "Financiamiento UE")
	FFOtrosPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Financiamiento Otros", help_text = "Financiamiento Otros")
	PFFFipPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null=True,verbose_name = "Porcentaje Financiamiento FIP",help_text = "Porcentaje Financiamiento FIP")
	PFFCliPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null=True, verbose_name = "Porcentaje Financiamiento UE", help_text = "Porcentaje Financiamiento UE")
	PFFOtrosPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Porcentaje Financiamiento Otros", help_text = "Porcentaje Financiamiento Otros")
	FinPProy = models.IntegerField(blank = True, null = True, verbose_name = "", help_text = "")
	VerPProy = models.IntegerField(blank = True, null = True, verbose_name = "Versión", help_text="Versión")
	EstPProy = models.CharField(max_length = 2,blank =True, null = True, verbose_name = "Estado",help_text = "Estado")
	FecIngPProy = models.DateField(blank = True, null = True, verbose_name = "Fecha de Ingreso", help_text = "Fecha de ingreso")
	IdUsuCreaPProy = models.CharField(max_length = 30, blank = True, null = True, verbose_name = "Creado por", help_text = "Creado por")
	FecModPProy = models.DateField(blank = True, null=True, verbose_name = "Fecha de modificacion", help_text = "Fecha de modificacion")
	IdUsuModPProy = models.CharField(max_length = 30, blank=True, null = True, verbose_name = "Modificado por", help_text = "Modificado por")
	CostEjePProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Costo de ejecución", help_text = "Ingrese el costo de ejecución")
	CostSalPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Saldo de la ejecución", help_text = "Saldo de la ejecución")
	IdMotCierrePProy = models.CharField(max_length = 4, blank = True, null = True, verbose_name = "Motivo de cierre", help_text="Seleccione el motivo de cierre")
	PorcCostEjePProy = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True, verbose_name = "Porcentaje de Costo de ejecución", help_text = "Porcentaje de costo de ejecución")
	BorradorPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Borrado", help_text = "Borrador")
	EstPresPProy = models.BooleanField(default = True, verbose_name = 'Estado')
	EstEvalPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Estado", help_text = "Estado")
	EstValidPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Estado", help_text = "Estado")
	EstAprobPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Estado", help_text = "Estado")
	EstModPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Estado", help_text = "Estado")

	def __unicode__(self):
		return u'%s - %s' %(self.IdPProy, self.NroPartPProy)

class CargaPresupuesto(models.Model):
	def urlExcel(self, filename):
		ruta = 'presup/%s' %(filename)
		return ruta
	doc_temp = models.FileField(upload_to = urlExcel, verbose_name = "Seleccionar Archivo", blank = True, null = True)

class CPProyectos(models.Model):
	IdCPProy = models.AutoField(primary_key = True)
	IdPProy = models.ForeignKey(PProyectos, blank = True, null = True, verbose_name = "Proyecto", help_text = "Proyecto")
	MesCPProy = models.IntegerField(blank = True, null = True, verbose_name = "Mes nro", help_text = "Mes nro")
	MesCCPProy = models.IntegerField(blank = True, null = True, verbose_name = "Mes correlativo", help_text = "Mes correlativo")
	AnioCCPProy = models.IntegerField(blank = True, null = True, verbose_name = "Año correlativo", help_text = "Año correlativo")
	MontoEjeCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Monto ejecutado", help_text = "Monto ejecutado")
	PorcEjeCProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Porcentaje", help_text = "Porcentaje")
	VerCProy = models.IntegerField(blank = True, null = True, verbose_name = "Versión", help_text = "Versión")
	SVerCProy = models.IntegerField(blank = True, null = True, verbose_name = "S. Versión", help_text = "S. Versión")
	EstCProy = models.BooleanField(default = True, verbose_name = 'Estado')
	EstModifCProy = models.CharField(max_length =2, blank = True, null= True, verbose_name="Estado modificación", help_text="Estado modificación")
	MontoEjeFipCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank= True, null = True, verbose_name="Monto ejecutado Fip")
	PorcEjeFipCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank= True, null = True, verbose_name = "Porc. ejecutado Fip")
	MontoEjeCliCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank= True, null = True, verbose_name = "Monto ejecutado UE")
	PorcEjeCliCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank= True, null = True, verbose_name = "Porc. ejecutado UE")
	MontoRealCPProy = models.DecimalField(max_digits =15, decimal_places = 2, blank= True, null = True, verbose_name = "Monto ejecutado Real")
	PorcRealCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank= True, null = True, verbose_name = "Porc. ejecutado Real")
	MontoRealFipCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank= True, null = True, verbose_name = "Monto ejecutado Real Fip")
	PorcRealFipCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank= True, null = True, verbose_name = "Porc. ejecutado Real Fip")
	MontoRealCliCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank= True, null = True, verbose_name = "Monto ejecutado Real UE")
	PorcRealCliCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank= True, null = True, verbose_name = "Porc. ejecutado Real UE")
	MontoDifEjecRealCPProy = models.DecimalField(max_digits = 15, decimal_places = 2, blank = True, null = True, verbose_name = "Dif Monto ejecutado Real")
	PorcDifEjecRealCPProy = models.DecimalField(max_digits = 6, decimal_places = 2, blank = True, null = True, verbose_name = "Dif Porc. ejecutado Real")
	EstVisCPProy = models.CharField(max_length = 2, blank = True, null = True, verbose_name = "Estado", help_text = "Estado")

	def __unicode__(self):
		return u'Proyecto:%s | Partida: %s | Mes: %s| MesC: %s | MontoFip: %s | MontoUE: %s |' %(self.IdPProy.IdPProy, self.IdPProy.NroPartPProy, self.MesCPProy, self.MesCCPProy, self.MontoRealFipCPProy, self.MontoRealCliCPProy  )



