function call_url(url) {
    $.ajax({
      url: url,
      complete: function(xhr, statusText) {
        if(statusText === 'success'){
            $('body').append(
                "<div class=\"w-100 h-100 d-flex flex-row justify-content-center align-items-center position-fixed\" style='top: 0; background-color: rgba(0,0,0,0.3); z-index: 2000'><div class=\"alert alert-success position-absolute m-5\" " +
                "role=\"alert\">" + $.parseJSON(xhr.responseText).message + "</div></div>");
            setTimeout(function(){
                location.reload()
            }, 1500);
        } else {
            alert(xhr.status)
        }
      }
    })
}


function search(url) {
    let key = $('#search-key').val();
    window.open(url + key, '_self');
}
