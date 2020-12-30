// Initialize and add the map
var lat = 0
var lng = 0

var addr = "5172+Orange+Ave,+Cypress,+CA"
var addr = document.getElementById("address").innerText
$.ajax({
  url: "https://maps.googleapis.com/maps/api/geocode/json?address="+addr+"&key=AIzaSyCLtjAn_nhq_RkDrbiXOLBQOxiXhpWJbS0",
  success: function(result){
    console.log(result)
    lat = result.results[0].geometry.location.lat
    lng = result.results[0].geometry.location.lng
    console.log(lat)
    console.log(lng)
  }
});

function initMap() {
  // The location of Uluru
  console.log(lat)
  console.log(lng)
  if(lat == 0){
    setTimeout(function(){
      initMap()
      }, 1000);
  }

  const uluru = { lat: 33.823737, lng: parseFloat(lng) };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}
        
      