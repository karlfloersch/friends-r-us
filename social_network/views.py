# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import connection


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
            "first_name": row[1]}
    return render(request, "home.html", dictionary=data)


@login_required
def redirect_user(request):

    return HttpResponseRedirect("../" + str(request.user.username))
