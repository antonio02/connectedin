$(document).ready(function() { var form = $('#new-post-form');
    form.submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            complete: function(xhr, textStatus) {
                if(xhr.status === 200){
                    location.reload();
                } else {
                    alert(xhr.status);
                }
            }
        });
        return false;
    });
});