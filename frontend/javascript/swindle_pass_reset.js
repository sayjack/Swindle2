/////////////////////Begin Mootools functionality/////////////////////////////

window.addEvent('domready', function() {
    var name;
    var email;
    var pass;
    
    $('id_inputUsername').addEvent('blur', function() {
        email = this.get('value');
     });
     
    $('id_button_reset_pass').addEvent('click',function(){
        if(email == "" || email === undefined) {
            $('spanId_prompt').setStyle('visibility', 'visible');
            $('spanId_prompt').set('html', 'Email required!');
        } else {
            var passReset = new Request.JSON({
                url: '/pass_reset',
                method: 'post',
                data: {
                      'email': email,
                },
                onComplete: function(response){
                    $('loginDivId').empty();
                    $('loginDivId').set('html', response.fromServer);
                }
            });
            passReset.send();
        }
    });
    
});
