#!/usr/bin/env python
import os
import jinja2
import webapp2

from datetime import datetime

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

def calculator(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1-num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2

def pretvori_mft(vrednost):
    return round(float(vrednost) * 3.28084, 0)

def pretvori_kglbs(vrednost):
    return round(float(vrednost) * 2.20462, 1)

def pretvori_kmhms(vrednost):
    return round(float(vrednost) * 0.27778, 1)

class HelloHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")

class KalkHandler(BaseHandler):
    def post(self):
        st1 = int(self.request.get("stevilo1"))
        st2 = int(self.request.get("stevilo2"))
        oper = self.request.get("operacija")
        rezultat = calculator(st1, st2, oper)
        podatki = {
            'stevilo1': st1,
            'stevilo2': st2,
            'operacija': oper,
            'rezultat': rezultat
        }
        return self.render_template("kalkulator.html", params=podatki)

class UganiHandler(BaseHandler):
    def post(self):
        stevilo = self.request.get("stevilo")
        podatki = {
            'stevilo': stevilo
        }
        return self.render_template("uganistevilo.html", params=podatki)

class PretvoriHandler(BaseHandler):
    def post(self):
        vredn1 = int(self.request.get("vrednost"))
        enote = self.request.get("enote")
        if enote == "mft":
            vredn2 = pretvori_mft(vredn1)
            enota1 = "m"
            enota2 = "ft"
        elif enote == "kglbs":
            vredn2 = pretvori_kglbs(vredn1)
            enota1 = "kg"
            enota2 = "lbs"
        elif enote == "kmhms":
            vredn2 = pretvori_kmhms(vredn1)
            enota1 = "km/h"
            enota2 = "m/s"

        podatki = {
            'vredn1': vredn1,
            'enota1': enota1,
            'enota2': enota2,
            'vredn2': vredn2
        }
        return self.render_template("pretvornikenot.html", params=podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', HelloHandler),
    webapp2.Route('/kalkulator', KalkHandler),
    webapp2.Route('/uganistevilo', UganiHandler),
    webapp2.Route('/pretvornikenot', PretvoriHandler)
], debug=True)
