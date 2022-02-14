from operator import truediv
from django.shortcuts import render
from django.db import connection

# Create your views here.

def returnHomepage(request):
    isLoggedIn=False
    acType=""
    if request.session.has_key('cus_email'):
        isLoggedIn=True
        acType="customer"
    if request.session.has_key('seller_email'):
        isLoggedIn=True
        acType="seller"

    cursor = connection.cursor()
    sql = "SELECT CATEGORY_ID, CATEGORY_NAME FROM CATEGORY"
    
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    catList = []

    for r in result:
        cat_id = r[0]
        cat_name = r[1]

        row = {'cat_id':cat_id, 'cat_name':cat_name}
        catList.append(row)

    context={'isLoggedIn':isLoggedIn, 'acType':acType, 'catList':catList}

    return render(request, 'homeApp/home_page.html', context)
