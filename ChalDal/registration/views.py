from audioop import reverse
from django.shortcuts import render, redirect, reverse
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.

def findAcType(email):
    cursor = connection.cursor()
    sql = 'SELECT COUNT(CUSTOMER_ID) FROM CUSTOMER WHERE EMAIL_ID=:email_id'
    cursor.execute(sql,{'email_id':email})
    result_cus = cursor.fetchall()

    sql = 'SELECT COUNT(SELLER_ID) FROM SELLER WHERE EMAIL_ID=:email_id'
    cursor.execute(sql,{'email_id':email})
    result_seller = cursor.fetchall()
    cursor.close()

    if result_cus>0:
        return "customer"
    elif result_seller>0:
        return "seller"

def categoryList():
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

    return catList


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
            return redirect('homeApp:home')

        else:
            return render(request, 'registration/cus_login.html',context={'status':"Incorrect email or password"} )

    return render(request, 'registration/cus_login.html' )

def returnSellerLogin(request):
    isLoggedIn=False
    if request.method == 'POST':
        #print("hello world")
        email = request.POST.get('email')
        password = request.POST.get('password')
        cursor = connection.cursor()
        sql = "select PASSWORD from SELLER where EMAIL_ID=%s"
        cursor.execute(sql,[email])
        result = cursor.fetchone()
        cursor.close()

        if result==None:
            return render(request, 'registration/seller_login.html',context={'status':"Incorrect email or password"} )

        elif password==result[0]:
            #request.session['email'] = email
            isLoggedIn= True
            request.session['seller_email'] = email
            #return HttpResponseRedirect(reverse('cus_home'))
            #return render(request, 'registration/cus_home.html', context={'isLoggedIn':isLoggedIn} )
            return redirect('registration:seller_home')

        else:
            return render(request, 'registration/seller_login.html',context={'status':"Incorrect email or password"} )

    return render(request, 'registration/seller_login.html' )

def returnLogout(request):
    isLoggedIn=False
    if request.session.has_key('cus_email'):
        request.session.pop('cus_email')
        return redirect('home')
    if request.session.has_key('seller_email'):
        request.session.pop('seller_email')
        return redirect('home')
    if request.session.has_key('del_guy_email'):
        request.session.pop('del_guy_email')
        return redirect('home')
    if request.session.has_key('admin_email'):
        request.session.pop('admin_email')
        return redirect('home')
    if request.session.has_key('cus_care_email'):
        request.session.pop('cus_care_email')
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

    catList = categoryList()

    basic_info = {
        'isLoggedIn':isLoggedIn, 'catList':catList,
        'firstname':firstname, 'lastname':lastname, 'address':address, 'phone_no':phone_no, 'dob':dob, 'email_id':email_id
    }
    
    return render(request, 'registration/cus_home.html', basic_info )

def returnSellerHome(request):
    seller_email= request.session['seller_email']
    isLoggedIn = True
    catList = categoryList()

    cursor = connection.cursor()
    sql = "SELECT NAME, ADDRESS, PHONE_NUMBER,  EMAIL_ID, WEBSITE, BALANCE FROM SELLER WHERE EMAIL_ID= :email_id"
    cursor.execute(sql,{'email_id':seller_email})
    result = cursor.fetchall()
    cursor.close()

    name = result[0][0]
    address = result[0][1]
    phone_no = result[0][2]
    email_id = result[0][3]
    website = result[0][4]
    balance = result[0][5]

    basic_info = {
        'isLoggedIn':isLoggedIn, 'catList':catList,
        'name':name, 'address':address, 'phone_no':phone_no, 'email_id':email_id, 'website':website, 'balance':balance
    }
    
    return render(request, 'registration/seller_home.html', basic_info )

def returnSellerProducts(request):
    seller_email= request.session['seller_email']
    isLoggedIn = True
    catList = categoryList()

    cursor = connection.cursor()
    sql = """SELECT P.NAME, C.CATEGORY_NAME, 
        (SELECT COUNT(*) FROM PRODUCT_UNIT U WHERE U.STATUS='not sold' AND U.PRODUCT_ID=P.PRODUCT_ID AND U.SELLER_ID=P.SELLER_ID) AS IN_STOCK 
        FROM PRODUCT P JOIN CATEGORY C ON(P.CATEGORY_ID=C.CATEGORY_ID) 
        WHERE P.SELLER_ID=(SELECT S.SELLER_ID FROM SELLER S WHERE S.EMAIL_ID=:email_id)"""
    cursor.execute(sql,{'email_id':seller_email})
    result = cursor.fetchall()
    cursor.close()
    print(result)
    products_view = []
    for row in result:
        x={
            'prod_name':row[0],
            'cat_name':row[1],
            'in_stock':row[2]
        }
        products_view.append(x)
    view_product = {
        'isLoggedIn':isLoggedIn, 'catList':catList,
        'products_view':products_view
    }
    return render(request, 'registration/seller_products.html', view_product)

def returnCusorder(request):
    cus_email= request.session['cus_email']
    isLoggedIn = True
    catList = categoryList()

    cursor = connection.cursor()
    sql = """SELECT CUSTOMER_ORDER.ORDER_DATE AS DATE_OF_ORDER, PURCHASE_ORDER.DELIVERED_DATE AS DELIVERED_DATE,
    PURCHASE_ORDER.DELIVERY_STATUS AS DELIVERY_STATUS, 
    (SELECT (FIRST_NAME ||' '|| LAST_NAME) FROM EMPLOYEE WHERE EMPLOYEE_ID = PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID) AS DELIVERY_EMPLOYEE_NAME,
    (SELECT PHONE_NUMBER FROM EMPLOYEE WHERE EMPLOYEE_ID = PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID) AS PHONE_NUMBER, 
    RETURN_ORDER.APPROVAL_STATUS, CUSTOMER_ORDER.ORDER_ID
    FROM CUSTOMER_ORDER LEFT OUTER JOIN PURCHASE_ORDER
    ON(CUSTOMER_ORDER.ORDER_ID = PURCHASE_ORDER.ORDER_ID)
    LEFT OUTER JOIN RETURN_ORDER
    ON(CUSTOMER_ORDER.ORDER_ID = RETURN_ORDER.ORDER_ID)
    WHERE CUSTOMER_ID = (SELECT CUSTOMER_ID FROM CUSTOMER WHERE EMAIL_ID =:email_id)
    ORDER BY CUSTOMER_ORDER.ORDER_DATE DESC;"""
    cursor.execute(sql,{'email_id':cus_email})
    result = cursor.fetchall()
    
    orders_view = []
    buttoninfo = ""
    for row in result:
        id = row[6]
        sql = """SELECT PRODUCT.PRODUCT_ID, PRODUCT.NAME, COUNT(ORDERED_ITEMS.ITEM_NUMBER) ITEM_COUNT
        FROM ORDERED_ITEMS LEFT OUTER JOIN PRODUCT
        ON(ORDERED_ITEMS.PRODUCT_ID = PRODUCT.PRODUCT_ID)
        WHERE ORDER_ID =:id
        GROUP BY PRODUCT.PRODUCT_ID, PRODUCT.NAME;"""
        cursor.execute(sql,{'id':id})
        result1 = cursor.fetchall()
        items = ""
        for row1 in result1:
            items = items + "," + row1[1] + "(" + str(row1[2]) + " pcs)"
        items = items[1:]
        
        
        if row[2] is None:
            buttoninfo = "nothing"
            
        
        elif row[5] is not None:
            if row[5]=="Accepted":
                buttoninfo = "accepted"
            else:
                buttoninfo = "waiting"
            
        else:
            buttoninfo = "Return Order"
            
        x={
            'date_of_order':row[0],
            'delivered_date':row[1],
            'delivery_status':row[2],
            'delivery_guy':row[3],
            'phone':row[4],
            'return_status':row[5],
            'items':items,
            'buttoninfo':buttoninfo,
            'ord_id':id
        }
        orders_view.append(x)
    cursor.close()
    if request.method=="POST":
        complain_ord_id = request.POST.get('order_id')
        complaint_des = request.POST.get('complain')
        
        cursor = connection.cursor()
        sql = "INSERT INTO RETURN_ORDER VALUES(%s,%s,3, SYSDATE, 'Waiting for approval')"
        
        cursor.execute(sql,[complain_ord_id, complaint_des])
        connection.commit()
        cursor.close()

        return redirect('registration:cus_order')
    order_info = {
        'isLoggedIn':isLoggedIn, 'catList':catList,
        'orders_view':orders_view,
        
    }
    return render(request, 'registration/cus_order.html', order_info)


def returnCusReview(request):
    cus_email= request.session['cus_email']
    isLoggedIn = True
    catList = categoryList()

    cursor = connection.cursor()
    sql = """SELECT REVIEW.REVIEW_DATE, PRODUCT.NAME, SELLER.NAME, REVIEW.DESCRIPTION, REVIEW.RATING
    FROM REVIEW LEFT OUTER JOIN PRODUCT
    ON REVIEW.PRODUCT_ID = PRODUCT.PRODUCT_ID
    LEFT OUTER JOIN SELLER
    ON REVIEW.SELLER_ID = SELLER.SELLER_ID
    LEFT OUTER JOIN CUSTOMER
    ON REVIEW.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID
    WHERE CUSTOMER.EMAIL_ID =:email_id;"""
    cursor.execute(sql,{'email_id':cus_email})
    result = cursor.fetchall()
    cursor.close()
    print(result)
    reviews_view = []
    for row in result:
        x={
            'date_of_review':row[0],
            'product_name':row[1],
            'seller_name':row[2],
            'description':row[3],
            'rating': row[4]
        }
        reviews_view.append(x)
    reviews_info = {
        'isLoggedIn':isLoggedIn, 'catList':catList,
        'reviews_view':reviews_view
    }
    return render(request, 'registration/cus_review.html', reviews_info)


def returnSellerOffers(request):
    seller_email= request.session['seller_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT PRODUCT.NAME, TO_CHAR(OFFER.START_DATE, 'MONTH DD, YYYY'), TO_CHAR(OFFER.END_DATE, 'MONTH DD, YYYY'), OFFER.PERCENTAGE_DISCOUNT
    FROM OFFER LEFT OUTER JOIN SELLER
    ON(OFFER.SELLER_ID = SELLER.SELLER_ID)
    LEFT OUTER JOIN PRODUCT
    ON(OFFER.PRODUCT_ID = PRODUCT.PRODUCT_ID)
    WHERE SELLER.EMAIL_ID =:email_id;"""
    cursor.execute(sql,{'email_id':seller_email})
    result = cursor.fetchall()
    cursor.close()
    offers_view = []
    for row in result:
        x={
            'name_of_product':row[0],
            'start_date':row[1],
            'end_date':row[2],
            'discount':row[3]
        }
        offers_view.append(x)
    reviews_info = {
        'isLoggedIn':isLoggedIn,
        'offers_view':offers_view
    }
    return render(request, 'registration/seller_offers.html', reviews_info)


def returnEmployeeLogin(request):
    isLoggedIn = False
    if request.method == 'POST':
        emp_type = request.POST.get('employee_type')
        print(emp_type)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        cursor = connection.cursor()
        if emp_type == 'admin':
            sql = """SELECT EMPLOYEE.PASSWORD
            FROM ADMIN LEFT OUTER JOIN EMPLOYEE
            ON(ADMIN.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
            WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
            cursor.execute(sql,{'email_id':email})
            result = cursor.fetchone()
            cursor.close()            
            if result == None:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
            elif password == result[0]:
                isLoggedIn= True
                request.session['admin_email'] = email
                return redirect('registration:admin_home')
            else:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
        elif emp_type == 'cus_care':
            sql = """SELECT EMPLOYEE.PASSWORD
            FROM CUSTOMER_CARE_EMPLOYEE LEFT OUTER JOIN EMPLOYEE
            ON(CUSTOMER_CARE_EMPLOYEE.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
            WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
            cursor.execute(sql,{'email_id':email})
            result = cursor.fetchone()
            cursor.close()            
            if result == None:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
            elif password == result[0]:
                isLoggedIn= True
                request.session['cus_care_email'] = email
                return redirect('registration:cus_care_home')
            else:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
        
        elif emp_type == 'delivery_guy':
            sql = """SELECT EMPLOYEE.PASSWORD
            FROM DELIVERY_GUY LEFT OUTER JOIN EMPLOYEE
            ON(DELIVERY_GUY.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
            WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
            cursor.execute(sql,{'email_id':email})
            result = cursor.fetchone()
            cursor.close()            
            if result == None:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
            elif password == result[0]:
                isLoggedIn= True
                request.session['del_guy_email'] = email
                return redirect('registration:delivery_guy_home')
            else:
                return render(request, 'registration/employee_login.html',context={'status':"Incorrect email or password"} )
        
        else: 
            print("Oh boy")
    return render(request, 'registration/employee_login.html' )

def returnDeliveryPending(request):
    del_guy_email = request.session['del_guy_email']
    cursor = connection.cursor()
    sql = "SELECT EMPLOYEE_ID FROM EMPLOYEE WHERE EMAIL_ID= :del_guy_email"
    cursor.execute(sql, {'del_guy_email':del_guy_email})
    result = cursor.fetchone()
    cursor.close()
    del_guy_id = result[0]

    isLoggedIn = True
    cursor = connection.cursor()
    sql ="""SELECT (CUSTOMER.FIRST_NAME ||' '|| CUSTOMER.LAST_NAME), CUSTOMER_ORDER.ORDER_DATE, CUSTOMER_ORDER.PICKUP_ADRS ,
            CUSTOMER_ORDER.ORDER_ID
            FROM CUSTOMER_ORDER LEFT OUTER JOIN CUSTOMER 
            ON(CUSTOMER_ORDER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID)
            WHERE ORDER_ID IN (SELECT ORDER_ID FROM CUSTOMER_ORDER MINUS SELECT ORDER_ID FROM PURCHASE_ORDER);"""
    cursor.execute(sql)
    result = cursor.fetchall()
    order_view = []
    for row in result:
        x = {
            'cus_name':row[0],
            'date':row[1],
            'address':row[2],
            'order_id': row[3]
        }
        order_view.append(x)
    
    if request.method == "POST":
        ord_id = request.POST.get('order_id')
        print(ord_id)
        cursor = connection.cursor()
        sql = "INSERT INTO PURCHASE_ORDER VALUES(:ord_id, :del_guy_id, SYSDATE, 'Delivered')"
        cursor.execute(sql, {'ord_id':ord_id, 'del_guy_id':del_guy_id})
        cursor.close()
        return redirect('registration:delivery_pending')

    view_order = {
        'isLoggedIn':isLoggedIn,
        'order_view':order_view
    }
    return render(request, 'registration/del_guy_pending.html', view_order)

def returnAdminHome(request):
    admin_email= request.session['admin_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT (FIRST_NAME || ' ' || LAST_NAME), EMAIL_ID, SALARY, PHONE_NUMBER, ADDRESS 
    FROM EMPLOYEE 
    WHERE EMAIL_ID =:email_id;"""
    cursor.execute(sql,{'email_id':admin_email})
    result = cursor.fetchall()
    cursor.close()

    name = result[0][0]
    email_id = result[0][1]
    salary = result[0][2]
    phone_no = result[0][3]
    address = result[0][4]

    basic_info = {
        'isLoggedIn':isLoggedIn,
        'name':name, 
        'address':address,
        'phone_no':phone_no,
        'email_id':email_id,
        'salary':salary
    }
    return render(request, 'registration/admin_home.html', basic_info )

def returnCusCareHome(request):
    cus_care_email = request.session['cus_care_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT (FIRST_NAME || ' ' || LAST_NAME), EMAIL_ID, SALARY, PHONE_NUMBER, ADDRESS 
    FROM EMPLOYEE 
    WHERE EMAIL_ID =:email_id;"""
    cursor.execute(sql,{'email_id':cus_care_email})
    result = cursor.fetchall()
    cursor.close()
    name = result[0][0]
    email_id = result[0][1]
    salary = result[0][2]
    phone_no = result[0][3]
    address = result[0][4]

    basic_info = {
        'isLoggedIn':isLoggedIn,
        'name':name, 
        'address':address,
        'phone_no':phone_no,
        'email_id':email_id,
        'salary':salary
    }
    return render(request, 'registration/cus_care_home.html', basic_info )

def returnCusCarePendingReviews(request):
    cus_care_email = request.session['cus_care_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT FIRST_NAME || ' ' ||LAST_NAME, CUSTOMER_CARE_EMPLOYEE.EMPLOYEE_ID
    FROM CUSTOMER_CARE_EMPLOYEE LEFT OUTER JOIN EMPLOYEE
    ON(CUSTOMER_CARE_EMPLOYEE.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
    WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
    cursor.execute(sql, {'email_id':cus_care_email})
    result2 = cursor.fetchone()
    cus_care_emplID = result2[1]
    sql = """SELECT CUSTOMER.FIRST_NAME || ' ' || CUSTOMER.LAST_NAME, 
    CUSTOMER_ORDER.ORDER_DATE, RETURN_ORDER.RETURN_DATE, RETURN_ORDER.COMPLAINT_DES, 
    RETURN_ORDER.ORDER_ID, PURCHASE_ORDER.DELIVERED_DATE, EMPLOYEE.FIRST_NAME ||' '|| EMPLOYEE.LAST_NAME
    FROM RETURN_ORDER LEFT OUTER JOIN CUSTOMER_ORDER
    ON(RETURN_ORDER.ORDER_ID = CUSTOMER_ORDER.ORDER_ID)
    LEFT OUTER JOIN PURCHASE_ORDER
    ON(RETURN_ORDER.ORDER_ID = PURCHASE_ORDER.ORDER_ID)
    LEFT OUTER JOIN CUSTOMER
    ON(CUSTOMER_ORDER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID)
    LEFT OUTER JOIN EMPLOYEE
    ON(PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
    WHERE RETURN_ORDER.APPROVAL_STATUS = 'Waiting for approval';"""
    cursor.execute(sql)
    result = cursor.fetchall()
    orders_view = []
    for row in result:
        id = row[4]
        sql = """SELECT PRODUCT.PRODUCT_ID, PRODUCT.NAME, COUNT(ORDERED_ITEMS.ITEM_NUMBER) ITEM_COUNT
        FROM ORDERED_ITEMS LEFT OUTER JOIN PRODUCT
        ON(ORDERED_ITEMS.PRODUCT_ID = PRODUCT.PRODUCT_ID)
        WHERE ORDER_ID =:id
        GROUP BY PRODUCT.PRODUCT_ID, PRODUCT.NAME;"""
        cursor.execute(sql,{'id':id})
        result1 = cursor.fetchall()
        items = ""
        for row1 in result1:
            items = items + "," + row1[1] + "(" + str(row1[2]) + " pcs)"
        items = items[1:]
        x = {
            'cus_name':row[0],
            'order_date':row[1],
            'return_date':row[2],
            'complaint':row[3],
            'delivery_date':row[5],
            'delivery_guy':row[6],
            'items':items,
            'ord_id':id
        }
        orders_view.append(x)
    cursor.close()

    if request.method =="POST":
        return_ord_id = request.POST.get('ord_id')
        print(return_ord_id)

        cursor = connection.cursor()
        sql = "UPDATE RETURN_ORDER SET CUSTOMER_CARE_EMPLOYEE_ID=:empl_id, APPROVAL_STATUS='Accepted' WHERE ORDER_ID=:ord_id"
        
        cursor.execute(sql,{'empl_id':cus_care_emplID, 'ord_id':return_ord_id})
        connection.commit()
        cursor.close()

        return redirect('registration:cus_care_past_review')
        

    order_info = {
        'isLoggedIn':isLoggedIn,
        'orders_view':orders_view,
        'name':result2[0],
    }


    return render(request, 'registration/cus_care_review.html', order_info )

def returnCusCarePastReview(request):
    cus_care_email = request.session['cus_care_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT FIRST_NAME || ' ' ||LAST_NAME
    FROM CUSTOMER_CARE_EMPLOYEE LEFT OUTER JOIN EMPLOYEE
    ON(CUSTOMER_CARE_EMPLOYEE.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
    WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
    cursor.execute(sql, {'email_id':cus_care_email})
    result2 = cursor.fetchone()
    sql = """SELECT CUSTOMER.FIRST_NAME || ' ' || CUSTOMER.LAST_NAME, CUSTOMER_ORDER.ORDER_DATE, 
    RETURN_ORDER.RETURN_DATE, RETURN_ORDER.COMPLAINT_DES, RETURN_ORDER.ORDER_ID, 
    PURCHASE_ORDER.DELIVERED_DATE, PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID, 
    E1.FIRST_NAME ||' '|| E1.LAST_NAME, RETURN_ORDER.APPROVAL_STATUS
    FROM RETURN_ORDER LEFT OUTER JOIN CUSTOMER_ORDER
    ON(RETURN_ORDER.ORDER_ID = CUSTOMER_ORDER.ORDER_ID)
    LEFT OUTER JOIN PURCHASE_ORDER
    ON(RETURN_ORDER.ORDER_ID = PURCHASE_ORDER.ORDER_ID)
    LEFT OUTER JOIN CUSTOMER
    ON(CUSTOMER_ORDER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID)
    LEFT OUTER JOIN EMPLOYEE E1
    ON(PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID = E1.EMPLOYEE_ID)
		LEFT OUTER JOIN EMPLOYEE E2
		ON(RETURN_ORDER.CUSTOMER_CARE_EMPLOYEE_ID=E2.EMPLOYEE_ID)
    WHERE RETURN_ORDER.APPROVAL_STATUS <> 'Waiting for approval' AND E2.EMAIL_ID =:email_id;"""
    cursor.execute(sql, {'email_id':cus_care_email})
    result = cursor.fetchall()
    orders_view = []
    for row in result:
        id = row[4]
        sql = """SELECT PRODUCT.PRODUCT_ID, PRODUCT.NAME, COUNT(ORDERED_ITEMS.ITEM_NUMBER) ITEM_COUNT
        FROM ORDERED_ITEMS LEFT OUTER JOIN PRODUCT
        ON(ORDERED_ITEMS.PRODUCT_ID = PRODUCT.PRODUCT_ID)
        WHERE ORDER_ID =:id
        GROUP BY PRODUCT.PRODUCT_ID, PRODUCT.NAME;"""
        cursor.execute(sql,{'id':id})
        result1 = cursor.fetchall()
        items = ""
        for row1 in result1:
            items = items + "," + row1[1] + "(" + str(row1[2]) + " pcs)"
        items = items[1:]
        x = {
            'cus_name':row[0],
            'order_date':row[1],
            'return_date':row[2],
            'complaint':row[3],
            'delivery_date':row[5],
            'delivery_guy':row[6],
            'action':row[7],
            'items':items
        }
        orders_view.append(x)
    cursor.close()
    print(orders_view)
    order_info = {
        'isLoggedIn':isLoggedIn,
        'orders_view':orders_view,
        'name':result2[0],
    }
    return render(request, 'registration/cus_care_emp_past.html', order_info)

def returnDeliveryHome(request):
    del_guy_email = request.session['del_guy_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT (FIRST_NAME || ' ' || LAST_NAME), EMAIL_ID, SALARY, PHONE_NUMBER, ADDRESS 
    FROM EMPLOYEE 
    WHERE EMAIL_ID =:email_id;"""
    cursor.execute(sql,{'email_id':del_guy_email})
    result = cursor.fetchall()
    cursor.close()

    name = result[0][0]
    email_id = result[0][1]
    salary = result[0][2]
    phone_no = result[0][3]
    address = result[0][4]

    basic_info = {
        'isLoggedIn':isLoggedIn,
        'name':name, 
        'address':address,
        'phone_no':phone_no,
        'email_id':email_id,
        'salary':salary
    }
    return render(request, 'registration/del_guy_home.html', basic_info)

def returnDeliveryHomePast(request):
    del_guy_email = request.session['del_guy_email']
    isLoggedIn = True
    cursor = connection.cursor()
    sql = """SELECT (CUSTOMER.FIRST_NAME || ' ' || CUSTOMER.LAST_NAME),
    PURCHASE_ORDER.DELIVERED_DATE,  
    CUSTOMER_ORDER.PICKUP_ADRS, CUSTOMER_ORDER.ORDER_ID , CUSTOMER_ORDER.ORDER_DATE
    FROM PURCHASE_ORDER LEFT OUTER JOIN CUSTOMER_ORDER
    ON(PURCHASE_ORDER.ORDER_ID = CUSTOMER_ORDER.ORDER_ID)
    LEFT OUTER JOIN  CUSTOMER
    ON(CUSTOMER_ORDER.CUSTOMER_ID = CUSTOMER.CUSTOMER_ID)
    WHERE PURCHASE_ORDER.DELIVERY_EMPLOYEE_ID = 
    (SELECT EMPLOYEE_ID FROM EMPLOYEE WHERE EMAIL_ID =:email_id)"""
    cursor.execute(sql, {'email_id':del_guy_email})
    result = cursor.fetchall()
    sql = """SELECT FIRST_NAME || ' ' ||LAST_NAME
    FROM DELIVERY_GUY LEFT OUTER JOIN EMPLOYEE
    ON(DELIVERY_GUY.EMPLOYEE_ID = EMPLOYEE.EMPLOYEE_ID)
    WHERE EMPLOYEE.EMAIL_ID =:email_id;"""
    cursor.execute(sql, {'email_id':del_guy_email})
    result1 = cursor.fetchone()
    order_view = []
    for row in result:
        id = row[3]
        sql = """SELECT PRODUCT.PRODUCT_ID, PRODUCT.NAME, COUNT(ORDERED_ITEMS.ITEM_NUMBER) ITEM_COUNT
        FROM ORDERED_ITEMS LEFT OUTER JOIN PRODUCT
        ON(ORDERED_ITEMS.PRODUCT_ID = PRODUCT.PRODUCT_ID)
        WHERE ORDER_ID =:id
        GROUP BY PRODUCT.PRODUCT_ID, PRODUCT.NAME;"""
        cursor.execute(sql,{'id':id})
        result2 = cursor.fetchall()
        items = ""
        for row1 in result2:
            items = items + "," + row1[1] + "(" + str(row1[2]) + " pcs)"
        items = items[1:]
        x = {
            'cus_name':row[0],
            'del_date':row[1],
            'address':row[2],
            'items':items,
            'ord_date':row[4]
        }
        order_view.append(x)
    cursor.close()
    view_order = {
        'isLoggedIn':isLoggedIn,
        'order_view':order_view,
        'name':result1[0]
    }
    return render(request, 'registration/del_guy_home_past.html', view_order)

def returnHireCusCare(request):
    admin_email= request.session['admin_email']
    isLoggedIn = True
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        phn = request.POST.get('phn')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        salary = request.POST.get('salary')
        if fname == '' or lname == '' or dob == '' or phn == '' or address == '' or email == '' or password == '' or salary == '':
            return render(request, 'registration/hire_cuscare_employee.html' , context={'warning':"None of the fields can be Empty"})
        cursor = connection.cursor()
        sql = """SELECT COUNT(*) FROM EMPLOYEE WHERE EMAIL_ID =:email_id;"""
        cursor.execute(sql, {'email_id':email})
        result = cursor.fetchone()
        if result[0] > 0:
            return render(request, 'registration/hire_cuscare_employee.html' , context={'warning':"This email already has an associated Employee"})
        
        sql = """SELECT MAX(EMPLOYEE_ID) FROM EMPLOYEE;"""
        cursor.execute(sql)
        last_id = cursor.fetchone()
        last_id = last_id[0]
        if last_id is not None:
            emp_id = last_id+1
        else:
            emp_id = 1
        sql = """INSERT INTO EMPLOYEE VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,[emp_id, fname, lname, salary, phn, address, email, dob, password])
        sql = """INSERT INTO CUSTOMER_CARE_EMPLOYEE VALUES(%s)"""
        cursor.execute(sql,[emp_id])
        connection.commit()
        cursor.close()
        return redirect('registration:admin_home')
    return render(request, 'registration/hire_cuscare_employee.html' )

def returnHireDeliveryGuy(request):
    admin_email= request.session['admin_email']
    isLoggedIn = True
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        phn = request.POST.get('phn')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        salary = request.POST.get('salary')
        if fname == '' or lname == '' or dob == '' or phn == '' or address == '' or email == '' or password == '' or salary == '':
            print("hello world")
            return render(request, 'registration/hire_deliveryguy.html' , context={'warning':"None of the fields can be Empty"})

        cursor = connection.cursor()
        sql = """SELECT COUNT(*) FROM EMPLOYEE WHERE EMAIL_ID =:email_id;"""
        cursor.execute(sql, {'email_id':email})
        result = cursor.fetchone()
        if result[0] > 0:
            print("hello")
            return render(request, 'registration/hire_deliveryguy.html' , context={'warning':"This email already has an associated Employee"})
        sql = """SELECT MAX(EMPLOYEE_ID) FROM EMPLOYEE;"""
        cursor.execute(sql)
        last_id = cursor.fetchone()
        last_id = last_id[0]
        if last_id is not None:
            emp_id = last_id+1
        else:
            emp_id = 1
        sql = """INSERT INTO EMPLOYEE VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql,[emp_id, fname, lname, salary, phn, address, email, dob, password])
        sql = """INSERT INTO DELIVERY_GUY VALUES(%s,%s)"""
        cursor.execute(sql,[emp_id, "Bonani, Dhaka"])
        connection.commit()
        cursor.close()
        return redirect('registration:admin_home')
    return render(request, 'registration/hire_deliveryguy.html' )