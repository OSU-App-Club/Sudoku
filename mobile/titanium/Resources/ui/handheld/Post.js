function Feed(title) {
	var self = Ti.UI.createWindow({
		title : 'Sudoku',
		backgroundColor : '#d7e2ea'
	});
		
	var puzzle = Ti.UI.createTextArea({
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
	self.add(puzzle);
	
	var name = Ti.UI.createTextArea({
	    borderWidth: 2,
		borderColor: '#bbb',
		borderRadius: 5,
		color: '#888',
		font: {fontSize:20, fontWeight:'bold'},
		textAlign: 'left',
		value: 'Anonymous',
		top: 100,
		width: 300, 
		height : 50
	});
	self.add(name);

	var sendButton = Ti.UI.createButton({
	    width: 90, 
	    top: 160, 
	    height: 30,
	    title: 'Send!'
	});
	self.add(sendButton);

	sendButton.addEventListener("click", function(){
		 //var url = "http://sudoku496.appspot.com/solve";
		 var url = "http://localhost:8080/solve";
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
		 	puzzle:puzzle.value,
		 	author: name.value
		 }
		 client.send(params);
		 alert("Sent!")
	});
	
	return self;
};

module.exports = Feed;
