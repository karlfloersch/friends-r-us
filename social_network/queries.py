from django.contrib.auth.models import User
from django.db import connection
from datetime import date
import datetime
import time


# Queries in use

def get_user_info_by_id(cust_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person WHERE id=" + cust_id)
    row = cursor.fetchone()
    return row


def get_username_and_name_by_id(cust_id):
    cursor = connection.cursor()
    cursor.execute("SELECT firstname,lastname FROM person WHERE id="
                   + str(cust_id))
    row = cursor.fetchone()
    user = User.objects.filter(first_name=cust_id)[0]
    row = row + (user.username,)
    return row

def create_page(cust_id, associated_circle):
    cursor = connection.cursor()
    #id, post_count, associated_circle
    #pageowner, pageid
    cursor.execute('INSERT INTO page(id, post_count, associated_circle_id) VALUES(?,?,?)',(cust_id, 0, associated_circle))
    cursor.execute('SELECT id FROM page WHERE associated_circle_id=? AND post_count=?', (associated_circle, 0))

    page_id = cursor.fetchone()

    cursor.execute('INSERT INTO createpage(pageowner, page_id) VALUES(?,?)',(cust_id, page_id[0]))
    return page_id[0]


def get_page(cust_id, circle_name):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM circle JOIN page ON '
                   + 'circle.id=associated_circle_id WHERE owner_id='
                   + cust_id + ' AND name="' + circle_name + '"')
    row = cursor.fetchone()
    return row


def get_page_by_circle_id(circle_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM page WHERE associated_circle_id='
                   + circle_id)
    row = cursor.fetchone()
    return row


def get_posts(page_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM post WHERE page_id=' + str(page_id))
    row = cursor.fetchall()
    return row


def get_comments(post_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM comment WHERE post_id=' + str(post_id))
    row = cursor.fetchall()
    return row


def get_users_by_firstname(firstname):
    cursor = connection.cursor()
    cursor.execute('SELECT id,firstname,lastname FROM person WHERE firstname="'
                   + firstname + '"')
    rows = cursor.fetchall()
    return rows


def get_user_circles_info(user_id):
    circle_ids = get_user_circles_ids((user_id,))
    circle_info = []
    cursor = connection.cursor()
    for circle_id in circle_ids:
        sql_call = str("SELECT * FROM circle WHERE id=" + str(circle_id[0]))
        circle_info.append(cursor.execute(sql_call).fetchone())
    return circle_info


def get_user_messages(cust_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM message WHERE sender=" + cust_id
                   + " OR receiver=" + cust_id)
    row = cursor.fetchall()
    return row


def get_conversation_messages(cust_ids):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM message WHERE sender=" + cust_ids[0]
                   + " AND receiver=" + cust_ids[1] + " OR sender="
                   + cust_ids[1] + " AND receiver=" + cust_ids[0])
    row = cursor.fetchall()
    return row

def get_likes_by_post(post_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM likepost WHERE post_id=?', (post_id))
    likes = cursor.fetchall()
    is_liked = False
    for like in likes:
        if int(user_id) == int(like[1]):
            is_liked = True
    return len(likes), is_liked

def get_likes_by_comment(comment_id, user_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM likecomment WHERE comment_id=' + str(comment_id[0])
                   + ' AND cust_id=' + str(user_id))
    likes = cursor.fetchall()
    is_liked = False
    for like in likes:
        if user_id == like[1]:
            is_liked = True
    return len(likes), is_liked

def like_post(post_id, cust_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO likepost(post_id, cust_id) VALUES(?,?)',(post_id, cust_id))

def like_comment(comment_id, cust_id):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO likecomment(comment_id, cust_id) VALUES(?,?)',(comment_id, cust_id))


def make_a_post(content, customer_id, page_id):
    # INSERT INTO POSTS VALUES (?,Date(),?,0,?,?);
    # id            INT,
    #  date          DATE,
    #  time          TIMESTAMP,
    #  content       TEXT,
    #  comment_count INT,
    #  customerid    INT,
    #  page_id        INT,
    ts = datetime.datetime.now()
    date_now = time.strftime("%d/%m/%Y")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO post(date, time, content, comment_count, customerid, page_id) VALUES(?,?,?,?,?,?)', (date_now, ts, content, '0', customer_id, page_id))


def make_a_comment(content, post_id, cust_id):
    # INSERT INTO POSTS VALUES (?,Date(),?,0,?,?);
    # id            INT,
    #  date          DATE,
    #  time          TIMESTAMP,
    #  content       TEXT,
    #  comment_count INT,
    #  customerid    INT,
    #  page_id        INT,
    ts = datetime.datetime.now()
    date_now = '0'  # time.strftime("%d/%m/%Y")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO comment(date, time, content, author_id, post_id) VALUES(?,?,?,?,?)', (date_now, ts, content, cust_id, post_id))


# End queries in use

def search_for_a_user_add_to_circle(circle_id, real_first_name, real_last_name):
    # SELECT U.User_Id, U.First_Name, U.Last_Name FROM User U where U.First_Name
    # LIKE %?% OR U.Last_Name LIKE %?%
    # INSERT INTO AddedTo VALUES (?,?)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT U.User_Id, U.First_Name, U.Last_Name FROM User U" +
        " where U.First_Name LIKE %" + real_first_name +
        "% OR U.Last_Name LIKE %" + real_last_name + "%")
    cust_id = cursor.fetchone()
    cursor.execute("INSERT INTO AddedTo VALUES ("+cust_id+","+circle_id+")")


def create_a_circle(owner_id, name, circle_type):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO circle(owner_id, name, circle_type) VALUES(?,?,?)',(owner_id, name, circle_type))
    cursor.execute('SELECT id FROM circle WHERE owner_id=? AND name=? AND circle_type=?', (owner_id, name, circle_type))
    circle_id = cursor.fetchone()
    print(circle_id)
    circle_id_ = circle_id[0]
    cursor.execute('INSERT INTO createcircle(cust_id, circle_id) VALUES(?,?)',(owner_id, circle_id_))
    return circle_id_
    #cursor.execute(
    #    "INSERT INTO Circle VALUES( NULL," +
    #    owner_id +
    #    "," +
    #    name +
    #    "," +
    #    circle_type +
    #    ")")

#todo write method to get number of items available
def get_number_available_units(adv_id):
    cursor = connection.cursor()
    cursor.execute('SELECT num_aval_units FROM advertisement WHERE adv_id=?',(adv_id))
    num = cursor.fetchone()
    return num[0]

def validate_purchase_quantity(adv_id, num_units):
    cursor = connection.cursor()
    cursor.execute('SELECT num_aval_units FROM advertisement WHERE adv_id=?',(adv_id))
    num = cursor.fetchone()
    num_ = num[0]

    if (num_ - num_units) > 0:
        return True
    else:
        return False


def purchase_one_or_advertised_item(adv_id, num_units, date, customer_acc_num):
    cursor = connection.cursor()
    #cursor.execute(UPDATE advertisement SET num_aval_units = num_aval_units - num_units WHERE adv_id= " +
    #   ad_id)

    cursor.execute('UPDATE adversitement SET num_aval_units= num_aval_units - 1 WHERE adv_id=?',(adv_id))
    date_now = time.strftime("%d/%m/%Y")
    time = datetime.datetime.now()
    #cursor = connection.cursor("INSERT INTO buy (NULL," +
    #                           num_units +
    #                           "," +
    #                           date_now +
    #                           "," +
    #                           ts +
    #                           "," +
    #                           customer_acc_num +
    #                           "," +
    #                           ad_id +
    #                           ")")
    cursor.execute('INSERT INTO buy(num_units, date, time, customer_acc_num, adv_id) VALUES(?,?,?,?,?)', (num_units, date_now, time, customer_acc_num, adv_id))


    # not complete


def list_each_customer_account_account_history(cust_id):
    # SELECT P.* FROM Purchase P INNER JOIN Has_Account A ON (P.User,P.Account) = (A.User_Id,A.Account_Number) WHERE P.User = ?
    # buy
    # transaction_id   INT(30),
    #  num_units        INT,
    #  date             DATE,
    #  time             TIMESTAMP,
    #  customer_acc_num INT,
    #  adv_id           INT(30),

    # account
    # customer_id     INT,
    #  account_id       INT,
    #  create_date DATETIME NOT NULL,
    #  credit_card_num VARCHAR(50),

    # cursor = connection.cursor("SELECT * FROM buy B INNER JOIN account A ON (B.User,B.Account) = (A.User_Id,A.Account_Number) WHERE B.customer_acc_num = "+cust_id)
    # cursor.execute()
    val = cursor.fetchone()
    return val




def list_customers_current_circles(owner_id, circle_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM circle WHERE C.owner_id = " +
        owner_id +
        " UNION SELECT * FROM circle " +
        "C INNER JOIN memberofcircle " +
        "A ON C.id = A.circle_id WHERE A.circle_id =" +
        circle_id)
    val = cursor.fetchone()
    return val


def comment_on_a_post(content, author_id, post_id):
    # INSERT INTO COMMENT VALUES (?,Date(),?,?,?);
    # UPDATE Post SET Comment_Count = Comment_Count + 1 WHERE Post_Id = ?
    #     id        INT,
    # date      DATE,
    # time      TIMESTAMP,
    # content   TEXT,
    # author_id INT,
    # post_id INT,
    date_now = time.strftime("%d/%m/%Y")
    ts = date.isoformat()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO comment VALUES (NULL," +
        date_now +
        "," +
        ts +
        "," +
        content +
        "," +
        author_id +
        "," +
        post_id +
        ")")
    cursor.execute("UPDATE post SET Comment_Count = Comment_Count + 1" +
                   "WHERE Post_Id =" + post_id)

def remove_a_post(post_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM post where Post_Id =" + post_id)


def remove_a_comment(comment_id):
    # UPDATE Post SET Comment_Count = Comment_Count -1 WHERE Post_Id IN
    # (SELECT C.Post FROM Comment C WHERE C.Comment_Id = ?)
    # DELETE FROM Comment WHERE Comment_Id = ?
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE post SET comment_Count = comment_Count -1 WHERE post_id" +
        " IN (SELECT C.Post FROM comment C WHERE C.comment_id = " +
        comment_id +
        ")")
    cursor.execute("DELETE FROM Comment WHERE Comment_Id ="+comment_id)


def unlike_a_post(post_id, cust_id):
    # DELETE FROM User_Likes_Post WHERE Post = ? AND User = ?
    # post_id INT,
    # cust_id INT,

    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM likepost WHERE post_id = " +
        post_id +
        " AND cust_id =" +
        cust_id)


def unlike_a_comment(comment_id, cust_id):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM likecomment WHERE comment_id = " +
        comment_id +
        " AND cust_id=" +
        cust_id)


def modify_a_post(content, post_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE post SET content = "++" WHERE id ="+post_id)


def modify_a_comment(content, comment_id):
    # UPDATE Comment SET Content = ? WHERE Comment_Id = ?
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Comment SET Content = " +
        content +
        " WHERE id =" +
        comment_id)


def delete_a_circle(circle_id):
    # DELETE FROM Circle  WHERE Circle_Id = ?
    cursor = connection.cursor()
    cursor.execute("DELETE FROM circle  WHERE id = "+circle_id)


def rename_a_circle(name, circle_id):
    # Update Circle set  Circle_Name = ? WHERE Circle_Id = ?
    cursor = connection.cursor()
    cursor.execute("Update Circle set  name = "+name+" WHERE id = "+circle_id)


def join_a_circle(cust_id, circle_id):
    # Insert into AddedTo values (?,?)
    # cust_id   INT,
    # circle_id INT,

    cursor = connection.cursor()
    cursor.execute(
        "Insert into memberofcircle values (" +
        cust_id +
        "," +
        circle_id +
        ")")


def unjoin_a_circle(cust_id, circle_id):
    # DELETE FROM AddedTo WHERE user=? AND circle = ?
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM memberofcircle where cust_id =" +
        cust_id +
        "AND circle_id=" +
        circle_id)


def send_recieve_message(content, sender_id, receiver_id, subject):
    # INSERT INTO Message(?,Date(),?,?,?,?)
    # id                                    INT,
    #     content                           TEXT,
    #     sender                             INT,
    #     receiver                          INT,
    #     subject                            VARCHAR(30),
    #     date                              DATE,

    cursor = connection.cursor()
    date_now = time.strftime("%d/%m/%Y")
    cursor.execute(
        "INSERT INTO message(NULL," +
        content +
        "," +
        sender_id +
        "," +
        receiver_id +
        "," +
        date_now +
        ")")


def delete_message(message_id):
    # DELETE FROM Message WHERE Message_Id = ?
    cursor = connection.cursor()
    # date_now = time.strftime("%d/%m/%Y")
    cursor.execute("DELETE FROM message WHERE id ="+message_id)


def get_user_circles_ids(user_id):
    #""" Get a list of all the user's circles """
    cursor = connection.cursor()
    #sql_call = str("SELECT id FROM circle C WHERE C.owner_id = " + user_id +
    #              " UNION SELECT circle_id FROM circle C INNER JOIN " +
    #               "memberofcircle A ON C.id = A.circle_id WHERE " +
    #               "A.cust_id = " + str(user_id))
    # sql_call = str("SELECT circle_id FROM memberofcircle WHERE cust_id="
    #                + user_id)

    cursor = connection.cursor()
    cursor.execute('SELECT C.id, C.owner_id FROM circle C INNER JOIN memberofcircle CM ON C.id = CM.circle_id WHERE CM.cust_id=?', (user_id))
    #cursor.execute(sql_call)
    return cursor.fetchall()

def add_customer(firstname_, lastname_, password_, gender_, address_, city_, state_, zipcode_, telephone_, email_, dob_, credit_card_num):
    cursor = connection.cursor()
    ts = datetime.datetime.now()
    dt = datetime.datetime.strptime(dob_, '%m-%d-%Y')
    cursor.execute('INSERT INTO person(firstname, lastname, password, gender, address, city, state, zipcode, telephone) VALUES(?,?,?,?,?,?,?,?,?)',( firstname_, lastname_, password_, gender_, address_, city_, state_, zipcode_, telephone_))
    cursor.execute('SELECT id FROM person WHERE lastname=? AND firstname=? AND address=?', (lastname_, firstname_, address_))
    id_val = cursor.fetchone()
    id_val = id_val[0]
    cursor.execute('INSERT INTO account(customer_id, create_date, credit_card_num) VALUES(?,?,?)',(id_val, ts, credit_card_num))
    cursor.execute('INSERT INTO customer(cust_id, email, rating, date_of_birth) VALUES(?,?,?,?)', (id_val, email_, 5, dt))
    id_circle = create_a_circle(id_val, "Friends", "Friends")
    create_page(id_val, id_circle)
    return id_val

def remove_customer(cust_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM customer WHERE cust_id=?',(cust_id))
    #Check to see if account is deleted when a customer is removed from the system.

def remove_employee(cust_id):
    print(cust_id)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM employee WHERE emp_id=?',(cust_id))
    #Check to see if account is deleted when a customer is removed from the system.

def update_customer(cust_id, rating, firstname_, lastname_, gender_, address_, city_, state_, zipcode_, telephone_, email_):
    cursor = connection.cursor()
    cursor.execute("UPDATE customer SET email=?, rating=? WHERE cust_id =?",(email_, rating, cust_id))
    cursor.execute('UPDATE person SET firstname =?, lastname=?, gender=?, address=?, city=?, state=?, telephone=? WHERE id = ?',(firstname_, lastname_, gender_, address_, city_, state_, telephone_, cust_id))

def update_customer_credit_card(account_id, credit_card_num):
    cursor = connection.cursor()
    cursor.execute('UPDATE account SET credit_card_num=? WHERE account_id=?',(credit_card_num, account_id))

def customer_mailing_list():
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT email FROM customer')
    email_list = cursor.fetchall()
    return email_list

def item_suggestions(emp_id, cust_id):
    #SELECT A.Item_Name, A.Advertisement_Id  FROM  Advertisement  A  WHERE A.Employee = ? AND A.Number_Of_Units>0  AND A.Type  IN (SELECT DISTINCT (A.Type) FROM Advertisement A INNER JOIN Purchase P INNER JOIN User U ON A.Advertisement_Id = P.Advertisement AND P.User = U.User_Id WHERE U.User_Id = ? )
    cursor = connection.cursor()
    cursor.execute('SELECT A.item_name, A.adv_id FROM advertisement A WHERE A.employee_id=? AND A.num_aval_units > 0 AND A.type IN (SELECT DISTINCT A.type FROM advertisement A INNER JOIN buy B INNER JOIN customer C ON A.adv_id = B.adv_id AND B.customer_acc_num = C.cust_id WHERE C.cust_id=?)',(emp_id, cust_id))
    item_suggestions = cursor.fetchall()
    del item_suggestions[0]
    return item_suggestions


def add_employee(
        firstname,
        lastname,
        password,
        gender,
        address,
        city,
        state,
        zipcode,

        telephone,
        ssn,
        start_date,
        hourly_rate,
        role):
    cursor = connection.cursor()

    cursor.execute('INSERT INTO person(firstname, lastname, password, gender, address, city, state, telephone) VALUES(?,?,?,?,?,?,?,?)',(firstname, lastname, password, gender, address, city, state,telephone))
    cursor.execute('SELECT id FROM person WHERE lastname=? AND firstname=? AND address=?', (lastname, firstname, address))
    id_val = cursor.fetchone()
    cursor.execute('INSERT INTO employee(emp_id, ssn, start_date, hourly_rate, role) VALUES(?,?,?,?,?)', (id_val[0], ssn, start_date, hourly_rate, role))
    return id_val[0]


def get_employee_id(firstname, lastname, address):
    #sql_call = str(
    #    "select id from person where lastname = " +
    #    lastname +
    #    " and " +
    #    "firstname = " +
    #    firstname +
    #    " address = " +
    #    address)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM person WHERE lastname=? AND firstname=? AND address=?', (lastname_, firstname_, address_))
    #cursor.execute(sql_call)
    id_val = cursor.fetchone()
    return id_val[0]


def delete_employee(emp_id):
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM person where emp_id=?',(emp_id))


# needs to be done
def update_employee(
        firstname,
        lastname,
        password,
        gender,
        address,
        city,
        state,
        zipcode,
        telephone,
        hourly_rate,
        role,
        emp_id):

    # Update Person
    # Set PhoneNumber = 6314136666
    # Where SSN= 123456789

    print('IN THIS SON')

    cursor = connection.cursor()
    target_id = emp_id

    cursor.execute('UPDATE person SET firstname =?, lastname=?, password=?, gender=?, address=?, city=?, state=?, telephone=? WHERE id = ?',(firstname, lastname, password, gender, address, city, state, telephone, target_id))
    cursor.execute('UPDATE employee SET hourly_rate=?, role=? WHERE id=?', (hourly_rate, role, target_id[0]))


    #sql_call = str("update person  " + firstname + ", " +
    #               lastname + "," + password + "," + gender + ", " + address +
    #               "," + city + ", " + state + ", " + telephone + ")")
    #cursor.execute(sql_call)

    #sql_call = str(
    #    "Insert into employee Values (NULL, " +
    #    ssn +
    #    "," +
    #    start_date +
    #    ", " +
    #    hourly_rate +
    #    " , " +
    #    role +
    #    " )")
    #cursor.execute(sql_call)


#def obtain_sales_report_by_month(date):
#    cursor = connection.cursor()
    # emp_id INT,
    # adv_id INT,
#    sql_call = str(
#        "SELECT  A.adv_id,  A.item_name , E.emp_id, " +
#        "SUM(P.num_units) as TSaleOnItem, SUM(P.num_units * A.unit_price) " +
#       " FROM employee E INNER JOIN buy P INNER JOIN advertisement A ON " +
#        "P.adv_id =A.adv_id AND A.Employee = E.emp_id  " +
#        "WHERE MONTH(P.date) = " +
#        date +
#        " GROUP BY A.adv_id")
#    cursor.execute(sql_call)
#    val = cursor.fetchone()
#    return val


def sales_report_month(date):
    cursor = connection.cursor()
    #SELECT  A.AdvertisementId,  A.Item_Name , E.EmployeeId, SUM(P.Number_Of_Units) as TSaleOnItem, SUM(P.Number_Of_Units * A.Unit_Price)  FROM Employee E INNER JOIN Purchase P INNER JOIN Advertisement A ON P.Advertisement =A.AdvertisementId AND A.Employee = E.EmployeeId  WHERE MONTH(P.Date) = ? GROUP BY A.AdvertisementId
    cursor.execute("SELECT A.adv_id, A.item_name, E.emp_id, SUM(B.num_units) as TSaleOnItem, SUM(B.num_units * A.unit_price) FROM employee E INNER JOIN buy B INNER JOIN advertisement A ON B.adv_id = A.adv_id AND A.employee_id = E.emp_id WHERE strftime('%m', B.date)=? GROUP BY A.adv_id", (date))
    report = cursor.fechone()
    return report

def produce_list_of_all_items_advertised():
    cursor = connection.cursor()
    sql_call = str(
        "SELECT A.adv_id, A.item_name, A.unit_price, A.num_aval_units FROM advertisement A")

    cursor.execute(sql_call)
    val = cursor.fetchall()
    return val

# check this one


def produce_list_of_transactions_item_name_cust_name(
        item_name,
        lastname,
        firstname):
    cursor = connection.cursor()
    sql_call = str(
        "SELECT * from buy B " +
        "INNER JOIN Advertisement A INNER JOIN customer C" +
        "ON A.adv_id = B.adv_id  AND  " +
        "B.customer_acc_num = C.cust_id  WHERE  A.item_name = " + item_name +
        " OR (C.lastname=" + lastname + " AND C.firstname=" + firstname + ")")

    cursor.execute(sql_call)
    val = cursor.fetchall()
    return val

def transactions_by_customer_id(cust_id):
    cursor = connection.cursor()
    cursor.execute('SELECT P.firstname, P.lastname, B.transaction_id, B.num_units, B.time FROM person P INNER JOIN buy B ON P.id =? B.customer_acc_num', (cust_id))
    transactions = cursor.fetchall()
    return transactions

def list_users_by_product(product_id):
    cursor = connection.cursor()
    cursor.execute('SELECT P.firstname, P.lastname, C.email FROM buy B INNER JOIN (person P INNER JOIN customer C ON P.id = C.cust_id) ON B.customer_acc_num=? AND B.adv_id=?)',(product_id))
    users = cursor.fetchall()
    return users

def create_advertisement(item_name, num_aval_units, unit_price, content, employee_id, type, date, company):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO advertisement(item_name, num_aval_units, unit_price, content, employee_id, type, date, company) VALUES(?,?,?,?,?,?,?,?)',(item_name, num_aval_units, unit_price, content, employee_id, type, date, company))
    adv_obj = cursor.fetchone()
    return adv_obj

def delete_advertisement(adv_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM advertisement WHERE adv_id=?',(adv_id))

def get_revenue_of_item(adv_id, type_in, customer_acc_num):
    if(adv_id == ""):
        adv_id = 00000000000
    if(type_in == ""):
        type_in = "eoifdofusdosi"
    if(customer_acc_num == ""):
        customer_acc_num = 000000000

    cursor = connection.cursor()
    cursor.execute('CREATE VIEW TotalSale AS SELECT A.adv_id,  A.item_name,  A.unit_price, SUM(B.num_units) AS Number_Sold FROM Advertisement A  INNER JOIN buy B ON B.adv_id =? A.adv_id GROUP BY A.adv_id',(adv_id))
    cursor.execute('SELECT TS.adv_id, TS.item_name, TS.num_units * TS.unit_price  AS Revenue FROM TotalSale TS where TS.adv_id = ? OR TS.type = ? OR TS.customer_acc_num = ?',(adv_id, type_in, customer_acc_num))
    revenue_obj = cursor.fetchone()
    return revenue_obj

def customer_rep_highest_revenue():
    #SELECT E.SSN, P2.First_Name, P2.Last_Name,  SUM(P.Number_Of_Units * A.Unit_Price) AS Revenue FROM Employee E INNER JOIN Advertisement A  INNER JOIN Purchase P INNER JOIN Person P2 ON E.SSN = P2.SSN AND E.SSN = A.Employee AND P.Advertisement = A.AdvertisementId GROUP BY E.EmployeeId
    #ORDER BY Revenue DESC LIMIT 1
    cursor = connection.cursor()
    cursor.execute('SELECT E.SSN, P.firstname, P.lastname, SUM(B.num_units * A.unit_price) AS Revenue FROM employee E INNER JOIN advertisement A INNER JOIN buy B INNER JOIN person P ON E.emp_id = P.id AND E.ssn = A.employee_id AND B.adv_id = A.adv_id GROUP BY E.emp_id ORDER BY Revenue DESC LIMIT 1')
    rep = cursor.fetchone()
    return rep

def customer_list():
    cursor = connection.cursor()
    cursor.execute("SELECT P.id, P.firstname, P.lastname, P.gender, P.address, P.city, P.state, P.zipcode, P.telephone, C.email, C.rating, strftime('%d-%m-%Y', C.date_of_birth) FROM person P INNER JOIN customer C ON P.id = C.cust_id")
    cust_list = cursor.fetchall()
    return cust_list

def employee_list():
    cursor = connection.cursor()
    row = cursor.execute("SELECT P.firstname, P.lastname, P.gender, P.address, P.city, P.state, P.zipcode, P.telephone, strftime('%d-%m-%Y', E.start_date), E.hourly_rate, E.role, P.id FROM person P INNER JOIN employee E ON P.id = E.emp_id")
    return row.fetchall()

def advertisements_by_company(company_name):
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT A.adv_id, A.item_name, A.num_aval_units, A.unit_price, A.content, A.type, A.date FROM advertisement A WHERE A.company=?', (company_name))
    adv_list = cursor.fetchall()
    return adv_list


