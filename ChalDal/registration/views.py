from sqlite3 import Cursor
from unittest import result
from django.shortcuts import render
from django.db import connection
import datetime

# Create your views here.
def returnSignUp(request):
    return render(request, 'registration/signup.html')

def returnCustomerList(request):

    """cursor = connection.cursor()
    sql = "INSERT INTO CUSTOMER VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    dob = datetime.datetime(1990,5,5)
    cursor.execute(sql,[3, 'MTZ', 'Pranto', 'BUET', '00001111', dob, 'mtz@gmail.com','mtzp'])
    connection.commit()
    cursor.close()"""

    cursor = connection.cursor()
    sql = "select FIRST_NAME, LAST_NAME, PHONE_NUMBER from CUSTOMER"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    custlist = []

    for r in result:
        fname = r[0]
        lname = r[1]
        phn = r[2]

        row = {'fname':fname, 'lname':lname, 'phn':phn}
        custlist.append(row)
    return render(request, 'registration/customerlist_test.html', {'custlist':custlist})