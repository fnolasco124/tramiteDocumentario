var nombre_tabla = "#tabla"; // id
var nombre_boton_eliminar = ".delete"; // Clase
var nombre_formulario_modal = "#frmEliminar"; //id
var nombre_ventana_modal = "#myModal"; // id

    $(document).on('ready',function(){
        $("#suprimir").on('click',function(e){
            //alert('estamos aki');
            $( "#myModal").modal("show");
            //e.preventDefault();
            var nombres = [];
            $('input[name="chk[]"]:checked').each(
                function ()
                {
                    
                    //alert($(this).val());
                    nombres.push($(this).val());
                });
            alert(nombres.join("\n"));
            
            //listaId.push($(this).attr("value"))
            //alert(listaId)
            $('#modal_numItems').text(nombres.length);
            $('#modal_id').val(nombres);
            //alert(nuevo);
        });
        

        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            var id = $(this).attr('id');
            var nombre = $(this).data('name');
            $('#modal_id').val(id);
            $('#modal_numItems').text(id.length());
        });

         var options = {
                success:function(response)
                {
                    alert(response.status);
                    if(response.status=="True"){
                        alert("Eliminado!");
                        //alert(response.cadEnvio);
                        //var idObj = response.cadEnvio;
                        var elementos= $(nombre_tabla+' >tbody >tr').length;
   
                        if(elementos==1){
                                location.reload();
                        }else{
                            for (var i=0;i<listaId.length;i++){
                                $('#tr'+listaId[i]).remove();    
                                //alert(idObj[i]);
                            }                                                                        
                            $(nombre_ventana_modal).modal('hide');
                        }                        
                    }else{
                        alert("Hubo un error al eliminar!");
                        $(nombre_ventana_modal).modal('hide');
                    };
                }
            };
        $(nombre_formulario_modal).ajaxForm(options);
        //Codigo para borrar los registros seleccionados
        


});
    
    
        
            
        
