#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Autor: Nolasco Bonilla, Francisco 
# Email: fnolasco124@gmail.com	

from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns =  patterns('swFondoIP.apps.tramiteDoc.views',
	url(r'^$', Login_View.as_view(), name ='Login_View'),
	url(r'^logout/$', Logout_View.as_view(), name ='Logout_View'),
	url(r'^administracion/personal/nuevo/$', Personal_View.as_view(), name ='vista_personal'),
	url(r'^administracion/uejecutora/nuevo/$', Cliente_View.as_view(), name ='vista_Nuevo_UEjecutora'),
	
	url(r'^administracion/personal/$', PersonalListView.as_view(), name ='list-personal'),
	url(r'^administracion/unidadesejecutoras/$', ClienteListView.as_view(), name ='list-cliente'),
	url(r'^administracion/usuarios/$', UsuarioListView.as_view(), name ='list-usuario'),
	url(r'^administracion/tablasmaestro/$', MTablaListView.as_view(), name ='vista_TablasMaestro'),
	
	url(r'^sistema/listaDTablas/$', ListaDTabla_View.as_view(), name ='vista_lstDTabla'),
	url(r'^sistema/tablas/$', Tabla_View.as_view(), name ='vista_tabla'),
	url(r'^sistema/dtablas/$', DTabla_View.as_view(), name ='vista_dtabla'),
	
	# MENU DE TRAMITE DOCUMENTARIO
	
	#url(r'^tramite/protocolo/$', Protocolo_View.as_view(), name ='vista_Protocolo'),
	url(r'^tramite/protocolo/$', CreateProtocolo_View.as_view(), name ='crear-protocolo'),
	url(r'^tramite/convenios/$', ProyectoListView.as_view(), name ='list-proyecto'),
	url(r'^tramite/convenios/crear/$', CreateProyecto_View.as_view(), name = 'crear-proyecto'),
	url(r'^tramite/convenios/editar/(?P<pk>.+)/$', UpdateProyecto_View.as_view(), name = 'update-proyecto'),
	#url(r'^tramite/bandeja/page/(?P<pagina>.*)/$', BandejaListView.as_view(), name ='list-bandeja'),
	url(r'^tramite/bandeja/$', BandejaListView.as_view(), name ='list-bandeja'),
	url(r'^tramite/localizar/$', LocalizarProtocolo_View.as_view(), name ='vista_LocalizarProtocolo'),
	url(r'^tramite/proyecto/nuevo$', CreateProyecto_View.as_view(), name ='vista_Convenio'),
	
	url(r'^tramite/adendas/(?P<proyecto>.*)/$', CreateModificatoria.as_view(), name ='create-modificatoria'),
	url(r'^tramite/colaboradores/(?P<proyecto>.*)/$', CreateColaborador.as_view(), name ='create-colaborador'),

	url(r'^tramite/detalleprotocolo/(?P<idpr>.{15})/$', CreateDetalleProtocolo_View.as_view(), name ='detalle-protocolo'),
	#url(r'^tramite/detalleprotocolo/(?P<idpr>[A-Z]{2}\d{4}.\d{8})/$', DetalleProtocolo_View.as_view(), name ='detalle-protocolo'),
	url(r'^tramite/proyecto/protocolos/$', ProtocoloPorProyecto_View.as_view(), name = 'vista_ProtocolosProyectos'),
	url(r'^supervision/presupuesto/$',ConveniosSupervisor_View.as_view(), name='vista_Convenio_Supervisor'),
	url(r'^supervision/presupuesto/(?P<proyecto>.*)/$',SupervisarProyecto_View.as_view(), name='vista_Supervisar_Proyecto'),


	url(r'^uejecutora/cargar/$',CargarPresupuesto_View.as_view(), name='vista_Cargar_Presupuesto'),
	url(r'^uejecutora/presupuesto/$',Presupuesto_View.as_view(), name='vista_Presupuesto'),
	#url(r'^tramitedoc/busquedaAjax/$', BusquedaAjax_View.as_view()),
	
	#url(r'^tramitedoc/maestroConvenioAjax/$', MaestroConvenioAjax_View.as_view()),
	
	#url(r'^tramitedoc/colaboradoresConvenioAjax/$', ColaboradoresConvenioAjax_View.as_view()),
	#url(r'^tramitedoc/modificatoriasConvenioAjax/$', ModificatoriasConvenioAjax_View.as_view()),
	#url(r'^tramitedoc/maestroPersonalAjax/$', MaestroPersonalAjax_View.as_view()),

	#url(r'^tramitedoc/localizarPorProtocoloAjax/$', LocalizarPorProtocoloAjax_View.as_view()),
	#url(r'^tramitedoc/localizarPorProyectoAjax/$', LocalizarPorProyectoAjax_View.as_view()),
	#url(r'^tramitedoc/localizarPorUnidadEjecutoraAjax/$', LocalizarPorUnidadEjecutoraAjax_View.as_view()),
	#url(r'^tramitedoc/localizarPorReferenciaAjax/$', LocalizarPorReferenciaAjax_View.as_view()),
	#url(r'^tramitedoc/localizarPorFechaAjax/$', LocalizarPorFechaAjax_View.as_view()),
	url(r'^tramitedoc/listaDepartamentoAjax/$', ListaDepartamentoAjax_View.as_view()),
	url(r'^tramitedoc/listaProvinciaAjax/$', ListaProvinciaAjax_View.as_view()),
	url(r'^tramitedoc/listaDistritoAjax/$', ListaDistritoAjax_View.as_view()),

	url(r'^ajax/personal_tipo/$', TipoPersonalAjax.as_view()),
	url(r'^ajax/transferencia_dprotocolo/$', TransferenciaDProtocoloAjax.as_view()),
	
	#url(r'^tramitedoc/registrarColaboradorAjax/$', RegistrarColaboradorAjax_View.as_view()),

	#url(r'^tramitedoc/usuarioAjax/$', UsuarioAjax_View.as_view()),
	
	#url(r'^tramitedoc/observarProtocolo/$', ObservarAjax_View.as_view()),
	

	#url(r'^ajax/editar_usuario/$',EditarUsuario_View.as_view(),name="usuarioAjax"),
	#url(r'^ajax/detalle_protocolo/$', MaestroProtocoloAjax_View.as_view()),
	url(r'^ajax/datos_convenio/$', DatosConvenioAjax.as_view()),
	url(r'^ajax/detalle_protocolo/$', DatosProtocolo.as_view()),
	url(r'^ajax/documentos_protocolos/$', DocumentosProtocoloAjax.as_view()),
	url(r'^ajax/eliminar_registro/$', EliminarRegistroAjax_View.as_view(), name = 'eliminar_registro'),
	url(r'^ajax/protocoloproyecto/$', ProtocolosPorProyecto_dos_Ajax_View.as_view()),
	url(r'^ajax/localizar/$', LocalizarProtocoloAjax_View.as_view()),
	url(r'^ajax/detalle-localizar/$', SeguimientoProtocoloAjax_View.as_view()),
	url(r'^ajax/protocolo_proyecto/$', ProtocolosPorProyectoAjax_View.as_view()),
	url(r'^ajax/descarga_protocolo/$', DescargaProtocoloAjax_View.as_view()),
	url(r'^ajax/bancos_sectores/$', BancosSectoresAjax_View.as_view()),
	url(r'^ajax/grabar_mtabla/$', CreateMTablaAjax.as_view()),
	url(r'^ajax/empresas_responsables/$', ListaEmpresasResponsablesAjax.as_view()),
	url(r'^ajax/modificar_password/$', ModificarPasswordAjax.as_view()),
	
	)
