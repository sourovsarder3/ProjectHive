from django.urls import path
from . import views
from .middlewares.chat_user import UserAuthMiddleware, LoginMiddlware


urlpatterns = [
    path("", UserAuthMiddleware(views.message), name='chat_page'),
    path("workspace/", views.workspace, name='workspace'),
    path("login/", LoginMiddlware(views.login), name='login'),
    path("signup/", views.signup, name='signup'),
    path("forget-password/", views.forget_password, name='forget_password'),
    path("change-password/", views.change_password, name='change_password'),
    path("update_password/", views.update_password, name='update_password'),
    path("logout/", views.logout, name='logout'),
    path("workspacelogout/", views.workspacelogout, name='workspacelogout'),
    path("createChannel/", views.createChannel, name='createChannel'),
    path("addChannelMember/", views.addChannelMember, name='addChannelMember'),
    path("deleteChannel/", views.deleteChannel, name='deleteChannel'),
    path("invitationAccept", views.invitationAccept, name='invitationAccept'),
    path("invitationSend/", views.invitationSend, name='invitationSend'),
    path("leaveWorkspace/", views.leaveWorkspace, name='leaveWorkspace'),
    path("removeWorkspace/", views.removeWorkspace, name='removeWorkspace'),
    path("update_seen_by/", views.update_seen_by, name='update_seen_by')
]
