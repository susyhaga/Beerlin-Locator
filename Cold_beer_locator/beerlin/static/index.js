let markers;
let map;
const image =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
// Initialize and add the map
function initMap(local) {
  // The location of Uluru
  const berlin = { lat: 52.520008, lng: 13.404954 };

  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: berlin,
    fullscreenControl: false,
    streetViewControl: false, 
    mapTypeId: "roadmap",
  });


  var mapStyles = [ 
{ 
  "featureType": "administrative", 
  "stylers": [ { "visibility": "on" } ] 
},{ 
  "featureType": "road", 
  "elementType": "labels", 
  "stylers": [ { "visibility": "on" } ] 
},{ 
  "featureType": "road", 
  "elementType": "geometry.stroke", 
  "stylers": [ { "visibility": "on" } ] 
},{ 
  "featureType": "transit", 
  "stylers": [ { "visibility": "on" } ] 
},{ 
  "featureType": "poi.attraction", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.business", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.government", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.medical", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.park", 
  "elementType": "labels", 
  "stylers": [ { "visibility": "off" } ]                  
},{ 
  "featureType": "poi.place_of_worship", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.school", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
  "featureType": "poi.sports_complex", 
  "stylers": [ { "visibility": "off" } ] 
},{ 
"featureType": "road", 
"elementType": "geometry.fill", 
"stylers": [ 
    { "visibility": "on" }, 
    { "color": "#ffffff" }
] 
},{ 
  "featureType": "landscape.man_made", 
  "stylers": [ 
      { "visibility": "off" }, 
      { "color": "#E8E8E8" } 
  ] 
},{ 
  "featureType": "landscape.natural", 
  "elementType": "labels", 
  "stylers": [ { "visibility": "off" } ] 
}
];  
map.setOptions({ styles: mapStyles });


google.maps.event.addListener(map, 'idle', function(){
var zoom = map.getZoom();
var center = map.getCenter();
console.log("Map idle zoom:"+zoom);
console.log("Map idle center:"+center);
renderMarkers(center, zoom);
});




  const image =
    "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";

  const return_query = local;

  
  // const add_to_map = return_query.forEach(
  //   (place) => {
  //     new google.maps.Marker({
  //       position: { lat: place[1], lng: place[2] },
  //       map: map,
  //       title: place[0],
  //       icon: image,
  //     });
  //   }
  // );

  // The marker, positioned at Uluru

  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });
  let markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];
    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };
      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        })
      );

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });



var radiusToZoomLevel = [
1000000, // zoom: 0
1000000, // zoom: 1
900000, // zoom: 2
800000, // zoom: 3
700000, // zoom: 4
600000, // zoom: 5
500000, // zoom: 6
400000, // zoom: 7
300000, // zoom: 8
200000, // zoom: 9
100000, // zoom: 10
50000, // zoom: 11
20000, // zoom: 12
10000, // zoom: 13
8000, // zoom: 14
6000, // zoom: 15
3000, // zoom: 16
1500, // zoom: 17
1000, // zoom: 18
500,  // zoom: 19
100   // zoom: 20
];

function renderMarkers(mapCenter, zoomLevel) {
// If we had already some markers in the map, we need to clear them
clearMarkers();

// we call the backend to get the list of markers
var params = {
"lat" : mapCenter.lat(),
"lng" : mapCenter.lng(),
"radius" : radiusToZoomLevel[zoomLevel]
}
var url = "http://127.0.0.1:5000/api/get_stores_in_radius?" + dictToURI(params) 
loadJSON(url, function(response) {
// Parse JSON string into object
var actual_JSON = JSON.parse(response);
console.log(actual_JSON);

// place new markers in the map
placeStoresInMap(actual_JSON)
});
}

var DEFAULT_ICON = {
path: mapIcons.shapes.MAP_PIN,
fillColor: '#696969',
fillOpacity: 1,
strokeColor: '#9c4343',
strokeWeight: 1.5
}

var SELECTED_ICON = {
path: mapIcons.shapes.MAP_PIN,
fillColor: '#000000',
fillOpacity: 1,
strokeColor: '#9c4343',
strokeWeight: 1.5
}

//When the user clicks on a marker, it will become
// the selected one:
var selectedMarker = null;

function placeStoresInMap(stores) {
// Add some markers to the map.
// Note: The code uses the JavaScript Array.prototype.map() method to
// create an array of markers based on the given "profiles" array.
// The map() method here has nothing to do with the Google Maps API.
markers = stores.map(function(store, i) {
var marker = new mapIcons.Marker({
  map: map,
  position: store.location, 
  icon: DEFAULT_ICON,
  title: store.name,
  map_icon_label: '<span class="map-icon map-icon-liquor-store"></span>'
});

//we attach the profile to the marker, so when the marker is selected
//we can get all the profile data to fill the highlighted profile box under
// the map 
marker.store = store;

google.maps.event.addListener(marker, 'click', function(evt) {
  markerClick(this);
});

return marker;
});

/*console.log(markers);
console.log(markers.length);*/
}

function clearMarkers() {
if (markers) {
markers.map(function(marker, i) {
marker.setMap(null);
});
}

markers = new Array();
selectedMarker = null;
}

function markerClick(marker) {
console.log('Marker clicked');
console.log(marker);

// de-select the previously active marker, if present
if (selectedMarker) selectedMarker.setIcon(DEFAULT_ICON);
marker.setIcon(SELECTED_ICON);

// Fill in the Highlighted Profile article with
// the marker profile data:
document.getElementById('hpUser').innerHTML=marker.profile.name;
document.getElementById('hpAddress').innerHTML=marker.profile.address;
document.getElementById('hpLanguages').innerHTML="Teaches "+marker.profile.languages;
document.getElementById('hpTitle').innerHTML=marker.profile.title;
document.getElementById('hpDescription').innerHTML=marker.profile.description;

// upadete selected marker reference
selectedMarker = marker;
}

function loadJSON(url, callback) {   
var xobj = new XMLHttpRequest();

xobj.overrideMimeType("application/json");
xobj.open('GET', url, true); 
xobj.onreadystatechange = function () {
  if (xobj.readyState == 4 && xobj.status == "200") {
    // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
    callback(xobj.responseText);
  }
  //TODO: what to do in case of failures?
};
xobj.send(null);  
}

function dictToURI(dict) {
var str = [];
for(var p in dict){
str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
}
return str.join("&");
}





}


