Arnolfini = {};

Arnolfini.bodyclick = false
Arnolfini.searchopen = false
Arnolfini.menuopen = false

Arnolfini.doesBlockOverflow = function (block)
{
    var $this = $(block);
    var $children = $this.find('.tileMedia');
    var len = $children.length;
    
    return len > 3;
}

Arnolfini.archiveShowButtons = function ()
{
    $('.archiveBlocks').each(function ()
                 {
                    if (Arnolfini.doesBlockOverflow($(this)))
                    {
                        $(this).find('.archiveViewAllButton').show();
                    }
                })
}

Arnolfini.events = function ()
{
    // show search form on click
    $('.showmenu a').click(function(event) {
        if (!Arnolfini.menuopen) {
            $('#portal-globalnav').fadeIn();
            $('#portal-globalnav').addClass('openelement');
            Arnolfini.bodyclick = true
            Arnolfini.menuopen = true
        }
        else
        {
            //Close the menu on second click
            $('.openelement').fadeOut('fast');
            $('.openelement').removeClass('openelement');
            Arnolfini.searchopen = false;
            Arnolfini.menuopen = false;
            Arnolfini.bodyclick = false;
        }
        event.stopPropagation();
        return false;
    });
    
    // show search form on click
    $('.headerSearch .searchButton').click(function(event) {
        event.stopPropagation();
        if (Arnolfini.searchopen) {
            $('#nolivesearchGadget_form').submit();
        } else {
            $('.searchField').fadeIn();
            $('.searchField').addClass('openelement');
            $('.searchField').focus();
            Arnolfini.bodyclick = true
            Arnolfini.searchopen = true
        }
        return false;
    });
    
    // when the menu or the search box are open, we close them on body click
    $("body").click(function(event) {   
        if (Arnolfini.bodyclick && !$(event.target).is('.openelement, a') && !$(event.target).closest('.openelement').length) {
            event.stopPropagation();
            $('.openelement').fadeOut('fast');
            $('.openelement').removeClass('openelement');
            Arnolfini.searchopen = false;
            Arnolfini.menuopen = false;
            Arnolfini.bodyclick = false;
        }
    });
    
    //For iphone and ipad
    if (navigator.appName != "Microsoft Internet Explorer")
    {
        document.addEventListener('touchend',function(event) {
            if (Arnolfini.bodyclick && !$(event.target).is('.openelement, a') && !$(event.target).closest('.openelement').length) {
                event.stopPropagation();
                $('.openelement').fadeOut('fast');
                $('.openelement').removeClass('openelement');
                Arnolfini.searchopen = false;
                Arnolfini.menuopen = false;
                Arnolfini.bodyclick = false;
            }
        });
    }

}

mediaShow.buttonPrevContent = "&larr;";
mediaShow.buttonNextContent = "&rarr;";

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
    Arnolfini.getNextEvent(slideshow)
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
    Arnolfini.getPrevEvent(slideshow)
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
          descriptionDiv = '<div class="mediaShowDescription">'+$("<div />").html(data.description).text();+'</div>';
        }
        else
        {
      var separator = " ";
      if (data.description != "")
      {
        separator = " - ";
      }
      
      var breadcrumb = (slideNumber + 1) + " of " + slideshow.size + separator;
      if (onSlodeshowSkipPrev == null && slideshow.size <= 1)
      {
        descriptionDiv = $('<div class="mediaShowDescription">'+ data.description +'</div>');
      }
          else
      {
        descriptionDiv = $('<div class="mediaShowDescription">'+ breadcrumb + data.description + '</div>');
      }
        }
    
        var infoDiv = $('<div class="mediaShowInfo"></div>');
        
        infoDiv.append(descriptionDiv);
        slideContainer.append(infoDiv);
        
        //INFO: Uncomment this if you want clickable pictures
        /*var link = '<a href="'+slide.url+'"></a>';
        if (data.media.type == 'Video' || data.media.type == 'Youtube' || data.media.type == 'Vimeo')
        {
          var link = "<a></a>";
        }*/
        
        //INFO: Comment next line if you want clickable pictures 
        var link = '<a onclick="mediaShow.next('+mediaShow.indexOf(slideshow)+');"></a>';
        
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
mediaShow.ratioX = 768;
mediaShow.ratioY = 512;
mediaShow.infoSize = 60;

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

Arnolfini.getNextEvent = function (slideshow)
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

Arnolfini.getPrevEvent = function (slideshow)
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
                "loaded": mediaShow.NOT_LOADED
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

Arnolfini.portletLinks = function ()
{
    $('.portletStaticText ul li a').not("#FooterPortletManager .portletStaticText ul li a").each(function()
        {
            var elem = $(this);
            var link = $(this).attr("href") 
            var URL = link + '/get_number_of_results';
            
            if (link == window.location.href)
            {
                $(this).addClass("highlighted")
            }
            
            $.getJSON(URL, function(data)
                  {
                    if (data != null)
                    {
                        var count = $('<span class="resultCount"> '+data+'</span>')
                        if (data == 0)
                        {
                            elem.hide();
                        }
                        else
                        {
                            elem.after(count);
                        }
                    }
                  });
        });
};

Arnolfini.resizeImg = function (id, scale)
{
    $(id).find("img").each(function ()
                   {
                    var src = $(this).attr('src');
                    var new_src = src.replace(/\/image_.+/g, "/image_"+scale);
                    $(this).attr('src', new_src);
                });
}

/*   resizer handler */
resizer.onResize = function ()
{
    mediaShow.recalculateAllHeights();

    if (resizer.currentMode == "small" || resizer.currentMode == "mobile")
    {
        $('#portal-columns').after($("#FrontPageManagerLeft"));
        Arnolfini.resizeImg("#FrontPageManagerRight .portletWrapper .portletCollection", "crop");
        $('#FrontPageManagerLeft').masonry({columnWidth:189, gutterWidth:69, itemSelector:'.portletWrapper', isResizable:true, animate:false});
        $('#portal-column-one').masonry({columnWidth:189, gutterWidth:69, itemSelector:'.portletWrapper', isResizable:true, animate:false});
        $('#portal-column-two').masonry({columnWidth:189, gutterWidth:69, itemSelector:'.portletWrapper', isResizable:true, animate:false});
    }
    else
    {
        try
        {
            $('#FrontPageManagerLeft.masonry').masonry( 'destroy' );
            $('#portal-column-one.masonry').masonry( 'destroy' );
            $('#portal-column-two.masonry').masonry( 'destroy' );
        }
            catch(err)
        {
            //Do nothing
        }
        
        Arnolfini.resizeImg("#FrontPageManagerRight .portletWrapper .portletCollection", "crop");
        
        $("#FrontPageManagerRight").after($("#FrontPageManagerLeft"))
    }
    
    //$('.carousel').resizeCarousel();
}

// Test for nth-child(...n) support
Modernizr.testStyles(" #modernizr div:nth-child(3n){width:10px;} ", function(elem, rule) {
    var bool = false, divs = elem.getElementsByTagName("div");
    if (divs.length == 7){
        var test = window.getComputedStyle ? function(i){
            return getComputedStyle(divs[i], null)["width"] == "10px";
        } : function(i){
            return divs[i].currentStyle["width"] == "10px";
        };
        bool = !test(0) && !test(1) && test(2) && !test(3) && !test(4) && test(5) && !test(6);
    }

    Modernizr.addTest("nthchildn", bool);
}, 7);

Arnolfini.IEFixNthChild = function () {
    $(".threecol div.tileItem:nth-child(3n+2)").addClass("threecolNthChild");
}

Arnolfini.showShareCounters = function ()
{
    $('.addthis_counter').each(function ()
                {
                    if ($(this).text() !== '0')
                    {
                        $(this).addClass('visible');
                    }
                });
}


Arnolfini.frontPageColors = function ()
{
    var colors = []
    
    for (j in Arnolfini.colorMapping)
    {
        colors.push(Arnolfini.colorMapping[j]['class']);
    }
    
    for (i in Arnolfini.colorMapping)
    {
        tag = Arnolfini.colorMapping[i];
        
        $("body.template-front_page_view .tag_" + tag['tag'].replace(" ", "_" )).each(function () {
            var taken = false;
            
            for (c in colors)
            {
                if ($(this).hasClass(colors[c]))
                {
                    taken = true;
                }
            }
            
            if(!taken)
            {
                $(this).addClass(tag["class"]);
                $(this).find(".imagelink").append($('<div class="colorTag '+tag["class"]+'">'+tag["tag"]+'</div>'));
            }
            
        });
    }
}

Arnolfini.carouselFix = function ()
{
    $("#MainContent .carousel").css('visibility', 'visible');
    $("#MainContent").css("background-image", "none");
}

Arnolfini.trackEcommerce = function (title, price, category)
{
    var d = new Date();
    var timestamp = d.getDate().toString() + "-" + (d.getMonth() + 1) +"-"+ d.getFullYear().toString() +"-"+ d.getHours().toString() +":"+ d.getMinutes().toString();
    console.log("Tracking transaction "+encodeURIComponent(title) + timestamp +" with price: " + price);
    _gaq.push(['_addTrans',
       encodeURIComponent(encodeURIComponent(title) + "-" + timestamp),           // transaction ID - required
       'Arnolfini', // affiliation or store name
       price.toString(),          // total - required
       '',           // tax
       '',          // shipping
       '',       // city
       '',     // state or province
       ''      // country
    ]);
    _gaq.push(['_addItem',
       encodeURIComponent(title),           // transaction ID - necessary to associate item with transaction
       '',           // SKU/code - required
       title,        // product name
       category,   // category or variation
       price.toString(),          // unit price - required
       '1'               // quantity - required
    ]);
    _gaq.push(['_trackTrans']);
}

$(document).ready(function() {
    $('#portal-globalnav li a').removeAttr('title');
    setTimeout(Arnolfini.carouselFix, 1000);
    Arnolfini.frontPageColors();
    Arnolfini.events();
    Arnolfini.archiveShowButtons();
    if ($(".columns").length > 0)
    {
         var currentLetter= "";
         $('.separateByLetters').find('h2.summary a').each(function ()
                {
                    var name = $(this).text();
                    firstLetter = name[0].toUpperCase();
                    if (firstLetter != currentLetter)
                    {
                        currentLetter = firstLetter;
                        $(this).parent().prepend($('<a class="letter dontend" name="'+firstLetter+'">'+firstLetter+'</a>'));
                    }
                });
         $('.columns').columnize({ width:300 });
    }
    
    Arnolfini.portletLinks();
    
    if (!Modernizr.nthchildn)
    {
        Arnolfini.IEFixNthChild();
    }
    
    setTimeout(Arnolfini.showShareCounters, 5000);
    
    //Fixing the mailchimp error html reading
    errorText = $('.portletMailChimp dl.error dd').text();
    $('.portletMailChimp dl.error dd').html(errorText);
    
    //Adding the arrow to the submit forms
    $('input[type="submit"]').each(function()
                               {
                                if ($(this).attr('value') == 'Submit' || $(this).attr('value') == 'Subscribe' || $(this).attr('value') == 'Save')
                                {
                                    $(this).attr('value', $(this).attr('value') + " \u2192");
                                }
                            });
    
    //iPad Viewport
    if( navigator.userAgent.match(/iPad/i) == null ){  
        viewport = document.querySelector("meta[name=viewport]");
        
        if (navigator.userAgent.match(/Android/i) != null)
        {
            viewport.setAttribute('content', "width=500, initial-scale=0.3");
        }
        else if (navigator.userAgent.match(/iPhone/i) != null)
        {
            viewport.setAttribute('content', "width=500, initial-scale=0.6");
            
        }
    }
    
    $('.membershipForm').submit(function() {
        var name = $(this).find("input[name='item_name']").attr('value');
        var price = $(this).find("input[name='amount']").attr('value');
        console.log("Adding tracking for: " + name)
        return Arnolfini.trackEcommerce(name, price, 'Membership');
    });
});

