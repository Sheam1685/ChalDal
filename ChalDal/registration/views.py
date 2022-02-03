from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

# Create your views here.
def returnSignUp(request):

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        phn = request.POST.get('phn')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        cursor = connection.cursor()
        sql = 'SELECT MAX(CUSTOMER_ID) FROM CUSTOMER'
        cursor.execute(sql)
        
        last_id = cursor.fetchone()
        last_id = last_id[0]
        if last_id is not  None:
            user_id = last_id + 1
        else:
            user_id = 1

        cursor = connection.cursor()
        sql = "INSERT INTO CUSTOMER VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        
        cursor.execute(sql,[user_id, fname, lname, address, phn, dob, email,password])
        connection.commit()
        cursor.close()

        return render(request, 'homeApp/home_page.html')

        #print(user_id, fname, lname,  address, phn, dob, email,password)


    return render(request, 'registration/signup.html')

def returnSellerSignUp(request):

    if request.method == 'POST':
        
        name = request.POST.get('name')
        phn = request.POST.get('phn')
        email = request.POST.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')
        password = request.POST.get('pass')

        cursor = connection.cursor()
        sql = 'SELECT MAX(SELLER_ID) FROM SELLER'
        cursor.execute(sql)
        
        last_id = cursor.fetchone()
        last_id = last_id[0]
        if last_id is not  None:
            user_id = last_id + 1
        else:
            user_id = 1

        cursor = connection.cursor()
        sql = "INSERT INTO SELLER VALUES(%s,%s,%s,%s,%s,%s,%s)"
        
        cursor.execute(sql,[user_id, name, address, phn, email,website, password])
        connection.commit()
        cursor.close()

        return render(request, 'homeApp/home_page.html')


    return render(request, 'registration/seller_signup.html')

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


def returnLogin(request):
    if request.method == 'POST':
        print("hello world")
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        sql = "select PASSWORD from CUSTOMER where EMAIL_ID=%s"
        cursor.execute(sql,[email])
        result = cursor.fetchone()
        cursor.close()

        print(email, password, result)

        if password==result[0]:
            return HttpResponse("Hello user")
            #request.session['cus_email'] = email
            #return redirect('home')

        else:
            return render(request, 'registration/cus_login.html',context={'status':"Incorrect email or password"} )

    return render(request, 'registration/cus_login.html' )