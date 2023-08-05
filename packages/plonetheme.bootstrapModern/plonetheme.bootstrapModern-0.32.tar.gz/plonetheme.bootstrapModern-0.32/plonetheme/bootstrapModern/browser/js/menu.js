$(document).ready(function() {

	$("header h5.hiddenStructure").html('');
	$("#portal-personaltools-wrapper p.hiddenStructure").html('');


	$(".embededMediaShow.javascripted").hover(function(){
		$(".mediaShowButtons").css('opacity', 1);
	}, function() {
		$(".mediaShowButtons").css('opacity', 0);
	});	
	
	$("#portal-languageselector li:first-child").append(' / ');
	var $items = $( '.menu ul li' );
	var totalItems = $items.length;
	var maxHeight = 100/totalItems;
	maxHeight = maxHeight + "%";
	$( '.menu ul li' ).css('height', maxHeight);

	var triggerBttn = document.getElementById( 'trigger-overlay' );
	var overlay = document.querySelector( '.menu' );
	if (overlay != undefined) {
		var closeBttn = overlay.querySelector( 'button.overlay-close' );
		transEndEventNames = {
			'WebkitTransition': 'webkitTransitionEnd',
			'MozTransition': 'transitionend',
			'OTransition': 'oTransitionEnd',
			'msTransition': 'MSTransitionEnd',
			'transition': 'transitionend'
		},
		transEndEventName = transEndEventNames[ Modernizr.prefixed( 'transition' ) ],
		support = { transitions : Modernizr.csstransitions };
	}

	function toggleOverlay() {
		if (overlay != undefined) {
			if( classie.has( overlay, 'open' ) ) {
				classie.remove( overlay, 'open' );
				classie.add( overlay, 'close' );

				var onEndTransitionFn = function( ev ) {
					if( support.transitions ) {
						if( ev.propertyName !== 'visibility' ) return;
						this.removeEventListener( transEndEventName, onEndTransitionFn );
					}
					$(triggerBttn).show();
					$("#portal-languageselector").hide();
					classie.remove( overlay, 'close' );
				};
				if( support.transitions ) {
					overlay.addEventListener( transEndEventName, onEndTransitionFn );
				}
				else {
					onEndTransitionFn();
				}
			}
			else if( !classie.has( overlay, 'close' ) ) {
				$(triggerBttn).hide();
				$("#portal-languageselector").show();
				classie.add( overlay, 'open' );
			}
		}
	}
	if (triggerBttn != null) {
		triggerBttn.addEventListener( 'click', toggleOverlay );
		closeBttn.addEventListener( 'click', toggleOverlay );
	}

	$("#collectionFilters .portletStaticText a").each(function() {
		var elem = $(this);
		var link = $(this).attr("href");
		var link_alt = link + "/";
		var link_aggregator = link + "/aggregator";

		var URL = link + "/get_number_of_results";

		if (link == window.location.href || link_alt == window.location.href || link_aggregator == window.location.href+"aggregator" || link_aggregator == window.location.href+"/aggregator") {
			$(this).addClass("highlighted")
		}

		$.getJSON(URL, function(data) {
			if (data != null) {
				var count = $('<span class="resultCount"> (' + data + ') </span>')
				if (data == 0) {
					elem.hide();
				} else {
					elem.after(count);
				}
			}
		});
	});
});

mediaShow.buttonPrevContent = "<img src='++resource++plonetheme.bootstrapModern.css/arr-left.svg' class='arrow-img'/>";
mediaShow.buttonNextContent = "<img src='++resource++plonetheme.bootstrapModern.css/arr-right.svg' class='arrow-img'/>";
//Override slideshow behaviour
//Show the next slide in the given slideshow
onSlodeshowSkipNext = null;
onSlodeshowSkipPrev = null;

mediaShow.next = function (slideshowIndex)
{
  var slideshow = mediaShow.slideshows[slideshowIndex];
  if(slideshow.currentSlide + 1 <= slideshow.size - 1)
  { 
    mediaShow.goToSlide(slideshow.currentSlide + 1, slideshow); 
  }
  else
  {
    bootstrapModern.getNextEvent(slideshow)
  }
  
  return false;
}

//Show the previews slide in given slideshow
mediaShow.prev = function (slideshowIndex)
{
  var slideshow = mediaShow.slideshows[slideshowIndex];
  if(slideshow.currentSlide - 1 >= 0)
  {
    mediaShow.goToSlide(slideshow.currentSlide - 1, slideshow);
  }
  else
  {
    bootstrapModern.getPrevEvent(slideshow)
  }
  
  return false;
}

//This reads the URL hash and updates the slideshows acordingly
mediaShow.readURLAndUpdate = function ()
{
  var hash = document.location.hash;
  if(hash == "")
    return;
  
  if(hash == "#lastpic")
  {
	document.location.hash = "";
	$.each(mediaShow.slideshows, function(index, slideshow)
	       {
			mediaShow.updateURL(slideshow, slideshow.slides.length -1);
	       });
  }
  
  var hash_split = hash.substring(1,hash.length).split(",");
  $.each(hash_split, function(index, hsh){
    $.each(mediaShow.slideshows, function(index, slideshow){
      var slideIndex = mediaShow.idToIndex(slideshow, hsh);
      if (slideIndex > -1)
      {
        slideshow.hash = hsh;
        mediaShow.goToSlide(slideIndex, slideshow);
        return false;
      }
      return true;
    });
  });
};

//This starts loading a slide assynchrounosly and when it finishes loading it starts the next one
mediaShow.loadSlide = function (slideshow, slideNumber)
{
    var slide = slideshow.slides[slideNumber];
    var URL = slide.url + '/get_media_show_item';
    
    if(slideshow.presentation)
    {
      URL = slide.url + '/get_media_show_item?presentation=true'
    }
    else{
      URL = slide.url + '/get_media_show_item';
    }
    
    $.getJSON(URL, function(data, textStatus, jqXHR) {
        var slideContainer = $(slideshow.obj).find(".mediaShowSlide_" + slideNumber);
        
        if (slideNumber == 4)
        {
          test = "breakpoint";
        }
        
        //var titleDiv = '<div class="mediaShowTitle"><h2><a href="'+slide.url+'">'+data.title+'</a></h2></div>';
        var descriptionDiv = "";
        if(slideshow.presentation)
        {
          descriptionDiv = $('<div class="mediaShowDescription col-lg-11 col-md-11 col-sm-11 col-xs-11">'+ data.description +'</div>');
        }
        else
        {
	  var separator = " ";
	  if (data.description != "")
	  {
		separator = "  ";
	  }
	  
	  var breadcrumb = (slideNumber + 1) + "/" + slideshow.size + separator;
	  if (onSlodeshowSkipPrev == null && slideshow.size <= 1)
	  {
		descriptionDiv = $('<div class="mediaShowDescription col-lg-11 col-md-11 col-sm-11 col-xs-11">'+ data.description +'</div>');
	  }
          else
	  {
		descriptionDiv = $('<div class="mediaShowDescription col-lg-1 col-md-1 col-sm-1 col-xs-1">'+ breadcrumb + '</div>' + '<div class="mediaShowDesc col-lg-11 col-md-11 col-sm-11 col-xs-11">' + data.description + '</div>' );
	  }
        }
	
        var infoDiv = $('<div class="mediaShowInfo row-fluid"></div>');
        
        infoDiv.append(descriptionDiv);
        slideContainer.append(infoDiv);
        
        //INFO: Uncomment this if you want clickable pictures
        /*var link = '<a href="'+slide.url+'"></a>';
        if (data.media.type == 'Video' || data.media.type == 'Youtube' || data.media.type == 'Vimeo')
        {
          var link = "<a></a>";
        }*/
        
        //INFO: Comment next line if you want clickable pictures 

  
    	var link = '<div class="slideshow-wrapper"><a onclick="mediaShow.next('+mediaShow.indexOf(slideshow)+');"></a></div>';
        
        slideContainer.append('<div class="mediaShowMedia mediaShowMediaType_'+data.media.type+'">'+link+'</div>');
        
        if (slideshow.height == 0)
        {
          slideshow.height = $(slideContainer).find(".mediaShowMedia").height();
          slideshow.width = $(slideContainer).find(".mediaShowMedia").width();
        }
        
        //TODO: Here I prepend the loader image but for now it is not working so well I need to change the loading event processing a bit no make it nicer.
        //slideContainer.find('.mediaShowMedia').prepend(mediaShow.loaderObj);
        
        slideContainer.find('.mediaShowMedia a').append(mediaShow.getMediaObject(data.media, slideshow));
        
        if(slideshow.presentation)
        {
          slideContainer.find('.mediaShowDescription').css({'top': '50%', 'margin-top': -(slideContainer.find('.mediaShowDescription').height()/2)});
        }
        
        slide.loaded = mediaShow.LOADED;
        
        $(slideContainer).touchwipe({
            wipeLeft: function() {mediaShow.prev(mediaShow.indexOf(slideshow)) },
            wipeRight: function() { mediaShow.next(mediaShow.indexOf(slideshow)) },
            preventDefaultEvents: false
        });
        
        mediaShow.loadNext(slideshow);
    });
}


//XXX: [RatioProblem] This is the best way until now to do the ratio of the images. I disable it in collective.mediaShow because it implies refactoring CSS in a lot of websites.
//for now the solution will be maturing here.
//Basically on CSS I am setting the top and bottom properties of the mediaShowMedia container instead of  setting a fixed height.
//I am calculating the height of every slideshow depending on the width to fit the ratio and then adding the space necessary for the commands (buttons and descriptions)
mediaShow.ratioX = 1280;
mediaShow.ratioY = 720;
mediaShow.infoSize = 50;

mediaShow.recalculateHeight = function (obj) {
        var MSwidth = $(obj).width();
        var MSheight = (MSwidth * mediaShow.ratioY) / mediaShow.ratioX;
        $(obj).css("height", '' + (MSheight + mediaShow.infoSize) + 'px')
}

mediaShow.findSlideshows = function ()
{
  $('.embededMediaShow a').each(function (){
        //Hide the link that generates the mediaShow
        $(this).css('display', 'none');
        $(this).parent().addClass('javascripted');

        //--------------Calculate the height of the whole slideshow so that if fits the configured ratio
        //XXX: [RatioProblem] This is the best way until now to do the ratio of the images. I disable it in collective.mediaShow because it implies refactoring CSS in a lot of websites.
        //for now the solution will be maturing here.
        //Basically on CSS I am setting the top and bottom properties of the mediaShowMedia container instead of  setting a fixed height.
        //I am calculating the height of every slideshow depending on the width to fit the ratio and then adding the space necessary for the commands (buttons and descriptions)
        mediaShow.recalculateHeight($(this).parent());
        
        //-------------------- Declaration of Slideshow ------------------
        mediaShow.slideshows.push(
                                  {"obj": $(this).parent(),
                                   "url": $(this).attr("href"),
                                   "currentSlide": 0,
                                   "slides": new Array(),
                                   "initialized": false,
                                   "size": 0,
                                   "hash": "",
                                   "presentation": $(this).parent().hasClass('presentationShow'),
                                   "recursive": !$(this).parent().hasClass('disableRecursive'),
                                   "height": 0,
                                   "width": 0
                                  });
    });  
};


bootstrapModern = {};


bootstrapModern.getNextEvent = function (slideshow)
{
	if (onSlodeshowSkipNext !== null)
	{
		window.location = onSlodeshowSkipNext;
	}
	else
	{
		mediaShow.goToSlide(0, slideshow);
	}
}

bootstrapModern.getPrevEvent = function (slideshow)
{
	if (onSlodeshowSkipPrev !== null)
	{
		window.location = onSlodeshowSkipPrev + "#lastpic";
	}
	else
	{
		mediaShow.goToSlide(slideshow.size-1, slideshow);
	}
}

mediaShow.getContentListing = function (slideshow)
{
    var URL, querystring;
    //extract passed query string
    if (slideshow.url.indexOf("?") != -1)
    {
        //there is a query string
        querystring = slideshow.url.slice(slideshow.url.indexOf("?") +1)
        slideshow.url = slideshow.url.slice(0, slideshow.url.indexOf("?"))
    }
    else
    {
        //There is no query string
        querystring = ""
    }

    slideshow.recursive = false;
   	querystring = "";

    if (slideshow.recursive)
    {
        if (querystring == "")
        {
            URL = slideshow.url + '/mediaShowListing';
        }
        else
        {
            URL = slideshow.url + '/mediaShowListing' + '?' + querystring;
        }
    }
    else
    {
        if (querystring == "")
        {
            URL = slideshow.url + '/mediaShowListing?recursive=false'
        }
        else
        {
            URL = slideshow.url + '/mediaShowListing' + '?' + querystring + "&recursive=false";
        }
    }
    
    $.getJSON(URL, function(data) {

        $.each(data, function(index, item) {
            //-------------------- Declaration of Slide ------------------
            slideshow.slides.push({
                "url":item.url,
                "UID" : item.UID,
                "loaded": mediaShow.NOT_LOADED,
                "link_to_video": item.link_to_video,
                });
            slideshow.size++;
        });
        
        if (slideshow.slides.length == 0)
        {
            $.each(mediaShow.slideshows, function(index, item){
                if(slideshow == item)
                {
                    mediaShow.slideshows.splice(index,1);
                    slideshow.obj.remove();
                }
            });
        }
        else
        {
            //If there is only one slide disable the buttons
            if (slideshow.slides.length == 1)
            {
		if (onSlodeshowSkipPrev == null)
		{
			$(slideshow.obj).find(".mediaShowButtons").addClass("disabled")
		}
            }
            mediaShow.markAsInitialized(slideshow);
        }
    });
}


