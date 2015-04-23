from django.http import HttpResponse
# from django.shortcuts import render
from django.db import connection


def my_custom_sql():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person")
    row = cursor.fetchone()
    return row


def test_view(request):
    """ Simple view to test querying the DB """
    row = my_custom_sql()
    html = "<html><body> string: " + str(row) + "</body></html>"
    return HttpResponse(html)
