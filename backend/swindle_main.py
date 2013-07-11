import sys
import os.path
import json
import time
from email_pass import *
import cherrypy
from cherrypy.lib.static import serve_file
import sqlite3
from passlib.hash import sha256_crypt


#current directory variable for use in cherrypy (_cp_config) config for static files, css, javascript, images, etc.
par_dir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#cherrypy class that serves URL's
class Swindle:
    
    #serves static static css, javascript, images, etc.
    _cp_config = {'tools.staticdir.on' : True, 'tools.staticdir.dir' : par_dir + '/frontend'}
    
    def __init__(self):
        self.url_pass = ''
    
    def index(self):
       return serve_file(par_dir + "/frontend/index.html", content_type="text/html")
    index.exposed = True
    
    def sign_up(self, **data):
        if len(data) == 0:
            return serve_file(par_dir + "/frontend/sign_up.html", content_type="text/html")
        else:
            pass
        conn = sqlite3.connect("../data/database/users.db")
        cursor = conn.cursor()
        name_from_client = data['name']
        email_from_client = data['email']
        password_from_client = data['password']
        sql = 'SELECT email_db FROM users WHERE email_db = ?'
        cursor.execute(sql, [(email_from_client)])
        email_in_DB = cursor.fetchone()
        email_check = 'nuts'
        if email_in_DB == None:
            pass
        elif email_from_client == email_in_DB[0]:
            email_response = {'fromServer': email_check}
            return json.dumps(email_response)
        pass_from_client = data['password']
        time_stamp = time.time()
        hash_pass = sha256_crypt.encrypt(password_from_client)
        new_user = (name_from_client, email_from_client, hash_pass, time_stamp)
        cursor.execute("INSERT INTO users Values (?, ?, ?, ?)", new_user)
        conn.commit()
        conn.close()
        response = "<h1>Welcome " + name_from_client + "!</h1>"
        result = {"fromServer" : response}
        return json.dumps(result)
    sign_up.exposed = True        
     
     
    def pass_reset(self, **data):
        if len(data) == 0:
            return serve_file(par_dir + "/frontend/pass_reset.html", content_type="text/html")
        else:
            pass
        conn = sqlite3.connect("../data/database/users.db")
        cursor = conn.cursor()
        user_email = data['email']
        temp_pass = new_pass()
        time_stamp = int(time.time())
        sql = "UPDATE users SET password_db = ?, time_db = ? WHERE email_db = ?"
        cursor.execute(sql, (temp_pass, time_stamp, user_email))
        conn.commit()
        conn.close()
        email_func(temp_pass, user_email)
        response = "<h1 id='h1IdEmailSent'>Email sent!</h1><p>Check your inbox. You have 1 minute to update your password! If the link expires you will have to reset your password again.</p>"
        result = {"fromServer" : response}
        return json.dumps(result)
    pass_reset.exposed = True
    
    
    def enter_pass(self, temp_pass):
        self.url_pass = ''
        self.url_pass = temp_pass
        return serve_file(par_dir + "/frontend/enter_pass.html", content_type="text/html")
    enter_pass.exposed = True
    
    
    def confirm_new_pass(self, **data):
        conn = sqlite3.connect("../data/database/users.db")
        cursor = conn.cursor()
        temp_pass_user = self.url_pass
        sql = 'SELECT * FROM users WHERE password_db = ?'
        cursor.execute(sql, [(temp_pass_user)])
        temp_pass_in_DB = cursor.fetchone()
        time_stamp = int(time.time())
        if temp_pass_in_DB is None:
            response = 'nuts' 
        elif time_stamp - int(temp_pass_in_DB[3]) > 1800:
            response = '<h1>You temporary password has expired!  Go get another temporary password <a href="../pass_reset">here</a></h1>'
        else:
            sql_step2 = 'UPDATE users SET password_db = ? WHERE email_db = ?'
            new_hash_pass = sha256_crypt.encrypt(data['email'])
            cursor.execute(sql_step2, (new_hash_pass, temp_pass_in_DB[1]))
            conn.commit()
            response = "<h1>Success!</h1>"
        conn.close()
        result = {"fromServer": response}
        return json.dumps(result)
    confirm_new_pass.exposed = True
    
    
    def password(self, **data):
        conn = sqlite3.connect("../data/database/users.db")
        cursor = conn.cursor()
        pass_from_client = data['password']
        email_from_client = data['email']
        sql = 'SELECT * FROM users WHERE email_db = ?'
        cursor.execute(sql, [(email_from_client)])
        pass_in_DB = cursor.fetchone()
        if pass_in_DB is None or len(pass_in_DB[2]) < 51:
            response = "nuts"
        elif sha256_crypt.verify(pass_from_client, pass_in_DB[2]) == True:
            response = "<h1>Welcome back " + pass_in_DB[0] + "!</h1>"
        else:
            response = "nuts"
        conn.close()
        pass_response = {'fromServer': response}
        return json.dumps(pass_response)
    password.exposed = True
    
       
#start cherrypy server and serve Home() page
cherrypy.quickstart(Swindle())
