(function($) {
    $(document).ready(function() {

        // If the info viewlet isn't here, 
        // stop right away.
        if( $('#js_info').length < 1 )
        {
            return 0;
        }

        var url = document.URL;

        // We really don't need to ever use this on the edit page.
        if (url.indexOf('/edit') > 0) {
            return 0;
        }

        var json = $('#buttonJson').text();
        var settings = jQuery.parseJSON( json );

        if( settings.length < 1 )
        {
            return 0;
        }
        var stateDescription = settings.stateDescription;
        var allowed_transitions = settings.allowedTransitions;
        var state = settings.wfState;
        var pageElement = settings.pageElement;
        var fixed = settings.floating;
        var preferencesUrl = settings.preferencesUrl;
        var location = settings.floatLocation;
        var space = settings.floatSpacing + "px";

        function setLocation() {
            var top = "auto";
            var right = "auto";
            var bottom = "auto";
            var left = "auto";


            if( location == "upperLeft" )
            {
                top = space;
                left = space;
            }
            else if( location == "upperRight" )
            {
                top = space;
                right = space;
            }
            else if ( location == "bottomRight" )
            {
                bottom = space;
                right = space;
            }
            else if( location == "bottomLeft" )
            {
                left = space;
                bottom = space;
            }

            if( location !== null )
            {
                $('#transitionButtons').css('right', right).css('left', left).css('top', top).css('bottom', bottom);
            }
        }

        // This is needed since some URL's end in a slash,
        // and some don't
        function stripSlash(url) {
            if(url.substr(-1) == '/') {
                return url.substr(0, url.length - 1);
            }
            else
            {
                return url;
            }
        }

        function minimize() {
            var right = true;

            if( $(transitionButtons).css('left') !== "auto" )
            {
                right = false;
            }

        }

        function removeCookie() {
            document.cookie = 'buttonsHidden=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        }

        function checkIfHidden() {
            var hidden = getCookie('buttonsHidden');

            if( hidden == 'true' )
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        function hideButtons() {
            var side = location.indexOf('Right');

            if( side > 0 ) {
                side = 'right';
            }
            else {
                side = 'left';
            }

            $('#hideButtons').text('Show');
            $('#transitionButtons').css('right','').css('left','');
            $('#transitionButtons').children().hide();

            $('#hideButtons').show();

            $('#transitionButtons').addClass('hidden').addClass(side);
        }

        function showButtons() {
            $('#hideButtons').text('Hide');
            $('#transitionButtons').children().show();
            $('#transitionButtons').removeClass('hidden').removeClass('left').removeClass('right');

            removeCookie();
            setLocation();
        }
        //Borrowed from http://www.w3schools.com/js/js_cookies.asp.
        //Thanks W3C!
        function getCookie(cname) {
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for(var i=0; i<ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1);
                if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
            }
            return "";
        }

        var base = stripSlash($("base").attr("href"));

        // Since this is referring to links generated internally, and not by a theme,
        // this shouldn't change anytime soon.
        var modify_url_string = "/content_status_modify?workflow_action=";

        // This works by grabbing every <a> that has an href matching the 
        // URI corresponding to the given transitions
        var transitions = $("a[href^='" + base + modify_url_string + "']");

        var buttons = [];
        var allowed = [];
        var transitionClassNames = [];

        // Being very careful to grab the correct edit link
        var editUrl = $('#edit-bar').find('#contentview-edit').find('a');

        // Makes sure the pageElement property is set
        if($(pageElement).text() == "")
        {
            pageElement = "#portal-breadcrumbs";
        }

        $(allowed_transitions).each(function() {
            allowed.push(base + modify_url_string + this);
        });

        transitions.each(function() {

            // if statement checks that the links text is allowed
            if( $.inArray($(this).attr('href'), allowed) >= 0 )
            {
                buttons.push( this );
            }
        });

        if( $(editUrl).length > 0 )
        {
            buttons.push(editUrl);
        }

        if( buttons.length < 1 )
        {
            return 0;
        }

        var html ="<div id='transitionButtons'>";

        html = html + 
        '<span id="prefs_link" rel="#prefsDialog">x</span>' + 
        '<span id="hideButtons">Hide</span>' +
        '<h4>Workflow state: <span class="stateTitle" >' + state +'</span></h4>' +
        '<p class="tbText">' + stateDescription + '</p>' + 
        '<div class="button-row"></div></div>';

        var message = "If you no longer want to see this widget,";
        message += " check the \"Disable transition buttons widget\" option in personal preferences."

        $(html).insertBefore(pageElement);

        $(buttons).each(function() {

            var thisButton =
            '<button class="button" ' +
            'onclick="window.location.href=\'' + $(this).attr('href') + '\'">' +
            $(this).text() +
            '</button>';

            $('.button-row').append($(thisButton));
        })

        var currentState = $('.state-' + state.toLowerCase() );
        stateColor = currentState.css('background-color');
        
        if( stateColor != "rgba(0, 0, 0, 0)")
        {
            $('.stateTitle').css('background-color', stateColor);
        }
        else
        {
            $('.stateTitle').css('background-color', '#444');
        }

        // add class to make the box "float"
        if( fixed )
        {
            $('#transitionButtons').addClass('floating');
        }

        $('#prefsDialog').prepend(message);

        $('#hideButtons').click(function() {
            if( $('#transitionButtons').hasClass('hidden') ) {
                showButtons();
            }
            else {
                 hideButtons();
                document.cookie="buttonsHidden=true;";   
            }

        });

        $('#prefs_link').overlay({
                top: 250,
        });

        setLocation();

        if( checkIfHidden() )
        {
            hideButtons();   
        }
    
    });
})(jQuery);