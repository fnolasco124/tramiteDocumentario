$(document).on('ready',function(){
    var lstSeleccion = [];
    var lstDestino = [];
    var lstUsuario = [];
    var lstPk = [];
    var lstUsers = [];
    var lstNombres = [];
	
    $('.popover-dismiss').popover({
        trigger: 'focus'
    });

    $("#chkDocTec").click(selec_usuarios_tecnicos);
    $("#chkDocAdmin").click(selec_usuarios_admin);
    $("#chkATecnica").click(selec_usuarios_atecnica);
    $("#chkAFinanciera").click(selec_usuarios_afinanciera);
    $("#chkATesoreria").click(selec_usuarios_atesoreria);
    $("#chkAUsuarios").click(selec_usuarios_ausuarios);
    $("#chkALegal").click(selec_usuarios_alegal);
    //$("#btnProtocoloProyecto").click(buscar_protocolo_proyecto);
    $(".protocolos").click(cant_prot_selec);
    //$("#tblProtocoloProyecto").on("click",".btnDetalle", documento_protocolo);
    
    function cargar_modal(){
		$("#cargador2").show();
    };
    function selec_usuarios_tecnicos(){
        if ($(this).prop('checked')){
            $('.docTec').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
        }else{
            $('.docTec').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
        }
        };

        function selec_usuarios_admin(){
            
            if ($(this).prop('checked')){
                $('.docAdmin').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.docAdmin').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };
        function selec_usuarios_atecnica(){
            
            if ($(this).prop('checked')){
                $('.aTecnica').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.aTecnica').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };
        function selec_usuarios_afinanciera(){
            
            if ($(this).prop('checked')){
                $('.aFinanciera').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.aFinanciera').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };
        function selec_usuarios_atesoreria(){
            
            if ($(this).prop('checked')){
                $('.aTesoreria').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.aTesoreria').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };
        function selec_usuarios_ausuarios(){
            
            if ($(this).prop('checked')){
                $('.aUsuarios').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.aUsuarios').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };
        function selec_usuarios_alegal(){
            
            if ($(this).prop('checked')){
                $('.aLegal').prop("checked",true); // en versiones anteriores reemplazar el true por "checked"    
            }else{
                $('.aLegal').prop("checked",false); // en versiones anteriores reemplazar el true por "checked"    
            }
        };


        
	
    	$(".protocolos").click(cant_prot_selec);
    	function cant_prot_selec(){
    		var cant_reg = $('input[name="chk[]"]:checked').length;
    		if (cant_reg > 0){
				//console.log(cant_reg);
    			$("#btnEnviar").removeClass("hide");
    		}else{
    			$("#btnEnviar").addClass("hide");
    		}
    	};
        
        $('.select').on('click',function(){
           var val = $(this).attr('value');
	       $('#tr'+val).toggleClass('seleccionado');
	    
        });    
        
        $("#btnEnviar").on('click',function(e){
            //alert('estamos aki');
            //e.preventDefault();
            lstSeleccion = [];
            $('input[name="chk[]"]:checked').each(
                function ()
                {                                  
                    lstSeleccion.push($(this).val());
                });
            $('#txtProtocolo').val(lstSeleccion);
            $('#cargador').show();
           
        });

        $("#btnFinalizarDestino").on('click',function(e){
            //alert('aki');
            lstDestino = [];
            lstUsuario = [];
            $('input[name="destino[]"]:checked').each(
                function ()
                {
                    
                    lstDestino.push($(this).attr("cod"));
                    lstUsuario.push($(this).attr("nom"));
                });
            $('#txtDestino').val(lstDestino);
            $('#txtUsuario').val(lstUsuario);
            $('#seleccionarDestino').modal('hide');
            
        });
        
        

        $(".cliente").bind("click",function(){
            //alert($(this).attr("nombre"));
            $('#NomMCli').val($(this).attr("nomCli"));
            $('#IdMCli').val($(this).attr("codCli"));
            $('#seleccionarUnidadEjecutora').modal('hide');
        });
             
        $.expr[':'].Contains = function(x, y, z){
            return jQuery(x).text().toLowerCase().indexOf(z[3].toLowerCase())>=0;
        };

        
        

        $(".btnObservar").bind("click",function(){
            var protocolo = $(this).attr("prot");
            var usuario = $(this).attr("usu");        
             $.ajax({
                data : {'protocolo':protocolo,'usuario':usuario},
                url : '/tramitedoc/observarProtocolo/',
                type: 'get',
                success: function(data){
                    
                    var html="";
                    html += '<h3> El protocolo: ' + protocolo + 'ha sido observado </h3>';
                    $('#mensajeError').html(html);
                    //alert('El Protocolo: '+ protocolo + ' ha sido observado.');
                    $('#frmMensaje').modal('show');
                    //location.reload();                    
                    }   
            });

        });

        $(".close").on("click",function(){
            band = $(this).attr("id");
            if(band !='false'){
                location.reload();
            }
            
        });

        //Bandeja
        $(".bandeja-detalle-protocolo").bind("click",function(){

            var codigo = $(this).attr("codigo");
                                  
            $.ajax({
                data : {'codigo': codigo},
                url : '/ajax/detalle_protocolo/',
                type: 'get',
                success: function(data){
                    $('#bandeja_detalle_protocolo').html(data.html);
                    $('#frmDetalleProtocolo').modal('show');
                }
                       
            });

        });
        
        $(".datos-convenio").on("click", datos_convenio);
        function datos_convenio(){
            var codigo = $(this).attr("codigo");
            $.ajax({
                data : {'codigo': codigo},
                url : '/ajax/datos_convenio/',
                type: 'get',
                success: function(data){
                    $("#div_datos_convenio").html(data.convenio);
                    $("#div_datos_colaboradores").html(data.colaboradores);
                    $("#div_datos_adendas").html(data.adendas);
                    $('#frmDetalleConvenio').modal('show');
                }    
            });            

        };
       
       
   
        $("#idRegMCli").on("change",function(){
            var idregion = $(this).attr("value");
            //alert(idregion);
            
            $.ajax({
                data : {'idregion':idregion},
                url : '/tramitedoc/listaDepartamentoAjax/',
                type: 'get',
                success: function(data){
                    html = '<option value="">Seleccione...</option>';
                    for(var i=0;i<data.length;i++){
                        //alert(data[x].fields.fecIniMCol + '- ' + data[x].fields.rutaPDFMCol);
                        html += '<option value="'+ data[i].pk +'">'+ data[i].fields.NomDTab +'</option>';
                                
                        }
                        $('#idDepMCli').html(html);

                }
            });

        });

        $("#idDepMCli").on("change",function(){
            var iddepa = $(this).attr("value");
            //alert(iddepa);
            
            $.ajax({
                data : {'iddepa':iddepa},
                url : '/tramitedoc/listaProvinciaAjax/',
                type: 'get',
                success: function(data){
                    html = '<option value="">Seleccione...</option>';
                    for(var i=0;i<data.length;i++){
                        //alert(data[x].fields.fecIniMCol + '- ' + data[x].fields.rutaPDFMCol);
                        html += '<option value="'+ data[i].pk +'">'+ data[i].fields.NomDTab +'</option>';
                                
                        }
                        $('#idProvMCli').html(html);

                }
            });

        });

        $("#idProvMCli").on("change",function(){
            var idprov = $(this).attr("value");
            //alert(iddepa);
            
            $.ajax({
                data : {'idprov':idprov},
                url : '/tramitedoc/listaDistritoAjax/',
                type: 'get',
                success: function(data){
                    html = '<option value="">Seleccione...</option>';
                    for(var i=0;i<data.length;i++){
                        //alert(data[x].fields.fecIniMCol + '- ' + data[x].fields.rutaPDFMCol);
                        html += '<option value="'+ data[i].pk +'">'+ data[i].fields.NomDTab +'</option>';
                                
                        }
                        $('#idDistMCli').html(html);

                }
            });

        });

        $(".montoReal").on("focusout",function(){
            var montoRealFip = 0.0;
            var montoRealClie = 0.0;
            var montoRealOtros = 0.0;
            
            montoRealFip = $("#montTInvRealFipMProy").val();
            montoRealClie = $("#montTInvRealCliMProy").val();
            montoRealOtros = $("#montTInvRealOtrMProy").val();
            

            var total = (parseFloat(montoRealFip) + parseFloat(montoRealClie) + parseFloat(montoRealOtros));

            //$('#idRefMProt').val($(this).attr("codRef"));
            
            $("#montTotRealMProy").val(total);
            
        });
        $(".montoAdendas").on("focusout",function(){
            var montoFip = 0.0;
            var montoClie = 0.0;
            var montoOtros = 0.0;
            
            montoFip = $("#montTotAdeFipMProy").val();
            montoClie = $("#montTotAdeCliMProy").val();
            montoOtros = $("#montTotAdeOtrMProy").val();
            

            var total = (parseFloat(montoFip) + parseFloat(montoClie) + parseFloat(montoOtros));

            //$('#idRefMProt').val($(this).attr("codRef"));
            
            $("#montTotAdeTotMProy").val(total);
            
        });

        /* ===  SOLO NUMEROS == */
        $(".noModificarValorDeTexto").keydown(function(event) {
            if(event.shiftKey)
            {
                event.preventDefault();
            }
            if(event.keyCode != 9){
                event.preventDefault();   
            }
        });
        
        
        
        $("#montoMenMCol").on("focusout",function(){
            //obtenemos la fecha de inicio y la de fin
            var fechaInicio = new Date($("#fecIniMCol").val());
            var fechaFin = new Date($("#fecFinMCol").val());

            var pagoMensual = parseFloat($(this).val());

            var difAnio = fechaFin.getYear() - fechaInicio.getYear();
            var difmes = fechaFin.getMonth() - fechaInicio.getMonth();
            var tiempo = (difAnio * 12) + difmes;

            var montoTotal = pagoMensual * tiempo;

            $("#tiempoMCol").val(tiempo);
            $("#montoMCol").val(montoTotal);
            console.log(tiempo);
        });

        $("#fecFinRealMProy").on("focusout",function(){
            //obtenemos la fecha de inicio y la de fin
            var fechaInicio = new Date($("#fecIniRealMProy").val());
            var fechaFin = new Date($("#fecFinRealMProy").val());

            var difAnio = fechaFin.getYear() - fechaInicio.getYear();
            var difmes = fechaFin.getMonth() - fechaInicio.getMonth();
            var tiempo = (difAnio * 12) + difmes;

            $("#tiempoMProy").val(tiempo);
            $("#fecEntRealMProy").val($("#fecFinRealMProy").val());
            
            
            
        });

        $("#chkObservar").on("click",function(){
            if($(this).is(":checked")){
                $("#protObservado").val("1");

            }else{
                $("#protObservado").val("0");
            }


            
        });
        //VERIFICAR SI ESTA FUNCION TRABAJA
        $("#agregar_usuario").on("click",function(){
            cod = '2';
            $.ajax({
                data : {'id':cod},
                url : '/ajax/editar_usuario/',
                type: 'get',
                success: function(data){
                    //html = '<option value="">Seleccione...</option>';
                    if(data.status=="True"){
                        
                        $("#personalExterno").addClass("hide");
                    }
                    else{
                        
                        $("#personalExterno").removeClass("hide");
                    }
                    
                    /*for(var i=0;i<data.length;i++){
                        //alert(data[x].fields.fecIniMCol + '- ' + data[x].fields.rutaPDFMCol);
                        html += '<option value="'+ data[i].pk +'">'+ data[i].fields.nomDTab +'</option>';
                                
                        }
                        $('#idDistMCli').html(html);*/

                }
            });
            
            
        });
        
        $("#nuevo_usuario").on("click",function(){
             $('#divMensaje').addClass("hide");
        });

        $("#nuevo_personal").on("click",function(){
             $('#divMensaje').addClass("hide");
        });


        $("#grabar_usuario").on("click",function(){
            
            p1 = $("#id_password").val();
            p2 = $("#id_password2").val();
            us = $("#id_username").val();
            tu = $("#id_tipoUsuario").val();
            cl = $("#id_idMCli").val();
            pr = $("#id_idMPer").val();
            //alert($("#id_fecIngreso").val());
            
            if(p1==='' || p2==='' || us==='' || tu==='' || cl==='' || pr===''){
                $('#mensaje_modal').removeClass("hide");
                $('#mensaje').text('Deben ingresarse todos los campos.');
            }
            else{
                if(p1!=p2){
                    $('#mensaje_modal').removeClass("hide");
                    $('#mensaje').text('Las constraseñas no coinciden.');

                }
                else{
                    var frm = $('#form_nuevo_usuario');
                    frm.serialize()
                    console.log(frm.attr("method"));
                    $.ajax({
                        type: 'post',
                        url: '/administracion/usuarios/',
                        data: frm.serialize(),
                        success: function (data) {
                            //alert(data.mensaje);
                            /*$(':input','#form_nuevo_usuario')
                                .not(':button, :submit, :reset, :hidden')
                                .val('')
                                .removeAttr('checked')
                                .removeAttr('selected');*/
                            $('#nuevo_usuario_modal').modal('hide');
                            html = '<tr class="text-info" id="tr'+ data.id +'"><td class="text-center">'+data.id+'</td><td class="nombre">'+data.last_name+'</td><td>'+data.first_name+'</td><td>'+data.username+'</td><td>'+data.tipoUsuario+'</td><td>'+ data.fecIngreso+'</td>';
                            html += '<td><a href="#" class="editar_registro" codigo="' + data.id + '" modelo="0"><span class="text-warning glyphicon glyphicon-pencil"></span></a></td><td ><a href="#" class="eliminar_registro" codigo="' + data.id + '" modelo="0"><span class="text-danger glyphicon glyphicon-trash"></span></a></td></tr>';
                            frm[0].reset();
                            $('#tabla').prepend(html);
                            $('#div_mensaje').removeClass("hide");
                            $('p#mensaje').text('Se ha registrado un nuevo usuario');

                        },
                        error: function(data) {
                            //alert('Ha sucedido un error' + data.mensaje);
                            $(':input','#form_nuevo_usuario')
                                .not(':button, :submit, :reset, :hidden')
                                .val('')
                                .removeAttr('checked')
                                .removeAttr('selected');
                            $('#nuevo_usuario_modal').modal('hide');
                            $('#div_mensaje').removeClass("hide");
                            $('#mensaje').text(data.mensaje + ', ' + data.status );
                        }
                    });   
                }
            }
        });
        
        
        $("#grabar_personal").on("click",function(){
            
            ap = $("#id_ApePMPer").val();
            am = $("#id_ApeMMPer").val();
            nom = $("#id_NomMPer").val();
            fn = $("#id_FechNacMPer").val();
            tp = $("#id_IdTipPerMPer").val();
            td = $("#id_IdTipDocMPer").val();
            nd = $("#id_NDocMPer").val();
            fi = $("#id_FecIngMPer").val();
            te = $("#id_Tel1MPer").val();
            em1 = $("#id_Email1MPer").val();
            ia = $("#id_IdArea").val();

            
            if(ap==='' || am==='' || nom===''){
                $('#mensaje_modal').removeClass("hide");
                $('#mensaje').text('Deben ingresarse todos los campos'); 
            }
            else{
                
                    var frm = $('#frm_nuevo_personal');
                    //alert(frm.attr('method'));
                    $.ajax({
                        type: 'post',
                        url: '/administracion/personal/',
                        data: frm.serialize(),
                        success: function (data) {

                            //alert(data.mensaje);
                            /*$(':input','#form_nuevo_personal')
                                .not(':button, :submit, :reset, :hidden, ')
                                .val('')
                                .removeAttr('checked')
                                .removeAttr('selected');*/
                            
                            html = '<tr class="text-info text-center"><td>'+data[0].pk+'</td><td>'+data[0].fields.ApePMPer +' ' +data[0].fields.ApeMMPer +'</td><td>'+data[0].fields.NomMPer+'</td><td>'+data[0].fields.FechNacMPer+'</td><td>'+data[0].NDocMPer+'</td><td>'+ data[0].fields.Tel1MPer+'</td><td>'+ data[0].fields.Email1MPer +'</td>';
                            html += '<td><a href="#" class="editar_registro" codigo="' + data[0].pk + '" modelo="4"><span class="text-warning glyphicon glyphicon-pencil"></span></a></td><td ><a href="#" class="eliminar_registro" codigo="' + data[0].pk + '" modelo="4"><span class="text-danger glyphicon glyphicon-trash"></span></a></td></tr>';
                            frm[0].reset();
                            
                            $('#mensaje_modal').removeClass("hide");
                            $('#mensaje_personal').text('success'+data.mensaje);
                            $('#nuevo_personal_modal').modal('hide');
                            $('#tabla').append(html);

                        },
                        error: function(data) {
                            //$('#nuevo_personal_modal').modal('hide');
                            $('#mensaje_modal').removeClass("hide");
                            $('#mensaje_personal').text('Error: ' + data.mensaje);
                        }
                    });   
                
            }
        });
        
        $("#btn_modificar_password").on("click",function(){
            
            pass1 = $("#pass1").val();
            pass2 = $("#pass2").val();
            if(pass2==='' || pass1===''){
                $('#divMensajePassword').removeClass("show");
                $('#mensaje_modificar_password').text('Ingresar datos en ambos campos.');
            }else{
                if(pass2===pass1){

                    $.ajax({
                        data : {'password':pass1, 'codigo':''},
                        url: '/ajax/modificar_password/',
                        type: 'get',
                        success: function(data){
                            if(data.estado === true){
                                alert("Se actualizo la contraseña!.");
                            }else{
                                alert("No se logro actualizar la contraseña. Error: " + data.mensaje);
                                $("#modificar_password_modal").modal("hide");   
                            }
                            $("#modificar_password_modal").modal("hide");
                        },
                        error: function(data){
                            alert("Sucedió un error al comunicarse con el servidor.");
                            $("#mensaje_modificar_password").text(data.mensaje);

                        }
                    });

                }
                else{
                    $("#divMensajePassword").removeClass("hide");
                    $("#mensaje_modificar_password").text("Las contraseñas no coinciden");
                }
            }
            
            
            
        });
        
         $("#btnCargarPresupuesto").on("click",function(){
            $("#cargador").show();
         });
         

});
