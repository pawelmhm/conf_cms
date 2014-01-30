function loadScript () {
    script = document.createElement('script');
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCijIMJe1z_6rKu_HbZgL4HiBUjighonCo&sensor=false&callback=init";
    document.body.appendChild(script);
}

function init (data) {
    var myLocation = new google.maps.LatLng(52.239968,21.015727);  
    var mapOptions = {
        zoom: 17,
        center:myLocation 
    };

    var map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

    var marker = new google.maps.Marker({
        position:myLocation,
        map: map,
        title: "It will take place here!"
    })

}

window.onload = loadScript;
