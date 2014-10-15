   $().ready(function () {
            $("#frmUser").validate({
                debug: false,
                //FORMULARIO USUARIO
                rules: {
                    idMPer      : { required: true },
                    logMUsu     : { required: true },
                    claMUsu     : { required: true, minlength: 8 },
                    claMUsu2    : { required: true, minlength: 8, equalTo:"#claMUsu" },
                    permMUsu    : { required: true },
                    estMUsu     : { required: true },
                    fecIngMUsu  : { required: true }
                    
                },
                messages: {
                    //FORMULARIO USUARIO
                    idMPer      : "Seleccione un personal",
                    idMUsu      : "Seleccione un personal",
                    logMUsu     : "Ing. el nombre de usuario",
                    claMUsu     : "Ing. una contraseña",
                    claMUsu2    : "Confirme contraseña",
                    permMUsu    : "Seleccione los permisos del usuario",
                    estMUsu     : "Seleccione un estado",
                    fecIngMUsu  : "Seleccione fecha"
                }
            });
        });