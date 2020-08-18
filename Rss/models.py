from . import *

# Feeds class stores the details and appends day to day informations and feeds.
class feeds:
    def __init__(self,feedTitle,summary,time,imageUrl,category,author,link,dispTime,logo,userId,tags):
        self.feedTitle=feedTitle
        self.summary=summary
        self.time=time
        self.imageUrl=imageUrl
        self.category=category
        self.author=author
        self.link=link
        self.dispTime=dispTime
        self.logo=logo
        self.userId=userId
        self.tags=tags
        
class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False
    def is_accessible(self):
        return current_user.is_authenticated