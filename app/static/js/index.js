var radius = 10;
var markers = [];
var map;

var searchResultHTML = "<dt class='listBorder resultEntry'></dt>";
var institutionNameHTML = "<div>%data%</div>";
var contactNameHTML = "<div>%data%</div>";
var addressHTML = "<div>%data%</div>";
var HTMLtags = "<div class='tagsEntry'></div>";
var HTMLtagEntry = "<span class='label label-default'>%DATA%</span>";

function initialize() {

  map = new google.maps.Map(document.getElementById('map-div'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	  zoom: 11,
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
  //map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

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
    markers = [];
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
        //console.log(data.items);
        placePins(data.items);
        displayResults(data.items);
      }
    }, "json");
  }

  function displayResults(items){
    $("#custom-counter").empty();
    for(var i = 0; i < items.length; i++){
      $("#custom-counter").append(searchResultHTML);
      $(".resultEntry:last").append(contactNameHTML.replace("%data%", items[i].c_name));
      $(".resultEntry:last").append(institutionNameHTML.replace("%data%", items[i].name));
      $(".resultEntry:last").append(addressHTML.replace("%data%", items[i].address));
      if(items[i].tags != undefined && items[i].tags.length > 0){
        $(".resultEntry:last").append(HTMLtags);
      }
      for(var x = 0; x < items[i].tags.length; x++){
        $(".tagsEntry:last").append(HTMLtagEntry.replace("%DATA%", items[i].tags[x].name));
      }

    }
    $("#leftMenu").show("slow","swing", function(){ $("#leftMenuMin").hide(); });
  }

  function placePins(items){
    for(var i = 0; i < items.length; i++){
      console.log(items[i]);
      var latlng = new google.maps.LatLng(items[i].lat,items[i].lng);
      placeMarker(latlng, map, items[i].name, false, i + 1);
    }
  }

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });

  /*google.maps.event.addListener(map, 'click', function(e) {
    var lat = e.latLng.A;
    var lng = e.latLng.F;
    clearMarkers();
    placeMarker(e.latLng, map, "", true);
    searchClosestContacts(lat, lng, radius);
    map.setCenter(e.latLng);
  });*/

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
    }
    markers.push(marker);
  }
}

$(document).ready(function(){
  $("#filterBtn").click(function(){ $("#filterBox").toggle("slow","swing") } );
  $("#busquedaBtn").click(function(){ $("#leftMenu").show("slow","swing", function(){ $("#leftMenuMin").hide(); })  } );
  $("#collapse").click(function(){ $("#leftMenu").hide( function(){ $("#leftMenuMin").show("slow","swing"); }) } );
  $("#maximize").click(function(){ $("#leftMenu").show( function(){ $("#leftMenuMin").hide()  ; }) } );
});

google.maps.event.addDomListener(window, 'load', initialize);