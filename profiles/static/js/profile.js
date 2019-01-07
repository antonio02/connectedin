function call_url(url) {
    $.ajax({
      url: url,
      complete: function(xhr, textStatus) {
        if(xhr.status == 200){
            location.reload();
        } else {
            alert(xhr.status)
        }
      }
    })
}
