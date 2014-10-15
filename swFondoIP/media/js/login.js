   $().ready(function () {
            $("#frmLog").validate({
                debug: false,
                //FORMULARIO LOGIN
                rules: {
                    username: { required: true, minlength: 2},
                    password: { required: true, minlength: 2}
                    
                },
                messages: {
                    //FORMULARIO USUARIO
                    username: "Campo obligatorio",
                    password: "Campo obligatorio"
                    
                   
                }
            });
        });