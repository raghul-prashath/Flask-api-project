from . import * 

#Admin Panel
def addView():
    admin.add_view(RolesController(Roles, db.session,category="Roles"))
    admin.add_view(UsersController(Users, db.session))
    admin.add_view(Controller(SpecialRights, db.session,category="Roles"))
    admin.add_view(FeedXmlsController(FeedXmls, db.session,category="Feeds"))
    admin.add_view(FeedsController(Feeds, db.session,category="Feeds"))
    admin.add_view(CommentController(Comments, db.session,category="Feeds"))
    admin.add_view(UserLikeController(UserLike, db.session,category="Feeds"))
    admin.add_link(MenuLink(name='Logout',url="/logout"))
