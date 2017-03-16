#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        prvo_stevilo = float(self.request.get("prvo_stevilo"))
        drugo_stevilo = float(self.request.get("drugo_stevilo"))
        znak = self.request.get("znak")

        rezultat = ""

        if znak == "+":
            rezultat = prvo_stevilo + drugo_stevilo
        elif znak == "-":
            rezultat = prvo_stevilo - drugo_stevilo
        elif znak == "*":
            rezultat = prvo_stevilo * drugo_stevilo
        elif znak == "/":
            rezultat = prvo_stevilo / drugo_stevilo

        return self.write(rezultat)

class SkritosteviloHandler(BaseHandler):
    def get(self):
        return self.render_template("skritostevilo.html")

    def post(self):
        stevilo = int(self.request.get("stevilo"))

        skrito_stevilo = random.randint(1, 5)

        if stevilo == skrito_stevilo:
            return self.write("Pravilno")
        else:
            return self.write("Narobe")

class PretvornikHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")

    def post(self):
        km = float(self.request.get("km"))
        return self.write(km * 0.62137)

    def post(self):
        milja = float(self.request.get("milja"))
        return self.write(milja / 0.62137)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/skritostevilo', SkritosteviloHandler),
    webapp2.Route('/pretvornik', PretvornikHandler),
], debug=True)
