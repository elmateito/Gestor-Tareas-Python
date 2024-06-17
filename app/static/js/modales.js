$(document).ready(function(){
    $('#btnAct').click (function(){
        $('modalContent').load('templates/modaltareas.html')
    })
})

function cargarModal(){
    $('#Musuarios').load(ruta, function(){
        $('#Musuarios').modal('show')
    })
}