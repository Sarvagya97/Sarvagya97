from flask import Flask, request,jsonify
from flask_mysqldb import MySQL
from flask import Response
from functools import wraps



app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="sar761@SARVAG"
app.config["MYSQL_DB"]="product"
mysql=MySQL(app)




def authenticate():
    return Response(
        'Could not verify your access level for that URL./n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == 'sarvagya' and auth.password == '123456'):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#post method of category

@app.route("/category/post", methods=["POST"])
@requires_auth
def category_post():
    cur = mysql.connection.cursor()
    c_name = request.json["c_name"]
    
    result=cur.execute("INSERT INTO category (c_name) VALUES (%s)", (c_name,))
    mysql.connection.commit()
    id = cur.lastrowid
    cur.close()
    if result==0:
        return jsonify ({"message":"data is not added"})
    return jsonify({"message": "Data added successfully", "c_id": id}), 201

#get method of category

@app.route("/category/get/<cat_id>",methods=["get"])
@requires_auth
def category_get(cat_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from category where c_id=%s",(cat_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found due to invalid category id"})
    return jsonify(data)

#put method of category

@app.route("/category/put/<user_id>",methods=["put"])
@requires_auth
def category_put(user_id):
    cur=mysql.connection.cursor()
    c_name=request.json["c_name"]
    result=cur.execute("update category set c_name=%s where c_id=%s ",(c_name,user_id))
    print(result)
    mysql.connection.commit()
    if result==0:
        return jsonify ({"message":"data not updated"})
    cur.close()
    return jsonify({"message":"data update successfully"})

#delete method of category

@app.route("/category/delete/<user_id>",methods=["delete"])
@requires_auth
def category_delete(user_id):
    cur=mysql.connection.cursor()
    cur.execute("select c_id from sub_category where c_id=%s",(user_id))
    sub_category_id=cur.fetchone()
    if sub_category_id:
        cur.close()
        return jsonify({"message":"category id uses in sub_category table so can't delete it"})
    cur.execute("delete from category where c_id=%s",(user_id))
    mysql.connection.commit()
    if cur.rowcount==0:
        cur.close()
        return jsonify({"message":"data not delete"})
    cur.close()
    return jsonify ({"message":"data delete successfully"})

#post method of sub_category

@app.route("/sub_category/post",methods=["post"])
@requires_auth
def sub_category_post():
    cur=mysql.connection.cursor()
    s_name=request.json["s_name"]
    c_id=request.json["c_id"]
    cur.execute("insert into sub_category (s_name,c_id) values (%s,%s)",(s_name,c_id))
    mysql.connection.commit()
    id = cur.lastrowid
    cur.close()
    return jsonify({"message": "Data added successfully", "s_id": id}), 201

#get method of sub_category

@app.route("/sub_category/get/<user_id>",methods=["get"])
@requires_auth
def sub_category_get(user_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from sub_category where s_id=%s",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found due to invalid id"})
    return jsonify(data)

#put method of sub_category

@app.route("/sub_category/put/<user_id>",methods=["put"])
@requires_auth
def sub_category_put(user_id):
    cur=mysql.connection.cursor()
    s_name=request.json["s_name"]
    result=cur.execute("update sub_category set s_name=%s where s_id=%s",(s_name,user_id))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of sub_category

@app.route("/sub_category/delete/<user_id>",methods=["delete"])
@requires_auth
def sub_category_delete(user_id):
    cur=mysql.connection.cursor()
    cur.execute("select s_id from product where s_id=%s",(user_id))
    product_id=cur.fetchone()
    if product_id:
        return jsonify ({"message":"s_id is using in product table so can't delete it"})
    result=cur.execute("delete from sub_category where s_id=%s",(user_id,))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"enter valid id"})
    return jsonify ({"message":"data delete successfully"})

#post method of product

@app.route("/product/post",methods=["post"])
@requires_auth
def product_post():
    cur=mysql.connection.cursor()
    p_name=request.json["p_name"]
    p_description=request.json["p_description"]
    s_id=request.json["s_id"]
    making_date=request.json["making_date"]
    batch_no=request.json["batch_no"]
    cur.execute("insert into product (p_name,p_description,s_id,making_date,batch_no) values (%s,%s,%s,%s,%s)",(p_name,p_description,s_id,making_date,batch_no))
    mysql.connection.commit()
    id = cur.lastrowid
    cur.close()
    return jsonify({"message": "Data added successfully", "p_id": id}), 201

#get method of product

@app.route("/product/get/<user_id>",methods=["get"])
@requires_auth
def product_get(user_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from product where p_id=%s",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found enter valid id"})
    return jsonify(data)

#put method of product

@app.route("/product/put/<user_id>",methods=["put"])
@requires_auth
def product_put(user_id):
    cur=mysql.connection.cursor()
    p_name=request.json["p_name"]
    result=cur.execute("update product set p_name=%s where p_id=%s",(p_name,user_id))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of product

@app.route("/product/delete/<user_id>",methods=["delete"])
@requires_auth
def product_delete(user_id):
    cur=mysql.connection.cursor()
    cur.execute("select p_id from inventory where p_id=%s",(user_id))
    invenory_id=cur.fetchone()
    if invenory_id:
        return jsonify({"message":"p_id is using in inventory table so can't delete it"})
    result=cur.execute("delete from product where p_id=%s",(user_id,))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter valid id"})
    return jsonify ({"message":"data delete successfully"})

#post method for inventory

@app.route("/inventory/post",methods=["post"])
@requires_auth
def inventory_post():
    cur=mysql.connection.cursor()
    p_id=request.json["p_id"]
    p_name=request.json["p_name"]
    quantity=request.json["quantity"]
    cur.execute("insert into inventory (p_id,p_name,quantity) values (%s,%s,%s)",(p_id,p_name,quantity))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Data added successfully"})

#get method of inventory

@app.route("/inventory/get/<user_id>",methods=["get"])
@requires_auth
def inventory_get(user_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from inventory where p_id=%s",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"messsage":"data not found enter correct id"})
    return jsonify(data)

#put method of inventory

@app.route("/inventory/put/<user_id>",methods=["put"])
@requires_auth
def inventory_put(user_id):
    cur=mysql.connection.cursor()
    p_name=request.json["p_name"]
    quantity=request.json["quantity"]
    result=cur.execute("update inventory set p_name=%s,quantity=%s where p_id=%s",(p_name,quantity,user_id))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated"})
    return jsonify({"message":"data update successfully"})

#delete method of inventory

@app.route("/inventory/delete/<user_id>",methods=["delete"])
@requires_auth
def inventory_delete(user_id):
    cur=mysql.connection.cursor()
    cur.execute("select p_id from sales where p_id=%s",(user_id))
    sales_p_id=cur.fetchone()
    if sales_p_id:
        return jsonify({"message":"p_id is using in sales table so cant delete p_id"})
    result=cur.execute("delete from inventory where p_id=%s",(user_id,))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter correct id"})
    return jsonify ({"message":"data delete successfully"})

#post method of customer

@app.route("/customer/post", methods=["POST"])
@requires_auth
def customer_post():
    cur = mysql.connection.cursor()
    customer_name = request.json["customer_name"]
    customer_pn = request.json["customer_pn"]
    cur.execute("INSERT INTO customer (customer_name,customer_pn) VALUES (%s,%s)", (customer_name,customer_pn))
    mysql.connection.commit()
    id = cur.lastrowid
    cur.close()
    return jsonify({"message": "Data added successfully", "customer_id": id}), 201

#get method of customer

@app.route("/customer/get/<user_id>",methods=["get"])
@requires_auth
def customer_get(user_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from customer where customer_id=%s",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found enter valid id"})
    return jsonify(data)

#put method of customer

@app.route("/customer/put/<user_id>",methods=["put"])
@requires_auth
def customer_put(user_id):
    cur=mysql.connection.cursor()
    customer_name=request.json["customer_name"]
    customer_pn=request.json["customer_pn"]
    result=cur.execute("update customer set customer_name=%s,customer_pn=%s where customer_id=%s",(customer_name,customer_pn,user_id))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not updated enter valid id"})
    return jsonify({"message":"data update successfully"})

#delete method for customes

@app.route("/customer/delete/<user_id>",methods=["delete"])
@requires_auth
def customer_delete(user_id):
    cur=mysql.connection.cursor()
    cur.execute("select customer_id from sales where customer_id=%s",(user_id))
    customer_id=cur.fetchone()
    if customer_id:
        return jsonify ({"message":"customes id is using in sales table so cant delete customer id"})
    result=cur.execute("delete from customer where customer_id=%s",(user_id,))
    mysql.connection.commit()
    cur.close()
    if result==0:
        return jsonify({"message":"data not deleted enter valid id"})
    return jsonify ({"message":"data delete successfully"})


#post method of sales

@app.route("/sales/post", methods=["POST"])
@requires_auth
def sales_post():
    cur = mysql.connection.cursor()

    p_id = request.json["p_id"]
    customer_id = request.json["customer_id"]
    units_purchased = request.json["units_purchased"]

    cur.execute("SELECT quantity FROM inventory WHERE p_id = %s", (p_id,))
    result = cur.fetchall()

    if not result:
        return jsonify({"message": "Product not found"}), 404
    current_stock = result[0]["quantity"]

    if units_purchased > current_stock:
        return jsonify({"message": "Insufficient stock"}), 400
    new_stock = current_stock - units_purchased

    cur.execute("insert into sales (p_id, customer_id, units_purchased, stock_after_purchase) VALUES (%s, %s, %s, %s)",(p_id, customer_id, units_purchased, new_stock))

    cur.execute("update inventory set quantity = %" \
    "s WHERE p_id = %s",(new_stock, p_id))

    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"message": "Data added successfully", "sales_id": new_id})

#get method for sales

@app.route("/sales/get/<user_id>",methods=["get"])
@requires_auth
def sales_get(user_id):
    cur=mysql.connection.cursor()
    result=cur.execute("select * from sales where sales_id=%s",(user_id,))
    data=cur.fetchall()
    column_name=[disc[0] for disc in cur.description]
    cur.close()
    for row in data:
        data=dict(zip(column_name,row))
    if result==0:
        return jsonify({"message":"data not found enter valid id"})
    return jsonify(data)



if (__name__)=="__main__":
    app.run(debug=True)