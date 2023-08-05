$(document).ready(function() {
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
				classie.add( overlay, 'open' );
			}
		}
	}
	if (triggerBttn != null) {
		triggerBttn.addEventListener( 'click', toggleOverlay );
		closeBttn.addEventListener( 'click', toggleOverlay );
	}
});
