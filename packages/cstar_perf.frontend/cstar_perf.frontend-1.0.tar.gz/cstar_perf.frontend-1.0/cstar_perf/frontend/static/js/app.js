function signinCallback(authResult) {
    if (authResult['status']['signed_in'] && authResult['status']['method'] == 'PROMPT') {
        // Update the app to reflect a signed in user
        // Hide the sign-in button now that the user is authorized, for example:
        document.getElementById('signinButton').setAttribute('style', 'display: none');

        // Send the code to the server
        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/octet-stream; charset=utf-8',
            success: function(result) {
                window.location.reload();
            },
            processData: false,
            data: authResult['code']
        });


    } else {
        // Update the app to reflect a signed out user
        // Possible error values:
        //   "user_signed_out" - User is signed-out
        //   "access_denied" - User denied access to your app
        //   "immediate_failed" - Could not automatically log in the user
        document.getElementById('signinButton').setAttribute('style', 'display: block');
        console.log('Sign-in state: ' + authResult['error']);
    }
}

function signinReady() {
    // Additional params including the callback, the rest of the params will
    // come from the page-level configuration.
    var additionalParams = {
        'callback': signinCallback
    };
    
    // Attach a click listener to a button to trigger the flow.
    var signinButton = document.getElementById('signinButton');
    $(signinButton).unbind();
    if(signinButton != undefined) {
        signinButton.addEventListener('click', function() {
            gapi.auth.signIn(additionalParams); // Will use page level configuration
        });
    }
}

$(document).ready(function() {
    $.getScript('https://apis.google.com/js/client:plusone.js?onload=signinReady');
    //Assign a temporary signin button callback. This get's unbound in signinReady():
    $('#signinButton').click(function() {
        alert("Google+ javascript hasn't loaded yet. Perhaps you need to whitelist this site in your adblocker or privacy filter?");
    });

});
