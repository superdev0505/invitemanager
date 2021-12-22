$(document).ready(function() {
    $("#invite_form").on('submit',function (e) {
        e.preventDefault();
        const data = $("#invite_form").serialize()
        $.post('/', data, function (res) {
            console.log(res)
        }).done(function(res) {
            alert( res );
        }).fail(function(e) {
            alert( e.responseText );
        })
    })
})