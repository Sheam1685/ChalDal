from multiprocessing import context
from django.shortcuts import render, redirect, reverse
from django.db import connection
from datetime import datetime

# Create your views here.

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

def returnAddProduct(request):
    isLoggedIn = True
    catList = categoryList()
    seller_email= request.session['seller_email']

    cursor = connection.cursor()
    sql = "SELECT CATEGORY_NAME FROM CATEGORY"
    cursor.execute(sql)
    result = cursor.fetchall()
    cat_list=[]
    for r in result:
        cat_list.append(r[0])

    cursor = connection.cursor()
    sql = "SELECT SELLER_ID FROM SELLER WHERE EMAIL_ID=:email_id"
    cursor.execute(sql,{'email_id':seller_email})
    result = cursor.fetchone()
    cursor.close()
    seller_id = result[0]

    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        cat_name = request.POST.get('cat_name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        quantity = int(quantity)
        exp_time_del = request.POST.get('exp_del_time')
        description = request.POST.get('description')

        pname = prod_name.lower()
        cursor = connection.cursor()
        sql = 'SELECT COUNT(*) FROM PRODUCT WHERE LOWER(NAME) = :pname AND SELLER_ID = :sel_id'
        cursor.execute(sql,{'pname': pname, 'sel_id':seller_id})
        result = cursor.fetchone()
        cursor.close()
        if result[0]>0:
            context = {'isLoggedIn':isLoggedIn, 'status':"Product already exist!", 'acType':"seller", 'catList':catList}
            return render(request, 'products/add_product.html', context)

        cursor = connection.cursor()
        sql = 'SELECT MAX(PRODUCT_ID) FROM PRODUCT'
        cursor.execute(sql)
        
        last_id = cursor.fetchone()
        last_id = last_id[0]
        if last_id is not  None:
            prod_id = last_id + 1
        else:
            prod_id = 1

        cursor = connection.cursor()
        sql = "SELECT CATEGORY_ID FROM CATEGORY WHERE CATEGORY_NAME = :cat"
        cursor.execute(sql,{'cat':cat_name})
        cat_id = cursor.fetchone()
        cat_id = cat_id[0]

        cursor = connection.cursor()
        sql = "INSERT INTO PRODUCT VALUES(%s,%s,%s,%s,%s,%s,%s)"

        print(prod_id, seller_id, prod_name, cat_id, description, exp_time_del, price)
        cursor.execute(sql,[prod_id, seller_id, prod_name, cat_id, description, exp_time_del, price])
        connection.commit()
        cursor.close()

        
        for i in range(quantity):
            cursor = connection.cursor()
            sql = "INSERT INTO PRODUCT_UNIT VALUES(%s,%s,%s,%s)"
            item_no = i+1
            cursor.execute(sql,[prod_id, seller_id, item_no, "not sold"])
            connection.commit
            cursor.close()
        return redirect('registration:seller_products')

    context = {
        'cat_list':cat_list, 'isLoggedIn':isLoggedIn, 'catList':catList,'acType':"seller"
    }
    return render(request, 'products/add_product.html', context)


def returnProductCat(request, cat_pk):

    isLoggedIn=False
    acType=""
    if request.session.has_key('cus_email'):
        isLoggedIn=True
        acType="customer"
    if request.session.has_key('seller_email'):
        isLoggedIn=True
        acType="seller"
    
    cursor = connection.cursor()
    sql = "SELECT CATEGORY_NAME FROM CATEGORY WHERE CATEGORY_ID = :cat_id"
    catList = categoryList()
    
    cursor.execute(sql,{'cat_id': cat_pk})
    result = cursor.fetchall()
    cursor.close()
    cat_name = result[0][0]

    cursor = connection.cursor()
    sql = "SELECT NAME, DESCRIPTION, PRICE, PRODUCT_ID FROM PRODUCT WHERE CATEGORY_ID= :cat_id"
    
    cursor.execute(sql,{'cat_id': cat_pk})
    result = cursor.fetchall()
    cursor.close()

    prod_list = []

    for r in result:
        prod_name = r[0]
        prod_des = r[1]
        prod_price = r[2]
        prod_id = r[3]
        row = {'prod_name':prod_name, 'prod_des':prod_des, 'prod_price': prod_price, 'prod_id':prod_id}
        prod_list.append(row)

    context = {
        'isLoggedIn':isLoggedIn, 'acType':acType,
        'cat_name':cat_name, 'prod_list':prod_list, 'catList':catList
    }
    
    return render(request, 'products/product_cat.html', context)



def returnProductDetails(request, prod_pk):
    isLoggedIn=False
    catList = categoryList()
    acType=""
    if request.session.has_key('cus_email'):
        isLoggedIn=True
        acType="customer"
    if request.session.has_key('seller_email'):
        isLoggedIn=True
        acType="seller"

    cursor = connection.cursor()
    sql = """SELECT S.NAME, P.NAME, P.DESCRIPTION, P.EXPECTED_TIME_TO_DELIVER, P.PRICE, C. CATEGORY_NAME, P.RATING, P.PRODUCT_ID,
            (SELECT PERCENTAGE_DISCOUNT FROM OFFER O WHERE O.PRODUCT_ID = P.PRODUCT_ID AND END_DATE>SYSDATE),
            (SELECT COUNT(*) FROM PRODUCT_UNIT PU WHERE P.PRODUCT_ID = PU.PRODUCT_ID AND STATUS = 'not sold')
            FROM PRODUCT P 
                JOIN SELLER S ON(P.SELLER_ID = S.SELLER_ID)
                JOIN CATEGORY C ON(P.CATEGORY_ID = C.CATEGORY_ID)
            WHERE P.PRODUCT_ID = :prod_pk """
    cursor.execute(sql,{'prod_pk': prod_pk})
    r = cursor.fetchone()
    cursor.close()

    
    seller_name = r[0]
    prod_name = r[1]
    prod_des = r[2]
    exp_del_time = r[3]
    prod_price = r[4]
    categ_name = r[5]
    prod_rating = int(r[6])
    prod_id = r[7]
    discount = r[8]
    quantity = r[9]
    if discount == None:
        discount=0
    else:
        discount = int(discount)
    disc_price = prod_price* (100-discount)/100

    rating_ind = []
    for i in range(prod_rating):
        rating_ind.append("a")

    context = {'isLoggedIn':isLoggedIn, 'acType':acType, 'catList':catList, 
                'seller_name':seller_name, 'prod_name':prod_name, 'prod_des':prod_des, 
                'exp_del_time':exp_del_time, 'prod_price': prod_price, 'categ_name':categ_name, 
                'rating_ind':rating_ind, 'prod_id':prod_id, 'discount':discount, 'disc_price':disc_price, 'quantity':quantity
                }
    return render(request, 'products/product_details.html', context)


def returnAddOffer(request):
    isLoggedIn = True
    seller_email= request.session['seller_email']
    cursor = connection.cursor()
    sql = """SELECT PRODUCT.NAME
    FROM PRODUCT LEFT OUTER JOIN SELLER
    ON(PRODUCT.SELLER_ID = SELLER.SELLER_ID)
    WHERE SELLER.EMAIL_ID =: email_id
    MINUS
    SELECT PRODUCT.NAME
    FROM PRODUCT LEFT OUTER JOIN SELLER
    ON(PRODUCT.SELLER_ID = SELLER.SELLER_ID)
    LEFT OUTER JOIN OFFER
    ON(PRODUCT.PRODUCT_ID = OFFER.PRODUCT_ID)
    WHERE SELLER.EMAIL_ID =: email_id AND OFFER.END_DATE > SYSDATE;"""
    cursor.execute(sql, {'email_id':seller_email})
    result = cursor.fetchall()
    product_list =[]
    for r in result:
        product_list.append(r[0])
    if not len(result):
        status = "All of your products have running offers. No new offers can be added."
        context = {
        'product_list':product_list, 'isLoggedIn':isLoggedIn, 'status':status
        }
        return render(request, 'products/add_offer.html', context)
    sql = """SELECT SELLER_ID FROM SELLER WHERE EMAIL_ID =: email_id;"""
    cursor.execute(sql, {'email_id':seller_email})
    result = cursor.fetchone()
    seller_id = result[0]
    
    if request.method == 'POST':
        prod_name = request.POST.get('product_name')
        end_date = request.POST.get('oed')
        discount = request.POST.get('pct')
        CurrentDate = datetime.now()
        if datetime.strptime(end_date, '%Y-%m-%d') < CurrentDate:
            msg = 'End Date must be later than today'
            context = {
            'product_list':product_list, 'isLoggedIn':isLoggedIn, 'msg':msg
            }
            return render(request, 'products/add_offer.html', context)
        sql = """SELECT PRODUCT_ID FROM PRODUCT 
        WHERE SELLER_ID =: id AND NAME =: prod_name;"""
        cursor.execute(sql, {'id':seller_id, 'prod_name':prod_name})
        result = cursor.fetchone()
        prod_id = result[0]
        sql = """SELECT MAX(OFFER_NUMBER)
        FROM OFFER
        GROUP BY PRODUCT_ID, SELLER_ID
        HAVING PRODUCT_ID =: prod_id AND SELLER_ID =: id;"""
        cursor.execute(sql, {'id':seller_id, 'prod_id':prod_id})
        count = cursor.fetchone()
        if count == None:
            offer_number = 1
        else:
            offer_number = count[0] + 1
        
        sql = """INSERT INTO OFFER VALUES(%s,%s,%s,SYSDATE,%s,%s)"""
        cursor.execute(sql,[prod_id, seller_id, offer_number, end_date, discount])
        connection.commit()
        cursor.close()
        return redirect('registration:seller_offers')

    context = {
        'product_list':product_list, 'isLoggedIn':isLoggedIn
    }
    return render(request, 'products/add_offer.html', context)


def returnCheckOut(request, prod_pk):
    cus_email = request.session['cus_email']

    cursor = connection.cursor()
    sql = """SELECT FIRST_NAME||' '||LAST_NAME AS NAME
            FROM CUSTOMER
            WHERE EMAIL_ID = :cus_email
            """
    
    cursor.execute(sql, {'cus_email':cus_email})
    result = cursor.fetchone()
    cursor.close()
    cus_name = result[0]

    cursor = connection.cursor()
    sql = """SELECT prod.NAME, prod.PRICE, sell.NAME
            FROM PRODUCT prod JOIN SELLER sell
            ON(prod.SELLER_ID = sell.SELLER_ID)
            WHERE prod.PRODUCT_ID = :prod_id
            """
    
    cursor.execute(sql, {'prod_id':prod_pk})
    result = cursor.fetchone()
    cursor.close()
    prod_name = result[0]
    prod_price = result[1]
    seller_name = result[2]

    if request.method == 'POST':
        pickup_addr = request.POST.get('pickup_add')

    context = {
        'cus_name':cus_name, 'cus_email':cus_email,
        'prod_name':prod_name, 'prod_price':prod_price, 'seller_name':seller_name
    }

    return render(request, 'products/checkout.html', context)