$(function(){
    $('#showPhone').on('click', function(){
        var span = $(this)
        var url = span.data('url')
        var token = $('[name=csrfmiddlewaretoken]').val()
        $.ajax({
            url: url,
            type: "POST",
            headers: {
                'X-CSRFToken': token,
            },

            success:function(data){
                span.html(data)
            },
            error:function(data){
                $('html').html(data['responseText'])
            }
        })
    })
})