$(document).ready(function(){
    
    if($(window).width() > 765) {


        if($('.about--paralax').length) {
            $(window).bind('load scroll', function(){
                $('.about--paralax').css('backgroundPosition', 'center -' + $(window).scrollTop() / 3 + 'px');
            });
        }

        if($('.form-line--paralax').length) {
            $(window).bind('load scroll', function(){
                $('.form-line--paralax').css('backgroundPosition', 'center -' + $(window).scrollTop() * 0.5 + 'px');
            });
        }

        if($('.h-block-paralax').length) {
            $(window).bind('load scroll', function(){
                $('.h-block-paralax').css('backgroundPosition', 'center -' + $(window).scrollTop() * 0.5 + 'px');
            });
        }
    }
    
    $('.mobile-menu-trigger').click(function(e){
        e.preventDefault();
        $(this).toggleClass('open');
        $('nav ul').toggleClass('open');
    });
    
    
   
    $('.short-search-trigger').click(function(e){
        e.preventDefault();
        $(this).addClass('open');
		if($(window).width() < 1180) {
        $('nav ul').addClass('hidden');
		}
        $('.short-search-form').addClass('open');
    });
	
    
    $('.btn-show-filter').click(function(e){
        e.preventDefault();
        var get_current_text = $(this).text();
        var get_new_text = $(this).attr('data-back-text');
        $(this).text(get_new_text);
        $(this).attr('data-back-text',get_current_text);
        $('.l-search').toggleClass('show');
        
    });
	
	$('.btn-show-subscribe').click(function(e){
        e.preventDefault();
        var get_current_text = $(this).text();
        var get_new_text = $(this).attr('data-back2-text');
        $(this).text(get_new_text);
        $(this).attr('data-back2-text',get_current_text);
        $('.subscription').toggleClass('show');
        
    });
    
    $('.item-tab-control a').click(function(e){
        e.preventDefault();
        $('.item-tab-control a').removeClass('active');
        $(this).addClass('active');
        var tab_id = $(this).attr('data-tab');
        
        $('.tab').removeClass('active');
        $('.tab').each(function(){
            if($(this).attr('data-tab') == tab_id) {
                $(this).addClass('active');
            }
        });
        
        
    });

    
    $("select").select2({
    });
	
 
  //  $('.item__favourites').click(function(e){
  //      e.preventDefault();
   //     $(this).toggleClass('added');
  //  });
    
    $('.two-ca').owlCarousel({
        loop:false,
        margin:10,
        nav:true,
        dots: false,
        responsive:{
            0:{
                items:1
            },
            768:{
                items:2
            },
            1000:{
                items:3
            },
            1416:{
                items:4
            },

            1700:{
                items:5
            }
        }
    });
	$('.one-ca').owlCarousel({
        loop:false,
        margin:10,
        nav:true,
        dots: false,
        responsive:{
            0:{
                items:1
            },
            768:{
                items:2
            },
            1000:{
                items:3
            },
            1216:{
                items:4
            }
        }
    });
    
    
    if($('.bxslider').length) {
        
        var index = 0;
        
        $('.slider-item').each(function(){
            $('.slider-thumbnails').append('<a data-slide-index="'+ index +'" href=""><img src="'+ $(this).find('img').attr('src') +'"  alt="img"></a>');
            
            index++;
        });
        
        $('.bxslider').bxSlider({
          pagerCustom: '.slider-thumbnails',
		  infiniteLoop:false
        });
    }
    
    $('.select2-results__option:first-child').click(function(e){
        e.preventDefault();
        e.stopPropagation();
        alert();
        $(this).toggleClass('active');
        $(this).siblings('.select2-results__option[aria-selected]').toggleClass('active');
    });
    
    if($('.slider').length) {
        $( function() {
            $( ".slider" ).slider({
              range: true,
              min: 0,
              max: $('#priceMax').data('max'),
              values: [ 0, $('#priceMax').data('max') ],
            slide: function( event, ui ) {
                
            $( "#priceMin" ).val( ui.values[ 0 ] );
	        $( "#priceMax" ).val( ui.values[ 1 ] );
              }
            });
           $('#priceMin,#priceMax').change(function() {
      $('#slider').slider('values', [parseInt($('#priceMin').val()), parseInt($('#priceMax').val())]);
}); 
            
            
        } );
    }
    
    
    $('.lang-list__trigger').click(function(e){
        e.preventDefault();
        $(this).toggleClass('open');
        $('.lang-list__ul').toggleClass('open');
    });
    
    
    $('body').click(function(e){
		if(!$(e.target).parents('.top-bar .open').length && !$(e.target).hasClass('open')) {
            $('.top-bar .open').removeClass('open');
            $('nav ul.hidden').removeClass('hidden');
        }
    });
    
    $('.inp-counter input, .inp-counter textarea').keyup(function(e){
        e.preventDefault();
        var val = +$(this).val().length;
        $(this).siblings('.inp-counter__count').html(+$(this).siblings('.inp-counter__count').attr('data-val') - val);
    });
    
		$(document).on('change', '[name="select_language"]', function(e){
		$('[name="select_language"]').submit();
	});
	    $('.flashmessage .ico-close').click(function(){
        $(this).parents('.flashmessage').remove();
    });
    $('#mask_as_form select').on('change',function(){
        $('#mask_as_form').submit();
        $('#mask_as_form').submit();
    });
    
	//  scrollreveal

    
});