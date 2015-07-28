var radius = 5;
var markers = [];
var map;
var searchResultHTML = "<div class='resultEntry'></div></br>";
var HTMLcontactName = "<div class'contactName'>%data%</div>";
var HTMLcontactAddress = "<div class'contactAddress'>%data%</div>";
var HTMLcontactNotes = "<div class'contactNotes'>%data%</div>";

function initialize() {

  var myLatlng = new google.maps.LatLng(20.711076, -103.410004);
  map = new google.maps.Map(document.getElementById('map-div'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: myLatlng,
	zoom: 13
  });

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

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
    searchClosestContacts(lat, lng, radius);
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

  function displayResults(items){
    $("#searchResults").empty();
    for(var i = 0; i < items.length; i++){
      $("#searchResults").append(searchResultHTML);
      $(".resultEntry:last").append(HTMLcontactName.replace("%data%", items[i].name));
      $(".resultEntry:last").append(HTMLcontactAddress.replace("%data%", items[i].address));
      $(".resultEntry:last").append(HTMLcontactNotes.replace("%data%", items[i].notas));
    }
  }

  function placePins(items){
    for(var i = 0; i < items.length; i++){
      console.log(items[i]);
      var latlng = new google.maps.LatLng(items[i].lat,items[i].lng);
      placeMarker(latlng, map, items[i].name);
    }
  }

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });

  google.maps.event.addListener(map, 'click', function(e) {
    var lat = e.latLng.A;
    var lng = e.latLng.F;
    clearMarkers();
    placeMarker(e.latLng, map, "");
    var contacts = searchClosestContacts(lat, lng, radius);
    map.setCenter(e.latLng);
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
      title: title
	  });
    markers.push(marker);
  }

}

google.maps.event.addDomListener(window, 'load', initialize);