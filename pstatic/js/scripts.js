$(document).ready(function(){
	document.getElementById('copyright').innerHTML = new Date().getFullYear();
});


function CallForm(ele){

  $.ajax({
    url : $(ele).data('url'),
    success: function(){
      var here = '';

    }
  })
};

function AjaxLink(ele){
  var btn = $(ele).button("loading");
  var showinmodal = $(ele).data('showinmodal');
  $.ajax({
    url : $(ele).data('url'),
    success: function(responsedata){
      if (showinmodal == "True"){
        console.log(responsedata);
        $('#ajax-modal-content').html(responsedata);
        $('#ajax-modal').modal('show');
      }
      else{
      var newthin = '<label class="label label-warning">' + responsedata + '</label>';
      $(ele).replaceWith(newthin);
      }
    }
  });
  btn.button('reset');
};


