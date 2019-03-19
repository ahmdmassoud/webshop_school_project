/*global
document, window, setTimeout, $, alert, jQuery
*/
function getCookie(name) {
 //  gets the cookies https://docs.djangoproject.com/en/2.1/ref/csrf/

 // this is used to get the csfr token so that django accepts the post request
    'use strict';
    var i, cookie, cookies, cookieValue = 0;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i += 1) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    'use strict';
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// creates a popup text letting the user get some response from what they click
function mySnackbar(message) {
    'use strict';
    // Get the snackbar DIV
    var x = $("#snackbar")[0];
    x.innerHTML = message;
    // Add the "show" class to DIV
    x.className = "show";
    // After 3 seconds, remove the show class from DIV
    setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}

// receives postMessage and checks which message type it is
function receiveMessage(event) {
    "use strict";
    // sets up ajax to use CSRFToken
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var gameMessage, msgType;
    msgType = event.data.messageType;
    gameMessage = JSON.stringify(event.data);

    // if the msg type is one of the above, it sends an ajax request
    if (msgType === 'SCORE' || msgType === 'SAVE' ||
              msgType === 'LOAD_REQUEST' || msgType === 'ERROR') {
        $.ajax({
            url: "",
            type: "post",
            data: {'values': gameMessage },
            success: function (response) {
                if (response.messageType === "LOAD") {
                    var iframeWin = $("#gameframe")[0].contentWindow;
                    iframeWin.postMessage(response, '*');
                    mySnackbar("Your last save has been loaded");
                } else {
                    mySnackbar(response);
                }
            }
        });
    // If the message is only settings, it resizes the frame
    } else if (event.data.messageType === "SETTING") {
        $('#gameframe')[0].width = event.data.options.width;
        $('#gameframe')[0].height = event.data.options.height;
    }
}
window.addEventListener('message', receiveMessage);
