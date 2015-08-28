var HTMLcontact = "<div class='list-group'><a href='#' class='list-group-item list-group-item-success'><h4 class='list-group-item-heading'>%DATAHEAD%</h4><p class='list-group-item-text'>%ADDRESS%</p><p class='list-group-item-text'>%TELEPHONE%</p><p class='list-group-item-text'>%EMAIL%</p></div></div>";


$(document).ready(function() {

  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $('#registeredOrganizations').on('mouseenter', '.list-group-item', function(){
    $(this).addClass('active');
  });
  $('#registeredOrganizations').on('mouseleave', '.list-group-item', function(){
    $(this).removeClass('active');
  });

  $('#organization-form').validator().on('submit', function (e) {
    if (e.isDefaultPrevented()) {
      // handle the invalid form...
      console.log("invalid form");
    } else {
      e.preventDefault();
      var posting = $.post('/registro/save', $("#organization-form").serialize());
      
      posting.done(function( data ) {
        if(data === 'success'){
          clearFormFields();
          $("#result").removeClass("error");
          $("#result").text("ORGANIZACION GUARDADA CORRECTAMENTE");

          $.get("/institutions", function(data, status){
            if(status === 'success') {
              displayOrganizations(data.items);
            }
          });

        }else{
              $("#result").addClass("error");
              $("#result").text(data);
            }
      });
    }
  });
}); 

function clearFormFields(){
  $(":input").not("#pac-input").not(':hidden').val('');
  $(".checkbox").each(function(i){
    if($(this).prop('checked')){
      $(this).click();
    }
  });
}

function displayOrganizations(items) {
  $("#registeredOrganizations").empty();
  for(var i = 0; i < items.length; i++) {
    var HTMLstring = HTMLcontact.replace("%DATAHEAD%", items[i].name).replace("%ADDRESS%", items[i].address).replace("%TELEPHONE%", items[i].phone1).replace("%EMAIL%", items[i].email);
    $("#registeredOrganizations").append(HTMLstring);
  }
}