function Post(title) {
	var self = Ti.UI.createWindow({
		title : title,
		backgroundColor : '#d7e2ea'
	});

	/*var shareButton = Ti.UI.createButton({
	    width: 90, 
	    bottom: 10, 
	    height: 30,
	    title: 'Tweet!'
	});
	self.add(shareButton);
	*/
	var sendButton = Ti.UI.createButton({
	    width: 90, 
	    bottom: 50, 
	    height: 30,
	    title: 'Send!'
	});
	self.add(sendButton);
	
	var msg = Ti.UI.createTextArea({
		borderWidth: 2,
		borderColor: '#bbb',
		borderRadius: 5,
		color: '#888',
		font: {fontSize:20, fontWeight:'bold'},
		textAlign: 'left',
		value: '',
    	hintText:'Put Sudoku Puzzle here', 
		top: 20,
		width: 300, 
		height : 70
	});
	self.add(msg);
	
	var social = require('social');
	var twitter = social.create({
	    site: 'Twitter', 
	    consumerKey: 'qG184nEm0u98xoPhk0hGYg', 
	    consumerSecret: 'Zf7XlMCPDCGiAmyXbimzrCAO59ZA5Ca6XFcCY' 
	});
	
	
	sendButton.addEventListener("click", function(){
		 var url = "http://sudoku496.appspot.com/solve";
		 var client = Ti.Network.createHTTPClient({
		     onload : function(e) {
		         Ti.API.info("Received text: " + this.responseText);
		     },
		     onerror : function(e) {
		         Ti.API.debug(e.error);
		     },
		     timeout : 5000  // in milliseconds
		 });
		 client.open("POST", url);
		 params={
		 	puzzle:msg.value,
		 	author:"ryley"
		 }
		 client.send(params);
	});
	/*
	shareButton.addEventListener('click', function() {
	    var alert = Titanium.UI.createAlertDialog({
			title:"Are you sure you want to tweet this:",
			buttonNames:['Yes', 'No'], 
			message: msg.value 
		});
		alert.addEventListener('click', function(ev) {
    		if (ev.index == 0) { // clicked "Yes"
				twitter.share({
       				message: "Used GAE to solve this sudoku: "+ msg.value,
					success: function() {
						INFO('Tweeted!');
					},
					error: function(error) {
						INFO('Oh no! ' + error);
					}
				});
			}else if (ev.index == 1) { // clicked "No"
				alert.close;
			} 
 		});
		alert.show();							
	});
	*/
	return self;
};

module.exports = Post;
