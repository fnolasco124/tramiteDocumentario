    $(document).on('ready',function(){
        
        var options = {
                alert('here');
                success:function(response)
                {
                	alert("Esto es lo que llega!");
                    
                    if(response.status=="True"){
                        alert("Esto es lo que llega!");
                        //alert(response.cadEnvio);
                        //var idObj = response.cadEnvio;
                        //var elementos= $(nombre_tabla+' >tbody >tr').length;
   
                        //if(elementos==1){
                        //        location.reload();
                        //}else{
                        //    for (var i=0;i<listaId.length;i++){
                        //        $('#tr'+listaId[i]).remove();    
                                //alert(idObj[i]);
                        //    }                                                                        
                            $('#AgregarDetalleProtocolo').modal('hide');
                        }                        
                    }else{
                        alert("Hubo un error al eliminar!");
                        $('#AgregarDetalleProtocolo').modal('hide');
                    };
                }
            };
        $('#frmDetalleProtocolo').ajaxForm(options);

        $("#suprimir").on('click',function(e){
            e.preventDefault();
            //var i=0
            var nuevo=[];
            $(".select").each(function(){
                if ($(this).attr("checked")){
                    //i++;
                    //($(this).attr("value"),false);
                    //nuevo.push($(this).attr("value"));
                    listaId.push($(this).attr("value"))
                }
            });
            $('#modal_numItems').text(listaId.length);
            $('#modal_id').val(listaId);
            //alert(nuevo);
        });

       
        
});
    
    
        
            
        
