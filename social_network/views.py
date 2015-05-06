from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotFound
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from .forms import DocumentForm
from .models import Document
from . import queries
import datetime
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
def profile_view(request, username, sub_page=None):
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
    circle_name, circle_id = get_current_circle(circles, sub_page)
    # Get the page's posts and comments
    if not circle_id:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    page_info = queries.get_page(user_id, circle_name)
    page_id = page_info[4]
    posts_info = queries.get_posts(page_id)
    posts = []
    for post in posts_info:
        author_info = queries.get_username_and_name_by_id(post[5])
        comment_info = queries.get_comments(post[0])
        comments = []
        for comment in comment_info:
            comment_author_info = queries.get_username_and_name_by_id(
                comment[4])
            comments.append(comment + comment_author_info)
        post = post + author_info + (comments,)
        posts.append(post)
    page_data = {"username": user.username,
                 "first_name": user_info[1],
                 "last_name": user_info[2],
                 "circles": circles,
                 "current_circle": {'name': circle_name, 'id': circle_id},
                 "posts": posts}
    data = make_data(request, username)
    data['page_data'] = page_data
    print(data['page_data']['posts'][0])
    if username == request.user.username:
        data['nbar'] = "nav_home"
    if not request.method == 'POST':
        return render(request, "profile.html", dictionary=data)
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


def get_current_circle(circles, sub_page):
    if sub_page:
        circle_name = sub_page.replace('_', ' ')
    else:
        circle_name = 'Friends'
    circle_id = None
    for circle in circles:
        if circle[2] == circle_name:
            circle_id = circle[0]
    return circle_name, circle_id


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
def get_friends_ajax(request):
    name = request.POST["name"]
    friends = queries.get_users_by_firstname(name)
    friends = [f + (User.objects.filter(first_name=f[0])[0].username,)
               for f in friends]
    data = {'friends': friends}
    return HttpResponse(json.dumps(data), content_type="application/json")


def submit_post_ajax(request):
    # userID = request.user.first_name
    page_id = queries.get_page_by_circle_id(request.POST.get('circle_id'))[0]
    data = {'post_text': request.POST.get('post_text'),
            'page_name': request.POST.get('page_name'),
            'page_id': page_id}
    print(data)
    queries.make_a_post(data['post_text'], request.user.first_name,
                        data['page_id'])
    return HttpResponse(json.dumps(data), content_type="application/json")


def submit_comment_ajax(request):

    data = {'comment_text': request.POST.get('comment_text'),
            'post_id': request.POST.get('post_id')}
    print(data)
    queries.make_a_comment(data['comment_text'], data['post_id'],
                           request.user.first_name)
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


def create_account_view(request):

    if request.method == 'GET':
        return render(request, "registration.html")
    elif request.method == 'POST':
        # print('poodle')

        print("checkValid")
        is_valid, data = validate_new_user(request)

        if is_valid:
                # Data is valid and let's store it in the db
            print("valid")

            dob = data['month'] + "-" + data['day'] + "-" + data['year']
            queries.add_customer(firstname_=data['first_name'], lastname_=data['last_name'], password_=data['pw'], gender_=data['gender'], address_=data[
                                 'address'], city_=data['city'], state_=data['state'], zipcode_=data['zipcode'], telephone_=data['telephone'], email_=data['email'], dob_=dob)
            user = User.objects.create_user(username=data['username'],
                                            password=data['pw'])
            user.is_active = False
            user.save()
            # month day year

            return HttpResponseRedirect("/login")
        else:
            print("invalid")
            return render(request, 'registration.html', dictionary=data)


def validate_new_user(request):
    """ return (True if data is valid, Dictionary of input and errors)
    validate the user data that was entered in request
    """
    #     email       VARCHAR(50),
    # rating      INT,
    # date_of_birth DATETIME NOT NULL,
    # id        INT,
    # firstname VARCHAR(50),
    # lastname  VARCHAR(50),
    # password  CHAR(15),
    # gender    VARCHAR(1),
    # address   VARCHAR(95),
    # city      VARCHAR(50),
    # state     VARCHAR(50),
    # zipcode   INT,
    # telephone VARCHAR(15),
    # Fill data with the information that the user entered
    data = {}
    data['name'] = request.POST.get('name', False).strip().split()
    data['email'] = request.POST.get('email', False)
    data['pw'] = request.POST.get('password', False)
    data['month'] = request.POST.get('month', False)
    data['day'] = request.POST.get('day', False)
    data['year'] = request.POST.get('year', False)
    data['gender'] = request.POST.get('gender', False)
    data['username'] = request.POST.get('username', False)
    data['password'] = request.POST.get('password', False)
    data['address'] = request.POST.get('address', False)
    data['city'] = request.POST.get('city', False)
    data['state'] = request.POST.get('state', False)
    data['zipcode'] = request.POST.get('zipcode', False)
    data['telephone'] = request.POST.get('telephone', False)
    # username gender
    valid_data = True
    # If any data is invalid, set valid_data to False and print error
    if len(data['name']) < 2 or len(data['name']) > 2:
        valid_data = False
        data['err_studName'] = "Please enter a valid name"
    else:
        data['first_name'] = data['name'][0]
        data['last_name'] = data['name'][1]
    if validate_email(data['email']):
        valid_data = False
        data['err_email'] = "Invalid email"
    if User.objects.filter(username=data['username']).count():
        valid_data = False
        data['err_email'] = "A user with that email already exists"
    if len(data['address'].strip()) == 0:
        valid_data = False
        data['err_address'] = "Please enter an address"
    if len(data['pw'].strip()) == 0:
        valid_data = False
        data['err_pw'] = "Please enter a password"
    if len(data['year'].strip()) == 0 or len(data['day'].strip()) == 0 or len(data['month'].strip()) == 0:
        valid_data = False
        data['err_date'] = "Please enter a date"
    # elif datetime.datetime(year=1900, month=1, day=1) < datetime.datetime(year=int(data['year']), month=int(data['month']), day=int(data['day'])) <= datetime.datetime.now():
    elif validate_date(str(data['month']+"/"+data['day']+"/"+data['year']))==False:
        # print('money')
        valid_data = False
        data['err_date'] = "Please enter a date"
    if len(data['city'].strip()) == 0:
        valid_data = False
        data['err_city'] = "Please enter a city"
    if len(data['state'].strip()) == 0:
        valid_data = False
        data['err_state'] = "Please enter a state"
    if len(data['zipcode'].strip()) == 0:
        valid_data = False
        data['err_zipcode'] = "Please enter a zip"
    if len(data['telephone'].strip()) == 0:
        valid_data = False
        data['err_telephone'] = "Please enter a telephone"

    # Return if the valid
    return valid_data, data


def validate_email(email):
    """ validate an email string """
    import re
    a = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if a.match(email):
        return False
    return True


def logout_view(request):
    """ log current user out """
    # Log the user out using Django Auth
    logout(request)
    return HttpResponseRedirect("/login")


def validate_date(d):
    try:
        datetime.strptime(d, '%m/%d/%Y')
        return True
    except ValueError:
        return False
