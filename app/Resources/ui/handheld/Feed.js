function Post(title) {
	var self = Ti.UI.createWindow({
		title : 'View',
		backgroundColor : '#d7e2ea'
	});
	
	var name = Ti.UI.createTextArea({
	    borderWidth: 2,
		borderColor: '#bbb',
		borderRadius: 5,
		color: '#888',
		font: {fontSize:20, fontWeight:'bold'},
		textAlign: 'left',
		value: 'Anonymous',
		top: 10,
		width: 300, 
		height : 40
	});
	self.add(name);
	
	var answer = Ti.UI.createTextArea({
		value:"solution",
		top:60,
		left:10,
		height:180,
		width:200
	});
	self.add(answer);

	var link = Ti.UI.createTextArea({
		value:"Shake to get share link!",
		bottom:70,
		height:60,
		width:300
	});
	self.add(link);

	var getAnswer = Ti.UI.createButton({
	    width: 90, 
	    bottom: 10, 
	    height: 30,
	    title: 'Get Answer!'
	});
	self.add(getAnswer);

	getAnswer.addEventListener("click", function(){
		var url = "http://localhost:8080/view?author="+name.value;
		var xhr = Titanium.Network.createHTTPClient();
		xhr.onload = function() {
			var response = this.responseText;
			Ti.API.info(response);
			answer.value = response;
		};
		 
		xhr.open("GET",url);
		xhr.send();
	});
	
	Ti.Gesture.addEventListener('shake',function(e) {
		var url = "http://localhost:8080/share?author="+name.value;
		var xhr = Titanium.Network.createHTTPClient();
		xhr.onload = function() {
			var response = this.responseText;
			Ti.API.info(response);
			link.value = response;
		};
		 
		xhr.open("GET",url);
		xhr.send();
	});

	link.addEventListener('click', function(e){
		//Ti.Platform.openURL(link.value);
		var webview = Titanium.UI.createWebView({url:link.value});
   		var win = Titanium.UI.createWindow();
    	win.add(webview);
    	win.open({modal:true});

	});
	
	return self;
};

module.exports = Post;
