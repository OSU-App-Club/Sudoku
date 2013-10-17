var social = require('social');

(function() {
	var osname = Ti.Platform.osname, 
		version = Ti.Platform.version,
		height = Ti.Platform.displayCaps.platformHeight,
		width = Ti.Platform.displayCaps.platformWidth;

	var Post;
	Post = require('ui/handheld/Post');

	var Feed;
	Feed = require('ui/handheld/Feed');

	var Tabs = require('ui/common/Tabs');
	new Tabs(Feed, Post).open();
})();
