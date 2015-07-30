var markers = [];
var map;
var lat;
var lng;

function initialize() {

  map = new google.maps.Map(document.getElementById('map-div'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	  zoom: 11
  });

  var input = (document.getElementById('pac-input'));
  var geocoder = new google.maps.Geocoder();

  // Try HTML5 geolocation
  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map.setCenter(pos);
      placeMarker(pos, map, "", true);
      lat = pos.lat()
      lng = pos.lng()

      //Get current address string and set to input address field

      geocoder.geocode({'location': pos}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          $("#pac-input").val(results[0].formatted_address);
          //infowindow.setContent(results[1].formatted_address);
        } else {
          window.alert('No fué posible encontrar su dirección, por favor introduzca su dirección manualmente');
        }
        } else {
          window.alert('No fué posible encontrar su dirección, por favor introduzca su dirección manualmente: ' + status);
        }
      });

    }, function() {
      //GeoLocation service failed
      map.setCenter(new google.maps.LatLng(20.711076, -103.410004));
    });
  } 
  else {
    // Browser doesn't support Geolocation
    map.setCenter(new google.maps.LatLng(20.711076, -103.410004));
  }

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
    lat = place.geometry.location.A;
    lng = place.geometry.location.F;

    placeMarker(place.geometry.location, map, place.title);
    map.setCenter(place.geometry.location);
  });

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
        lat = event.latLng.lat();
        lng = event.latLng.lng();
        //reverse geocoding
        geocoder.geocode({'location': new google.maps.LatLng(lat, lng)}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
              $("#pac-input").val(results[0].formatted_address);
            } else {
              window.alert('No fué posible encontrar su dirección, por favor introduzca su dirección manualmente');
            }
            } else {
              window.alert('No fué posible encontrar su dirección, por favor introduzca su dirección manualmente: ' + status);
            }
        });
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


  $("#contact-form").submit(function( event ) {
    event.preventDefault();
    $("#latInput").val(lat);
    $("#lngInput").val(lng);
    var posting = $.post('/contacts/save', $("#contact-form").serialize());
    
    posting.done(function( data ) {
      console.log(data);
      //$( "#result" ).empty().append( content );
    });

  });


});

google.maps.event.addDomListener(window, 'load', initialize);