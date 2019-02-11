function call_url(url) {
    $.ajax({
      url: url,
      complete: function(xhr, statusText) {
          location.reload()
      }
    })
}


function search(url) {
    let key = $('#search-key').val();
    window.open(url + key, '_self');
}
