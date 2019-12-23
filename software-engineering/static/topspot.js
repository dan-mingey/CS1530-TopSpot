var CurrentFloor;
var Spots;
var Friends;
var CurrentUser;

function setCurrentFloor(floor)
{
	CurrentFloor = floor;
}

function getSpots(user)
{
	CurrentUser = user;
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handleGetSpots(httpRequest) 
	};

	httpRequest.open("POST", "/get_spots");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "current_floor=" + CurrentFloor;
	httpRequest.send(data);
	//httpRequest.send()
}

function handleGetSpots(httpRequest)
{
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		
			Spots = JSON.parse(httpRequest.response)
			console.log(Spots)
			console.log(Spots[0])
			console.log(Spots[0][0])
			checkFriend();
			

		} else {
			alert("There was a problem with the post request.");
		}
	}
}


function setup()
{
	document.getElementById("unclaim_spot").addEventListener("click", confirmUnclaim, true);
}

function confirmUnclaim()
{
	if(confirm("Are you sure you want to unclaim your spot?"))
	{
		unclaimSpot();
	}
}

function unclaimSpot()
{
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handleUnclaimSpot(httpRequest) 
	};

	httpRequest.open("GET", "/unclaim_seating");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	//var data = "current_floor=" + CurrentFloor;
	//httpRequest.send(data);
	httpRequest.send()
}

function handleUnclaimSpot(httpRequest)
{
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		
			console.log("this means that the unclaim seating functionality worked correctly");
			var response = httpRequest.response
			if(response == "NoSeatOccupied")
			{
				alert("You have no seat claimed at this moment")
			} else 
			{
				document.getElementById(httpRequest.response).setAttribute("class", "spot_vacant");
			}
		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function handleGetFriends(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			console.log("in handle get friends")
			Friends = JSON.parse(httpRequest.response);
			console.log(Friends);
			checkOccupiedSpots();
		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function checkFriend()
{
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handleGetFriends(httpRequest); 
	};

	httpRequest.open("GET", "/get_friends");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	//var data = "seat_location=" + seatID + "&current_floor=" + CurrentFloor;
	//httpRequest.send(data);
	httpRequest.send()
}

function checkOccupiedSpots()
{	

	for(var i = 0; i < Spots.length; i++)
	{
		if(Spots[i][2] == 1)
		{
			console.log("This spot is occupied")
			document.getElementById(Spots[i][5]).setAttribute("class", "spot_taken");
			document.getElementById(Spots[i][5]).setAttribute("onclick","seatClicked(this.id)");
			if(Spots[i][3]==CurrentUser)
			{
				document.getElementById(Spots[i][5]).setAttribute("class", "user_spot");
			}
			for(var x = 0; x < Friends.length; x ++)
			{
				if(Spots[i][3] == Friends[x])
				{
					document.getElementById(Spots[i][5]).innerText = Spots[i][3];
				}
			}
			

		} else 
		{
			document.getElementById(Spots[i][5]).setAttribute("class", "spot_vacant");
			document.getElementById(Spots[i][5]).setAttribute("onclick","seatClicked(this.id)");

		}


		if(Spots[i][4]==1)
		{
			document.getElementById(Spots[i][5]).style.border = "solid gold 7px";
		}
	}
}

function checkFloorPlan(row, column)
{
	for(var i = 0; i < GroundFloorSpots.length; i++)
	{
		var rowColumn = row.toString(10) + "," + column.toString(10);
		if(rowColumn == GroundFloorSpots[i])
		{
			return true;
		}
	}
	return false;
}

// THIS FUNCTION IS TO CHECK IF THE USER ALREADY HAS A SPOT OCCUPIED
function getUserStatus(seatID)
{
	console.log("made it to getUserStatus")
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handleUserStatus(httpRequest, seatID) 
	};

	httpRequest.open("GET", "/get_user_status");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	//var data = "seat_location=" + seatID + "&current_floor=" + CurrentFloor;
	//httpRequest.send(data);
	httpRequest.send()
}

function getSeatInfo(seatID)
{
	console.log("made it to getSeatInfo")
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handleSeatInfo(httpRequest) 
	};

	httpRequest.open("POST", "/get_seat_info");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "seat_location=" + seatID + "&current_floor=" + CurrentFloor;
	httpRequest.send(data);
}


// this function will be called when a spot it clicked
// it can claim a spot if a user hasnt claimed one yet
// it can unclaim a spot if a user clicks on one they have already clicked on
function seatClicked(seatID)
{
	
	// GET THE SPOT INFORMATION ABOUT THE CURRENT USER
	getUserStatus(seatID);

}


// This function will = make a POST request to flask that will call the claim_seating function 
// it passes the seat location and current floor as variables
function reserveSeat(seatID)
{
	console.log("made it to reserve seat")
	var httpRequest = new XMLHttpRequest();
	
	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { 
		handlePost(httpRequest, seatID) 
	};

	httpRequest.open("POST", "/claim_seating");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data = "seat_location=" + seatID + "&current_floor=" + CurrentFloor;
	httpRequest.send(data);
}

function handlePost(httpRequest, seatID)
{
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		
			console.log("this means that the reserve seating functionality worked correctly");
			document.getElementById(seatID).setAttribute("class", "user_spot")

		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function handleUserStatus(httpRequest, seatID) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		
			// this will be the return value of the POST 
			// so if it works properly, reserve the seat and change the class to taken?
			//console.log(httpRequest.response)
			var user_seat_status = httpRequest.response;

			// Check to see if the user already has a seat occupied
			if(user_seat_status != "0")
			{
				alert("You already have a spot reserved!");
			}
			else {
				getSeatInfo(seatID);
				/*
				if(confirm("Are you sure you want to reserve the seat?"))
				{
					
					reserveSeat(seatID);
					console.log("the user wants to reserve the seat");
				} else {
					console.log("The user doesnt want to reserve the seat");
				}*/
			}

		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function handleSeatInfo(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
		
			// this will be the return value of the POST 
			// so if it works properly, reserve the seat and change the class to taken?
			seat = JSON.parse(httpRequest.response)
			console.log(seat)
			if(seat[2]==1)
			{
				alert("This seat is already occupied!")
			} else {
				if(confirm("Are you sure you want to reserve the seat?"))
				{
					reserveSeat(seat[5]);
					console.log("the user wants to reserve the seat");
				} else {
					console.log("The user doesnt want to reserve the seat");
				}
			}
			

		} else {
			alert("There was a problem with the post request.");
		}
	}
}

function createFloorPlan()
{
	var board = document.createElement("table");
	
	//for every row j
	for(var j = 1; j < 16; j++)
	{
		var row = document.createElement("tr");
		//row.setAttribute("height","20" );
		//row.setAttribute("width","20" );


		//for every column i in that row j
		for(var i = 1; i < 16; i++)
		{

			var col = document.createElement("td");
			//col.setAttribute("height","200" );
			//col.setAttribute("width","200" );
			col.setAttribute("id", String(j)+","+String(i));
			col.setAttribute("class", "not_spot");

			/*inFloorPlan = checkFloorPlan(j, i);

			if(inFloorPlan)
			{
				col.setAttribute("class", "spot_vacant")
				col.setAttribute("onclick","seatClicked(this.id)");
			} else {
				col.setAttribute("class","not_spot")
			}*/
			row.appendChild(col);
		}
		board.appendChild(row);
	}
	//board.setAttribute("border","2");
	board.setAttribute("align","center");
	board.setAttribute("width","75%");
	//board.style.backgroundColor = "lightblue";
	return board;
}

function addEventListeners()
{
	for(var i = 0; i < GroundFloorSpots.length; i++ )
	{
		document.getElementById(GroundFloorSpots[i]).setAttribute("onclick","seatClicked(this.id)");
	}
}
var GroundFloorSpots = ["1,1", "1,2","1,5" , "1,6","1,10", "1,11","1,14","1,15","2,1","2,2","2,5","2,6","2,10","2,11","2,14","2,15", "4,1","4,5","4,6","4,10","4,11","4,15","5,1", "5,5", "5,6", "5,10", "5,11", "5,15", "7,1", "7,5", "7,6", "7,10", "7,11", 
"7,15", "8,1", "8,5", "8,6", "8,10", "8,11", "8,15", "10,1", "10,2", "10,5", "10,6", "10,10", "10,11", "10,14 ","10,15", "12,1", "12,2", "12,5", "12,6", "12,10", "12,11", "12,14", "12,15", "15,1", "15,3", "15,5", "15,11", "15,13", 
"15,15"];


function AlertFriendDoesntExist()
{
	alert("The name you entered was not valid");
}