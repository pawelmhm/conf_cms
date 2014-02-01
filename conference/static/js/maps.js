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
    
    var dirButton = document.getElementById('directions');
    dirButton.addEventListener('click',getOrigin);
    
    function getDistance (origin) {
        // call google to get distance
         
        console.dir(origin)
        var lat = origin.coords.latitude,
            lng = origin.coords.longitude,
            origin = new google.maps.LatLng(lat,lng),
            destination = myLocation, 
            service = new google.maps.DistanceMatrixService();
        
        service.getDistanceMatrix({
            origins: [origin],
            destinations: [destination], 
            travelMode: google.maps.TravelMode.DRIVING
        }, parseDirections); 
    } 
    
    function parseDirections(response) {
        // append directions to the DOM
        var distance,duration;
        console.dir(response);
        response.rows.forEach(function (row) {
            row.elements.forEach(function (element){
                distance = element.distance.text;
                duration = element.duration.text;
            })
        });
        console.log(distance,duration);
        var outp = document.getElementById('directionsOutput');
        var span = document.createElement('span');
        var message = "Distance: <b>" + distance + "</b>";
        message += "<br>Duration of travel (by car, according to google maps): <b>" + duration + "</b>";
        message += "<br><a href='https://maps.google.co.uk/maps?q=university+of+Warsaw&hl=en&ll=52.240455,21.019206&spn=0.007897,0.019741&sll=51.528642,-0.101599&sspn=0.513467,1.263428&t=m&z=16&iwloc=A'>Get directions</a>";
        outp.innerHTML = message;
        //outp.appendChild(span);
    };
    
    function handleError(error) {
        console.log(error)
    }

    function getOrigin () {
        navigator.geolocation.getCurrentPosition(getDistance,handleError)
    }
    
}

window.onload = loadScript;
