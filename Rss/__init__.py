#Packages
import feedparser
from pytz import timezone
import dateutil.parser
import re
from datetime import date,datetime,timedelta
import dateutil.relativedelta
import os
#Flask
from flask import Flask,request,render_template,redirect, url_for,flash,jsonify,make_response
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,jwt_required,create_access_token,jwt_refresh_token_required
from flask_jwt_extended import create_refresh_token,get_jwt_identity,set_access_cookies,set_refresh_cookies, unset_jwt_cookies
from flask_restful import Resource, Api
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
#SQLAlchemy
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
login_manager= LoginManager()
login_manager.init_app(app)
db= SQLAlchemy(app)

from Rss.models import MyAdminIndexView,feeds
admin=Admin(app,name='Admin Panel',template_mode='bootstrap3',index_view=MyAdminIndexView())
from Rss.handleDbms import FeedXmls,Roles,Users,Feeds,Comments,UserLike,SpecialRights,db
from Rss.handleDbms import handleDb,getXml,getFeeds
from Rss.handleData import returnRecord,returnNoRepRecord,returnData,filtersort
from Rss.handleDbms import selectEmail,registerUser,addComment,getComment,feedEdit,feedUrlAdd,addLikes,addDislikes
from Rss.handleDbms import newRole,getFeeds,checkUserId,checkFeedId,getRole,deleteRole,deleteFeed,deleteUser,getSpecialRights, commentDelete,getUser, getAccess, updateAccess,deleteAccess,getPost
from Rss.handleAdmin import Controllers,RolesController,UsersController,FeedsController,UserLikeController,CommentController,FeedXmlsController,Controller
from Rss.handleAdmin import hashPass,load_user,adminLogin,adminLogout

records=returnRecord()
recordsNoRep=returnNoRepRecord(records)
data=returnData(records)
allFeeds=data[0]
category=data[1]

from Rss.appModels import categoryList,register,login,getFeedById,getValues,getValuesById,handleComment,userTemplate,refresh,logout
from Rss.appModels import editFeed,incrementLikes,incrementDislikes,addUrl,deleteUserById,deleteFeedById,user,role,access,tokenData
from Rss.handleAdminPanel import addView
from Rss.routes import routesApi

routesApi()
addView()
db.create_all()

if __name__=='__main__':
    app.run()

