// Basic implementation of show/hide links to fetch and display column data

(function(){
	var $ = django.jQuery; // Use the django version of jquery already included
	// Fetch the lazy admin URL
	var url = $('#lazy_url').attr('data-url');
	// Show link handler
	$(".lazy_show_link").click(function() {
		var self = $(this);
		var post_data = {
			app: self.attr('data-lazyapp'),
			model: self.attr('data-lazyclass'),
			method: self.attr('data-lazyfunc'),
			objid: self.attr('data-lazyobj')
		};
		var lazyid = post_data.method + post_data.objid;

		// Make the post request and dump the output in to the info container
		$.post(url, post_data, function(output) {
			$("#info" + lazyid).html(output).show();
			$("#show" + lazyid).hide();
			$("#hide" + lazyid).show();
		});
		event.preventDefault();
	});

	// Hide link handler
	$(".lazy_hide_link").click(function() {
		var self = $(this);
		var lazyid = self.attr('data-lazyid');
		self.hide();
		$("#info" + lazyid).hide();
		$("#show" + lazyid).show();
		event.preventDefault();
	});
}).call(this);