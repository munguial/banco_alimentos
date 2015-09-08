var radius = 10;
var markers = {};
var map;
var results = {};
var checked_tags = {}

var searchResultHTML = "<dt class='listBorder resultEntry' id='result-%DATA%'></dt>";
var institutionNameHTML = "<div>%data%</div>";
var contactNameHTML = "<div class='contact-name'>%data%</div>";
var contactDistanceHTML = "<span class='contact-distance'>  - Distancia: %data% km</span>";
var addressHTML = "<div>%data%</div>";
var HTMLtags = "<div class='tagsEntry'></div>";
var HTMLtagEntry = "<span class='label label-default'>%DATA%</span>";
var HTMLtagBarEntry = "<div class='object-tag' value='%data%'>%data%</div>";
var HTMLlargeDescription = "<div class='contact-description' hidden></div>";
var HTMLlargeDescPhone1 = "<div>Tel: %DATA%</div>";
var HTMLlargeDescPhone2 = "<div>Tel: %DATA%</div>";
var HTMLlargeDescNotes = "<div>%DATA%</div>";
var HTMLlargeDescUrl = "<div>Página web: <a href='%DATA%'>%DATA%</a></div>";
var HTMLlargeDescEmail = "<div>Email: %DATA%</div>";
var HTMLlargeDescIDescription = "<div>%DATA%</div>";

function initialize() {
  //Initialize Map
  map = new google.maps.Map(document.getElementById('map-div'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	  zoom: 12,
    scrollwheel: false
  });

  // Try HTML5 geolocation
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map.setCenter(pos);
      placeMarker(pos, map, "aquí estás", true, 0);
      searchClosestContacts(pos.lat(), pos.lng(), radius);
    }, function() {
      //GeoLocation service failed
      map.setCenter(new google.maps.LatLng(20.711076, -103.410004));
    });
  }
  else {
    // Browser doesn't support Geolocation
    map.setCenter(new google.maps.LatLng(20.711076, -103.410004));
  }

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));

  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    clearMarkers();

    // For each place, get the icon, place name, and location.
    markers = {};
    var bounds = new google.maps.LatLngBounds();

    var place = places[0];
    var lat = place.geometry.location.lat();
    var lng = place.geometry.location.lng();

    placeMarker(place.geometry.location, map, place.title, true, 0);
    map.setCenter(place.geometry.location);
    searchClosestContacts(lat, lng, radius);
  });

  function searchClosestContacts(lat, lng, radius){
    var url = "/search";
    $.get(url, {"lat":lat, "lng":lng, "radius":radius}, function(data, status){
      if(status === "success"){
        results = data.items;
        buildTagsFilter(results);
        placePins(results);
        displayResults(results);
        $("#tagCounter").css("display","none");
      }
    }, "json");
  }

  function buildTagsFilter(items) {
    $("#tags-div").empty();
    var tagsSet = {};
    for(var i = 0; i < items.length; i++){
      if(items[i].tags != undefined && items[i].tags.length > 0) {
        for(var x = 0; x < items[i].tags.length; x++){
          tagsSet[items[i].tags[x].name] = true;
        }
      }
    }
    var keys = [];
    for(var k in tagsSet){
      keys.push(k);
    }
    for(var i = 0; i < keys.length; i++){
      //console.log(keys[i]);
      $("#tags-div").append(HTMLtagBarEntry.replace("%data%", keys[i]).replace("%data%", keys[i]));
    }
  }

  function displayResults(items){
    $("#custom-counter").empty();
    if(filterExists()){
      items = filterResults(items);
    }
    for(var i = 0; i < items.length; i++){
      $("#custom-counter").append(searchResultHTML.replace("%DATA%", i + 1));
      $(".resultEntry:last").append(contactNameHTML.replace("%data%", items[i].c_name));
      var distance = Math.floor(items[i].distance * 100) / 100;
      $(".contact-name:last").append(contactDistanceHTML.replace("%data%", distance));
      $(".resultEntry:last").append(institutionNameHTML.replace("%data%", items[i].i_name));
      $(".resultEntry:last").append(addressHTML.replace("%data%", items[i].address));

      var largeDescDiv = $(HTMLlargeDescription);
      if(items[i].telephone1 != undefined && items[i].telephone1 != "") largeDescDiv.append(HTMLlargeDescPhone1.replace("%DATA%", items[i].telephone1));
      if(items[i].url != undefined && items[i].url != "") largeDescDiv.append(HTMLlargeDescUrl.replace("%DATA%", items[i].url).replace("%DATA%", items[i].url));
      if(items[i].email != undefined && items[i].email != "") largeDescDiv.append(HTMLlargeDescEmail.replace("%DATA%",items[i].email));
      if(items[i].i_description != undefined && items[i].i_description != "") largeDescDiv.append(HTMLlargeDescIDescription.replace("%DATA%", items[i].i_description));
      $(".resultEntry:last").append(largeDescDiv);

      if(items[i].tags != undefined && items[i].tags.length > 0){
       $(".resultEntry:last").append(HTMLtags);
       for(var x = 0; x < items[i].tags.length; x++){
          $(".tagsEntry:last").append(HTMLtagEntry.replace("%DATA%", items[i].tags[x].name));
       }
      }
    }
    $("#leftMenu").show("slow","swing", function(){ $("#leftMenuMin").hide(); });
  }

  function placePins(items){
    if(filterExists()){
      items = filterResults(items);
    }
    for(var i = 0; i < items.length; i++){
      var latlng = new google.maps.LatLng(items[i].lat,items[i].lng);
      placeMarker(latlng, map, items[i].name, false, i + 1);
    }
  }

  function filterResults(items) {
    checked_tags = {};
    filtered_items = [];
     $(".object-tag.selected").each(function(){
        checked_tags[$(this).attr('value')] = true;
     });

     for(var i = 0; i < items.length; i++) {
      if(items[i].tags != undefined && items[i].tags.length > 0){
       for(var x = 0; x < items[i].tags.length; x++){
          if(checked_tags[items[i].tags[x].name]){
            filtered_items.push(items[i]);
            break;
          }
        }
      }
    }
    results = filtered_items;
    return filtered_items;
  }

  function filterExists(){
    var count = 0;
    $(".object-tag.selected").each(function(){ count++; });
    return count > 0;
  }

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });

  function clearMarkers(){
    for (var i = 0, marker; marker = markers[i]; i++) {
      marker.setMap(null);
    }
  }

  function clearResultsMarkers(){
    for (var i = 0, marker; marker = markers[i]; i++) {
      if(marker.draggable === undefined){
        marker.setMap(null);
      }
    }
  }

  function placeMarker(position, map, title, isSetByUser, n) {
    var marker;
    if(isSetByUser) {
      marker = new google.maps.Marker({
        position: position,
        map: map,
        animation: google.maps.Animation.DROP,
        title: title,
        draggable: true
      });

      google.maps.event.addListener(marker,'dragend',function(event) {
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();
        clearResultsMarkers();
        searchClosestContacts(lat, lng, radius);
      });
    }
    else{
      marker = new google.maps.Marker({
        position: position,
        map: map,
        animation: google.maps.Animation.DROP,
        //icon: "static/images/icon.png",
        icon : 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + n + '|1e90ff|000000',
        title: title
      });

      marker.addListener('mouseover', function(){
          $("#result-" + n).effect('highlight', {color:"#50AE55"}, 1500);
          var scrollDiv = document.getElementById('result-' + n);
          var topPos = scrollDiv.offsetTop;
          document.getElementById('leftMenu').scrollTop = topPos;
      });

      marker.addListener('click', function(){
          var contactDiv = document.getElementById('result-' + n);
          toggleLongDesc(contactDiv);
          $("#result-" + n).effect('highlight', {color:"#50AE55"}, 1500);
      });
    }
    markers[n] = marker;
  }

  $("#filterBox").on('click', 'input:checkbox', function(){
     var filtered = filterResults(results);
     clearResultsMarkers();
     placePins(filtered);
     displayResults(filtered);
  });

  $("#tags-div").on('click', '.object-tag', function(){
    $(this).toggleClass("selected");
  });

  $("#custom-counter").on({
      mouseenter: function(){
          var n = $(this).attr('id').split('-')[1];
          $(this).addClass('highlight', 200);
          markers[n].setAnimation(google.maps.Animation.BOUNCE);
      },
      mouseleave: function() {
          var n = $(this).attr('id').split('-')[1];
          $(this).removeClass('highlight', 200);
          markers[n].setAnimation(null);
      }
    }, '.resultEntry');

  $("#custom-counter").on('click', '.resultEntry', function(){
      toggleLongDesc($(this));
  });

  function toggleLongDesc(divElement){
      var largeDescDiv = $('.contact-description', divElement);
      largeDescDiv.slideToggle('slow');
  }

  $("#filterButton").click(function(){
    $('#myModal').modal('hide');
     clearResultsMarkers();
     placePins(results);
     displayResults(results);
     var numItems = $('div.object-tag.selected').size();
     if(numItems > 0){
        $('#tagCounter').html(numItems);
        $("#tagCounter").css("display","inline-block");
     }
     else{
        $("#tagCounter").css("display","none");
     }
  });



  //$('.SlectBox').SumoSelect({ okCancelInMulti: true, selectAll: true, selectAlltext: 'Todo', placeholder: 'Filtrar resultados' });
  //$('#example-getting-started').multiselect({ buttonWidth: '300px', dropRight: true, maxHeight: 250, nonSelectedText: 'Filtrar resultados', includeSelectAllOption: true, selectAllText: 'Seleccionar todo'});

  //$("#filterBtn").click();
}

$(document).ready(function(){
  $("#collapse").click(function(){ $("#leftMenu").hide( function(){ $("#leftMenuMin").show("slow","swing"); }) } );
  $("#maximize").click(function(){ $("#leftMenu").show( function(){ $("#leftMenuMin").hide()  ; }) } );
});

google.maps.event.addDomListener(window, 'load', initialize);
