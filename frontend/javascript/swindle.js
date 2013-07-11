/////////////////////Begin Mootools functionality/////////////////////////////

//xhr.open('GET', 'http://localhost:9999', false);
window.addEvent('domready', function() {
    var email;
    var pass;
   
    $('idInputEmail').addEvent('blur', function() {
        email = this.get('value');
     });
     
    $('id_inputPass').addEvent('blur', function() {
        pass = this.get('value');
        //alert(pass);
    });

    $('id_button_login').addEvent('click',function(){
        if((pass == "" || pass === undefined) || (email == "" || email === undefined)) {
            $('spanId_pass').setStyle('visibility', 'visible');
            $('spanId_pass').set('html', 'Missing email or password!');
        } else {
            var passConfirm = new Request.JSON({
                url: '/password',
                method: 'post',
                data: {
                      'password': pass,
                      'email': email,
                },
                onComplete: function(response){
                    if(response.fromServer == 'nuts') {
                        $('spanId_pass').setStyle('visibility', 'visible');
                        $('spanId_pass').set('html', 'Wrong email or password!');
                    } else {
                        $('main').set('html', response.fromServer);
                    }
                }
            });
            passConfirm.send();
        }
    });
    
});
