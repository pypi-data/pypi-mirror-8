/* SVG SUPPORT */
function supportsSvg() {
    return document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#Shape", "1.1");
}

$(document).ready(function() {
  /* MEDIA SHOW HEIGHT RECALCULATION */

  //if (supportsSvg()) {
  //  $("#portal-logo img").attr('src', '++resource++plonetheme.bootstrapModern.css/logo.svg');
  //}

  mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));

  /* POPOVER */
  $('html').click(function(e) {
    $('.phone_popover').popover('hide');
  });

  $('.phone_popover').popover({
    html: true,
    trigger: 'manual'
  }).click(function(e) {
    $(this).popover('toggle');
    e.stopPropagation();
  });

  /* FASTCLICK */
  $(function() {
    FastClick.attach(document.body);
  });

  /* HIDDEN STRUCTS */
  $("header h5.hiddenStructure").html('');
  $("#portal-personaltools-wrapper p.hiddenStructure").html('');

  $(".slideshowContent").hover(function() {
    $(".mediaShowButtons").css('opacity', 1);
  }, function() {
    $(".mediaShowButtons").css('opacity', 0);
  });

  /* LANGUAGE SELECTOR */
  $("#portal-languageselector li:first-child").append(' / ');

  /* MENU */
  var $items = $('.menu ul li');
  var totalItems = $items.length;
  var maxHeight = 100 / totalItems;
  maxHeight = maxHeight + "%";
  $('.menu ul li').css('height', maxHeight);


  /* OVERLAY */
  var overlay = document.querySelector('.menu');

  if (overlay != undefined) {
    transEndEventNames = {
      'WebkitTransition': 'webkitTransitionEnd',
      'MozTransition': 'transitionend',
      'OTransition': 'oTransitionEnd',
      'msTransition': 'MSTransitionEnd',
      'transition': 'transitionend'
    },
    transEndEventName = transEndEventNames[Modernizr.prefixed('transition')],
    support = {
      transitions: Modernizr.csstransitions
    };
  }

  function toggleOverlay() {
    if (overlay != undefined) {
      if (classie.has(overlay, 'open')) {
        classie.remove(overlay, 'open');
        classie.add(overlay, 'close');
        $("#portal-languageselector").hide();
        $('.main_menu').toggleClass('open');

        var onEndTransitionFn = function(ev) {
          if (support.transitions) {
            if (ev.propertyName !== 'visibility') return;
            this.removeEventListener(transEndEventName, onEndTransitionFn);
          }
          classie.remove(overlay, 'close');
          $('.main_menu').toggleClass('trans');
        };
        if (support.transitions) {
          overlay.addEventListener(transEndEventName, onEndTransitionFn);
        } else {
          onEndTransitionFn();
        }
      } else if (!classie.has(overlay, 'close')) {
        $("#portal-languageselector").show();
        classie.add(overlay, 'open');
        $('.main_menu').toggleClass('open');
        $('.main_menu').toggleClass('trans')
      }
    }
  }

  $(".main_menu").click(function() {
    toggleOverlay();
  });

  $("#collectionFilters .portletStaticText a").each(function() {
    var elem = $(this);
    var link = $(this).attr("href");
    var link_alt = link + "/";
    var link_aggregator = link + "/aggregator";

    var URL = link + "/get_number_of_results";

    if (link == window.location.href || link_alt == window.location.href || link == window.location.href + "aggregator" || link == window.location.href + "/aggregator") {
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


// MEDIASHOW
//Override slideshow behaviour
//Show the next slide in the given slideshow

mediaShow.buttonPrevContent = "<img src='++resource++plonetheme.bootstrapModern.css/arr-left.svg' class='arrow-img'/>";
mediaShow.buttonNextContent = "<img src='++resource++plonetheme.bootstrapModern.css/arr-right.svg' class='arrow-img'/>";

onSlodeshowSkipNext = null;
onSlodeshowSkipPrev = null;


mediaShow.goToSlide = function(x, slideshow) {
  //Stop all videos that could be playing
  mediaShow.stopAllVideos();

  mediaShow.updateURL(slideshow, x);

  if (slideshow.slides[x].loaded == mediaShow.NOT_LOADED) {
    slideshow.currentSlide = x;
  } {
    slideshow.obj.find(".mediaShowSlide_" + x).show();
    if ($(slideshow.obj).hasClass('fullscreen')) {
      var sizeOfContainer = window.innerHeight;
    } else {
      var sizeOfContainer = slideshow.height;
    }
    var img = slideshow.obj.find(".mediaShowSlide_" + x).find('img')[0];

    height = $(img).attr('offsetHeight');

    if (height > 0 && height < sizeOfContainer) {
      var margin = (sizeOfContainer - height) / 2;
      $(img).css('margin-top', margin);
    }

    if (slideshow.presentation) {
      slideshow.obj.find(".mediaShowSlide_" + x).find('.mediaShowDescription').css({
        'top': '50%',
        'margin-top': -(slideshow.obj.find(".mediaShowSlide_" + x).find('.mediaShowDescription').height() / 2)
      });
    }

    slideshow.currentSlide = x;

    $.each(slideshow.slides, function(index, slide) {
      if (index != x) {
        slideshow.obj.find(".mediaShowSlide_" + index).hide();
      }
    });
  }
  mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));
}

mediaShow.getYoutubeEmbed = function(media) {
  var embed = "<iframe width='100%'' height='100%' class='embed-responsive-item' src='" + media.url + "' frameborder='0' allowfullscreen></iframe>";
  return embed;
}

mediaShow.next = function(slideshowIndex) {
  var slideshow = mediaShow.slideshows[slideshowIndex];
  if (slideshow.currentSlide + 1 <= slideshow.size - 1) {
    mediaShow.goToSlide(slideshow.currentSlide + 1, slideshow);
  } else {
    bootstrapModern.getNextEvent(slideshow)
  }

  return false;
}

//Show the previews slide in given slideshow
mediaShow.prev = function(slideshowIndex) {
  var slideshow = mediaShow.slideshows[slideshowIndex];

  if (slideshow.currentSlide - 1 >= 0) {
    mediaShow.goToSlide(slideshow.currentSlide - 1, slideshow);
  } else {
    bootstrapModern.getPrevEvent(slideshow)
  }

  mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));

  return false;
}

//This reads the URL hash and updates the slideshows acordingly
mediaShow.readURLAndUpdate = function() {
  var hash = document.location.hash;
  if (hash == "")
    return;

  if (hash == "#lastpic") {
    document.location.hash = "";
    $.each(mediaShow.slideshows, function(index, slideshow) {
      mediaShow.updateURL(slideshow, slideshow.slides.length - 1);
    });
  }

  var hash_split = hash.substring(1, hash.length).split(",");
  $.each(hash_split, function(index, hsh) {
    $.each(mediaShow.slideshows, function(index, slideshow) {
      var slideIndex = mediaShow.idToIndex(slideshow, hsh);
      if (slideIndex > -1) {
        slideshow.hash = hsh;
        mediaShow.goToSlide(slideIndex, slideshow);
        return false;
      }
      return true;
    });
  });
};

//This starts loading a slide assynchrounosly and when it finishes loading it starts the next one
mediaShow.loadSlide = function(slideshow, slideNumber) {
  var slide = slideshow.slides[slideNumber];
  var URL = slide.url + '/get_media_show_item';

  if (slideshow.presentation) {
    URL = slide.url + '/get_media_show_item?presentation=true'
  } else {
    URL = slide.url + '/get_media_show_item';
  }

  $.getJSON(URL, function(data, textStatus, jqXHR) {
    var slideContainer = $(slideshow.obj).find(".mediaShowSlide_" + slideNumber);
    if (slideNumber == 4) {
      test = "breakpoint";
    }

    //var titleDiv = '<div class="mediaShowTitle"><h2><a href="'+slide.url+'">'+data.title+'</a></h2></div>';
    var descriptionDiv = "";
    if (slideshow.presentation) {
      descriptionDiv = $('<div class="mediaShowDescription col-lg-11 col-md-11 col-sm-11 col-xs-11">' + data.description + '</div>');
    } else {
      var separator = " ";
      if (data.description != "") {
        separator = "  ";
      }

      var breadcrumb = (slideNumber + 1) + "/" + slideshow.size + separator;
      if (onSlodeshowSkipPrev == null && slideshow.size <= 1) {
        descriptionDiv = $('<div class="mediaShowDescription col-lg-11 col-md-11 col-sm-11 col-xs-11">' + data.description + '</div>');
      } else {
        descriptionDiv = $('<div class="mediaShowDescription col-lg-1 col-md-1 col-sm-1 col-xs-11">' + breadcrumb + '</div>' + '<div class="mediaShowDesc col-lg-11 col-md-11 col-sm-11 col-xs-11">' + data.description + '</div>');
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


    var link = '<div class="slideshow-wrapper"><a onclick="mediaShow.next(' + mediaShow.indexOf(slideshow) + ');"></a></div>';

    slideContainer.append('<div class="mediaShowMedia mediaShowMediaType_' + data.media.type + '">' + link + '</div>');

    if (slideshow.height == 0) {
      slideshow.height = $(slideContainer).find(".mediaShowMedia").height();
      slideshow.width = $(slideContainer).find(".mediaShowMedia").width();
    }

    //TODO: Here I prepend the loader image but for now it is not working so well I need to change the loading event processing a bit no make it nicer.
    //slideContainer.find('.mediaShowMedia').prepend(mediaShow.loaderObj);

    slideContainer.find('.mediaShowMedia a').append(mediaShow.getMediaObject(data.media, slideshow));

    if (slideshow.presentation) {
      slideContainer.find('.mediaShowDescription').css({
        'top': '50%',
        'margin-top': -(slideContainer.find('.mediaShowDescription').height() / 2)
      });
    }

    slide.loaded = mediaShow.LOADED;

    $(slideContainer).touchwipe({
      wipeLeft: function() {
        mediaShow.prev(mediaShow.indexOf(slideshow))
      },
      wipeRight: function() {
        mediaShow.next(mediaShow.indexOf(slideshow))
      },
      preventDefaultEvents: false
    });

    mediaShow.loadNext(slideshow);
  });
}


//XXX: [RatioProblem] This is the best way until now to do the ratio of the images. I disable it in collective.mediaShow because it implies refactoring CSS in a lot of websites.
//for now the solution will be maturing here.
//Basically on CSS I am setting the top and bottom properties of the mediaShowMedia container instead of  setting a fixed height.
//I am calculating the height of every slideshow depending on the width to fit the ratio and then adding the space necessary for the commands (buttons and descriptions)
mediaShow.firstLoading = true;
mediaShow.ratioX = 1280;
mediaShow.ratioY = 720;
mediaShow.infoSize = 50;

/* 
  Responsive Height recalculation for tablet and mobile devices
*/
mediaShow.recalculateHeight = function(obj) {
  if ($(".embededMediaShow.javascripted .mediaShowSlide .mediaShowMedia").css("padding-top") == '0px') {
    var currentSlide = mediaShow.slideshows[0].currentSlide;
    var img = $(".embededMediaShow.javascripted").find(".mediaShowSlide_" + currentSlide).find('img')[0];
    console.log(img);
    if (img != undefined) {
      var img_h = $(img).height();
      $(obj).css("height", (img_h + 60) + "px");
    }
  } else {
    var MSwidth = $(obj).width();
    var MSheight = (MSwidth * mediaShow.ratioY) / mediaShow.ratioX;
    $(obj).css("height", '' + (MSheight + mediaShow.infoSize) + 'px');
  }
}

$(window).resize(function() {
  $(".phone_popover").popover('hide');
  mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));
});

$(window).on("orientationchange", function() {
  mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));
});

mediaShow.findSlideshows = function() {
  $('.embededMediaShow a').each(function() {
    //Hide the link that generates the mediaShow
    $(this).css('display', 'none');
    $(this).parent().addClass('javascripted');

    //--------------Calculate the height of the whole slideshow so that if fits the configured ratio
    //XXX: [RatioProblem] This is the best way until now to do the ratio of the images. I disable it in collective.mediaShow because it implies refactoring CSS in a lot of websites.
    //for now the solution will be maturing here.
    //Basically on CSS I am setting the top and bottom properties of the mediaShowMedia container instead of  setting a fixed height.
    //I am calculating the height of every slideshow depending on the width to fit the ratio and then adding the space necessary for the commands (buttons and descriptions)


    //-------------------- Declaration of Slideshow ------------------
    mediaShow.slideshows.push({
      "obj": $(this).parent(),
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
    mediaShow.recalculateHeight($(this).parent());
  });
};


bootstrapModern = {};
bootstrapModern.getNextEvent = function(slideshow) {
  if (onSlodeshowSkipNext !== null) {
    window.location = onSlodeshowSkipNext;
  } else {
    mediaShow.goToSlide(0, slideshow);
  }
}

bootstrapModern.getPrevEvent = function(slideshow) {
  if (onSlodeshowSkipPrev !== null) {
    window.location = onSlodeshowSkipPrev + "#lastpic";
  } else {
    mediaShow.goToSlide(slideshow.size - 1, slideshow);
  }
}

mediaShow.getContentListing = function(slideshow) {
  var URL, querystring;
  //extract passed query string
  if (slideshow.url.indexOf("?") != -1) {
    //there is a query string
    querystring = slideshow.url.slice(slideshow.url.indexOf("?") + 1)
    slideshow.url = slideshow.url.slice(0, slideshow.url.indexOf("?"))
  } else {
    //There is no query string
    querystring = ""
  }

  slideshow.recursive = false;
  querystring = "";

  if (slideshow.recursive) {
    if (querystring == "") {
      URL = slideshow.url + '/mediaShowListing';
    } else {
      URL = slideshow.url + '/mediaShowListing' + '?' + querystring;
    }
  } else {
    if (querystring == "") {
      URL = slideshow.url + '/mediaShowListing?recursive=false'
    } else {
      URL = slideshow.url + '/mediaShowListing' + '?' + querystring + "&recursive=false";
    }
  }

  $.getJSON(URL, function(data) {

    $.each(data, function(index, item) {
      //-------------------- Declaration of Slide ------------------
      slideshow.slides.push({
        "url": item.url,
        "UID": item.UID,
        "loaded": mediaShow.NOT_LOADED,
        "link_to_video": item.link_to_video,
      });
      slideshow.size++;
    });

    if (slideshow.slides.length == 0) {
      $.each(mediaShow.slideshows, function(index, item) {
        if (slideshow == item) {
          mediaShow.slideshows.splice(index, 1);
          slideshow.obj.remove();
        }
      });
    } else {
      //If there is only one slide disable the buttons
      if (slideshow.slides.length == 1) {
        if (onSlodeshowSkipPrev == null) {
          $(".slideshowContent").find(".mediaShowButtons").addClass("disabled")
        }
      }
      mediaShow.markAsInitialized(slideshow);
    }
  });
}

mediaShow.addButtons = function(slideshow) {
  var slideshowIndex = mediaShow.indexOf(slideshow);
  var buttonNext = $('<a href="#" class="buttonNext" onclick="return mediaShow.next(' + slideshowIndex + ')">' + mediaShow.buttonNextContent + '</a>').css('background-image', 'url(' + mediaShow.buttonSprite + ')');
  var buttonPrev = $('<a href="#" class="buttonPrev" onclick="return mediaShow.prev(' + slideshowIndex + ')">' + mediaShow.buttonPrevContent + '</a>').css('background-image', 'url(' + mediaShow.buttonSprite + ')');
  var container = $('<div class="mediaShowButtons"></div>');
  $(container).append(buttonPrev);
  $(container).append(buttonNext);

  $(".slideshowContent").append(container);
}


