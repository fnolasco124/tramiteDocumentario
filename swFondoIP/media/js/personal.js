   $().ready(function () {
            $("#frmPersonal").validate({
                debug: false,
                
                rules: {

                    //FORMULARIO PERSONAL
                    idMPer : {required :true },
                    apePMPer : {required:true},
                    apeMMPer : {required:true},
                    nomMPer : {required:true},
                    fechNacMPer : {required:true},
                    idTipPerMPer : {required:true},
                    idTipDocMPer : {required:true},
                    nDocMPer : {required:true},
                    //estMPer = {required:true},
                    fecIngMPer : {required:true}
                },
                messages: {
                  
                    //FORMULARIO CLIENTE
                    //FORMULARIO PERSONAL
                    idMPer : "Ingrese un codigo",
                    apePMPer : "Campo obligatorio",
                    apeMMPer : "Campo obligatorio",
                    nomMPer : "Campo obligatorio",
                    fechNacMPer : "Campo obligatorio",
                    idTipPerMPer : "Campo obligatorio",
                    idTipDocMPer : "Campo obligatorio",
                    nDocMPer : "Campo obligatorio",
                    //estMPer = {required:true},
                    fecIngMPer : "Campo obligatorio"
                }
            });
        });