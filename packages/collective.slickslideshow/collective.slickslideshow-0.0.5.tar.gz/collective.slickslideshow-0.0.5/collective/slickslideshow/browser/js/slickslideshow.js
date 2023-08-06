/* ------------------------------------------------------------------------------
    S L I D E S H O W - E N H A N C E M E N T S
--------------------------------------------------------------------------------- */

slickSlideshow = {}

slickSlideshow.slides = []
slickSlideshow.debug = true

slickSlideshow.log = function(text) {
	if (slickSlideshow.debug) {
		console.log(text);
	}
}

slickSlideshow.getDetails = function() {
	slickSlideshow.url = slickSlideshow.$contentListingObj.attr('href');
	slickSlideshow.recursive = !slickSlideshow.$contentListingObj.parent().hasClass('disableRecursive');
	if (slickSlideshow.$obj.hasClass("audio")) {
		slickSlideshow.isAudioSlideshow = true;
		slickSlideshow.audioduration = slickSlideshow.$obj.attr("data-audio-duration");
		$(".audio-control-interface").show();
	}
}

slickSlideshow.getYoutubeEmbed = function (media) {
  var embed = '<iframe width="100%" height="100%" src="'+media.url+'" class="embed-responsive-item" frameborder="0" allowfullscreen></iframe>';
  return embed;
}

slickSlideshow.addAudioPlayer = function() {
	/*slickSlideshow.$obj.audioSlideshow({
		slickSlideshow: slickSlideshow
	});*/
}

slickSlideshow.addSlides = function() {
	var partial_duration = slickSlideshow.audioduration / slickSlideshow.slides.length;
	for (var i = 0; i < slickSlideshow.slides.length; i++) {
		if (slickSlideshow.isAudioSlideshow) {
			if (slickSlideshow.slides[i].video) {
			} else {
				var slide_time = i * partial_duration;
				var data_thumbnail = slickSlideshow.slides[i].url + "/@@images/image/large";
				slickSlideshow.$obj.slickAdd("<div><img src='"+slickSlideshow.slides[i].url+"' data-thumbnail='"+data_thumbnail+"' data-slide-time='"+slide_time+"'/></div>");
			}
		} else {
			if (slickSlideshow.slides[i].video) {
				slickSlideshow.$obj.slickAdd("<div>"+slickSlideshow.slides[i].embed+"</div>");
			} else {
				slickSlideshow.$obj.slickAdd("<div><img src='"+slickSlideshow.slides[i].url+"' data-slide-time='0'/></div>");
			}
		}
	};

	slickSlideshow.addAudioPlayer();
}

slickSlideshow.getSlideDetails = function(item, last) {
	var URL = "";
	var embed = "";
	var isVideo = false;

	URL = item.url + '/get_slideshow_item';

	var slide_item = {
		'url': item.url,
		'UID': item.UID
	}

	slickSlideshow.slides.push(slide_item);

	$.getJSON(URL, function(data) {
		if (data.media.type == "Youtube") {
			embed = slickSlideshow.getYoutubeEmbed(data.media);
			isVideo = true;
		} 

		slide_item.video = isVideo;
		slide_item.embed = embed;
		slide_item.description = data.description;

		if (last) {
			slickSlideshow.addSlides();
			slickSlideshow.$obj.slickGoTo(0);
		}
	});
}

slickSlideshow.getContentListing = function() {
	var URL, querystring;

	if (slickSlideshow.url.indexOf("?") != -1) {
		querystring = slickSlideshow.url.slice(slickSlideshow.url.indexOf("?") + 1);
		slickSlideshow.url = slickSlideshow.url.slice(0, slickSlideshow.url.indexOf("?"));
	} else {
		querystring = "";
	}

	// Make it non-recursive
	slickSlideshow.recursive = false;
	querystring = "";

	if (slickSlideshow.recursive) {
		if (querystring == "") {
			URL = slickSlideshow.url + '/slideshowListing';
		} else {
			URL = slickSlideshow.url + '/slideshowListing' + '?' + querystring;
		}
	} else {
		if (querystring == "") {
			URL = slickSlideshow.url + '/slideshowListing?recursive=false';
		} else {
			URL = slickSlideshow.url + '/slideshowListing' + '?' + querystring + "&recursive=false";
		}
	}
	
	$.getJSON(URL, function(data) {
		var data_len = $(data).length;

		$.each(data, function(index, item) {
			if (index == data_len - 1) {
				slickSlideshow.getSlideDetails(item, true)
			} else {
				slickSlideshow.getSlideDetails(item, false)
			}
		});
	});
}

slickSlideshow.addDescription = function(slideNumber) {
	/*var slide = slickSlideshow.slides[slideNumber];
	var total = slickSlideshow.slides.length;
	var numberOfSlides = (slideNumber+1)+"/"+total;
	$(".slideshowDetails .slideshow-description").html("<p>"+slide.description+"</p>");
	$(".slideshowDetails .slideshow-slides").html("<p>"+numberOfSlides+"</p>");*/
}

slickSlideshow.afterChange = function(event) {
	var currentSlide = event.currentSlide;
	slickSlideshow.addDescription(currentSlide);
}

slickSlideshow.initSlick = function() {
	slickSlideshow.$obj.slick({
		accessibility: true,
		dots: false,
		infinite: true,
		speed: 500,
		slidesToShow: 1,
		adaptiveHeight: true,
		focusOnSelect: true,
		onAfterChange: slickSlideshow.afterChange
	});
}

slickSlideshow.init = function() {
	slickSlideshow.log("==== INIT ====");
	slickSlideshow.$obj = $($('.slick-slideshow')[0]);
	slickSlideshow.$contentListingObj = $($('.slick-slideshow a')[0]);
	slickSlideshow.$contentListingObj.remove();
	slickSlideshow.$container = $($(".slideshow")[0]);
	slickSlideshow.getDetails();
	slickSlideshow.initSlick();
	slickSlideshow.getContentListing();
}

$(document).ready(function() {
	if ($('.slick-slideshow').length) {
		slickSlideshow.init();
	}
});

