
var temp;
var rise;
var set;

function click() {
    document.forms['cc'].action = "http://192.168.0.100:3000/page1.html";
    
}



webiopi().ready(function() {
        
       webiopi().setFunction(17, "Out");
       webiopi().setFunction(27, "Out");
       
        
        //Create a "UP" labeled button for GPIO 37
        var Downbutton = webiopi().createGPIOButton(17, "Down");
        var Upbutton = webiopi().createGPIOButton(27, "Up");


        // Append button to HTML element with ID="controls" using jQuery
        $("#controls").append(Upbutton);
		$("#controls").append(Downbutton);

        // Refresh GPIO buttons
        // pass true to refresh repeatedly of false to refresh once
        webiopi().refreshGPIO(true); 
		
		update(read_gpio())
			

});


//function read_gpio() { 
//	if (webiopi().digitalRead(5)==1){
//	alert("Curtain is Closed");
//	}
//}			





function update (weather){
	document.getElementById('temperature').innerHTML = weather.temp;
//	document.getElementById('sunset').innerHTML = weather.set;
//	document.getElementById('sunrise').innerHTML = weather.rise;

// this is for set time in UTC	
	var x = new Date (weather.set * 1000);
	var minutes = x.getMinutes();
	var hours = x.getHours();
	var seconds = x.getSeconds();
	var TIMEset = hours + ":" + minutes + ":" + seconds;
	
	document.getElementById('sunset').innerHTML = TIMEset;
	
//	this is for rise time in UTC
	var x = new Date (weather.rise * 1000);
	var minutes = x.getMinutes();
	var hours = x.getHours();
	var seconds = x.getSeconds();
	var TIMErise = hours + ":" + minutes + ":" + seconds;
	
	document.getElementById('sunrise').innerHTML = TIMErise;
}

function updatecity (city){
	var url = "http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&APPID=e43f2e1d61a364587b8ae902cc2a8dc1"
	sendRequest (url);	
}

function sendRequest(url){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var data = JSON.parse(xmlhttp.responseText);
	    var weather = {};
	        
	    weather.temp = (data.main.temp);
	    weather.set = (data.sys.sunset);
	    weather.rise = (data.sys.sunrise);
	
		
	  		
	    update(weather);
	}
   };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();    
}

window.onload = function() {
	
	
	
	updatecity();
		
}
