var markers = [];
var map;

function initialize() {

  map = new google.maps.Map(document.getElementById('map-div'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	  zoom: 11
  });

  // Try HTML5 geolocation
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map.setCenter(pos);
      placeMarker(pos, map, "aquí estás", true);
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
    var lat = place.geometry.location.A;
    var lng = place.geometry.location.F;

    placeMarker(place.geometry.location, map, place.title);
    map.setCenter(place.geometry.location);
  });

  function searchClosestContacts(lat, lng, radius){
    var url = "/search";
    $.get(url, {"lat":lat, "lng":lng, "radius":radius}, function(data, status){
      if(status === "success"){
        placePins(data.items);
        displayResults(data.items);
      }
    }, "json");
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

  function placeMarker(position, map, title) {
	  var marker = new google.maps.Marker({
	    position: position,
	    map: map,
      animation: google.maps.Animation.DROP,
      draggable: true,
      title: title
	  });

    google.maps.event.addListener(marker,'dragend',function(event) {
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();
      });

    markers.push(marker);
  }

}

$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

google.maps.event.addDomListener(window, 'load', initialize);