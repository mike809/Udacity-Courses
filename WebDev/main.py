import os
import re
import webapp2
import hmac
import random
import hashlib
import string
import json
import jinja2


from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+(\.[\S]+)+$')


jinja_env = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt=make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return h == make_pw_hash(name, pw, salt)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class BlogPosts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

class Users(db.Model):
    name = db.StringProperty(required=True)
    pw = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)

class Signup(BaseHandler):

    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if username_exists(username):
            params['existing_username']="That username already exists. Choose another one"
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            hash_pass = make_pw_hash(username, password)
            self.response.headers.add_header('Set-Cookie', 'name=%s|%s; Path=/' % (str(username), str(hash_pass)))
            Users(name = username, pw = hash_pass).put()
            self.redirect('/unit3/welcome')

class Login(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        have_error = False
        cookie_name = self.request.cookies.get('name').split('|')
        if(len(cookie_name)< 2):
            self.redirect('/blog/signup')
            return
        s_name = cookie_name[0]
        s_pass = cookie_name[1]+'|'+cookie_name[2]
        username = self.request.get('username')
        password = self.request.get('password')

        params = dict(username = username)
        if username != s_name:
            params['error_username'] = "That's not your username."
            have_error = True

        if not valid_pw(username, password, s_pass):
            params['error_password'] = "That's not your password."
            have_error = True

        if have_error:
            self.render('login.html', **params)
        else:
            self.response.headers.add_header('Set-Cookie', 'name=%s|%s; Path=/' % (str(username), str(s_pass)))
            self.redirect('/unit3/welcome')
    
class NewPost(BaseHandler):
    def render_front(self, title="", content="", error=""):
        self.render("newpost.html", title=title, content=content, error = error)

    def get(self):
        self.render("newpost.html")
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            new_post = BlogPosts(subject = subject, content = content)
            new_post.put()
            self.redirect("/blog/%s" % str(new_post.key().id()))

        else:
            error = "Please enter both a subject and content"
            self.render_front(subject, content, error)


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('BlogPosts', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class Blog(BaseHandler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM BlogPosts ORDER BY created DESC")
        self.render("blog.html", posts = posts)

    def get(self):
        self.render_front()

class Welcome(BaseHandler):
    def get(self):
        username = self.request.cookies.get('name')
        name = username.split('|')[0]
        if valid_username(name) and len(name)>0:
            self.render('welcome.html', username = name)
        else:
            self.redirect('/blog/signup')

class PermalinkJson(BaseHandler):
    def get(self, post_id):
        self.response.headers['Content-Type'] = 'application/json'
        post_num = post_id.split('.')[0]
        key = db.Key.from_path('BlogPosts', int(post_num))
        post = db.get(key)

        self.write( json.dumps( {"content" : post.content.replace('"', '\"'), "created" : str(post.created), "subject" : str(post.subject.replace('"', '\"'))}, sort_keys=False, indent=4, separators=(',', ': ')  ) )
        #self.write("," +json.dumps({"created" : str(post.created)}) )
        #self.write("," +json.dumps({"subject" : str(post.subject.replace('"', '\"'))}) )

class Logout(BaseHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
        self.redirect('/blog/signup')

class BlogJson(BaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        posts = db.GqlQuery("SELECT * FROM BlogPosts ORDER BY created DESC")
        output = []
        for post in posts:
            output += [ {"content" : post.content.replace('"', '\"'), "created" : str(post.created), "subject" : str(post.subject.replace('"', '\"'))}   ] 
        self.write(json.dumps(output))

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

def username_exists(username):
    users = db.GqlQuery("SELECT * FROM Users").get()
    
    if users:
        return True
    else:
        return False

app = webapp2.WSGIApplication([('/blog',                Blog),
                               ('/blog/',               Blog),
                               ('blog.json',            BlogJson),
                               ('/blog/login',          Login),
                               ('/blog/.json',          BlogJson),
                               ('/unit2/rot13',         Rot13),
                               ('/blog/signup',         Signup),
                               ('/blog/logout',         Logout),
                               ('/blog/newpost',        NewPost),
                               ('/blog/([0-9]+)',       PostPage),
                               ('/unit3/welcome',       Welcome),
                               ('/blog/([0-9]+\.json)', PermalinkJson)],
                               debug=True)
