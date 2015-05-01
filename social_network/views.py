from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from .forms import DocumentForm
from .models import Document
from . import queries
import json


def make_data(request, username):
    homepage = False
    if username == request.user.username:
        homepage = True
    cust_id = request.user.first_name
    user_info = queries.get_user_info_by_id(cust_id)
    data = {"username": request.user.username,
            "user_id": request.user.first_name,
            "first_name": user_info[1],
            "last_name": user_info[2],
            "homepage": homepage}
    return data


@login_required
def profile_view(request, username):
    """ Simple view to test querying the DB """
    user = User.objects.filter(username=username)
    if user.count() == 0:
        return HttpResponseRedirect('../../')
    # User exhists so display page
    # Get the page owner's user id, information and circles
    user = user[0]
    user_id = user.first_name
    user_info = queries.get_user_info_by_id(user_id)
    circles = queries.get_user_circles_info(user_id)
    page_data = {"username": user.username,
                 "first_name": user_info[1],
                 "last_name": user_info[2],
                 "circles": circles}
    data = make_data(request, username)
    data['page_data'] = page_data
    if username == request.user.username:
        data['nbar'] = "nav_home"

    # Handle file upload
    if request.method == 'POST':
        if request.user.username == username:
            data['form'] = DocumentForm(request.POST, request.FILES)
            if data['form'].is_valid():
                username = request.user.username
                newdoc = Document(username=username,
                                  docfile=request.FILES['docfile'])
                newdoc.save()
                # Redirect to the document list after POST
                return HttpResponseRedirect('/accounts/' + username)
            else:
                return render(request, "profile.html", dictionary=data)
    else:
        data['form'] = DocumentForm()  # A empty, unbound form
    return render(request, "profile.html", dictionary=data)


@login_required
def messages_view(request):
    """ Simple view to test querying the DB """
    messages = queries.get_user_messages(request.user.first_name)
    conversations = {}

    def build_conversations(message):
        """ Add the message to the conversations """
        # Extract data from the message
        message_id, content, sender_id = message[0], message[1], message[2]
        reciever_id, subject, date = message[3], message[4], message[5]
        # Get sender and reciever user info
        sender_info = queries.get_user_info_by_id(str(sender_id))
        sender_name = sender_info[1] + " " + sender_info[2]
        reciever_info = queries.get_user_info_by_id(str(reciever_id))
        reciever_name = reciever_info[1] + " " + reciever_info[2]
        # Get the conversation to add this to
        if str(sender_id) != str(request.user.first_name):
            convo_name = sender_name
            convo_username = User.objects.filter(first_name=sender_id)[0]
            convo_id = sender_id
        else:
            convo_name = reciever_name
            convo_username = User.objects.filter(first_name=reciever_id)[0]
            convo_id = reciever_id
        # Add the message to that conversation
        if convo_name not in conversations.keys():
            conversations[convo_username] = []
        conversations[convo_username].append({'message_id': message_id,
                                              'subject': subject,
                                              'date': date,
                                              'content': content,
                                              'sender': sender_id,
                                              'reciever': reciever_id,
                                              'sender_name': sender_name,
                                              'reciever_name': reciever_name,
                                              'convo_name': convo_name,
                                              'convo_id': convo_id})
    # Loop over the messages and build the conversations
    for message in messages:
        build_conversations(message)
    data = make_data(request, request.user.first_name)
    data['nbar'] = 'nav_messages'
    data['conversations'] = conversations
    print(conversations)
    return render(request, "messages.html", dictionary=data)


@login_required
def get_messages_ajax(request):
    convo_user = User.objects.filter(username=request.POST["convo_user"])[0]
    messages = queries.get_conversation_messages([request.user.first_name,
                                                  convo_user.first_name])
    data = {'messages': messages}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def redirect_user(request):
    return HttpResponseRedirect("../" + str(request.user.username))


@login_required
def redirect_to_home(request):
    return HttpResponseRedirect("accounts/profile/")


def list_view(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.user.username
            newdoc = Document(username=username,
                              docfile=request.FILES['docfile'])
            print(newdoc)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('/accounts/' + username)
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def logout_view(request):
    """ log current user out """
    # Log the user out using Django Auth
    logout(request)
    return HttpResponseRedirect("/login")
