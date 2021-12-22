$(document).ready(function() {
    $("#invite_form").on('submit',function (e) {
        e.preventDefault();
        const data = $("#invite_form").serialize()
        $.post('/', data, function (res) {
            console.log(res)
        }).done(function(res) {
            const alert_content = `
            <div class="alert alert-primary" role="alert">
                ${res}
            </div>
            `
            $('#alert_container').html(alert_content);
            setTimeout(function(){
                $('#alert_container').html('');
            }, 3000);
        }).fail(function(e) {
            const alert_content = `
            <div class="alert alert-danger" role="alert">
                ${e.responseText}
            </div>
            `
            $('#alert_container').html(alert_content);
            setTimeout(function(){
                $('#alert_container').html('');
            }, 3000);
        })
    })
})