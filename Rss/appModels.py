from . import *
        
#Register
class register(Resource):
    def post(self):
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        password = request.get_json()['password']
        records=selectEmail(email)
        def hasNumbers(inputString):
            return any(char.isdigit() for char in inputString)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if(bool(hasNumbers(first_name))==True or bool(hasNumbers(last_name))==True or len(password)<8 or bool(re.search(regex,email))==False ):
            return {'message':'Bad Request','Format': 'False'}, 401
        if records==None:
            registerUser(first_name,last_name,email,password,'user')
            access_token = create_access_token(identity = email)
            refresh_token= create_refresh_token(identity = email) 
            resp=jsonify({'message':'registered successfully','Format': 'True'})
            set_access_cookies(resp,access_token)
            set_refresh_cookies(resp,refresh_token)
            return make_response(resp, 200)
        else:
            return {'message':'user exist','Format': 'Fasle'}, 401

# Login
class login(Resource):
    def post(self):
        email = request.get_json()['email']
        password = request.get_json()['password']
        records=selectEmail(email)
        if records==None:
            return {'message':'Bad Request','Format': 'False'}, 401    
        elif bcrypt.check_password_hash(records[5],password):
            access_token = create_access_token(identity = email)
            refresh_token= create_refresh_token(identity = email)
            resp=jsonify({'message':'Login successfully','Format': 'True'})
            set_access_cookies(resp,access_token)
            set_refresh_cookies(resp,refresh_token)
            return make_response(resp, 200)
        else:   
            return {'message':'invalid username or password','Format': 'False'}, 401

# Returns category
class categoryList(Resource):
    def get(self):
        return {'category': category,'Format':'True'}, 200

# Get Feed by passing id
class getFeedById(Resource):
    def get(self,feedId):
        if checkFeedId(feedId):
            post=getPost(feedId)
            return {'format':'True','feeds': post, 'id': 'True'}, 200
        else:
            return {'format':'False'}, 401


# Returns feeds,keys of feeds,apply sorts and filters.
# Feeds returned after all the filters and sorts
class getValuesById(Resource):
    def get(self,category,filterType,order,time,page,key=None,search=None):
        feedsList=[]
        records=returnRecord()
        recordsNoRep=returnNoRepRecord(records)
        result = filtersort(category.capitalize(),filterType,order,time,records,recordsNoRep,key,search)
        if filterType == "likes":
            if len(result[0][filterType][int(key)])%10 < 5:
                pageno=round(len(result[0][filterType][int(key)])/10)+1
            else:
                pageno=round(len(result[0][filterType][int(key)])/10)
            if pageno == page:
                i=page
                lp=len(result[0][filterType][int(key)])-((round(len(result[0][filterType][int(key)])/10)))*10
                for i in range(i*10-10,(i*10-10)+lp):
                    feedsList.append(result[0][filterType][int(key)][i])
            elif pageno > page: 
                i=page
                for i in range(i*10-10,i*10):
                    feedsList.append(result[0][filterType][int(key)][i])
            else:
                return {'message':'Invalid key','Format': 'False'} ,400
        else:
            if len(result[0][filterType][key.capitalize()])%10 < 5:
                pageno=round(len(result[0][filterType][key.capitalize()])/10)+1
            else:
                pageno=round(len(result[0][filterType][key.capitalize()])/10) 
            if pageno == page:
                i=page
                lp=len(result[0][filterType][key.capitalize()])%10
                for i in range(i*10-10,i*10-10+lp):
                    feedsList.append(result[0][filterType][key.capitalize()][i])
            elif pageno > page: 
                i=page
                for i in range(i*10-10,i*10):
                    feedsList.append(result[0][filterType][key.capitalize()][i])
            else:
                return {'message':'Invalid key','Format': 'False'} ,400
        return {'feed':feedsList,'format':'True'}, 200

# Get feed values
class getValues(Resource):
    def get(self,category,filterType,order,time,key=None,search=None):
        records=returnRecord()
        recordsNoRep=returnNoRepRecord(records)
        result = filtersort(category.capitalize(),filterType,order,time,records,recordsNoRep,key,search)
        return result, 200

# Handled get and post comments
class handleComment(Resource):
    def get(self):
        feedId = request.get_json()['feedId']
        if checkFeedId(feedId):
            return getComment(feedId),200
        else:
            return {'message':'invalid feedId','Format': 'False'}, 400
    def post(self):
        feedId = request.get_json()['feedId']
        userId = request.get_json()['userId']
        comments = request.get_json()['comments']
        if checkFeedId(feedId) and checkUserId(userId):
            return addComment(feedId,userId,comments), 200
        else:
            return {'message':'feedid or userid doesnt exist','Format': 'False'}, 400
    
    def delete(self):
        commentId = request.get_json()['commentId']
        comment = commentDelete(commentId)
        return comment


# User Template, A new feed by user            
class userTemplate(Resource):
    def post(self):
        feedsList=[]
        userId=request.get_json()['userId']
        feedTitle=request.get_json()['feedTitle']
        summary=request.get_json()['summary']        
        imageUrl=request.get_json()['imageUrl']
        category=request.get_json()['category']
        author=request.get_json()['author']
        link=request.get_json()['link']
        logo='https://th.bing.com/th/id/OIP.w2McZSq-EYWxh02iSvC3xwHaHa?pid=Api&rs=1'
        likes=0,
        dislikes=0,
        time= datetime.now()
        time=str(time.strftime('%Y-%m-%d %H:%M:%S'))+'+5:30' 
        times = datetime.strptime(time[:19],'%Y-%m-%d %H:%M:%S')
        dispTime= str(times.strftime('%H:%M:%S %d %B %Y,%A'))
        d = datetime.strptime(dispTime[:5],"%H:%M")
        dispTime=str(d.strftime("%I:%M %p"))+' on '+dispTime[8:]
        
        if len(feedTitle)==0 or len(summary)==0 or len(author)==0 or checkUserId(userId)==0:
            return {'message':'Bad Request','Format':'False'}, 400
        if len(imageUrl)==0:
            imageUrl='https://www.zylogelastocomp.com/wp-content/uploads/2019/03/notfound.png'
        if len(category)==0:
            category='Headline'
        tags='rp'
        feedsList.append(feeds(feedTitle,summary,time,imageUrl,category,author,link,dispTime,logo,userId,tags))        
        value=getFeeds(feedsList,1)
        if value==0:
            return {'message':'Bad Request','Format':'False'}, 400
        else:
            return {'message':'Feed added','Format':'True'}, 200

# Edit a feed
class  editFeed(Resource):
    def post(self, feedId):
        title = request.get_json()['title']
        summary = request.get_json()['summary']
        category=request.get_json()['category']
        author=request.get_json()['author']
        link=request.get_json()['link']
        fId = checkFeedId(feedId)
        if fId:
            records=feedEdit(title,summary,category,author,link,feedId)
            return {'message':'Feed edited','Format': 'True'}, 200
        else:
            return {'message':'Bad Request','Format': 'False'}    

# Admin
# Adding a new feedXml
class addUrl(Resource):
    def post(self):
        url = request.get_json()['url']
        parsed=feedparser.parse(url)
        categoryUrl = request.get_json()['category'].capitalize()
        if categoryUrl in category:
            if len(parsed.feed)!=0:
                feedUrl = feedUrlAdd(url,categoryUrl)
                return feedUrl
        return {'message':'category not found','Format': 'False'}

# Admin         
# Adding a new role by admin
class adminRegister(Resource):
    def post(self):
        first_name = request.get_json()['first_name']
        last_name = request.get_json()['last_name']
        email = request.get_json()['email']
        role = request.get_json()['role']
        password = request.get_json()['password']
        records=selectEmail(email)
        if records==None:
            registerUser(first_name,last_name,email,password,role)
            access_token = create_access_token(identity = email)
            refresh_token= create_refresh_token(identity = email)
            resp=jsonify({'message':'registered successfully','Format': 'True'})
            set_access_cookies(resp,access_token)
            set_refresh_cookies(resp,refresh_token)
            return make_response(resp, 200)
        else:
            return {'message':'user exist','Format': 'Fasle'}, 401

# Increase dislikes
class incrementDislikes(Resource):
    def post(self,userId,feedId):
        uId = checkUserId(userId)
        if uId:
            fId = checkFeedId(feedId)
            if fId:
                disLikes = addDislikes(userId,feedId)
                if disLikes==True:
                    return {'message':'post disliked','Format': 'True'}, 200              
                else:
                    return {'message':'post already disliked','Format': 'False'}, 400              
            else:
                return {'message':'feedid doesnt exist','Format': 'False'}, 400
        else:
            return {'message':'userid doesnt exist','Format': 'False'}, 400

# Increase likes
class incrementLikes(Resource):
    def post(self,userId,feedId):
        uId = checkUserId(userId)
        if uId:
            fId = checkFeedId(feedId)
            if fId:
                likes = addLikes(userId,feedId)
                if likes==True:
                    return {'message':'post liked','Format': 'True'}, 200              
                else:
                    return {'message':'post already liked','Format': 'False'}, 400              
            else:
                return {'message':'feedid doesnt exist','Format': 'False'}, 400
        else:
            return {'message':'userid doesnt exist','Format': 'False'}, 400

# Admin
# Delete User
class deleteUserById(Resource):
    def get(self,userId):
        if checkUserId(userId):
            deleteUser(userId)
            return {'message':'user deleted','Format': 'True'}, 200              
        else:
            return {'message':'Bad Request','Format': 'False'}, 401

# Admin
# Delete Feed
class deleteFeedById(Resource):
    def get(self,feedId,userId):
        if checkFeedId(feedId) and checkUserId(userId):
            return deleteFeed(feedId,userId)
        else:
            return {'message':'Bad Request','Format': 'False'}, 401

class user(Resource):
    def get(self,userId):
        user = getUser(userId)
        return user

class role(Resource):
    def get(self):
        return getRole()  
    def delete(self):
        id = request.get_json()['id']
        return deleteRole(id)
    def post(self):
        role = request.get_json()['role']
        return newRole(role)

class access(Resource):
    def get(self):
        userId = request.get_json()['userId']
        return getAccess(userId=None)    
    def post(self):
        userId = request.get_json()['userId']
        colId = request.get_json()['colId']
        cFeed = request.get_json()['cFeed']
        rFeed = request.get_json()['rFeed']
        uFeed = request.get_json()['uFeed']
        dFeed = request.get_json()['dFeed']
        rolesTable = request.get_json()['rolesTable']
        usersTable = request.get_json()['usersTable']
        feedsTable = request.get_json()['feedsTable']
        userLikeTable= request.get_json()['userLikeTable']
        commentTable= request.get_json()['commentTable']
        feedXmlsTable= request.get_json()['feedXmlsTable']
        return updateAccess(userId,colId,cFeed,rFeed,uFeed,dFeed,rolesTable,usersTable,feedsTable,userLikeTable,commentTable,feedXmlsTable)
    def delete(self):
        id = request.get_json()['id']
        return deleteAccess(id)

#Logout
class logout(Resource):
    @jwt_required
    def post(self):
        resp=jsonify(logout=True)
        unset_jwt_cookies(resp)
        return make_response(resp, 200)


class refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        return {'access_token': create_access_token(identity=current_user)},200

class tokenData(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        return {'logged in as : ' : email}, 200