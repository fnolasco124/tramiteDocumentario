# usr/local/bin/python
# -*- coding: utf-8 -*-
# Autor: Nolasco Bonilla, Francisco 
# Email: fnolasco124@gmail.com	

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from .forms  import *

from .models import *
from .decorators import access_permission

from django.views.generic import View, ListView, TemplateView, FormView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core import serializers

import datetime
import os
import django
import re
import decimal
from decimal import *
import json



class Login_View(TemplateView):
	def get(self, request, *args, **kwargs):
		return render_to_response('tramite/index.html',context_instance=RequestContext(request))
	
	def post(self,request, *args, **kwargs):
		username = request.POST['username']
		password = request.POST['password']
		usuario = authenticate(username=username,password=password)
		if (usuario is not None and usuario.is_active):
			login(request,usuario)
			if int(request.user.TipoUsuario) == 3:
				return HttpResponseRedirect('/uejecutora/cargar')
			else:
				return HttpResponseRedirect('/tramite/bandeja/')
		else:
			mensaje = "Sus datos son incorrectos o el usuario no esta activo"
			return render_to_response('tramite/index.html',{'mensaje':mensaje},context_instance=RequestContext(request))

class Logout_View(TemplateView):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect('/')

def enviar_correo(mensaje, mail_list, html_content):
        try:
        	asunto = "Recepcion de protocolo"
        	mensaje = mensaje
        	origen = "wffip@fondoitaloperuano.org"
        	msg = EmailMultiAlternatives(asunto, mensaje, origen, mail_list)
        	msg.attach_alternative(html_content,"text/html")
        	msg.send()
        except Exception, e:
        	import os
        	os.system('clear')
        	print e

def reportar_error(mensaje):
	correo = ['fnolasco124@gmail.com', 'fnolasco@fondoitaloperuano.org']
	html_content = mensaje
	enviar_correo('', correo, html_content)

class Personal_View(FormView):
	#template_name = 'tramite/frmPersonal.html'
	#form_class = MPersonalForm
	error = ""
	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request):
		lstTipoDoc = DTabla.objects.filter(IdMTab__IdMTabla='011')
		lstAreas = DTabla.objects.filter(IdMTab__IdMTabla='008')
		lstTipPersonal = DTabla.objects.filter(IdMTab__IdMTabla='022')
		ctx = {'lstTipoDoc':lstTipoDoc,'lstAreas':lstAreas,'lstTipPersonal':lstTipPersonal}
		return render_to_response('tramite/frmPersonal.html',ctx,context_instance=RequestContext(request))

	def generarCodigo(self):
		anio = datetime.date.today().strftime("%Y")
		if (MPersonal.objects.count()==0):
			anio = datetime.date.today().strftime("%Y")
			codigo = 'PE'+anio+'-00000001'

		else:
			obj = MPersonal.objects.last()
			cod = obj.IdMPer
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'PE'+ anio + '-' + codigo + str(num)
		return codigo
	
	def post(self, request, *args, **kwargs):
		form = MPersonalForm(request.POST) # A form bound to the POST data
		try:

			if form.is_valid():
				add = form.save(commit= False)
				add.EstMPer = 1
				add.IdMPer = self.generarCodigo()
				add.save()
				message= {'mensaje':'Personal registrado, los datos ingresados son correctos.'}
				return HttpResponse(json.dumps(message),mimetype='application/json')
			else:
				message= {'mensaje':'Los datos ingresados no son correctos!. Intente nuevamente.'}
				return HttpResponse(json.dumps(message),mimetype='application/json')
		except Exception, e:
			reportar_error(e)
			message = {'mensaje':e}
			return HttpResponse(json.dumps(message),mimetype='application/json')
	
class Cliente_View(FormView):
	template_name = 'tramite/form_cliente.html'
	form_class = MClienteForm
	error = ""
	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request, *args, **kwargs):
		lstPais = DTabla.objects.filter(IdMTab__IdMTabla='001')
		lstRegion = DTabla.objects.filter(IdMTab__IdMTabla='002')
		lstTipo = DTabla.objects.filter(IdMTab__IdMTabla = '015')
		#lstDepartamento = DTabla.objects.filter(idMTab__idMTabla='003')
		#lstProvincia = DTabla.objects.filter(idMTab__idMTabla='004')
		#lstDistrito = DTabla.objects.filter(idMTab__idMTabla='005')
		lista = MCliente.objects.all()
		ctx = {'lista':lista,'error':self.error,'lstPais':lstPais,'lstRegion':lstRegion,'lstTipo':lstTipo}
		return render_to_response('tramite/form_cliente.html',ctx,context_instance=RequestContext(request))

	def post(self, request, *args, **kwargs):
		try:
			obj = MCliente()
			if (MCliente.objects.count() == 0):
				obj.IdMCli = 'CL2014-00000001'
			else:
				obj.IdMCli = self.generarCodigo()
			
			obj.NomMCli = request.POST['nomMCli']
			obj.IdTipMCli = request.POST['idTipMCli']
			obj.IdTipInstMCli = request.POST['idTipInstMCli']
			obj.DirMCli = request.POST['dirMCli']		
			obj.IdPaisMCli = request.POST['idPaisMCli']
			obj.IdRegMCli = request.POST['idRegMCli']
			obj.IdDepMCli = request.POST['idDepMCli']
			obj.IdProvMCli = request.POST['idProvMCli']
			obj.IdDistMCli = request.POST['idDistMCli']
			obj.RefMCli = request.POST['refMCli']
			obj.Tel1MCli = request.POST['tel1MCli']
			obj.Tel2MCli = request.POST['tel2MCli']
			obj.Tel3MCli = request.POST['tel3MCli']
			obj.FechCreaMCli = timezone.now()
			obj.EstMCli = '1'
			obj.FecIngMCli = timezone.now()
			obj.Email1MCli = request.POST['emailMCli']
				#obj.idUsuCreaMCli = '1'
			obj.save()
				
			return HttpResponseRedirect('/administracion/unidadesejecutoras/')
		except Exception, e:
			reportar_error(e)
		return self.get(request)

	def generarCodigo(self):

		obj = MCliente.objects.last()
		cod = obj.IdMCli
		num = cod[7:]
		num = int(num)
		num = num + 1
		can = len(str(num))
		dif = 8-can
		codigo = ''
		codigo = '0'*dif
		
		codigo = 'CL2014'+ '-' + codigo + str(num)

		return codigo

class CreateProyecto_View(CreateView):
	template_name = 'tramite/form_convenio.html'
	form_class = MProyectoForm
	success_url = reverse_lazy('list-proyecto')

	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(CreateProyecto_View, self).get(request, *args, **kwargs)

	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if (self.request.POST['IdMCli'] != ''):
			form.instance.IdMCli = MCliente.objects.get(pk = self.request.POST['IdMCli'])

		#form.instance.IdMProy = self.generar_codigo()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateProyecto_View, self).get_context_data(**kwargs)
		listaUE = MCliente.objects.all()
		lstBancos = DTabla.objects.filter(IdMTab__IdMTabla='007')
		lstSector = DTabla.objects.filter(IdMTab__IdMTabla='010')
		context['listaUE'] = listaUE
		context['lstBancos'] = lstBancos
		context['lstSector'] = lstSector
		context['codigo_proyecto'] = self.generar_codigo()
		return context
	
	def form_valid(self, form):
		form.instance.IdMProy = self.generar_codigo()
		return super(CreateProyecto_View, self).form_valid(form)
	
	def generar_codigo(self):
		convenios = MProyecto.objects.filter(IdMProy__contains = '-2014-')
		if (len(convenios) == 0):
			codigo = 'CF-001-1-2014-FIP'
		else:
			codigo_ant = convenios[len(convenios)-1].IdMProy
			matriz = codigo_ant.split('-')
			correlativo = int(matriz[1])
			correlativo += 1
			can = 3 - len(str(correlativo))
			numero = '0' * can + str(correlativo)
			codigo = 'CF-' + str(numero) + '-1-2014-FIP'
		return codigo
	
class UpdateProyecto_View(UpdateView):
	template_name = 'tramite/form_convenio.html'
	model = MProyecto
	form_class = MProyectoForm
	success_url = reverse_lazy('list-proyecto')
	
	def get(self, request, **kwargs):
		codigo = kwargs['pk']
		self.object = MProyecto.objects.get(IdMProy = codigo)
		self.cod_cliente = self.object.IdMCli.IdMCli
		self.nom_cliente = self.object.IdMCli.NomMCli
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(object=self.object, form=form)

		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super(UpdateProyecto_View, self).get_context_data(**kwargs)
		context['cliente_nombre'] = self.nom_cliente
		context['cliente_codigo'] = self.cod_cliente
		return context
	
class PersonalListView(ListView):
	model = MPersonal
	queryset = MPersonal.objects.filter(EstMPer = True) # Para un queryset personalizado
	context_object_name = 'lista' # Sin este parametro se reciviria toda la lista como object_list
	template_name = 'tramite/lista_personal.html'
	paginate_by = 10

	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(PersonalListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(PersonalListView, self).get_context_data(**kwargs)
		context['frm'] = MPersonalForm()
		return context

	def post(self, request, *args, **kwargs):
		
		form = MPersonalForm(request.POST) # A form bound to the POST data
		try:

			if form.is_valid():
				add = form.save(commit= False)
				add.EstMPer = 1
				add.IdMPer = self.generarCodigo()
				add.save()
				last_personal = []
				last_personal.append(MPersonal.objects.last())
				data = serializers.serialize('json', last_personal)
				message= {'mensaje':'Personal registrado, los datos ingresados son correctos.','usuario':last_personal}
				return HttpResponse(data,mimetype='application/json')
			else:
				message= {'mensaje':'Los datos ingresados no son correctos!. Intente nuevamente.'}
				return HttpResponse(json.dumps(message),mimetype='application/json')
		except Exception, e:
			reportar_error(e)
			message = {'mensaje':e}
			return HttpResponse(json.dumps(message),mimetype='application/json')

	def generarCodigo(self):
		anio = datetime.date.today().strftime("%Y")
		if (MPersonal.objects.count()==0):
			anio = datetime.date.today().strftime("%Y")
			codigo = 'PE'+anio+'-00000001'

		else:
			obj = MPersonal.objects.last()
			cod = obj.IdMPer
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'PE'+ anio + '-' + codigo + str(num)
		return codigo

class ClienteListView(ListView):
	model = MCliente
	context_object_name = 'lista'
	template_name = 'tramite/lista_unidad_ejecutora.html'
	paginate_by = 10

	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request,*args, **kwargs):
		return super(ClienteListView, self).get(request, *args, **kwargs)
		"""
		lista = MCliente.objects.all()
		ctx = {'lista':lista,}
		return render_to_response('tramite/lista_unidad_ejecutora.html',ctx, context_instance=RequestContext(request))
		"""

class UsuarioListView(ListView):
	model = User
	context_object_name = 'lista'
	queryset = User.objects.filter(is_active = True).order_by('-pk')
	template_name = 'tramite/lista_usuario.html'
	paginate_by = 10

	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(UsuarioListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UsuarioListView, self).get_context_data(**kwargs)
		context['form'] = UsuarioForm()
		context['personal'] = MPersonal.objects.all().order_by('ApePMPer')
		context['clientes'] = MCliente.objects.all().order_by('NomMCli')
		return context

	def post(self, request, *args, **kwargs):
		form = UsuarioForm(request.POST) # A form bound to the POST data
		try:
			if form.is_valid():
				add = form.save(commit=False)
				add.set_password(add.password)
				add.idMPer = request.POST['idMPer']
				add.idMCli = request.POST['idMCli']
				o_per = MPersonal.objects.get(IdMPer = add.idMPer)
				add.last_name = '%s %s' %(o_per.ApePMPer, o_per.ApeMMPer)
				add.first_name = o_per.NomMPer
				add.email = o_per.Email1MPer
				add.save()
				last_user = User.objects.last()
				message= {'username':last_user.username,'last_name':last_user.last_name, 'first_name':last_user.first_name, 'tipoUsuario':last_user.tipoUsuario, 'fecIngreso':str(last_user.fecIngreso),'id':last_user.pk}
				return HttpResponse(json.dumps(message),mimetype='application/json')	
			else:
				message= {'mensaje':'Los datos ingresados no son correctos!. Intente nuevamente.'}
				return HttpResponse(json.dumps(message),mimetype='application/json')
		except Exception, e:
			reportar_error(e)
			message = {'mensaje':e}
			return HttpResponse(json.dumps(message),mimetype='application/json')

class ProyectoListView(ListView):
	model = MProyecto
	queryset = MProyecto.objects.filter(EstMProy = '1').order_by('-IdConv','-FecIngMProy')
	context_object_name = 'lista'
	template_name = 'tramite/lista_convenio.html'
	paginate_by = 15

	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(ProyectoListView, self).get(request, *args, **kwargs)

class MTablaListView(ListView):
	model = MTabla
	context_object_name = 'lista'
	template_name = 'tramite/tablas_maestro.html'
	paginate_by = 15

	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(MTablaListView, self).get(request, *args, **kwargs)

	def get_queryset(self):
		queryset = MTabla.objects.filter(EstMTabla = True)
		return queryset

class ListaDTabla_View(TemplateView):
	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request,*args, **kwargs):
		pr = DTabla()
		lista = DTabla.objects.all()
		
		cabecera = pr.get_nombreCampos()
		ctx = {'lista':lista, 'listFields':cabecera,'nomTabla':'Tablas del sistema (detalle)'}
		return render_to_response('tramite/lstDTabla.html',ctx, context_instance=RequestContext(request))

class Tabla_View(FormView):
	template_name = 'tramite/frmTabla.html'
	form_class = MTablaForm
	error = ""
	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request,*error):
		return render_to_response('tramite/frmTabla.html',context_instance=RequestContext(request))

	def post(self, request, *args, **kwargs):
		try:
			obj = MTabla()


			obj.IdMTabla = request.POST['idMTab']
			obj.NomMTabla = request.POST['nomMTab']
			obj.AbrMTabla = request.POST['abrMTab']
			obj.PropMTabla = request.POST['propMTab']
			obj.EstMTabla = request.POST['estMTab']
			obj.save()
			return HttpResponseRedirect('/sistema/listaTablas/')
		except Exception, e:
			reportar_error(e)
			error = e
		return self.get(request)

class DTabla_View(FormView):
	template_name = 'tramite/frmDTabla.html'
	form_class = DTablaForm
	error = ""
	@method_decorator(access_permission([0,]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request,*error):
		lista = DTabla.objects.all()
		cod = '5'
		return render_to_response('tramite/frmDTabla.html',{'lista':lista,'cod':cod},context_instance=RequestContext(request))

	def post(self, request, *args, **kwargs):
		#try:
			obj = DTabla()


			obj.IdMTabla = MTabla.objects.get(pk=request.POST['idMTabla'])
			obj.IdDTabla = '000'
			obj.NomDTabla = request.POST['nomDTabla']
			obj.AbrDTabla = request.POST['abrDTabla']
			obj.AbrOptDTabla = obj.abrDTabla
			obj.PropDTabla = request.POST['propDTabla']
			obj.IdRefDTabla = request.POST['idRefDTabla']

			obj.save()
			
			return HttpResponseRedirect('/tramite/listaDTablas/')
		#except Exception, e:
		#	reportar_error(e)
		#	error = e
			
		#return self.get(request)

class CreateModificatoria(CreateView):
	template_name = 'tramite/modificatoria_convenio.html'
	form_class = DProyectoForm
	
	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		self.codigo = kwargs['proyecto']
		return super(CreateModificatoria, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.codigo = self.request.POST['codigo_proyecto']
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('create-modificatoria', kwargs = {'proyecto': self.codigo})

	def get_context_data(self, **kwargs):
		context = super(CreateModificatoria, self).get_context_data(**kwargs)
		context['instance'] = MProyecto.objects.get(IdMProy = self.codigo)
		context['tipo_adendas'] = DTabla.objects.filter(IdMTab__IdMTabla="021")
		context['adendas'] = DProyecto.objects.filter(IdMProy__IdMProy = self.codigo)
		return context
	
	def form_valid(self, form):
		form.instance.IdDProy = self.generar_codigo()
		form.instance.IdMProy = MProyecto.objects.get(IdMProy = self.codigo)
		form.instance.IdTipDocDProy = self.request.POST['IdTipDocDProy']
		return super(CreateModificatoria, self).form_valid(form)

	def generar_codigo(self):
		anio = datetime.date.today().strftime("%Y")
		if (DProyecto.objects.count()==0):
			anio = datetime.date.today().strftime("%Y")
			codigo = 'MC'+anio+'-00000001'
		else:
			obj = DProyecto.objects.last()
			cod = obj.IdDProy
			num = int(cod[7:]) + 1
			can = len(str(num))
			dif = 8-can
			codigo = 'MC'+ anio + '-' + ('0'*dif) + str(num)
		return codigo

class CreateColaborador(CreateView):
	template_name = 'tramite/colaborador_convenio.html'
	form_class = MColaboradorForm

	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		self.codigo = kwargs['proyecto']
		return super(CreateColaborador, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CreateColaborador, self).get_context_data(**kwargs)
		context['instance'] = MProyecto.objects.get(IdMProy = self.codigo)
		context['personal'] = MPersonal.objects.filter(EstMPer = True)
		context['colaboradores'] = MColaborador.objects.filter(IdMProy__IdMProy = self.codigo, EstMCol = True)
		return context

	def get_success_url(self):
		return reverse('create-colaborador', kwargs = {'proyecto': self.codigo})

	def post(self, request, *args, **kwargs):
		self.codigo = self.request.POST['codigo_proyecto']
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		form.instance.IdMPer = MPersonal.objects.get(IdMPer = self.request.POST['colaborador_convenio'])
		form.instance.IdMProy = MProyecto.objects.get(IdMProy = self.request.POST['codigo_proyecto'])
		form.instance.IdTipoCargoProy = self.request.POST['cargo']
		if (self.request.POST['externo'] == "0"):
			form.instance.FecIniMCol = None
			form.instance.FecFinMCol = None

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

class BandejaListView(ListView):
	model = Bandeja
	context_object_name = 'lista' # Sin este parametro se reciviria toda la lista como object_list
	template_name = 'tramite/bandeja_protocolo.html'
	paginate_by = 9

	@method_decorator(access_permission([0,1,2]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(BandejaListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(BandejaListView, self).get_context_data(**kwargs)
		#context['g_doc_tecnicos'] = DTabla.objects.filter(IdMTab = '023', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		context['g_doc_admin'] = DTabla.objects.filter(IdMTab = '024', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		context['g_area_tecnica'] = DTabla.objects.filter(IdMTab = '025', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		#context['g_area_financiera'] = DTabla.objects.filter(IdMTab = '026', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		#context['g_tesoreria'] = DTabla.objects.filter(IdMTab = '027', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		context['g_usuarios'] = DTabla.objects.filter(IdMTab = '028', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		#context['g_alegal'] = DTabla.objects.filter(IdMTab = '029', EstDTab = True, IdMTab__EstMTabla = True).order_by('NomDTab')
		return context
	
	def get_queryset(self):
		queryset = Bandeja.objects.filter(IdMUsuRec = self.request.user.pk, EstBProt = True).order_by('-IdBandeja')
		return queryset

	def post(self,request,*args,**kwargs):
		send_to = request.POST['txtDestino']
		registers = request.POST['txtProtocolo']
		mensaje = request.POST['txtMensaje']
		
		#send_by = request.user.pk
		#send_by_name = request.user.username
		#envx = request.user.username
		
		list_prot = registers.split(',')
		list_destiny = send_to.split(',')
		users = User.objects.filter(username__in = list_destiny)
		list_destiny = [u.pk for u in users]
		obs_state = request.POST['protObservado']

		#self.registrar_protocolo(list_destiny, list_prot, mensaje, send_by, send_by_name, obs_state)
		self.registrar_protocolo(list_destiny, list_prot, mensaje, obs_state)
			
		return HttpResponseRedirect('/tramite/bandeja/')

	def observado(self, cod):
		obj = Bandeja.objects.get(idBandeja=cod)
		if (obj.EstObservado == '1'):
			return 'Se encuentra observado'
		else:
			return 'No esta observado'

	def registrar_protocolo(self, send_to, registers, mensaje, obs_state = '0'):
		list_user = User.objects.filter(pk__in = send_to)
		list_regs = Bandeja.objects.filter(pk__in = registers)
		#user_id = send_by
		#user_name = send_by_name
		band_cierre = False
		nuevos_registros = []
		
		if (obs_state == "1"):
			html_content = '<div style = "background-color:#333333; height: 100%; width: 100%;"><p style = "color:#ff0000;">Protocolo observado</p><br><center>'
		else:
			html_content = '<div style = "background-color:#333333; height: 100%; width: 100%;"><center>'
		
		for reg in list_regs:
			new_reg = Bandeja()
			new_reg.MenBProt = mensaje
			new_reg.IdMUsuEnv = self.request.user
			new_reg.IdMProt = reg.IdMProt
			#new_reg.CliBProt = reg.CliBProt
			#new_reg.ProyBProt = reg.ProyBProt
			new_reg.IdProtRef = reg.IdProtRef
			new_reg.FecEnv = timezone.now()
			new_reg.FecRec = timezone.now()
			new_reg.FecSist = timezone.now()
			#new_reg.EstBProt = '1' #Estado del BProt, cuando es 1 está activo, si es 0 esta eliminado logicamente
			new_reg.EstAccion = '0' #Cambia de valor a 1 cuando el protocolo esta enviado
			new_reg.EstObservado = obs_state #Cambia de valor a 1 cuando el protocolo esta observado
			#new_reg.NomMUsuEnv = send_by_name
			if new_reg.IdMProt.IdMProy:
				proyecto = new_reg.IdMProt.IdMProy.NomMProy + ' - ' + new_reg.IdMProt.IdMProy.NomMProy
				cliente = new_reg.IdMProt.IdMProy.IdMCli.NomMCli
			else:
				proyecto = new_reg.IdMProt.EmpMProt
				cliente = new_reg.IdMProt.RespMProt

			nuevos_registros.append(new_reg)
			
			data_reg = {'cod_prot': new_reg.IdMProt.IdMProt, 'nom_proy': proyecto, 'nom_ue': cliente,\
							'asunto': new_reg.IdMProt.DescMProt, 'mensaje': mensaje}

			reg.EstAccion = '1'
			reg.save()
			if list_user[0].username == 'CIERRE':
				band_cierre = True
			
			html_content += """<br><br><br><div>\
					<table style = "border 1px solid: #000; width:800px; background-color:#f2f2f2; border-collapse: collapse;">\
					<thead><tr>\
					<th colspan = "2">Datos del Protocolo</th></tr></thead>\
					<tbody>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>Protocolo Nro</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + data_reg['cod_prot'] + """</td></tr>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>Convenio</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + data_reg['nom_proy'] + """</td></tr>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>U.E.</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + data_reg['nom_ue'] + """</td></tr>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>Asunto</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + data_reg['asunto'] + """</td></tr>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>Mensaje</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + data_reg['mensaje'] + """</td></tr>\
					<tr><td style = "width:150px; color: #2c3f50;"><strong>Enviado por</strong></td>\
					<td style = "width:650px; color: #484848;">: """ + str(self.request.user.username) + """</td></tr></tbody></table>"""

		html_content += '</center></div>'

		for us in list_user:
			for r in nuevos_registros:
				new_cod = int((((Bandeja.objects.last()).pk).split('-'))[1]) + 1
				new_cod = "BD2014-" + ((8-len(str(new_cod)))*'0') + str(new_cod)
				r.IdBandeja = new_cod
				r.IdMUsuRec = us
				#r.NomMUsuRec = us.username
				r.save()

		enviar_correo("Mensaje Adjunto", [u.email for u in list_user], html_content)

		if band_cierre:
			registros = Bandeja.objects.filter(IdMProt__in = [reg.IdMProt for reg in list_regs])
			for r in registros:
				r.finalizar()

class Enviados_View(ListView):
	def get(self,request,*args,**kwargs):
		pr = Bandeja()
		usuario = request.user.pk
		lista = Bandeja.objects.filter(idMUsuREc=usuario, estAccion='1')
		listaUsuario = User.objects.all()
		cabecera = pr.get_nombreCampos()
		ctx = {'lista':lista, 'listFields':cabecera,'nomTabla':'Protocolos Enviados', 'listaUsuario':listaUsuario}
		return render_to_response('tramite/lstEnviados.html',ctx, context_instance=RequestContext(request))
	def post(self,request,*args,**kwargs):
		
		for d in destino:
			for p in protocolo:
				prot = Bandeja.objects.get(pk=p)
				protocolo = prot.IdMProt
				clie = MCliente.objects.get(pk=prot.IdMCli)
				cliente = clie.NomMCli
				proy = MProyecto.objects.get(pk=prot.IdMProy)
				referencia = prot.EdRefMProt
				proyecto = proy.NomMProy
				regProtocoloEnBandeja(protocolo,enviadoPor,d,usuario,cliente,referencia, proyecto,observacion,mensaje)

		
		return self.get(request)		

class CreateProtocolo_View(CreateView):
	template_name = 'tramite/form_protocolo.html'
	form_class = MProtocoloForm
	#success_url = reverse_lazy('detalle-protocolo')

	@method_decorator(access_permission([0,1,2]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		return super(CreateProtocolo_View, self).get(request, *args, **kwargs)

	
	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		form.instance.DocInter = self.request.POST['procedencia_documento']
		
		if self.request.POST['codigo_proyecto']:
			form.instance.IdMProy = MProyecto.objects.get(IdMProy = self.request.POST['codigo_proyecto'])
		anio = str(datetime.date.today().strftime("%Y"))
		
		if(int(self.request.POST['procedencia_documento']) == 8299):
			form.instance.IdMProt = self.generarCodigoFS(anio)
		else:
			form.instance.IdMProt = self.generarCodigoPR(anio)
		self.codigo_protocolo = form.instance.IdMProt
		form
		form.instance.FecEntRealMProt = self.request.POST['FecEntMProt']
		form.instance.IdTipFormEntMProt = self.request.POST['formato_entrega']
		form.instance.IdRefMProt = self.request.POST['referencia_protocolo']
		form.instance.IdTipDocGen = self.request.POST['documento_generado']
		
		responsable = self.request.POST['RespMProt']
		empresa = self.request.POST['EmpMProt']
		

		if empresa.lstrip() != "" :
			iempresa = DTabla.objects.filter(NomDTab = empresa.lstrip(), IdMTab__IdMTabla = '034')
			if len(iempresa) == 0:
				instance = DTabla()
				instance.NomDTab = empresa.upper()
				instance.IdMTab = MTabla.objects.get(IdMTabla = '034')
				instance.FactDTab = '0'
				instance.IndDTab = '0'
				instance.PropDTab = '1'
				instance.save()

		if responsable.lstrip() != "" :
			iresponsable = DTabla.objects.filter(NomDTab = responsable.lstrip(), IdMTab__IdMTabla = '035')
			if len(iresponsable) == 0:
				instance = DTabla()
				instance.NomDTab = responsable.upper()
				instance.IdMTab = MTabla.objects.get(IdMTabla = '035')
				instance.FactDTab = '0'
				instance.IndDTab = '0'
				instance.PropDTab = '1'
				instance.save()

		if form.is_valid():
			self.registrar_protocolo_bandeja(form.instance.IdRefMProt)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(CreateProtocolo_View, self).get_context_data(**kwargs)
		documento_generado = DTabla.objects.filter(IdMTab__IdMTabla='012')
		lista_protocolo = MProtocolo.objects.filter(EstMProt = True)
		tipo_documento = DTabla.objects.filter(IdMTab__IdMTabla = '031')
		formato_documento = DTabla.objects.filter(IdMTab__IdMTabla = '033')
		fecha_actual = datetime.datetime.today()
		context['lista_proyecto'] = MProyecto.objects.all()
		context['lista_protocolo'] = lista_protocolo
		context['documento_generado'] = documento_generado
		context['fecha_actual'] = fecha_actual
		context['tipo_documento'] = tipo_documento
		context['formato_documento'] = formato_documento
		return context

	def get_success_url(self):
		return reverse('detalle-protocolo', kwargs={'idpr': self.codigo_protocolo})
					
	def generarCodigoPR(self, convo):
		listaPR = MProtocolo.objects.filter(IdMProt__contains = 'PR')
		if (len(listaPR) == 0):
			codigo = 'PR2014-00000001'
		else:
			obj = MProtocolo.objects.filter(IdMProt__contains = 'PR').order_by('-IdMProt')[0]
			cod = obj.IdMProt
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			convocatoria = convo.split()
			codigo = 'PR'+ convocatoria[0] + '-' + codigo + str(num)
		return codigo

	def generarCodigoFS(self, convo):
		listaFS = MProtocolo.objects.filter(IdMProt__contains = 'FS')
		if (len(listaFS) == 0):
			codigo = 'FS2014-00000001'
		else:
			obj = MProtocolo.objects.filter(IdMProt__contains = 'FS').order_by('-IdMProt')[0]
			cod = obj.IdMProt
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			convocatoria = convo.split()
			codigo = 'FS'+ convocatoria[0] + '-' + codigo + str(num)
		return codigo

	def registrar_protocolo_bandeja(self, referencia):
		bd = Bandeja()
		codigo = ''
		if Bandeja.objects.count() > 0:
			band = Bandeja.objects.last()
			cod = band.IdBandeja
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'BD'+ '2014' + '-' + codigo + str(num)

		else:
			codigo = 'BD2014-00000001'
		
		bd.IdBandeja = codigo
		bd.IdMUsuEnv = User.objects.get(pk = self.request.user.id)
		bd.IdMUsuRec = User.objects.get(pk = self.request.user.id)
		bd.FecEnv = timezone.now()
		bd.FecRec = timezone.now()
		bd.FecSist = timezone.now()
		bd.EstBProt = True #Estado del BProt, cuando es 1 está activo, si es 0 esta eliminado logicamente
		bd.EstAccion = '0' #Cambia de valor a 1 cuando el protocolo esta enviado
		bd.EstObservado = '0' #Cambia de valor a 1 cuando el protocolo esta observado
		if referencia:
			bd.IdProtRef = referencia
		bd.save()

class LocalizarProtocolo_View(ListView):
	@method_decorator(access_permission([0,1,2]))
	@method_decorator(login_required(login_url='/'))
	def get(self,request):
		fecha_actual = datetime.datetime.today()
		ctx = {'fecha_actual': fecha_actual}
		return render_to_response('tramite/frm_localizar.html', ctx, context_instance=RequestContext(request))
	
class LocalizarProtocoloAjax_View(TemplateView):
	@method_decorator(access_permission([0,1,2]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request):
		from django.db.models import Q
		valores = (request.GET['valores']).split(",")
		valores = [v.lstrip() for v in valores]
		campos = (request.GET['nombres']).split(",")
		
		dic_prop = {
					'codigo': 'IdMProt__icontains =',
					'cliente': 'IdMProy__IdMCli__NomMCli__icontains =',
					'referencia': 'IdRefMProt__icontains = ',
					'proyecto': 'IdMProy__NomMProy__icontains =',
					'empresa': 'EmpMProt__icontains =',
					'responsable': 'RespMProt__icontains =',
					'cproyecto': 'IdMProy__IdCFMProy__icontains =',
					'descripcion': 'DescMProt__icontains ='

					}
		filtro = []
		for i in range(len(campos)):
			try:
				filtro.append('Q('+ (dic_prop[campos[i]] + '"' + valores[i]+ '")'))
			except KeyError as ke:
				pass

		str_eval = "MProtocolo.objects.filter("+ " | ".join(filtro) + ")"
		lista_filtro = eval(str_eval)
		data = serializers.serialize('json', lista_filtro, use_natural_keys = True)
		return HttpResponse(data, mimetype = 'application/json')

class Observados_View(ListView):
	@method_decorator(login_required(login_url='/'))
	def get(self,request,*args,**kwargs):
		pr = Bandeja()
		usuario = request.user.pk
		
		lista = Bandeja.objects.filter(IdMUsuREc = usuario, EstAccion = '0', EstObservado = '1' ).order_by('-IdMProt')
		listaUsuario = User.objects.all()
		
		cabecera = pr.get_nombreCampos()
		ctx = {'lista':lista, 'listFields':cabecera,'nomTabla':'Protocolos Observados'}
		return render_to_response('tramite/bandejaProt.html', ctx, context_instance = RequestContext(request))

class BusquedaAjax_View(TemplateView):
	
	def get(self,request,*args,**kwargs):
		
		protocolo = request.GET['protocolo']
		
		try:
			lista = Bandeja.objects.filter(IdMProt__contains=protocolo, EstAccion='0').order_by('-IdBandeja')
			data = serializers.serialize('json', lista)		
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class ObservarProtocoloAjax_View(TemplateView):

	def get(self,request,*args,**kwargs):
		protocolo = request.GET['protocolo']
		lstCod = obtenerNumeros(protocolo)
				
		try:
			for cod in lstCod:
				lstobj = Bandeja.objects.filter()
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class CreateDetalleProtocolo_View(CreateView):
	template_name = 'tramite/detalle_protocolo.html'
	form_class = DProtocoloForm
	
	@method_decorator(access_permission([0,1]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		self.codigo = kwargs['idpr']
		print self.codigo
		return super(CreateDetalleProtocolo_View, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CreateDetalleProtocolo_View, self).get_context_data(**kwargs)
		obj = MProtocolo.objects.get(IdMProt = self.codigo)
		context['codigo_protocolo'] = obj.IdMProt
		if obj.IdMProy:
			context['nombre_proyecto'] = obj.IdMProy.NomMProy
			context['cliente_proyecto'] = obj.IdMProy.IdMCli.NomMCli
		context['lista_detalle'] = DProtocolo.objects.filter(IdMProt__IdMProt = self.codigo)
		context['usuarios_archivo'] = MPersonal.objects.filter(IdArea__in = [dp.id for dp in DTabla.objects.filter(IdMTab__IdMTabla = '008', NomDTab = 'ARCHIVO')])
		context['formatos'] = DTabla.objects.filter(IdMTab__IdMTabla = '013')
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		self.codigo_protocolo = self.request.POST['codigo_protocolo']
		form.instance.IdDProt = self.generar_codigo()
		form.instance.IdMProt = MProtocolo.objects.get(IdMProt = self.request.POST['codigo_protocolo'])
		form.instance.UbLogDProt = self.request.user.id
		form.instance.UbiFisDProt = self.request.POST['ubicacion_detalle']
		form.instance.IdTipDocDProt = self.request.POST['formato_detalle']

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('detalle-protocolo', kwargs={'idpr': self.codigo_protocolo})

	def generar_codigo(self):
		anio = datetime.date.today().strftime("%Y")

		if (DProtocolo.objects.count() == 0):
			anio = datetime.date.today().strftime("%Y")
			codigo = 'DP'+anio+'-00000001'

		else:
			obj = DProtocolo.objects.last()
			cod = obj.IdDProt
			num = cod[7:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'DP'+ anio + '-' + codigo + str(num)
		return codigo

class ConveniosSupervisor_View(TemplateView):
	@method_decorator(access_permission([0,2]))
	def get(self, request, *args, **kwargs):
		IdMPer = request.user.idMPer
		lista_proyectos = MColaborador.objects.filter(IdMPer__IdMPer = IdMPer)
		lista = []
		for item in lista_proyectos:
			lista.append(item.IdMProy)
		ctx = {'lista':lista}
		return render_to_response('tramite/supervision_convenio.html',ctx, context_instance=RequestContext(request))

class CargarPresupuesto_View(TemplateView):
	@method_decorator(access_permission([0,3]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		id_tipoUsuario = request.user.tipoUsuario
		
		if int(id_tipoUsuario) != 3:
			msj = 'Ud no puede cargar presupuestos.'
			ctx = {'mensaje':msj}
		else:
			id_cliente = request.user.idMCli
			proy = MProyecto.objects.filter(IdMCli__IdMCli= id_cliente).order_by('-IdConv')
			if len(proy) > 0 :
				proy = proy[0]			
				lista_p = PProyectos.objects.filter(IdMProy__IdMProy = proy.IdMProy)
				if len(lista_p) > 0:
					msj = 'Ya existe un presupuesto, si desea cargar un nuevo presupuesto contacte al supervisor asignado.'
					ctx = {'mensaje':msj}
				else:
					form = CargaForm()
					ctx = {'form': form}
			else:
				msj = 'No existe ningun convenio registrado con esta Unidad Ejecutora.'
				ctx = {'mensaje':msj}

		return render_to_response('tramite/form_presupuesto.html', ctx,context_instance=RequestContext(request))
		
	def post(self, request, *args, **kwargs):
		from .proceso import Presupuesto
		msj = ""
		filename = ""
		n_meses = 0
		try:
			
			form = CargaForm(request.POST,request.FILES) # A form bound to the POST data
			if form.is_valid():
				add = form.save(commit=False)
				add.save()
				msj = 'El archivo fue subido con exito'
			else:
				msj = 'El formulario no es valido'
		
		except Exception, e:
			pass	
			
		
		errores = []
		datos = []
		query = Presupuesto()
		filename = CargaPresupuesto.objects.last()
		filename = str(filename.doc_temp)
		filename = filename.split('/')
		filename = filename[-1]

		hasname = query.inicio(filename)
		le = []
		ld = []
		if hasname:
			resultado = query.procesar_pres()
			cant_meses = int(query.duracion_proyecto())
			filas_resultados = query.get_lista_fni
			lista_resultados = query.get_lista_resultados
			valido = resultado[0]
			datos = resultado[1]
			errores = resultado[2]
			self.guardar_presupuesto(request, filas_resultados,lista_resultados,datos)
		if len(errores)>2:
			le = errores[:-2]
		elif len(errores)<3:
			ld = datos
			
		n_meses = 5
		rango = range(1,cant_meses+1)
		ctx = {'msj':msj,'errores':le,'n_meses':n_meses,'datos':datos,'lista_resul':lista_resultados,'rango':rango}
		return render_to_response('tramite/form_presupuesto.html', ctx,context_instance=RequestContext(request))

	def guardar_presupuesto(self,request, fni, desc_fni, datoPres):
	
		id_cliente = request.user.idMCli
		proy = MProyecto.objects.filter(IdMCli__IdMCli= id_cliente, EstMProy = 1).order_by('-IdConv')
		proy = proy[0]
		FECHA = datetime.datetime.today()
		index = 1
		for p in datoPres:
			
			pres = PProyectos()
			cod_pres = self.generar_Codigo()
			pres.IdPProy = cod_pres
			
			
			pres.IdMProy = proy
			pres.NroPartPProy = p['partida']
			pres.IdNivPartPProy = p['nivel']
			pres.TitPProy = p['tit']
			pres.DescPProy = p['desc']
			pres.NroPartPerProy = self.pertenece_a(p['partida'])
			pres.IdUnidMed = p['um']
			try:
				pres.CantPProy = int(p['cant'])	
			except ValueError as ve:
				pres.CantPProy = 0.0
			except Exception, e:
				pres.CantPProy = 0.0
			try:
				pres.CostUnitPProy = float(p['cu'])
			except Exception, e:
				pres.CostUnitPProy = 0.0
			try:
				pres.CostTotPProy = float(p['ct'])
			except Exception, e:
				pres.CostTotPProy = 0.0
			try:
				pres.FFFipPProy = float(p['ifip'])
			except Exception, e:
				pres.FFFipPProy = 0.0
			try:
				pres.FFCliPProy = float(p['iue'])
			except Exception, e:
				pres.FFCliPProy = 0.0
			try:
				pres.FFOtrosPProy = float(p['iotros'])
			except Exception, e:
				pres.FFOtrosPProy = 0.0
			try:
				ct =  float(p['ct'])
			except ValueError as ve:
				ct = 0.0
			try:
				ifip =  float(p['ifip'])
				pres.PFFFipPProy = (ifip * 100)/ct
			except ValueError as ve:
				ifip = 0.0
			except ZeroDivisionError as dz:
				pres.PFFFipPProy = 0
			try:
				iue =  float(p['iue'])
				pres.PFFCliPProy = (iue * 100)/ct
			except ValueError as ve:
				iue = 0.0
			except ZeroDivisionError as dz:
				pres.PFFCliPProy = 0.0
			try:
				iotros =  float(p['iotros'])
				pres.PFFOtrosPProy = (iotros * 100)/ct
			except ValueError as ve:
				iotros = 0.0
			except ZeroDivisionError as dz:
				pres.PFFOtrosPProy = 0.0

			pres.FinPProy = '0'
			pres.VerPProy = '0'
			pres.EstPProy = '1'
			pres.FecIngPProy = FECHA.strftime('%Y-%m-%d')
			
			pres.IdUsuCreaPProy = request.user.id
			
			pres.IdUsuModPProy = ''
			pres.CostEjePProy = 0.0
			pres.CostSalPProy = 0.0
			pres.IdMotCierrePProy = '0'
			pres.PorCostEjePProy = 0.0
			pres.BorradorPProy = '1'
			pres.EstPresPProy = '0'
			pres.EstEvalPProy = '0'
			pres.EstValidPProy = '0'
			pres.EstAprobPProy = '0'
			pres.EstModifPProy = '0'
			
			mes = proy.FecIniRealMProy 
			anio = mes.strftime('%Y')
			anio = int(anio)
			mes_ini = mes.strftime('%m')
			mes_ini = int(mes_ini)
			mes_c = 1
			
			pres.save()
			index = index + 1
			i=1
			x=0
			for m in p['cant_meses']:

				cpp = CPProyectos()
				cpp.IdPProy = pres
				cpp.MesCPProy = mes_c
				cpp.MesCCPProy = mes_ini
				cpp.AnioCCPProy = anio
				cpp.MontoEjecCPProy = 0
				cpp.PorcEjecCPProy = 0
				cpp.VerCPProy = 0
				cpp.SVerCPProy = 0
				cpp.EstCPProy = 1
				cpp.EstModifCPProy = 0
				cpp.MontoEjeFipCPProy = 0
				cpp.PorcEjeFipCPProy = 0
				cpp.MontoEjeCliCPProy = 0
				cpp.PorcEjeCliCPProy = 0
				cpp.MontoRealCPProy = 0
				cpp.PorcRealCPProy = 0
				if (x%2 == 0):
					cpp.MontoRealFipCPProy = m
					cpp.PorcRealFipCPProy = 0
					cpp.MontoRealCliCPProy = 0
					cpp.PorcRealCliCPProy = 0
				else :
					cpp.MontoRealFipCPProy = 0
					cpp.PorcRealFipCPProy = 0
					cpp.MontoRealCliCPProy = m
					cpp.PorcRealCliCPProy = 0

				cpp.MontoDifEjecRealCPProy = 0
				cpp.PorcDifEjecRealCPProy = 0
				cpp.EstVisCPProy = 0
				if (mes_ini == 12):
					mes_ini = 1
				if (i %2 == 0):
					mes_ini += 1
					mes_c += 1

				cpp.save()
				i += 1
				x += 1

	def pertenece_a(self, partida):
		val_part = partida.split(',')
		if (len(val_part) == 1):
			return partida
		else:
			val_part = val_part[:-1]
			pertence = '.'.join(val_part)
			return pertence

	def generar_Codigo(self):
		if (PProyectos.objects.count() == 0):
			codigo = 'PRES2014-00000001'
		else:
			anio = datetime.datetime.today().year
			anio = str(anio)
			obj = PProyectos.objects.last()
			cod = obj.IdPProy
			num = cod[-8:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'PRES'+anio+ '-' + codigo + str(num)
		return codigo

class ObservarAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		protocolo = request.GET['protocolo']
		usuario = request.GET['usuario']
		
		lstObservado = Bandeja.objects.filter(IdMProt=protocolo, IdMUsuEnv =usuario, EstAccion='0')
		for obj in lstObservado:
			obj.EstObservado = '1'
			obj.save()


		objBand = lstObservado[0]
		objBand.EstAccion = "0"
		codUsuarioEnvio = request.user.pk
		codUsuarioRecepcion = usuario
		nomUsuario = request.user.username
		observacion = ""
		mensaje = "El protocolo ha sido observado"
		
		regProtocoloEnBandeja(obj, codUsuarioEnvio, codUsuarioRecepcion,nomUsuario,observacion,mensaje)

		lista = Bandeja.objects.filter(IdMProt=protocolo, IdMUsuEnv =usuario, EstAccion='1')
		bd = Bandeja()

		data = serializers.serialize('json', lista)		
			
		
		return HttpResponse(data, mimetype='application/json')

class MaestroProtocoloAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		protocolo = request.GET['protocolo']
		
		try:
			lista = MProtocolo.objects.filter(IdMProt=protocolo)[:1]
			
			data = serializers.serialize('json', lista)
			
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class DatosConvenioAjax(TemplateView):
	def get(self, *args, **kwargs):
		self.codigo = self.request.GET['codigo']
		datos_convenio = self.datos_convenio()
		datos_colaboradores = self.datos_colaboradores()
		datos_adendas = self.datos_adendas()
		message = {'convenio': datos_convenio, 'colaboradores': datos_colaboradores, 'adendas': datos_adendas}
		return HttpResponse(json.dumps(message), mimetype = 'application/json')
		
	def datos_convenio(self, *args, **kwargs):
		try:
			instance = MProyecto.objects.get(IdMProy = self.codigo)
			pdf_perfil, ruta_perfil = "No registrado", "#"
			pdf_convenio, ruta_convenio = "No registrado", "#"
			pdf_ac, ruta_ac = "No registrado", "#"

			if instance.RutaPDFMProy:
				pdf_perfil, ruta_perfil = str(instance.RutaPDFMProy)[11:], "/media/" + str(instance.RutaPDFMProy)
			if instance.RutaPDFConvMProy:
				pdf_convenio, ruta_convenio = str(instance.RutaPDFConvMProy)[11:],  "/media/" + str(instance.RutaPDFConvMProy)
			if instance.RutaPDFACMProy:
				pdf_ac, ruta_ac = str(instance.RutaPDFACMProy)[11:],  "/media/" + str(instance.RutaPDFACMProy)

			html = """<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">N de Convenio </label>\
						<label class="col-lg-8 control-label">: """+ instance.IdCFMProy +"""</label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Convocatoria</label>\
						<label class="col-lg-8 control-label">: """+ instance.IdConv +"""</label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Unidad Ejecutora</label>\
						<label class="col-lg-8 control-label">: """+ instance.IdMCli.NomMCli +"""</label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Nombre del Proyecto</label>\
						<label class="col-lg-8 control-label">: """+ instance.NomMProy +"""</label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">CCI</label>\
						<label class="col-lg-8 control-label">: """+ instance.NumCtaInterMProy +"""</label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Perfil del Proyecto</label>\
						<a target="_blank" href=" """+ ruta_perfil +""" "><label class="col-lg-8 control-label">: """+ pdf_perfil +"""</label></a>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Convenio</label>\
						<a target="_blank" href=" """+ ruta_convenio +""" "><label class="col-lg-8 control-label">: """+ pdf_convenio +"""</label></a>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Acta de Cierre</label>\
						<a target="_blank" href=" """ + ruta_ac + """ "><label class=col-lg-8 control-label>: """+ pdf_ac +"""</label></a>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-12 control-label"></label>\
						<label class="col-lg-12 control-label"></label>\
						<label class="col-lg-12 control-label"></label>\
					</div>\
					<div class="form-group">\
						<label class="col-lg-4 control-label" style="color:#082C4D;">Inicia el</label>\
						<label class="col-lg-3 control-label">: """ + (str(instance.FecIniRealMProy) if (instance.FecIniRealMProy != None) else 'No asignado') + """</label>\
						<label class="col-lg-2 control-label" style="color:#082C4D;">Termina</label>\
						<label class="col-lg-3 control-label">: """ + (str(instance.FecFinRealMProy) if (instance.FecFinRealMProy != None) else 'No asignado') + """</label>\
					</div>\
					<div class="form-group">\
					    <label class="col-lg-4 control-label" style="color:#082C4D;"">Duracion (m)</label>\
					    <label class="col-lg-8 control-label">: """ + (str(instance.TiempoMProy) if (instance.TiempoMProy != None) else '0') + """ meses</label>\
					</div>\
					<div class="form-group">\
	                    <label class="col-lg-12 control-label"></label>\
	                    <label class="col-lg-12 control-label"></label>\
	                    <label class="col-lg-12 control-label"></label>\
	                </div>\
	                <div class="form-group col-lg-12">\
                        <table class="table table-condensed">\
                            <thead>\
                                <tr style="align:center;">\
                                    <th></th>\
                                    <th style="width:120px; text-align:center; background-color: #222; color:#fff">Financiamiento</th>\
                                    <th style="width:120px; text-align:center; background-color: #222; color:#fff">Adendas</th>\
                                    <th style="width:120px; text-align:center; background-color: #222; color:#fff">Total</th>\
                                </tr>\
                            </thead>\
                            <tbody>\
                    	        <tr>\
                                    <td align="center">Fondo Italo Peruano</td>\
                                    <td align="right"> S/. """ + str(instance.MontTInvRealFipMProy) + """</td>\
                                    <td align="right"> S/. """ + str(instance.MontTotAdeFipMProy) + """</td>\
                                    <td style="font-weight: bold; text-align:right;"> S/. """ + str(float(instance.MontTInvRealFipMProy) + float(instance.MontTotAdeFipMProy)) + """ </td>\
                                </tr>\
                                <tr>\
                                    <td align="center">Unidad Ejecutora</td>\
                                    <td align="right"> S/. """ + str(instance.MontTInvRealCliMProy) + """</td>\
                                    <td align="right"> S/. """ + str(instance.MontTotAdeCliMProy) + """</td>\
                                    <td style="font-weight: bold; text-align:right;"> S/. """ + str(float(instance.MontTInvRealCliMProy) + float(instance.MontTotAdeCliMProy)) + """ </td>\
                                </tr>\
                                <tr>\
                                    <td align="center">Asociados</td>\
                                    <td align="right"> S/. """ + str(instance.MontTInvRealOtrMProy) + """</td>\
                                    <td align="right"> S/. """ + str(instance.MontTotAdeOtrMProy) + """</td>\
                                    <td style="font-weight: bold; text-align:right;"> S/. """ + str(float(instance.MontTInvRealOtrMProy) + float(instance.MontTotAdeOtrMProy)) + """</td>\
                                </tr>\
                                <tr>\
                                    <td colspan="3" style="font-weight: bold; text-align:right;">TOTAL</td>\
                                    <td style="font-weight: bold; text-align:right;"> S/. """ + str(float(instance.MontTInvRealOtrMProy) + float(instance.MontTotAdeOtrMProy) + float(instance.MontTInvRealCliMProy) + float(instance.MontTotAdeCliMProy) + float(instance.MontTInvRealFipMProy) + float(instance.MontTotAdeFipMProy)) + """</td>\
                                </tr>\
                                <tr>\
                                    <td colspan="3"></td>\
                                    <td></td>\
                                </tr>\
                                <tr>\
                                    <td colspan="3"></td>\
                                    <td></td>\
                                </tr>\
                            </tbody>\
                        </table>\
                    </div>"""

		except Exception as e:
			html = 'No se pudo recuperar los datos del convenio. Error ' + str(e)
		return html
			
	def datos_colaboradores(self, *args, **kwargs):
		instance = MColaborador.objects.filter(IdMProy__IdMProy = self.codigo)
		try:
			html = """<table id="" class="table table-condensed"><thead><tr><th>Responsable</th><th>Inicia</th>\
					<th>Termina</th><th>Duración (m)</th><th>Monto Total S/.</th><th>PDF</th><tr></thead><tbody>"""

			body = ''

			for item in instance:
				body += '<tr>'
				body += '<td>' + str(item.IdMPer) + '</td>'
				body += '<td>' + str(item.FecIniMCol) + '</td>'
				body += '<td>' + str(item.FecFinMCol) + '</td>'
				body += '<td>' + str(item.TiempoMCol) + '</td>'
				body += '<td>' + str(item.MontoMCol) + '</td>'
				body += '<td><a href="/media/'+  str(item.RutaPDFMCol) +'" target="_blank">' + str(item.RutaPDFMCol)[12:] + '</a></td>'
				body += '</tr>'
			html += body + '</tbody></table>'
		except Exception as e:
			html = 'No se pudo recuperar los datos de los responsables. Error: ' + str(e)
		return html

	def datos_adendas(self, *args, **kwargs):
		instance = DProyecto.objects.filter(IdMProy__IdMProy = self.codigo)
		try:
			html = """<table id="" class="table table-condensed"><thead><tr><th>Inicia</th><th>Finaliza</th><th>F. FIP</th>\
				<th>F. UE</th><th>F. ASOC</th><th>PDF</th><tr></thead><tbody>"""

			body = ''
			for item in instance:
				body +="""<tr>
					<td>""" + str(item.FecFirmaDProy) + """</td>
					<td>""" + str(item.FecFinDProy) + """</td>
					<td class="text-right">S/. """ + str(item.MontAportFIPDProy) + """</td>
					<td class="text-right">S/. """ + str(item.MontAportCliDProy) + """</td>
					<td class="text-right">S/. """ + str(item.MontAportOtrDProy) + """</td>
					<td><a href="/media/""" + str(item.RutaPDFDProy) + """ " target="_blank">""" + str(item.RutaPDFDProy)[11:] + """</a></td>
					</tr>"""
			html += body + '</tbody></table>'
		except Exception as e:
			html = 'No se pudo recuperar los datos de los responsables. Error: '+ str(e)
		return html

class ColaboradoresConvenioAjax_View(TemplateView):
	def get(self, *args,**kwargs):
		convenio = request.GET['convenio']
		
		try:
			lista = MColaborador.objects.filter(IdMProy__IdMProy=convenio)
			data = serializers.serialize('json', lista, use_natural_keys=True)	
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class ModificatoriasConvenioAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		convenio = request.GET['convenio']
		
		try:
			lista = DProyecto.objects.filter(IdMProy__IdMProy=convenio)
			
			data = serializers.serialize('json', lista)
			
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

"""
class MaestroPersonalAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		convenio = request.GET['convenio']
		
		try:
			lista = MPersonal.objects.all()
			data = serializers.serialize('json', lista)
			
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class LocalizarPorProtocoloAjax_View(TemplateView):
	def get(self,request, *args, **kwargs):

		protocolo = request.GET['protocolo']
		nombre = request.GET['nombre']
		cliente = request.GET['cliente']
		referencia = request.GET['referencia']
		
		try:
			lista = Bandeja.objects.filter(IdMProt__contains=protocolo, ProyBProt__contains=nombre.upper(), CliBProt__contains= cliente.upper()).order_by('-IdBandeja')
			data = serializers.serialize('json', lista)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class LocalizarPorProyectoAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		
		proyecto = request.GET['protocolo']
				
		try:
			lista = Bandeja.objects.filter(ProyBProt__contains=proyecto, EstAccion='0').order_by('-IdBandeja')
			data = serializers.serialize('json', lista)
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class LocalizarPorUnidadEjecutoraAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		
		cliente = request.GET['cliente']
		
		
		try:
			lista = Bandeja.objects.filter(CliBProt__contains=cliente, EstAccion='0').order_by('-IdBandeja')
			data = serializers.serialize('json', lista)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class LocalizarPorReferenciaAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		referencia = request.GET['referencia']
				
		try:
			lista = Bandeja.objects.filter(IdProtRef__contains=referencia, EstAccion='0').order_by('-IdBandeja')
			data = serializers.serialize('json', lista)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class LocalizarPorFechaAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):

		fecha = request.GET['fecha']
		anio = datetime.datetime.now().year
		mes = datetime.datetime.now().month
		dia= datetime.datetime.now().day
		datafec = fecha.split('-')	
		lista = []
		
		if (len(datafec) == 3):
			
			if(len(datafec[0]) == 4):
				anio = int(datafec[0])
			

			if(len(datafec[1]) == 2):
				mes = int(datafec[1])
				dia = int(datafec[2])
			

			lista = Bandeja.objects.filter(FecEnv__year=anio,FecEnv__month=mes,FecEnv__day=dia, EstAccion='0').order_by('-IdBandeja')

		elif (len(datafec) == 2):
			
			if(len(datafec[0]) == 4):
				anio = int(datafec[0])
			
			if(len(datafec[1]) == 2):
				mes = int(datafec[1])
			
			lista = Bandeja.objects.filter(FecEnv__year=anio,FecEnv__month=mes, EstAccion='0').order_by('-IdBandeja')
		
		elif (len(datafec) == 1):
			
			if(len(datafec[0]) == 4):
				anio = int(datafec[0])
				lista = Bandeja.objects.filter(FecEnv__year=anio, EstAccion='0').order_by('-IdBandeja')
			

			if(len(datafec[0]) == 2):
				mes = int(datafec[0])
				lista = Bandeja.objects.filter(FecEnv__month=mes, EstAccion='0').order_by('-IdBandeja')
			
		
		try:
			data = serializers.serialize('json', lista)
		except Exception, e:
			pass

		return HttpResponse(data, mimetype='application/json')
"""		

class RegistrarColaboradorAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		if request.is_ajax() :
			col = MColaborador()
			es = request.GET["esto"]
			obj = MPersonal.objects.get(pk=4)
			col.IdMPer = obj
			obj2 = MProyecto.objects.get(pk=5)
			col.IdMProy = obj2
			col.IdTipoCargoProy = '1'
			col.FecIniMCol = '2014-12-12' #datetime.datetime.now()
			col.FecFinMCol = '2014-12-12' #datetime.datetime.now()
			col.FecFirmaMCol = '2014-12-12'
			col.TiempoMCol = '5'
			col.MontoMCol = 2
			col.MontoMenMCol =5 
			col.EstMCol = '1'
			col.EstActMCol = '1'
			col.RutaPDFMCol = request.GET["archivo"]
			col.RutaOCRMCol = request.GET["archivo"]
			col.save()
		msj={'status':'esto es para ti json'}
		return HttpResponse(json.dumps(msj),mimetype='application/json')

class ListaDepartamentoAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		idregion = request.GET['idregion']
		obj = DTabla.objects.get(pk =idregion)			
		region = obj.IdDTab
		try:
			lstDepartamento = DTabla.objects.filter(IdMTab__IdMTabla='003',IdRefDTab=region).order_by('NomDTab')
			data = serializers.serialize('json', lstDepartamento)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class ListaProvinciaAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		iddepa = request.GET['iddepa']
		obj = DTabla.objects.get(pk =iddepa)			
		departamento = obj.IdDTab
			
		try:
			lstPronvincia = DTabla.objects.filter(IdMTab__IdMTabla='004', IdRefDTab=departamento).order_by('NomDTab')
			data = serializers.serialize('json', lstPronvincia)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class ListaDistritoAjax_View(TemplateView):
	def get(self,request,*args,**kwargs):
		idprov = request.GET['idprov']
		obj = DTabla.objects.get(pk =idprov)			
		provincia = obj.IdDTab
			
		try:
			lstDistrito = DTabla.objects.filter(IdMTab__IdMTabla='005',IdRefDTab=provincia).order_by('NomDTab')
			data = serializers.serialize('json', lstDistrito)
				
		except Exception, e:
			pass
		return HttpResponse(data, mimetype='application/json')

class TipoPersonalAjax(TemplateView):
	def get(self,request,*args,**kwargs):
		codigo = request.GET['codigo']
		instance = MPersonal.objects.get(IdMPer = codigo)
		item = DTabla.objects.get(pk = instance.IdTipPerMPer)
		mensaje = {'status': True}
		if item:
			if (item.NomDTab == 'EXTERNO'):
				mensaje['status']= False
		
		return HttpResponse(json.dumps(mensaje), mimetype='application/json')

class EditarUsuario_View(TemplateView):
	def get(self,request,*args,**kwargs):
		cod = request.GET['id']
		usuario = User.objects.get(pk=cod)
		data = serializers.serialize('json', usuario)
		return HttpResponse(data, mimetype='application/json')

class ModificarPasswordAjax(TemplateView):
	def get(self, request, *args, **kwargs):
		password = self.request.GET['password']
		try:
			if (self.request.GET['codigo'] != ''):
				usuario = User.objects.get(pk = self.request.GET['codigo'])
			else:
				usuario = self.request.user
				
			usuario.set_password(password)
			usuario.save()
			message= {'estado':True}
			return HttpResponse(json.dumps(message), content_type = 'application/json')
		except Exception, e:
			message= {'mensaje': e}
		return HttpResponse(json.dumps(message), content_type = 'application/json')

class SeguimientoProtocoloAjax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		cod_prot = request.GET['protocolo']
		d_general = MProtocolo.objects.get(IdMProt = cod_prot)
		r_proto = Bandeja.objects.filter(IdMProt = cod_prot)
		estado_prot = 'En tramite'
		for reg in r_proto:
			if (reg.IdMUsuRec == "61"):
				estado_prot = 'FINALIZADO'
		proyecto = "No pertenece a proyecto"
		cliente = "No existe unidad ejecutora"
		if d_general.IdMProy:
			proyecto, cliente = d_general.IdMProy.NomMProy, d_general.IdMProy.IdMCli.NomMCli

		html = ''
		html += '<p class = "text-danger text-center"><strong>DATOS GENERALES</strong></p><div class = "from-group"><label class = "col-lg-3 text-danger"><strong>PROTOCOLO</strong></label><label class = "col-lg-9 text-info">: ' + d_general.IdMProt +'</label></div>'
		html += '<div class = "form-group"><label class = "col-lg-3 text-danger"><strong>NOMBRE</strong></label><label class = "col-lg-9 text-info">: '+ d_general.NomMProt + '</label></div>'
		html += '<div class = "form-group"><label class = "col-lg-3 text-danger"><strong>DESCRIPCION</strong></label><label class = "col-lg-9 text-info">: ' + d_general.DescMProt + '</label></div>'
		html += '<div class = "form-group"><label class = "col-lg-3 text-danger"><strong>CONVENIO</strong></label><label class = "col-lg-9 text-info">: ' + proyecto + '</label></div>'
		html += '<div class = "form-group"><label class = "col-lg-3 text-danger"><strong>U.E.</strong></label><label class = "col-lg-9 text-info">: ' + cliente + '</label></div>'
		html += '<div class = "form-group"><label class = "col-lg-3 text-danger"><strong>ESTADO</strong></label><label class = "col-lg-9 text-info">: ' + estado_prot + '</label></div>'

		# Codigo html para el seguimiento del protocolo
		html += '<br><br><div class = "form-group col-lg-12">'
		html += '<p class = "text-warning text-center"><strong>Seguimiento del protocolo:</strong></p></div><br>'

		#html += '<center><table class = "table table-bordered" style = "width:100px;"><thead><tr class ="text-danger"><th><strong>Usuario</strong></th><th><strong>Fecha</strong></th></tr></thead><tbody>'
		html += '<center><div class = "form-group col-lg-12">'
		html += '<table class = "table table-bordered" style = "width:600px;">'
		html += '<thead><tr style = "background-color:#F0F0F0;"><th class = "text-center">DE:</th><th class ="text-center">A:</th></tr></thead>'
		
		bandeja = r_proto.order_by('IdBandeja')
		#dic_seguimiento = {}
		row_html = ''
		while bandeja:
			cont = 0
			lista = []
			user_pk = bandeja[0].IdMUsuEnv
			user_name = bandeja[0].IdMUsuEnv.username
			for b in bandeja:
				if(user_pk == b.IdMUsuEnv):
					cont += 1
				else:
					break
			lista = [(b.IdMUsuRec.username +' ('+ str(b.FecSist)+')').upper() for b in bandeja[:cont]]
			#lista = [b.NomMUsuRec for b in bandeja[:cont]]
			row_html += '<tr><td>' + user_name + '</td><td><ol><small>' +'<li>'+ '</li><li>'.join(lista) + '</li>'+ '</small></ol></td></tr>'
			#row_html = ' '.join(lista)
			bandeja = bandeja[cont:]

		#row_html += '</tbody></table>' 
		
		#usuarios = [(reg.NomMUsuRec + '(' + str(reg.FecRec) + ') ').upper() for reg in r_proto]
		"""
		seguimiento_html= ' <span class = "text-danger glyphicon glyphicon-chevron-right"></span> '.join(usuarios)
		"""
		#html += seguimiento_html
		html += row_html
		html += '</tbody></table></div></center>'
		message = {'html':html}

		return HttpResponse(json.dumps(message), mimetype = 'application/json')

class ProtocolosPorProyectoAjax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		cod_prot = request.GET['protocolo']

		try:
			proy = (MProtocolo.objects.get(pk = cod_prot)).IdMProy.IdMProy
		except AttributeError as ae:
			proy = ""

		if (proy != ""):
			dat_proy = MProyecto.objects.get(pk = proy)
			protocolos = MProtocolo.objects.filter(IdMProy__IdMProy = proy)

			html = '<table class = "table table-bordered">'
			html += '<thead><tr class = "text-center">'
			html += '<th><input class = "select" type = "checkbox" id = "protocolos_por_proyecto"></input></th><th>Codigo</th><th>Nombre</th><th>Descripcion</th><th>F. Ent.</th><th>Documentos</th></tr><tbody>'
			fila = ''
			for pr in protocolos:
				fila += '<tr style = "font-size:11px;"><td><input class = "select prot_por_proy" id="desc_prot[]" name = "desc_prot[]" type = "checkbox" codigo = "' + pr.IdMProt+ '"></input></td>'
				fila += '<td>' + pr.IdMProt + '</td><td>' + pr.NomMProt + '</td><td>' + pr.DescMProt + '</td><td>' + str(pr.FecEntMProt) + '</td><td><ol>'
				detalles = DProtocolo.objects.filter(IdMProt__IdMProt = pr.IdMProt)
				for dt in detalles:
					fila += '<li><a href ="/media/'+ str(dt.RutaPdfDProt) + '" target= "_blank">' + dt.NomDProt + '</a></li>'

				fila += '</ol></td>'
				fila += '</tr>'

			html += fila
			html += '</tbody></table>'
			#message = {'html': html}
		else:
			proto = MProtocolo.objects.get(pk = cod_prot)
			detalles = DProtocolo.objects.filter(IdMProt__IdMProt = cod_prot)
			html = '<table class = "table table-bordered">'
			html += '<thead><tr class = "text-center">'
			html += '<th><input class = "select" type = "checkbox" id = "protocolos_por_proyecto"></input></th><th>Codigo</th><th>Nombre</th><th>Descripcion</th><th>F. Ent.</th><th>Documentos</th></tr><tbody>'
			html += '<tr style = "font-size:11px;"><td><input class = "select prot_por_proy" id = "desc_prot[]" name = "desc_prot[]" type = "checkbox" codigo = "' + proto.IdMProt + '"></input></td>'
			html += '<td>' + proto.IdMProt + '</td><td>' + proto.NomMProt + '</td><td>' + proto.DescMProt + '</td><td>' + str(proto.FecEntMProt) + '</td><td><ol>' 
			fila = ''
			for dt in detalles:
				fila += '<li><a href= "/media/'+ str(dt.RutaPdfDProt) + '" target= "_blank">' + dt.NomDProt + '</a></li>'
			fila += '</ol></td></tr></tbody></table>'
			html += fila

		message = {'html': html}
		return HttpResponse(json.dumps(message), mimetype = 'application/json')

class DescargaProtocoloAjax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		import os
		from django.conf import settings
		path_to_copy = settings.MEDIA_ROOT + '/'
		protocolo = request.GET['protocolo']
		lista_prt = protocolo.split(',')
		protocolos = MProtocolo.objects.filter(pk__in = lista_prt)
		import datetime
		hora = datetime.datetime.now()
		hora = str(hora.hour) + '' + str(hora.minute) + '' + str(hora.second)
		if len(protocolos >= 2):
			proy_nombre = protocolos[0].IdMProy.IdCFMProy
		else:
			proy_nombre = protocolos[0].IdMProy.NomMProy
		

		proy_nombre = proy_nombre[:10] + hora
		comando = ('mkdir '+ path_to_copy + proy_nombre)

		os.system(comando)

		for prt in protocolos:
			cod = prt.IdMProt
			detalles = DProtocolo.objects.filter(IdMProt__IdMProt = cod)
			cont = 1
			for dtl in detalles:
				try:
					ruta_dtl = dtl.RutaPdfDProt.path
					nombre = dtl.IdMProt.IdMProt
					nombre_act = ((dtl.RutaPdfDProt.name).split('/'))[1]
					mt_copia = ('cp '+ruta_dtl + ' ' + path_to_copy + proy_nombre +'/')
					os.system(mt_copia)
					comando = ('mv '+ path_to_copy + proy_nombre +'/' + nombre_act + ' ' + path_to_copy + proy_nombre +'/' + nombre + '_' + str(cont)+'.pdf')
					os.system(comando)
					cont += 1
				except ValueError as ve:
					reportar_error("Sucedio un error en la descargar del protocolo " + str(e))
		os.system('cd ' + path_to_copy + ' && zip -r ' + proy_nombre + '.zip ' + proy_nombre+'/' )
		message = {'html': '/media/'+proy_nombre+'.zip'}
		return HttpResponse(json.dumps(message),  mimetype = 'applicaton/json')

class Presupuesto_View(TemplateView):
	@method_decorator(access_permission([0,3]))
	@method_decorator(login_required(login_url='/'))
	def get(self, request, *args, **kwargs):
		tipo_usuario = request.user.tipoUsuario
		if int(tipo_usuario) == 3 :
			id_cliente = request.user.idMCli
			proy = MProyecto.objects.filter(IdMCli__IdMCli= id_cliente, EstMProy = 1).order_by('-FecIngMProy')
			id_proy = proy[0].IdMProy
			nombre_proyecto = proy[0].NomMProy
			nombre_cliente =  proy[0].IdMCli.NomMCli
			convenio = proy[0].IdMProy
			presupuesto_proyecto = PProyectos.objects.filter(IdMProy__IdMProy = id_proy)
			lista = []
			rango = 0
			for pp in presupuesto_proyecto:
				dic_dp = {}
				dic_dp['IdPProy'] = pp.IdPProy
				dic_dp['partida'] = pp.NroPartPProy
				dic_dp['tit'] = pp.TitPProy
				dic_dp['desc'] = pp.DescPProy
				dic_dp['um'] = pp.IdUnidMed
				dic_dp['cant'] = pp.CantPProy
				dic_dp['cu'] = pp.CostUnitPProy
				dic_dp['ct'] = pp.CostTotPProy
				dic_dp['ifip'] = pp.FFFipPProy
				dic_dp['iue'] = pp.FFCliPProy
				dic_dp['iotros'] = pp.FFOtrosPProy
				dic_dp['pifip'] = pp.PFFOtrosPProy
				dic_dp['piue'] = pp.PFFCliPProy
				dic_dp['piotros'] = pp.PFFOtrosPProy
				lista_meses = []
				detalle_pres = CPProyectos.objects.filter(IdPProy__IdPProy = pp.IdPProy)
				index = 0
				for cp in detalle_pres:
					if (index%2==0):
						lista_meses.append(cp.MontoRealFipCPProy)
					else:
						lista_meses.append(cp.MontoRealCliCPProy)
					index += 1
				
				dic_dp['cant_meses'] = lista_meses
				rango = len(lista_meses)

				lista.append(dic_dp)

			rango = rango/2
			rango = range(1, rango+1)
			
			self.imprimir(lista)

			ctx = {'proyecto':nombre_proyecto,'cliente':nombre_cliente,'datos':lista,'rango':rango,'convenio':convenio}
		else:
			ctx = {'msg':'No existe presupuesto.'}
		
		return render_to_response('tramite/presupuesto.html', ctx, context_instance= RequestContext(request))

	def imprimir(self, datos):
		pass
	def post(self, request, *args, **kwargs):
		pass
		
class EliminarRegistroAjax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		try:
			c_modelo = request.GET['modelo']
			c_registro = request.GET['codigo']
			modelos = {
						'0': User,
						'1': MTabla,
						'2': DTabla,
						'3': DProyecto,
						'4': MPersonal,
						'5': MColaborador,
						'6': MCliente,
						'7': MProyecto,
						'8': MProtocolo,
						'9': DProtocolo,
						'10': Bandeja,
						'11': PProyectos,
						'12': CPProyectos
					}
			eval('model.objects.get(pk=codigo).delete()',{'model':modelos[c_modelo],'codigo':c_registro})

			msj = True
		except Exception, e:
			msj = 'Error: ' + str(e)
		message= {'mensaje':msj}
		return HttpResponse(json.dumps(message),mimetype='application/json')

class DatosProtocolo(TemplateView):
	
	def get(self, request, *args, **kwargs):
		
		try:
			codigo = request.GET['codigo']
			item = MProtocolo.objects.get(pk = codigo)
			procedencia = DTabla.objects.get(pk = item.DocInter).NomDTab
			if item.IdMProy:
				proyecto = item.IdMProy.IdCFMProy + ' - ' + item.IdMProy.NomMProy
				cliente = item.IdMProy.IdMCli.NomMCli
			else:
				proyecto = item.EmpMProt
				cliente = item.RespMProt

			html = """<tr><td><strong>PROTOCOLO</strong></td><td>"""+ item.IdMProt +"""</td></tr>\
					<tr><td><strong>DESCRIPCION</strong></td><td>"""+ item.DescMProt +"""</td></tr>\
					<tr><td><strong>CONVENIO/Emp.</strong></td><td>"""+ proyecto +"""</td></tr>\
					<tr><td><strong>U.E/Resp.</strong></td><td>"""+ cliente +"""</td></tr>\
					<tr><td><strong>FEC. RECEPCION</strong></td><td>"""+ str(item.FecEntMProt) +"""</td></tr>\
					<tr><td><strong>REFERENCIA</strong></td><td>"""+ item.IdRefMProt +"""</td></tr>\
					<tr><td><strong>PROCEDENCIA</strong></td><td>"""+ procedencia +"""</td></tr>"""
		except Exception, e:
			html = 'No se logró ubicar el protocolo o no existe.'
			pass
		message = {'html':html}

		return HttpResponse(json.dumps(message), mimetype = 'application/json')
		
class DocumentosProtocoloAjax(TemplateView):
	
	def get(self, request, *args, **kwargs):
		protocolos = request.GET['protocolos']
		protocolos = protocolos.split(',')
		html = []
		
		try:
			for codigo in protocolos:
				documentos = codigo + ':<ol>'
				ruta = "#"
				lista = DProtocolo.objects.filter(IdMProt__IdMProt = codigo)
				for item in lista:
					if (item.RutaPdfDProt != ''):
						ruta = '/media/'+ str(item.RutaPdfDProt)
					documentos += '<li><a href='+ ruta +' target = "_blank">'+ item.NomDProt +'</a></li>'
				documentos += '</ol>'
				html.append(documentos)
			msj = '\n'.join(html)
		except Exception, e:
			msj = str(e)
		message = {'html': msj}
		return HttpResponse(json.dumps(message), content_type = 'application/json')
		
class SupervisarProyecto_View(TemplateView):
	def get(self, request, proyecto):
		current_p = proyecto
		lista = PProyectos.objects.filter(IdMProy__IdMProy = current_p, EstPProy=1)
		if len(lista) > 0 :
			proy = MProyecto.objects.get(IdMProy = current_p, EstMProy = 1)
			id_proy = proy.IdMProy
			nombre_proyecto = proy.NomMProy 
			nombre_cliente =  proy.IdMCli.NomMCli
			convenio = proy.IdMProy
			presupuesto_proyecto = PProyectos.objects.filter(IdMProy__IdMProy = current_p)
			lista = []
			rango = 0
			for pp in presupuesto_proyecto:
				dic_dp = {}
				dic_dp['IdPProy'] = pp.IdPProy
				dic_dp['partida'] = pp.NroPartPProy
				dic_dp['tit'] = pp.TitPProy
				dic_dp['desc'] = pp.DescPProy
				dic_dp['um'] = pp.IdUnidMed
				dic_dp['cant'] = pp.CantPProy
				dic_dp['cu'] = pp.CostUnitPProy
				dic_dp['ct'] = pp.CostTotPProy
				dic_dp['ifip'] = pp.FFFipPProy
				dic_dp['iue'] = pp.FFCliPProy
				dic_dp['iotros'] = pp.FFOtrosPProy
				dic_dp['pifip'] = pp.PFFOtrosPProy
				dic_dp['piue'] = pp.PFFCliPProy
				dic_dp['piotros'] = pp.PFFOtrosPProy
				lista_meses = []
				detalle_pres = CPProyectos.objects.filter(IdPProy__IdPProy = pp.IdPProy)
				index = 0
				for cp in detalle_pres:
					if (index%2==0):
						lista_meses.append(cp.MontoRealFipCPProy)
					else:
						lista_meses.append(cp.MontoRealCliCPProy)
					index += 1
				
				dic_dp['cant_meses'] = lista_meses
				rango = len(lista_meses)

				lista.append(dic_dp)

			rango = rango/2
			rango = range(1, rango+1)
			
			ctx = {'proyecto':nombre_proyecto,'cliente':nombre_cliente,'datos':lista,'rango':rango,'convenio':convenio}
			
		else :
			form = CargaForm()
			ctx = {'form': form, 'mensaje':'El proyecto no cuenta con un presupuesto','proyecto':current_p}
		return render_to_response('tramite/pres_proyecto.html', ctx, context_instance = RequestContext(request))
	
	def post(self, request, *args, **kwargs):
		from .proceso import Presupuesto
		msj = ""
		filename = ""
		n_meses = 0
		proyecto = ""
		try:
			
			form = CargaForm(request.POST,request.FILES) # A form bound to the POST data
			proyecto = request.POST['proyecto']
			if form.is_valid():
				add = form.save(commit=False)
				add.save()
				msj = 'El archivo fue subido con exito'
			else:
				msj = 'El formulario no es valido'
		except Exception, e:
			msj = "Sucedio un error al momento de guardar"

		c_p = MProyecto.objects.get(IdMProy = proyecto)
		nombre_proyecto = c_p.NomMProy 
		nombre_cliente =  c_p.IdMCli.NomMCli
		convenio = c_p.IdMProy

		errores = []
		datos = []
		query = Presupuesto()
		filename = CargaPresupuesto.objects.last()
		filename = str(filename.doc_temp)
		filename = filename.split('/')
		filename = filename[-1]

		hasname = query.inicio(filename)
		le = []
		ld = []
		if hasname:
			resultado = query.procesar_pres()
			cant_meses = int(query.duracion_proyecto())
			filas_resultados = query.get_lista_fni
			lista_resultados = query.get_lista_resultados
			valido = resultado[0]
			datos = resultado[1]
			errores = resultado[2]

			
		if len(errores)>2:
			le = errores[:-2]
			ctx = {'errores':le}
			return render_to_response('tramite/pres_proyecto.html', ctx, context_instance=RequestContext(request))
		elif len(errores)<3:
			ld = datos
			self.guardar_presupuesto(request, filas_resultados,lista_resultados,datos,proyecto)
			n_meses = 5
			rango = range(1,cant_meses+1)
			ctx = {'datos':datos,'lista_resul':lista_resultados,'rango':rango, 'proyecto':nombre_proyecto,'cliente':nombre_cliente, 'convenio':convenio}
			return render_to_response('tramite/pres_proyecto.html', ctx,context_instance=RequestContext(request))

	def guardar_presupuesto(self,request, fni, desc_fni, datoPres, proyecto):
	
		proy = MProyecto.objects.get(IdMProy= proyecto, EstMProy = 1)
		FECHA = datetime.datetime.today()
		index = 1
		for p in datoPres:
			
			pres = PProyectos()
			cod_pres = self.generar_Codigo()
			pres.IdPProy = cod_pres
			
			
			pres.IdMProy = proy
			pres.NroPartPProy = p['partida']
			pres.IdNivPartPProy = p['nivel']
			pres.TitPProy = p['tit']
			pres.DescPProy = p['desc']
			pres.NroPartPerProy = self.pertenece_a(p['partida'])
			pres.IdUnidMed = p['um']
			try:
				pres.CantPProy = int(p['cant'])	
			except ValueError as ve:
				pres.CantPProy = 0.0
			except Exception, e:
				pres.CantPProy = 0.0
			try:
				pres.CostUnitPProy = float(p['cu'])
			except Exception, e:
				pres.CostUnitPProy = 0.0
			try:
				pres.CostTotPProy = float(p['ct'])
			except Exception, e:
				pres.CostTotPProy = 0.0
			try:
				pres.FFFipPProy = float(p['ifip'])
			except Exception, e:
				pres.FFFipPProy = 0.0
			try:
				pres.FFCliPProy = float(p['iue'])
			except Exception, e:
				pres.FFCliPProy = 0.0
			try:
				pres.FFOtrosPProy = float(p['iotros'])
			except Exception, e:
				pres.FFOtrosPProy = 0.0
			try:
				ct =  float(p['ct'])
			except ValueError as ve:
				ct = 0.0
			try:
				ifip =  float(p['ifip'])
				pres.PFFFipPProy = (ifip * 100)/ct
			except ValueError as ve:
				ifip = 0.0
			except ZeroDivisionError as dz:
				pres.PFFFipPProy = 0
			try:
				iue =  float(p['iue'])
				pres.PFFCliPProy = (iue * 100)/ct
			except ValueError as ve:
				iue = 0.0
			except ZeroDivisionError as dz:
				pres.PFFCliPProy = 0.0
			try:
				iotros =  float(p['iotros'])
				pres.PFFOtrosPProy = (iotros * 100)/ct
			except ValueError as ve:
				iotros = 0.0
			except ZeroDivisionError as dz:
				pres.PFFOtrosPProy = 0.0

			pres.FinPProy = '0'
			pres.VerPProy = '0'
			pres.EstPProy = '1'
			pres.FecIngPProy = FECHA.strftime('%Y-%m-%d')
			
			pres.IdUsuCreaPProy = request.user.id
			
			pres.IdUsuModPProy = ''
			pres.CostEjePProy = 0.0
			pres.CostSalPProy = 0.0
			pres.IdMotCierrePProy = '0'
			pres.PorCostEjePProy = 0.0
			pres.BorradorPProy = '1'
			pres.EstPresPProy = '0'
			pres.EstEvalPProy = '0'
			pres.EstValidPProy = '0'
			pres.EstAprobPProy = '0'
			pres.EstModifPProy = '0'
			
			mes = proy.FecIniRealMProy 
			anio = mes.strftime('%Y')
			anio = int(anio)
			mes_ini = mes.strftime('%m')
			mes_ini = int(mes_ini)
			mes_c = 1
			
			pres.save()
			index = index + 1
			i=1
			x=0
			for m in p['cant_meses']:

				cpp = CPProyectos()
				cpp.IdPProy = pres
				cpp.MesCPProy = mes_c
				cpp.MesCCPProy = mes_ini
				cpp.AnioCCPProy = anio
				cpp.MontoEjecCPProy = 0
				cpp.PorcEjecCPProy = 0
				cpp.VerCPProy = 0
				cpp.SVerCPProy = 0
				cpp.EstCPProy = 1
				cpp.EstModifCPProy = 0
				cpp.MontoEjeFipCPProy = 0
				cpp.PorcEjeFipCPProy = 0
				cpp.MontoEjeCliCPProy = 0
				cpp.PorcEjeCliCPProy = 0
				cpp.MontoRealCPProy = 0
				cpp.PorcRealCPProy = 0
				if (x%2 == 0):
					cpp.MontoRealFipCPProy = m
					cpp.PorcRealFipCPProy = 0
					cpp.MontoRealCliCPProy = 0
					cpp.PorcRealCliCPProy = 0
				else :
					cpp.MontoRealFipCPProy = 0
					cpp.PorcRealFipCPProy = 0
					cpp.MontoRealCliCPProy = m
					cpp.PorcRealCliCPProy = 0

				cpp.MontoDifEjecRealCPProy = 0
				cpp.PorcDifEjecRealCPProy = 0
				cpp.EstVisCPProy = 0
				if (mes_ini == 12):
					mes_ini = 1
				if (i %2 == 0):
					mes_ini += 1
					mes_c += 1

				cpp.save()
				i += 1
				x += 1

	def pertenece_a(self, partida):
		val_part = partida.split(',')
		if (len(val_part) == 1):
			return partida
		else:
			val_part = val_part[:-1]
			pertence = '.'.join(val_part)
			return pertence

	def generar_Codigo(self):
		if (PProyectos.objects.count() == 0):
			codigo = 'PRES2014-00000001'
		else:
			anio = datetime.datetime.today().year
			anio = str(anio)
			obj = PProyectos.objects.last()
			cod = obj.IdPProy
			num = cod[-8:]
			num = int(num)
			num = num + 1
			can = len(str(num))
			dif = 8-can
			codigo = ''
			codigo = '0'*dif
			codigo = 'PRES'+anio+ '-' + codigo + str(num)
		return codigo	
		
class ProtocoloPorProyecto_View(TemplateView):
	def get(self, request, *args, **kwargs):
		proyectos = MProyecto.objects.all()
		ctx = {'lista': proyectos}
		return render_to_response('tramite/protocolos_proyectos.html', ctx, context_instance = RequestContext(request))

class ProtocolosPorProyecto_dos_Ajax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		codigo_proyecto = request.GET['proyecto']
		protocolos = MProtocolo.objects.filter(IdMProy__IdMProy = codigo_proyecto)
		data = serializers.serialize('json', protocolos)
		return HttpResponse(data, mimetype = "application/json")

class BancosSectoresAjax_View(TemplateView):
	def get(self, request, *args, **kwargs):
		
		bancos = DTabla.objects.filter(IdMTab__IdMTabla='007')
		sectores = DTabla.objects.filter(IdMTab__IdMTabla='010')
		html_bancos, html_sectores = "<option value = "">Default</option>", "<option value = "">Default</option>"

		for b in bancos:
			html_bancos += '<option value = "'+ str(b.pk) + '">' + b.NomDTab + '</option>'

		for s in sectores:
			html_sectores += '<option value = "' + str(s.pk) + '">' + s.NomDTab + '</option>'

		message = {'bancos':html_bancos, 'sectores': html_sectores}
		return HttpResponse(json.dumps(message), content_type = 'application/json')

class TransferenciaDProtocoloAjax(TemplateView):
	def get(self, request, *args, **kwargs):
		operacion = self.request.GET['opcion']
		if (operacion == "filtrar"):
			protocolo = self.request.GET['codigo']
			try:
				lista = DProtocolo.objects.filter(IdMProt__IdMProt = protocolo)
				
				if (len(lista)>0):
					personal = MPersonal.objects.filter(EstMPer = True).exclude(IdMPer = self.request.user.IdMPer)
					personal_html = '<option value="">[Seleccione destino]</option>'
					for p in personal:
						#personal_html += '<option value = "' + p.IdMPer + '">' + p.ApePMPer + ' ' + p.ApeMMPer + ', ' +  p.NomMPer + '</option>'
						personal_html += '<option value = "' + p.IdMPer + '">' + unicode(p) + '</option>'

					html = """<a href = "#" id="transf_protocolo" name="transf_protocolo"  protocolo =" """ + lista[0].IdMProt.IdMProt + """">
								Transferir todos los documentos</a>
								<select class ="destino_prot hide">""" + personal_html + """
								</select>
								<a href = "#" class="hide" id="btnTransferProt" name="btnTransferProt" cod =" """ + lista[0].IdMProt.IdMProt +"""" dest=""  tipo_doc="0">
									<span class ="glyphicon glyphicon-send text-warning"></span>
								</a>
								<table class = "table table-bordered">
								<thead>
									<tr style="background: #084057; color: #fff;">
										<th class ="text-center" style="width:350px;">Documento</th>
										<th class ="text-center" style="width:450px;">U. Actual</th>
										<th class ="text-center">Destino</th>
										<th> </th>
									</tr>
								</thead>
								<tbody>"""
					content = ""
					for item in lista:
						ubi_act_cod = item.UbiFisDProt
						ubi_act_name = "[No se logro ubicar]"
						if ubi_act_cod:
							try:
								mper = MPersonal.objects.get(IdMPer = ubi_act_cod)
								ubi_act_name = mper.ApePMPer + ' ' + mper.ApeMMPer + ', ' + mper.NomMPer
							except Exception as e:
								ubi_act_name = '[El personal esta inactivo]'
								pass


						content += """<tr id="tr""" + item.pk + """" name="tr""" + item.pk + """">
										<td>""" + item.NomDProt + """</td>
										<td>""" + ubi_act_name + """</td>
										<td><select doc = " """ + item.pk +""" " class ="destino_doc">""" + personal_html + """
											</select>
										</td>
										<td>
											<a href = "#" class="hide transf_doc" id="btn""" + item.pk + """" name="btn""" + item.pk + """" dest="" cod=" """ + item.pk + """" tipo_doc="1">
												<span class ="glyphicon glyphicon-send text-warning"></span>
											</a>
										</td>
									</tr>"""
					content += '</tbody></table><br><br><br><p class="text-center text-danger">Historial de Transferencia </p>'
					html += content

					# Obtenemos el historial de los documentos del protocolo
					historial = FProtocolo.objects.filter(EstFProt = True, IdDProt__IdMProt__IdMProt = protocolo).order_by('-FecFProt')
					historial_html = """<div>
										<input type ="text" id = "filtro_historial" name = "filtro_historial" class ="col-lg-4 pull-right" placeholder="[Ingrese texto a buscar]">
										</div><br><br>
										<center>
										<table class = "table table-bordered" id="tabla_historial" name="tabla_historial" style="width:1000px;">
										<thead>
											<tr style="background: #084057; color: #fff;">
												<th class ="text-center" style="width:200px;">Documento</th>
												<th class ="text-center" style="width:200px;">DE:</th>
												<th class ="text-center" style="width:200px;">A:</th>
												<th class ="text-center" style="width:100px;">Fecha y Hora</th>
											</tr>
										</thead>
										<tbody>"""
					for h in historial:
						historial_html += """<tr style="font-size:10px;">
												<td style="width:200px;" class = "documento">""" + h.IdDProt.NomDProt.lstrip() + """</td>
												<td style="width:200px;" class = "nombre">""" + unicode(h.IdMPerE).lstrip() + """</td>
												<td style="width:200px;">""" + unicode(h.IdMPerR).lstrip() + """</td>
												<td style="width:100px;">""" + h.FecFProt.strftime("%d-%m-%Y %H:%M") + """ </td>
										</tr>"""
					historial_html += '</tbody></table></center><br>'
					
					html += historial_html

				else:
					html = 'El protocolo no posee documentos adjuntos'

			except Exception as e:
				html = "Sucedio un error al recuperar los datos. Error: " + str(e)

			message = {'filtro': html}
			return HttpResponse(json.dumps(message), content_type='application/json')
		elif(operacion == "transferir"):
			print 'TRANSFERENCIA'
			tipo_doc = self.request.GET['tipo_doc']
			cod = self.request.GET['cod']
			dest = self.request.GET['dest']
			listDocuments = []
			
			if (int(tipo_doc) == 0):
				# El tipo de transferencia es por protocolo
				listDocuments = DProtocolo.objects.filter(IdMProt__IdMProt = cod)
			elif(int(tipo_doc) == 1):
				# El tipo de transferencia es un solo documento
				listDocuments = DProtocolo.objects.filter(IdDProt = cod)
			registers = []
			if listDocuments:
				for item in listDocuments:
					F = FProtocolo()
					F.IdMPerE = MPersonal.objects.get(IdMPer = self.request.user.IdMPer)
					F.IdMPerR = MPersonal.objects.get(IdMPer = dest)
					F.FecFProt = timezone.now()
					F.IdDProt = item
					fila = {}
					fila['estado']= True
					fila['enviado_por'] = unicode(F.IdMPerE)
					fila['recep_por'] = unicode(F.IdMPerR)
					fila['documento'] = F.IdDProt.NomDProt
					fila['fecha'] = F.FecFProt.strftime("%d-%m-%Y %H:%M")
					fila['fila']= F.IdDProt.IdDProt
					F.save()
					registers.append(fila)
					item.UbiFisDProt = dest
					item.save()

			return HttpResponse(json.dumps(registers), content_type='application/json')
		else:
			message = {'filtro': 'No se ejecutor la operacion.'}
			return HttpResponse(json.dumps(message), content_type='application/json')

class CreateMTablaAjax(TemplateView):
	def get(self, *args, **kwargs):
		try:
			instance = MTabla()
			instance.NomMTabla = self.request.GET['nombre']
			instance.PropMTabla = self.request.GET['prop']
			instance.AbrMTabla = self.request.GET['abr']
			instance.IdMTabla = self.generar_codigo()
			instance.save()
			estado = True
			nCodigo = instance.IdMTabla
			message = {'estado': estado, 'nCodigo': nCodigo}
		except Exception as e:
			estado = 'Error al grabar: ' + str(e)
			message = {'estado': estado}
		return HttpResponse(json.dumps(message), content_type = 'application/json')
	def generar_codigo(self):
		codigo = MTabla.objects.last().IdMTabla
		codigo = ((len(codigo)-len(str(int(codigo))))*'0') + str (int(codigo)+1)
		return codigo

class ListaEmpresasResponsablesAjax(TemplateView):
	def get(self, *args, **kwargs):
		listaEmpresas = []
		listaResponsables = []
		try:
			listaEmpresas = [item.NomDTab for item in DTabla.objects.filter(IdMTab__IdMTabla = '034')]
			listaResponsables = [item.NomDTab for item in DTabla.objects.filter(IdMTab__IdMTabla = '035')]
		except Exception, e:
			pass
		message = {'empresas': listaEmpresas, 'responsables': listaResponsables}
		return HttpResponse(json.dumps(message), content_type='application/json')
