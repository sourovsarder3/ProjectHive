import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Prefetch
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Thread, WorkSpace, Channel, WorkspaceMembership, Invitation, PrivateChannelMembership, ChannelMessage, SeenByChannel


def workspace(request):
    if request.method == "GET":
        user_id = request.session.get('user_id')
        user_name = User.objects.get(id=user_id).name
        work_space = WorkspaceMembership.objects.filter(user=user_id)
        invitation = Invitation.objects.filter(send_to=user_id)
        context = {
            'user_id': user_id,
            'user_name': user_name,
            'work_spaces': work_space,
            'invitations': invitation
        }
        return render(request, "chat/workspace.html", context)
    else:
        name = request.POST.get('workspaceName')
        description = request.POST.get('description')
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        workspace = WorkSpace(
            workspaceName=name, workspaceDescription=description, createdBy=user)
        workspace.save()
        workspace_membership = WorkspaceMembership(
            workspace=workspace, user=user)
        workspace_membership.save()
        return redirect('workspace')


def invitationAccept(request):
    if request.POST.get('invitation') == "Accept":
        workspace_id = request.POST.get('workspaceID')
        invitation_id = request.POST.get('invitationID')
        user_id = request.session.get('user_id')
        workspace_obj = WorkSpace.objects.get(id=workspace_id)
        user_obj = User.objects.get(id=user_id)
        workspace_membership = WorkspaceMembership(
            workspace=workspace_obj, user=user_obj)
        workspace_membership.save()
        invitation_obj = Invitation.objects.get(id=invitation_id)
        invitation_obj.delete()
        workspace_member = User.objects.filter(
            workspacemembership__workspace=workspace_id).exclude(pk=user_id)

        for second_user_obj in workspace_member:
            Thread.objects.create(
                first_person=user_obj, second_person=second_user_obj, workspace=workspace_obj)

        return redirect('workspace')
    else:
        invitation_id = request.POST.get('invitationID')
        invitation_obj = Invitation.objects.get(id=invitation_id)
        invitation_obj.delete()
        return redirect('workspace')


def invitationSend(requests):
    send_to_user_id = requests.POST.get('userID')
    send_by_user_id = requests.session.get('user_id')
    workspace_id = requests.session.get('workspaceID')
    send_to_user_obj = User.objects.get(id=send_to_user_id)
    send_by_user_obj = User.objects.get(id=send_by_user_id)
    workspace_obj = WorkSpace.objects.get(id=workspace_id)
    invitation_obj = Invitation(
        send_by=send_by_user_obj, send_to=send_to_user_obj, workspace=workspace_obj)
    invitation_obj.save()
    return redirect('chat_page')


def createChannel(request):
    workspaceID = request.session.get('workspaceID')
    userID = request.session.get('user_id')
    workspace = WorkSpace.objects.get(id=workspaceID)
    user_obj = User.objects.get(id=userID)
    newChannelName = request.POST.get('channelName')
    checked = request.POST.get('checkbox')
    print("Checkbox: ", checked)
    if checked:
        newChannel = Channel(channelName=newChannelName,
                             workspace=workspace, private=True, created_by=user_obj)
        newChannel.save()
        channelMembership = PrivateChannelMembership(
            channel=newChannel, user=user_obj)
        channelMembership.save()
    else:
        newChannel = Channel(channelName=newChannelName,
                             workspace=workspace, private=False, created_by=user_obj)
        newChannel.save()
    return redirect('chat_page')


def deleteChannel(request):
    chat_id = request.POST.get('chatID')
    if request.POST.get('delChannel') == "Yes":
        chat_obj = Channel.objects.get(id=chat_id)
        chat_obj.delete()
        return redirect('chat_page')
    else:
        return redirect('chat_page')


def addChannelMember(request):
    user_id = request.POST.get('userID')
    channel_id = request.POST.get('channelID')
    user_obj = User.objects.get(id=user_id)
    channel_obj = Channel.objects.get(id=channel_id)
    channel_member = PrivateChannelMembership(
        channel=channel_obj, user=user_obj)
    channel_member.save()
    return redirect('chat_page')


def get_non_members_for_private_channel(channel_id, workspaceID):
    channel = Channel.objects.get(id=channel_id)
    members = User.objects.filter(privatechannelmembership__channel=channel)
    user_list = User.objects.filter(workspacemembership__workspace=workspaceID)
    non_members = user_list.exclude(id__in=members)
    return list(non_members)


def get_non_members_for_private_channels(channel_ids, workspace):
    non_members_by_channel = {}
    for channel_id in channel_ids:
        non_members = get_non_members_for_private_channel(
            channel_id, workspace)
        non_members_by_channel[channel_id] = list(non_members)

    return non_members_by_channel


def message(request):
    user_id = request.session.get('user_id')
    user_name = User.objects.get(id=user_id).name
    workspaceID = request.POST.get('workspaceID')

    if workspaceID:
        request.session['workspaceID'] = workspaceID
    else:
        workspaceID = request.session.get('workspaceID')

    workspace_owner = WorkSpace.objects.get(id=workspaceID)
    print("OwnerID: ", workspace_owner.createdBy.id)
    thread = Thread.objects.by_user(
        user=user_id, workspace=workspaceID).prefetch_related('chatmessage_thread')

    channels = Channel.objects.filter(Q(workspace=workspaceID, private=False) | Q(
        privatechannelmembership__user=user_id, workspace=workspaceID)).prefetch_related(Prefetch('message_channel', queryset=ChannelMessage.objects.prefetch_related('message_seen_by')))

    user_list = User.objects.filter(workspacemembership__workspace=workspaceID)

    all_users = User.objects.all()

    users_not_in_workspace = all_users.exclude(
        id__in=user_list.values_list("id", flat=True))

    user = User.objects.get(id=user_id)
    channels_id = Channel.objects.filter(
        created_by=user, workspace=workspaceID, private=True).values_list('id', flat=True)

    not_private_channel_user = get_non_members_for_private_channels(
        channels_id, workspaceID)

    channel_id_for_file = Channel.objects.values(
        'id').filter(workspace=workspaceID)
    all_file = ChannelMessage.objects.filter(
        channel__id__in=channel_id_for_file, has_file='1')

    context = {
        'user_id': user_id,
        'workspaceID': workspaceID,
        'workspace_owner': workspace_owner,
        'user_name': user_name,
        'Threads': thread,
        'user_list': user_list,
        'channels': channels,
        'users_not_in_workspace': users_not_in_workspace,
        'not_private_channel_users': not_private_channel_user,
        'all_file': all_file
    }

    return render(request, "chat/messages.html", context)


def leaveWorkspace(request):
    user_id = request.POST.get('userID')
    workspaceID = request.session.get('workspaceID')
    workspace = WorkspaceMembership.objects.get(
        user__id=user_id, workspace__id=workspaceID)
    workspace.delete()
    threads = Thread.objects.by_user(
        user=user_id, workspace=workspaceID)
    for thread in threads:
        thread.delete()
    return redirect('workspace')


def removeWorkspace(request):
    user_id = request.POST.get('userID')
    workspaceID = request.session.get('workspaceID')
    workspace = WorkspaceMembership.objects.get(user__id=user_id)
    workspace.delete()
    threads = Thread.objects.by_user(
        user=user_id, workspace=workspaceID)
    for thread in threads:
        thread.delete()
    return redirect('chat_page')


def login(request):
    if request.method == "GET":
        return render(request, "chat/login.html")

    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('workspace')
            else:
                return render(request, "chat/login.html", {'error': 'Email or Password is invalid'})
        except:
            return render(request, "chat/login.html", {'error': 'Email or Password is invalid'})


def signup(request):
    if request.method == "GET":
        return render(request, 'chat/signup.html')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        hash_password = make_password(password)
        user = User(name=name, email=email, password=hash_password)
        user.save()
        return redirect('login')


def generate_code():
    return str(random.randint(100000, 999999))


def send_email(name, code, email):
    subject = 'Your ChatApplication Password Reset Code'
    body = f'Hello {name}, Your password reset code is "{code}". Please do not share code to others'
    from_mail = 'sourovsarder3@gmail.com'
    to_mail = [email]
    send_mail(subject, body, from_mail, to_mail)
    print('Mail sent.... ')


def forget_password(request):
    if request.method == "GET":
        return render(request, 'chat/forget_password.html')
    else:
        email = request.POST.get('email')
        code = generate_code()
        try:
            user = User.objects.get(email=email)
            user_name = user.name
            send_email(user_name, code, email)
            user.forget_pass_code = code
            user.save()
            return render(request, 'chat/enter_code.html', {'user_email': user.email})
        except:
            return render(request, 'chat/forget_password.html', {'error': 'Sorry, Email doesn\'t exists '})


def change_password(request):
    if request.method == 'GET':
        return redirect('forget_password')
    else:
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            user = User.objects.get(email=email)
            if user.forget_pass_code == code:
                return render(request, 'chat/change_password.html', {'email': email, 'code': code})
            else:
                return render(request, 'chat/enter_code.html', {'user_email': email, 'error': 'Code doesn\'t match'})
        except:
            return render(request, 'chat/enter_code.html', {'user_email': email, 'error': 'Something went wrong'})


def update_password(request):
    if request.method == 'GET':
        return redirect('forget_password')
    else:
        first_pass = request.POST.get('first_pass')
        second_pass = request.POST.get('second_pass')
        email = request.POST.get('email')
        code = request.POST.get('code')
        if first_pass == second_pass:
            try:
                user = User.objects.get(email=email, forget_pass_code=code)
                hash_password = make_password(first_pass)
                user.password = hash_password
                user.forget_pass_code = None
                user.save()
                return redirect('login')
            except:
                return render(request, 'chat/change_password.html', {'email': email, 'code': code, 'error': 'Something went wrong'})
        else:
            return render(request, 'chat/change_password.html', {'email': email, 'code': code, 'error': 'Both Password is not matching'})


def update_seen_by(request):
    user_id = request.session.get('user_id')
    chat_id = request.POST.get('chat_id')
    user_obj = User.objects.get(id=user_id)
    chat_obj = Channel.objects.get(id=chat_id)
    try:
        previous_records = SeenByChannel.objects.filter(
            channel__id=chat_id, seen_by__id=user_id)
        for item in previous_records:
            item.delete()

        print('Records deletded')
    except:
        print('No records')

    last_message = ChannelMessage.objects.filter(channel=chat_id).last()
    seen_by_obj = SeenByChannel(
        channel=chat_obj, message=last_message, seen_by=user_obj)
    seen_by_obj.save()
    print(last_message)
    print('Ajax', chat_id, user_id)

    return JsonResponse({'success': True})


def logout(request):
    request.session.flush()
    return redirect('login')


def workspacelogout(request):
    del request.session['workspaceID']
    return redirect('workspace')
