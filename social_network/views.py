# from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection


def my_custom_sql():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person")
    row = cursor.fetchone()
    return row


def home_view(request):
    """ Simple view to test querying the DB """
    row = my_custom_sql()
    html = str(row)
    data = {"user_info": html}
    return render(request, "home.html", dictionary=data)
