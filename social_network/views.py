# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db import connection
from .forms import DocumentForm
from .models import Document


def get_user_info_by_id(cust_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person WHERE id=" + cust_id)
    row = cursor.fetchone()
    return row


@login_required
def home_view(request, username):
    """ Simple view to test querying the DB """
    row = get_user_info_by_id(request.user.first_name)
    html = str(row)
    data = {"user_info": html, "username": request.user.username,
            "first_name": row[1],
            "last_name": row[2]}
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
