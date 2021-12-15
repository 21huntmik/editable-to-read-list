var books = []
var editID = null;
var addButton = document.querySelector(".enterButton"); //Add the button querySelector

var registeringscreen = document.querySelector("#registeringscreen");
registeringscreen.style.display = "none";
var loginscreen = document.querySelector("#loginscreen");
loginscreen.style.display = "block";
var loggedin = document.querySelector("#loggedin");
loggedin.style.display = "none";
var loginerror = document.querySelector(".loginerror");
loginerror.style.display = "none";
var createaccounterror = document.querySelector(".createaccounterror");
createaccounterror.style.display = "none";
var welcome = document.querySelector("#welcome");
welcome.style.display = "none";
var dropbtn = document.querySelector(".dropbtn");
var logmeout = document.querySelector(".logmeout");

dropbtn.onclick = function() {
	document.getElementById("myDropdown").classList.toggle("show");
};

logmeout.onclick = function() {
	fetch("http://localhost:8080/sessions", {
		method: "DELETE",
		credentials: 'include'
	}).then(function (response) {
		loadBooksFromServer();
	});
}

window.onclick = function(event) {
	if (!event.target.matches('.dropbtn')) {
		var dropdowns = document.querySelector(".dropdown-content");
		var i;
		for (i = 0; i < dropdowns.length; i++) {
			var openDropdown = dropdowns[i];
			if (openDropdown.classList.contains('show')) {
				openDropdown.classList.remove('show');
			};
		};
	};
};

var addForm = document.querySelector("#editbox");
addForm.style.display = "none";

var gotologinButton = document.querySelector("#gotologin");

gotologinButton.onclick = function() {
	registeringscreen.style.display = "none";
	loginscreen.style.display = "block";
	loggedin.style.display = "none";
	createaccounterror.style.display = "none";
	loginerror.style.display = "none";
};

var gotoregisterButton = document.querySelector("#gotoregister");

gotoregisterButton.onclick = function() {
	registeringscreen.style.display = "block";
	loginscreen.style.display = "none";
	loggedin.style.display = "none";
	createaccounterror.style.display = "none";
	loginerror.style.display = "none";
};

var createAccountButton = document.querySelector("#createaccount");

createAccountButton.onclick = function() {
	//query the info
	var first = document.querySelector(".registerfirstname");
	var firstname = first.value;

	var last = document.querySelector(".registerlastname");
	var lastname = last.value;

	var regemail = document.querySelector(".registeremail");
	var registeremail = regemail.value;

	var regpassword = document.querySelector(".registerpassword");
	var registerpassword = regpassword.value;

	var data = "email=" + encodeURIComponent(registeremail) + "&password=" + encodeURIComponent(registerpassword) + "&fname=" + encodeURIComponent(firstname) + "&lname=" + encodeURIComponent(lastname);

	var welcomeMessage = "&#9886; Welcome " + encodeURIComponent(firstname) + " " + encodeURIComponent(lastname) + "! &#9887;";
	//send the info
	//what is the method and path??
	fetch("http://localhost:8080/users", {
		method: "POST",
		body: data,
		credentials: 'include',
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then( function(response) {
		console.log(response.status);
		if (response.status == 201) {
			registeringscreen.style.display = "none";
			loginscreen.style.display = "none";
			loggedin.style.display = "block";
			welcome.innerHTML = welcomeMessage;
			welcome.style.display = "block"
			setInterval(function() {
				welcome.style.display = "none";
			}, 15000);
			regpassword.value = "";
			regemail.value = "";
			last.value = "";
			first.value = "";
			loadBooksFromServer();
		}
		else if (response.status == 422) {
			registeringscreen.style.display = "block";
			loginscreen.style.display = "none";
			loggedin.style.display = "none";
			createaccounterror.style.display = "block";
			regpassword.value = "";
			regemail.value = "";
			last.value = "";
			first.value = "";
			return;
		}
		else {
			return;
		}
	});
};

	//WHAT HAPPENS IN THE SERVER
		//when this button is clicked, check to see if the email is already in the database
		//if the email is in the database,
		//save the email, password, first name, and last name
		//if the email is not in the database,
		//create a div with red words that say something went wrong
		//do not tell them what is wrong... security problem
		//after they create their account... it is like they logged in
		//let them see the data

var logInButton = document.querySelector("#login");

logInButton.onclick = function() {
	//query the info
	var logemail = document.querySelector(".loginemail");
	var loginemail = logemail.value;

	var logpassword = document.querySelector(".loginpassword");
	var loginpassword = logpassword.value;

	var data = "email=" + encodeURIComponent(loginemail) + "&password=" + encodeURIComponent(loginpassword);

	//send the info
	//what is the method and the path????
	fetch("http://localhost:8080/sessions", {
		method: "POST",
		body: data,
		credentials: 'include',
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then( function(response) {
		console.log(response.status);
		var status = response.status;
//COME BACK TO THIS!!!!!!!!!!!
		if (status == 201) {
			registeringscreen.style.display = "none";
			loginscreen.style.display = "none";
			loggedin.style.display = "block";
			logemail.value = "";
			logpassword.value = "";
			loadBooksFromServer();
		}
		else if (status == 401) {
			registeringscreen.style.display = "none";
			loginscreen.style.display = "block";
			loggedin.style.display = "none";
			loginerror.style.display = "block";
			logemail.value = "";
			logpassword.value = "";
			return;
		}
		else {
			return;
		}
	});
};
	//WHAT HAPPENS IN THE SERVER
		//check to see if the email is in the database
		//if it doesn't exist, then it won't work
		//if found:
		//verify given password against hash in DB
		//bcrypt.verify()
		//if match:
		//respond 201 (created)
		//**side affect is created right here
		//else:
		//respond 401 (unauthenticated)
		//else:
		//respond 401 (unauthenticated)

var updateButton = document.querySelector(".updateButton");

updateButton.onclick = function() {
	var titleinput = document.querySelector(".titleinpute");
	var booktitle = titleinput.value;
	titleinput.value = "";

	var authorinput = document.querySelector(".authorinpute");
	var bookauthor = authorinput.value;
	authorinput.value = "";

	var yearinput = document.querySelector(".yearinpute");
	var bookyear = yearinput.value;
	yearinput.value = "";

	var pageinput = document.querySelector(".pageinpute");
	var bookpages = pageinput.value;
	pageinput.value = "";

	var genreinput = document.querySelector(".genreinpute");
	var bookgenre = genreinput.value;
	genreinput.value = "";

	var data = "title=" + encodeURIComponent(booktitle) + "&author=" + encodeURIComponent(bookauthor) + "&date=" + encodeURIComponent(bookyear) + "&pages=" + encodeURIComponent(bookpages) + "&genre=" + encodeURIComponent(bookgenre);

	fetch("http://localhost:8080/books/" + editID, {
		method: "PUT",
		body: data,
		credentials: 'include',
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		loadBooksFromServer();
	});

	editbox.style.display = "None";
	inputbox.style.display = "Block";
};

addButton.onclick = function() {
	var titleinput = document.querySelector(".titleinput");
	var booktitle = titleinput.value;
	titleinput.value = "";

	var authorinput = document.querySelector(".authorinput");
	var bookauthor = authorinput.value;
	authorinput.value = "";

	var yearinput = document.querySelector(".yearinput");
	var bookyear = yearinput.value;
	yearinput.value = "";

	var pageinput = document.querySelector(".pageinput");
	var bookpages = pageinput.value;
	pageinput.value = "";

	var genreinput = document.querySelector(".genreinput");
	var bookgenre = genreinput.value;
	genreinput.value = "";

	var data = "title=" + encodeURIComponent(booktitle) + "&author=" + encodeURIComponent(bookauthor) + "&date=" + encodeURIComponent(bookyear) + "&pages=" + encodeURIComponent(bookpages) + "&genre=" + encodeURIComponent(bookgenre);

	fetch("http://localhost:8080/books", {
		method: "POST",
		body: data,
		credentials: 'include',
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response){
		loadBooksFromServer();
	});
};

function deleteBookFromServer(bookID){
	fetch("http://localhost:8080/books/" + bookID, {
		method: "DELETE",
		credentials: 'include'
	}).then(function (response) {
		loadBooksFromServer();
	});
};

function updateBooksFromServer(bookID){
	fetch("http://localhost:8080/books" + bookID, {
		method: "PUT",
		body: data,
		credentials: 'include',
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		}
	}).then(function (response) {
		loadRestaurantsFromServer();
	});
};

function loadBooksFromServer() {
	fetch("http://localhost:8080/books", {
		credentials: 'include'
	}).then(function (response) {
		if (response.status == 200) {
		//show the data
			loggedin.style.display = "block";
			registeringscreen.style.display = "none";
			loginscreen.style.display = "none";
		}
		else if (response.status == 401) {
		//show the login or register
			loggedin.style.display = "none";
			loginscreen.style.display = "block";
			registeringscreen.style.display = "none";
			return;
		}
		else {
		//confused
			return;
		}
		response.json().then(function (data) {
			books = data;
			var list = document.querySelector("#output");
			list.innerHTML = "";
			books.forEach(function (book) {
				var newListItem = document.createElement("li");
				newListItem.style.listStyleType = "none";

				var titleDiv = document.createElement("div");
				titleDiv.innerHTML = book.title + " By: " + book.author;
				titleDiv.style.float = "clear";
				newListItem.appendChild(titleDiv);

				//var authorDiv = document.createElement("div");
				//authorDiv.innerHTML = "By: " + book.author;
				//authorDiv.style.float = "clear";
				//newListItem.appendChild(authorDiv);

				var yearDiv = document.createElement("div");
				yearDiv.innerHTML = "Year: " + book.date + " Pages: " + book.pages + " Genre: " + book.genre;
				yearDiv.style.float = "clear";
				newListItem.appendChild(yearDiv);

				//var pageDiv = document.createElement("div");
				//pageDiv.innerHTML = "Pages: " + book.pages;
				//pageDiv.style.float = "left";
				//newListItem.appendChild(pageDiv);

				//var genreDiv = document.createElement("div");
				//genreDiv.innerHTML = "Genre: " + book.genre;
				//genreDiv.style.float = "clear";
				//newListItem.appendChild(genreDiv);

				list.appendChild(newListItem);

				var deleteButton = document.createElement("button");
				deleteButton.innerHTML = "X";
				deleteButton.style.float = "left";
				deleteButton.onclick = function() {
					if (confirm("Are you sure you want to delete " + book.title + "?")) {
						deleteBookFromServer(book.id);
					};
				};
				newListItem.appendChild(deleteButton);

				var editButton = document.createElement("button");
				editButton.innerHTML = "Edit";
				editButton.style.float = "clear";
				editButton.onclick = function() {
					//first, save the id for editing
					editID = book.id;
					// display hidden edit form
					// assign input values to pre fill
					var editbox = document.querySelector("#editbox");
					editbox.style.display = "block";

					var inputbox = document.querySelector("#inputbox");
					inputbox.style.display = "none";

					var titleinput = document.querySelector(".titleinpute");
					titleinput.value = book.title;

					var authorinput = document.querySelector(".authorinpute");
					authorinput.value = book.author;

					var yearinput = document.querySelector(".yearinpute");
					yearinput.value = book.date;

					var pageinput = document.querySelector(".pageinpute");
					pageinput.value = book.pages;

					var genreinput = document.querySelector(".genreinpute");
					genreinput.value = book.genre;
				};
				newListItem.appendChild(editButton);

				var spacerDiv = document.createElement("div");
				spacerDiv.innerHTML = "";
				spacerDiv.style.height = "15px";
				spacerDiv.style.width = "15px";
				newListItem.appendChild(spacerDiv);
			});
		});
	});
};

loadBooksFromServer();

/*function loadLoggedInScreen() {
	registeringscreen.style.display = "none";
	loginscreen.style.display = "none";
	loggedin.style.display = "block";
};*/