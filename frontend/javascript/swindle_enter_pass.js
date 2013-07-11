/////////////////////Begin Mootools functionality/////////////////////////////

window.addEvent('domready', function() {
    var name;
    var email;
    var email2;
    var pass;
    var temp_pass;
    
    $('id_inputUsername').addEvent('blur', function() {
        email = this.get('value');
     });
     
     $('id_inputUsername2').addEvent('blur', function() {
        email2 = this.get('value');
     });
     
    $('id_button_reset_pass').addEvent('click',function(){
        if(email == "" || email === undefined) {
            $('spanId_prompt').setStyle('visibility', 'visible');
            $('spanId_prompt').set('html', 'Please fill in both fields.');
        } else if(email != email2) {
            $('spanId_prompt').setStyle('visibility', 'visible');
            $('spanId_prompt').set('html', "Passwords don't match mate.");
        } else {
            var passReset = new Request.JSON({
                url: '/confirm_new_pass',
                method: 'post',
                data: {
                      'email': email2,
                },
                onComplete: function(response){
                    if(response.fromServer == 'nuts') {
                        $('spanId_prompt').setStyle('visibility', 'visible');
                        $('spanId_prompt').set('html', "Something went wrong!");
                    } else {
                        $('spanId_prompt').setStyle('visibility', 'visible');
                        $('spanId_prompt').set('html', response.fromServer);
                    }       
                }
            });
            passReset.send();
        } 
    });
    
});
