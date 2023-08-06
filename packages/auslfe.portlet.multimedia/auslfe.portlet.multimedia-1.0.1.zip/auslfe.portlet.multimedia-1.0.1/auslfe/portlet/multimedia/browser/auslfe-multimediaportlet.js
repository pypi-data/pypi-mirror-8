/*
 * Multimedia Javascript for auslfe.portlet.multimedia 
 */

jQuery.auslfe_multimedia = {
    timeout: 30000,
	i18n: {
		en: {
			stopReload: 'Click to stop auto-reload',
			restartReload: 'Click to restart auto-reload'
		},
		it: {
			stopReload: 'Click per fermare il caricamento automatico',
			restartReload: 'Click per avviare di nuovo il caricamento automatico'
		}
	}
};

(function($) {

	$(document).ready(function() {
		// TODO: this code is still in a jQuery 1.2 style
		
		// Site language
		var lang = $("html").attr('lang') || 'en';
		var i18n = $.auslfe_multimedia.i18n[lang] || $.auslfe_multimedia.i18n['en'];
		
		/**
		 * A function for random sorting an array or array-like object
		 */
		function randOrd(){
			return (Math.round(Math.random())-0.5);
		} 
		
		/**
		 * At load time, remove all images and stop links HREF
		 */
		$('.portletMultimedia .galleryMultimedia a').each(function() {
			$(this).attr("href", "javascript:;").find("img").remove();
		});
		
		/**
		 * Prepare portlets to AJAX load images from server
		 */
		$('.portletMultimedia').each(function(index) {
			var portlet = $(this);
			// Load random images?
			var rnd = $("span.random",portlet).length>0;
			// Client reload images?
			var client_reload = $("span.client_reload",portlet).length>0;
			var link = $(".portletFooter a", portlet);
			// var timestamps = new Date().getTime();
			var images = null;
			
			/**
			 * Change order on the stored images
			 * @param {boolean} startHidden true if images must start hidden
			 */
			function reorder(startHidden) {
				var startHidden = startHidden || false;
				if (rnd) images.sort(randOrd);
				$(".galleryMultimedia a", portlet).each(function(index) {
					var link = $(this);
					var curData = images[index];
					if (!curData.image)
						curData.image = $('<img alt="'+curData.description+'" title="'+curData.title+'" src="'+curData.url+'/image_tile" '+(startHidden?' style="display:none"':'')+'/>');
					link.append(curData.image);
					curData.image.imagesLoaded(function(e) {
						$(this).fadeIn("fast");
					});
					link.attr("href", curData.url+"/image_view_fullscreen");
				});
			}
			
			$.get(link.attr('href')+'/@@query_images', {}, function(data) {
				images = data;
				reorder();
				portlet.removeClass("hideFlag");
			}, dataType='json');
			
			if (rnd && client_reload) {
				// 1 - bind the reload image event
				portlet.bind("portletRefresh", function(event) {
					$("img", portlet).fadeOut("fast", function() {
						$("img", portlet).remove();
						reorder(true);
					});
				});
				
				var reloadEventHandler = function() {
					portlet.trigger("portletRefresh");
				};
				var reload_timeout = this.getAttribute('data-reloadtimeout') || $.auslfe_multimedia.timeout;
				var intval = setInterval(reloadEventHandler, reload_timeout);
	
				// 2 - handle clicks on portlet title
				$(".portletHeader", this).attr('title', i18n['stopReload']);
				$(".portletHeader", this).click(function(e) {
					client_reload = !client_reload;
					if (client_reload) {
						$(this).attr('title', i18n['stopReload']);
						intval = setInterval(reloadEventHandler, reload_timeout);
						reloadEventHandler();
					}
					else {
						$(this).attr('title', i18n['restartReload']);
						clearInterval(intval);
					}
				});
			}
			
		});
	});
	
})(jQuery);


