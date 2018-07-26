# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
from google.appengine.api import users

import hfwwgDB

"""
#Remove the standard version of Django
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

#For sys.path to have our own directory first, in case we want to import form it
if os.name=='nt':
    os.unlink=lambda:None

#Add Django 1.0 archive to the path
django_path='django.zip'
sys.path.insert(0,django_path)

#Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE']='settings'
"""


"""继承ModelForm 创建一个新类，然后将这个新类连接到你的数据模型"""
class SightingForm(djangoforms.ModelForm):
    class Meta:
        model=hfwwgDB.Sighting
        exclude=['which_user']
        

class SightingInputPage(webapp.RequestHandler):
    def get(self):
        html=template.render('templates/header.html',{'title':'Report a Possible Sight'})
        html=html+template.render('templates/form_start.html',{})
        html=html+str(SightingForm(auto_id=False))
        """设置False name=属性名"""
        html=html+template.render('templates/form_end.html',{'sub_title':'Submit Sighting'})
        html=html+template.render('templates/footer.html',{'links':''})
        self.response.out.write(html)

    def post(self):
        new_sighting=hfwwgDB.Sighting()
        new_sighting.which_user=users.get_current_user()
        new_sighting.name=self.request.get('name')
        new_sighting.email=self.request.get('email')
        new_sighting.date=self.request.get('date')
        new_sighting.time=self.request.get('time')
        new_sighting.location=self.request.get('location')
        new_sighting.fin_type=self.request.get('fin_type')
        new_sighting.whale_type=self.request.get('whale_type')
        new_sighting.blow_type=self.request.get('blow_type')
        new_sighting.wave_type=self.request.get('wave_type')
        new_sighting.put()
        html=template.render('templates/header.html',{'title':'Thank You!'})
        html=html+'<p>Thank you for providing your sighting data.</p>'
        html=html+template.render('templates/footer.html',{'links':'Enter<a href="/">another sighting</a>'})
        self.response.out.write(html)

        
"""为应用创建一个新的webapp对象"""
app=webapp.WSGIApplication([('/.*',SightingInputPage)],debug=True)

"""启动web应用"""
def main():
    run_wsgi_app(app) 




if __name__=='__main__':
    main()
