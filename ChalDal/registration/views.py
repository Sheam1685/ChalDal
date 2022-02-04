from audioop import reverse
from django.shortcuts import render, redirect, reverse
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect

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
    isLoggedIn=False
    if request.method == 'POST':
        #print("hello world")
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        sql = "select PASSWORD from CUSTOMER where EMAIL_ID=%s"
        cursor.execute(sql,[email])
        result = cursor.fetchone()
        cursor.close()

        if result==None:
            return render(request, 'registration/cus_login.html',context={'status':"Incorrect email or password"} )

        elif password==result[0]:
            #request.session['email'] = email
            isLoggedIn= True
            request.session['cus_email'] = email
            #return HttpResponseRedirect(reverse('cus_home'))
            #return render(request, 'registration/cus_home.html', context={'isLoggedIn':isLoggedIn} )
            return redirect('home')

        else:
            return render(request, 'registration/cus_login.html',context={'status':"Incorrect email or password"} )

    return render(request, 'registration/cus_login.html' )

def returnLogout(request):
    isLoggedIn=False
    if request.session.has_key('cus_email'):
        request.session.pop('cus_email')
        return redirect('home')

def returnCustomerHome(request):
    cus_email= request.session['cus_email']
    isLoggedIn = True

    cursor = connection.cursor()
    sql = "SELECT FIRST_NAME, LAST_NAME, ADDRESS, PHONE_NUMBER, TO_CHAR(DOB,'dd MONTH, yyyy'), EMAIL_ID FROM CUSTOMER WHERE EMAIL_ID= :email_id"
    cursor.execute(sql,{'email_id':cus_email})
    result = cursor.fetchall()
    cursor.close()

    firstname = result[0][0]
    lastname = result[0][1]
    address = result[0][2]
    phone_no = result[0][3]
    dob = result[0][4]
    email_id = result[0][5]

    basic_info = {
        'isLoggedIn':isLoggedIn,
        'firstname':firstname, 'lastname':lastname, 'address':address, 'phone_no':phone_no, 'dob':dob, 'email_id':email_id
    }
    
    return render(request, 'registration/cus_home.html', basic_info )