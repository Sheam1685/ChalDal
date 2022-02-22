from operator import truediv
from django.shortcuts import redirect, render
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

    if request.method == 'POST':
        searchTerm = request.POST.get('searchTerm')
        
        
        return redirect('homeApp:productSearch', searchT=searchTerm)

    context={'isLoggedIn':isLoggedIn, 'acType':acType, 'catList':catList, 'searchbar':"yes"}

    return render(request, 'homeApp/home_page.html', context)

def searchProduct(request, searchT):
    
    searchContext = searchT
    searchT = searchT.lower()
    
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

    searchT = '%' + searchT + '%'
    cursor = connection.cursor()
    sql = """SELECT P.PRODUCT_ID, P.NAME, P.PRICE, 
            NVL(O.PERCENTAGE_DISCOUNT,0), ROUND(AVG_RATING(P.PRODUCT_ID),1)
            FROM PRODUCT P 
            LEFT JOIN OFFER O 
                ON(O.PRODUCT_ID = P.PRODUCT_ID AND O.END_DATE>SYSDATE)
            WHERE LOWER(P.NAME) LIKE %s """
    cursor.execute(sql, [searchT])
    result = cursor.fetchall()
    cursor.close()
    prod_list = []

    for r in result:
        prod_id = r[0]
        prod_name = r[1]
        prod_price = r[2]
        discount = r[3]
        rating = int(r[4])
        dis_price = prod_price - prod_price*discount/100
        rating_string = []
        for i in range(rating):
            rating_string.append('a')

        row = {'prod_name':prod_name,'prod_price': prod_price, 'dis_price':dis_price, 'prod_id':prod_id, 
            'discount':discount, 'rating':rating, 'rating_string':rating_string}
        prod_list.append(row)

    
    context={'isLoggedIn':isLoggedIn, 'acType':acType, 'catList':catList, 'prod_list':prod_list, 'searchContext':searchContext}
    return render(request, 'homeApp/productSearch.html', context)

    
