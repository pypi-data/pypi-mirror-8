/* SVG SUPPORT */
function supportsSvg() {
    return document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#Shape", "1.1");
}

$(document).ready(function() {
  /* MEDIA SHOW HEIGHT RECALCULATION */

  //if (supportsSvg()) {
  //  $("#portal-logo img").attr('src', '++resource++plonetheme.bootstrapModern.css/logo.svg');
  //}

  //mediaShow.recalculateHeight($(".embededMediaShow.javascripted"));

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

  /*$(".slideshowContent").hover(function() {
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



