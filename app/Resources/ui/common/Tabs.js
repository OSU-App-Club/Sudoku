function Tabs(Feed, Post) {
	var self = Ti.UI.createTabGroup();
	var feed_win = new Feed('Feed')
	var post_win = new Post('Post');
	
	var feed_tab = Ti.UI.createTab({
		title: 'Feed',
		icon: '/images/KS_nav_ui.png',
		window: feed_win
	});
	feed_win.containingTab = feed_tab;
	
	var post_tab = Ti.UI.createTab({
		title: 'Post',
		icon: '/images/KS_nav_views.png',
		window: post_win
	});
	post_win.containingTab = post_tab;
	
	self.addTab(feed_tab);
	self.addTab(post_tab);
	return self;
};

module.exports = Tabs;
