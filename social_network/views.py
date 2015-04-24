# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import connection


def my_custom_sql():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person")
    row = cursor.fetchone()
    return row


@login_required
def home_view(request, username):
    """ Simple view to test querying the DB """
    row = my_custom_sql()
    html = str(row)
    data = {"user_info": html}
    return render(request, "home.html", dictionary=data)


@login_required
def redirect_user(request):

    return HttpResponseRedirect("../" + str(request.user.username))
