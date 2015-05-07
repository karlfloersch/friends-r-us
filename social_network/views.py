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
import pprint
import datetime
import json

pp = pprint.PrettyPrinter(indent=4)

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


def sort_posts(posts):
    posts = sorted(posts, key=lambda x: x[2], reverse=True)
    return posts


def build_page(username, user_info, user_id, circles, circle_name, circle_id):
    page_info = queries.get_page(user_id, circle_name)
    print("IM HERE")
    pp.pprint(page_info)
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
            num_likes, is_liked = queries.get_likes_by_comment((comment[5],),
                                                               user_id)
            comments.append(comment + comment_author_info
                            + (num_likes,) + (is_liked,))
        comments = sorted(comments, key=lambda x: x[2], reverse=True)
        num_likes, is_liked = queries.get_likes_by_post((post[0],), user_id)
        post = post + author_info + (comments,) + (num_likes,) + (is_liked,)
        posts.append(post)

    posts = sort_posts(posts)
    page_data = {"username": username,
                 "first_name": user_info[1],
                 "last_name": user_info[2],
                 "circles": circles,
                 "current_circle": {'name': circle_name, 'id': circle_id},
                 "posts": posts}
    return page_data


def upload_image(data, request, username, page_owner):
    if request.user.username == page_owner:
        data['form'] = DocumentForm(request.POST, request.FILES)
        if data['form'].is_valid():
            newdoc = Document(username=page_owner,
                              docfile=request.FILES['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect('/accounts/' + page_owner)
        else:
            return render(request, "profile.html", dictionary=data)


@login_required
def profile_view(request, page_owner, sub_page=None):
    """ Simple view to test querying the DB """
    # Redirect if the signed in user is an employee
    if request.user.last_name == 'employee':
        return HttpResponseRedirect('/employee')
    # Get the page owner's user object
    user = User.objects.filter(username=page_owner)
    if user.count() == 0:
        return HttpResponseRedirect('../../')
    # Get the page owner's information and circles
    user = user[0]
    user_id = user.first_name
    user_info = queries.get_user_info_by_id(user_id)
    # Get the page owner's circles
    circles = queries.get_user_circles_info(user_id)
    circle_name, circle_id = get_current_circle(circles, sub_page)
    # Redirect if the circle for this page does not exist
    if not circle_id:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    # Get the page's posts, comments and all related data
    page_data = build_page(page_owner, user_info, user_id,
                           circles, circle_name, circle_id)
    # Add the page data to our data object
    data = make_data(request, page_owner)
    data['page_data'] = page_data
    # Add the current navigation item indicator
    if page_owner == request.user.username:
        data['nbar'] = "nav_home"
    if request.method == 'POST':
        # Handle file upload
        return upload_image(data, request, request.user.username, page_owner)
    data['form'] = DocumentForm()  # A empty, unbound form
    return render(request, "profile.html", dictionary=data)


def get_current_circle(circles, sub_page):
    if sub_page:
        circle_name = sub_page.replace('_', ' ')
    else:
        circle_name = 'Friends'
    circle_id = None
    for circle in circles:
        print(circle)
        if circle[2] == circle_name:
            circle_id = circle[0]
    return circle_name, circle_id


@login_required
def messages_view(request):
    """ Display users messages page """
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
    return render(request, "messages.html", dictionary=data)


@login_required
def employee_view(request):
    """ Employee dashboard view """
    return render(request, "employee.html")


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

@login_required
def update_customer_ajax(request):
    val = request.POST.getlist('ar[]')
    # val = vals[0]
    print(val)
    queries.update_customer(cust_id = val[0], rating= val[1], firstname_= val[2], lastname_= val[3], password_= val[4], gender_= val[5], address_= val[6], city_= val[7], state_= val[8], zipcode_= val[9], telephone_= val[10], email_= val[11], dob_= val[12])
    # print("bob")
    return HttpResponse(json.dumps({}), content_type="application/json")
@login_required
def submit_like_ajax(request):
    post_id = request.POST.get("post_id")
    data = {'success': False}
    post_type = request.POST.get("text_type")
    like_type = request.POST.get("like_type")
    if like_type == 'like':
        if post_type == 'post':
            num_likes, is_liked =\
                queries.get_likes_by_post((post_id,),
                                          request.user.first_name)
        elif post_type == 'comment':
            num_likes, is_liked =\
                queries.get_likes_by_comment((post_id,),
                                             request.user.first_name)
        if is_liked:
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        data['success'] = True
        if post_type == 'post':
            queries.like_post(post_id, request.user.first_name)
        elif post_type == 'comment':
            queries.like_comment(post_id, request.user.first_name)
        return HttpResponse(json.dumps(data), content_type="application/json")

    elif like_type == 'unlike':
        if post_type == 'post':
            num_likes, is_liked =\
                queries.get_likes_by_post((post_id,),
                                          request.user.first_name)
        elif post_type == 'comment':
            num_likes, is_liked =\
                queries.get_likes_by_comment((post_id,),
                                             request.user.first_name)
        if not is_liked:
            return HttpResponse(json.dumps(data),
                                content_type="application/json")
        data['success'] = True
        if post_type == 'post':
            queries.unlike_a_post(post_id, request.user.first_name)
        elif post_type == 'comment':
            queries.unlike_a_comment(post_id, request.user.first_name)
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def delete_advertisement_ajax(request):
    id_ = request.POST.get("id")
    # print(id_)
    queries.delete_advertisement(id_)

    return HttpResponse(json.dumps({}) ,content_type="application/json")


@login_required
def list_all_customers_ajax(request):
    val = queries.customer_list()
    return HttpResponse(json.dumps({'items':val}) ,content_type="application/json")

@login_required
def del_customer_ajax(request):
    id_ = request.POST.get("id")
    val = queries.remove_customer(id_)
    return HttpResponse(json.dumps({}) ,content_type="application/json")

def generate_mailing_list_ajax(request):
    val = queries.customer_mailing_list()

    print(val)
    return HttpResponse(json.dumps({'items':val}) ,content_type="application/json")
@login_required
def produce_list_of_all_items_advertised_ajax(request):
    print("here")
    val = queries.produce_list_of_all_items_advertised()
    print(val)
    return HttpResponse(json.dumps({'items':val}) ,content_type="application/json")

@login_required
def create_advertisement_ajax(request):
       # 'item_name': $('#item_name').val(),
       #  'num_aval_units': $('#num_aval_units').val(),
       #  'unit_price': $('#unit_price').val(),
       #  'content': $('#content').val(),
       #  'type': $('#type').val(),
       #  'company': $('#company').val(),
    # print("things went well")
    item_name = request.POST.get("item_name")
    num_units = request.POST.get("num_aval_units")
    unit_price = request.POST.get("unit_price")
    content = request.POST.get("content")
    type_ad = request.POST.get("type")
    company = request.POST.get("company")
    employee_id = request.user.first_name

    # print("bob")
    print(datetime.datetime.now())
    product_id =33331
    val= queries.list_users_by_product(product_id)
    print (val)
    print("bob")
    # queries.create_advertisement(item_name, num_units, unit_price, content, employee_id, type_ad,company)

    return HttpResponse(json.dumps({}) , content_type="application/json")


def submit_post_ajax(request):
    # userID = request.user.first_name
    page_id = queries.get_page_by_circle_id(request.POST.get('circle_id'))[0]
    data = {'post_text': request.POST.get('post_text'),
            'page_name': request.POST.get('page_name'),
            'page_id': page_id}
    queries.make_a_post(data['post_text'], request.user.first_name,
                        data['page_id'])
    return HttpResponse(json.dumps(data), content_type="application/json")


def submit_comment_ajax(request):

    data = {'comment_text': request.POST.get('comment_text'),
            'post_id': request.POST.get('post_id')}
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


def create_employee_account_view(request):

    if request.method == 'GET':
        return render(request, "employeeregistration.html")
    elif request.method == 'POST':
        # print('poodle')

        print("checkValid")
        is_valid, data = validate_new_employee(request)

        if is_valid:
                # Data is valid and let's store it in the db
            print("employee creation")

            date = data['smonth'] + "-" + data['sday'] + "-" + data['syear']
            cust_id = queries.add_employee(firstname=data['first_name'], lastname=data['last_name'], password=data['pw'], gender=data['gender'], address=data['address'], city=data[
                                           'city'], state=data['state'], zipcode=data['zipcode'], telephone=data['telephone'], ssn=data['ssn'], start_date=date, hourly_rate=data['rate'], role=data['role'])
            user = User.objects.create_user(username=data['username'],
                                            password=data['pw'],
                                            first_name=cust_id, last_name = "employee")
            print(cust_id)
            user.first_name = cust_id
            user.is_active = True
            user.save()
            print("employee created")
            # month day year

            return HttpResponseRedirect("/login")
        else:
            print("invalid")
            return render(request, 'employeeregistration.html', dictionary=data)


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
            cust_id = queries.add_customer(firstname_=data['first_name'], lastname_=data['last_name'], password_=data['pw'], gender_=data['gender'], address_=data[
                                           'address'], city_=data['city'], state_=data['state'], zipcode_=data['zipcode'], telephone_=data[
                                           'telephone'], email_=data['email'], dob_=dob, credit_card_num = data['credit'])
            user = User.objects.create_user(username=data['username'],
                                            password=data['pw'],
                                            first_name=cust_id, last_name = "customer")
            print(cust_id)
            user.first_name = cust_id
            user.is_active = True
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
    data['credit'] = request.POST.get('credit', False)
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
    # elif datetime.datetime(year=1900, month=1, day=1) <
    # datetime.datetime(year=int(data['year']), month=int(data['month']),
    # day=int(data['day'])) <= datetime.datetime.now():
    elif validate_date(str(data['month'] + "/" + data['day'] + "/" + data['year'])) == False:
        # print('money')
        valid_data = False
        data['err_date'] = "Please enter a date"
    if len(data['city'].strip()) == 0:
        valid_data = False
        data['err_city'] = "Please enter a city"
    if len(data['state'].strip()) == 0:
        valid_data = False
        data['err_state'] = "Please enter a state"
    if len(data['zipcode'].strip()) == 0 or isInt(data['zipcode'])==False:
        valid_data = False
        data['err_zipcode'] = "Please enter a zip"
    if len(data['telephone'].strip()) == 0 or isInt(data['telephone'])==False:
        valid_data = False
        data['err_telephone'] = "Please enter a telephone"
    if len(data['credit'].strip()) ==0 or isInt(data['credit'])==False:
        print('credit')
        valid_data = False
        data['err_credit'] = "Please enter a credit"

    # Return if the valid
    return valid_data, data


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def validate_new_employee(request):
    """ return (True if data is valid, Dictionary of input and errors)
    validate the user data that was entered in request
    """
    data = {}
    data['name'] = request.POST.get('name', False).strip().split()
    data['pw'] = request.POST.get('password', False)
    data['gender'] = request.POST.get('gender', False)
    data['username'] = request.POST.get('username', False)
    data['password'] = request.POST.get('password', False)
    data['address'] = request.POST.get('address', False)
    data['city'] = request.POST.get('city', False)
    data['state'] = request.POST.get('state', False)
    data['zipcode'] = request.POST.get('zipcode', False)
    data['telephone'] = request.POST.get('telephone', False)

    data['smonth'] = request.POST.get('smonth', False)
    data['sday'] = request.POST.get('sday', False)
    data['syear'] = request.POST.get('syear', False)

    data['ssn'] = request.POST.get('ssn', False)
    data['rate'] = request.POST.get('rate', False)
    data['role'] = request.POST.get('role', False)
#     ssn: <input type ="text" name="ssn"><br>
# Hourly rate: <input type ="text" name="rate"><br>
# Role: <input type ="text" name="role"><br>

    # username gender
    valid_data = True
    error_location = 0
    # If any data is invalid, set valid_data to False and print error
    if len(data['name']) < 2 or len(data['name']) > 2:
        valid_data = False
        error_location = 1
        data['err_studName'] = "Please enter a valid name"
    else:
        data['first_name'] = data['name'][0]
        data['last_name'] = data['name'][1]
    if User.objects.filter(username=data['username']).count():
        valid_data = False
        error_location = 2
        data['err_email'] = "A user with that email already exists"
    if len(data['address'].strip()) == 0:
        valid_data = False
        error_location = 3
        data['err_address'] = "Please enter an address"
    if len(data['pw'].strip()) == 0:
        valid_data = False
        error_location = 4
        data['err_pw'] = "Please enter a password"
    if len(data['syear'].strip()) == 0 or len(data['sday'].strip()) == 0 or len(data['smonth'].strip()) == 0:
        valid_data = False
        error_location = 5
        data['err_date'] = "Please enter a date"
    # elif datetime.datetime(year=1900, month=1, day=1) <
    # datetime.datetime(year=int(data['year']), month=int(data['month']),
    # day=int(data['day'])) <= datetime.datetime.now():
    elif validate_date(str(data['smonth'] + "/" + data['sday'] + "/" + data['syear'])) == False:
        # print('money')
        valid_data = False
        error_location = 6
        print(str(data['smonth'] + "/" + data['sday'] + "/" + data['syear']))
        data['err_date'] = "Please enter a date"
    if len(data['city'].strip()) == 0:
        valid_data = False
        error_location = 7
        data['err_city'] = "Please enter a city"
    if len(data['state'].strip()) == 0:
        valid_data = False
        error_location = 8
        data['err_state'] = "Please enter a state"
    if len(data['zipcode'].strip()) == 0:
        valid_data = False
        error_location = 9
        data['err_zipcode'] = "Please enter a zip"
    if len(data['telephone'].strip()) == 0:
        valid_data = False
        error_location = 10
        data['err_telephone'] = "Please enter a telephone"
    if len(data['ssn'].strip()) == 0:
        valid_data = False
        error_location = 11
        data['err_ssn'] = "Please enter a ssn"
    if len(data['rate'].strip()) == 0:
        valid_data = False
        error_location = 12
        data['err_rate'] = "Please enter a rate"

    print(error_location)
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
        datetime.datetime.strptime(d, '%m/%d/%Y')
        return True
    except ValueError:
        return False
