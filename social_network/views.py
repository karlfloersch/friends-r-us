from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from .forms import DocumentForm
from .models import Document
from . import queries


def make_data(request, username):
    homepage = False
    if username == request.user.username:
        homepage = True
    cust_id = request.user.first_name
    user_info = queries.get_user_info_by_id(cust_id)
    data = {"username": request.user.username,
            "first_name": user_info[1],
            "last_name": user_info[2],
            "homepage": homepage}
    print(username)
    print(request.user.username)
    print(homepage)
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
                return render(request, "home.html", dictionary=data)
    else:
        data['form'] = DocumentForm()  # A empty, unbound form
    return render(request, "home.html", dictionary=data)


@login_required
def messages_view(request):
    """ Simple view to test querying the DB """
    user_info = queries.get_user_info_by_id(request.user.first_name)
    my_circles = queries.get_user_circles_info(request.user.first_name)
    html = str(user_info)
    circles = my_circles
    print(circles)
    data = {"user_info": html, "username": request.user.username,
            "first_name": user_info[1],
            "last_name": user_info[2],
            "circles": circles}
    # Handle file upload
    if request.method == 'POST':
        data['form'] = DocumentForm(request.POST, request.FILES)
        if data['form'].is_valid():
            username = request.user.username
            newdoc = Document(username=username,
                              docfile=request.FILES['docfile'])
            print(newdoc)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('/accounts/' + username)
        else:
            return render(request, "home.html", dictionary=data)
    else:
        data['form'] = DocumentForm()  # A empty, unbound form
    return render(request, "home.html", dictionary=data)


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
