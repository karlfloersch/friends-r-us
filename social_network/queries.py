from django.db import connection
from datetime import date
import time


# Queries in use

def get_user_info_by_id(cust_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM person WHERE id=" + cust_id)
    row = cursor.fetchone()
    return row


def get_user_circles_info(user_id):
    circle_ids = get_user_circles_ids(user_id)
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
    cursor.execute(
        "INSERT INTO Circle VALUES( NULL," +
        owner_id +
        "," +
        name +
        "," +
        circle_type +
        ")")


def make_a_post(customer_id, page_id):
    # INSERT INTO POSTS VALUES (?,Date(),?,0,?,?);
    # id            INT,
    #  date          DATE,
    #  time          TIMESTAMP,
    #  content       TEXT,
    #  comment_count INT,
    #  customerid    INT,
    #  page_id        INT,
    ts = date.isoformat()
    date_now = time.strftime("%d/%m/%Y")
    cursor = connection.cursor()
    cursor.execute(
        "insert into post values(NULL," +
        date_now +
        "," +
        ts +
        ",0," +
        customer_id +
        "," +
        page_id +
        ")")


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


def like_post(post_id, cust_id):
    # INSERT INTO User_Likes_Post VALUES (?,?);
    # post_id INT,
    # cust_id INT,
    cursor = connection.cursor()
    cursor.execute("INSERT INTO likepost  VALUES ("+post_id+","+cust_id+")")


def like_comment(comment_id, cust_id):
    # INSERT INTO likecomment VALUES (?,?)
    # comment_id INT,
    # cust_id    INT,
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO likecomment VALUES (" +
        comment_id +
        "," +
        cust_id +
        ")")


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


def unlike_a_Post(post_id, cust_id):
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
    """ Get a list of all the user's circles """
    cursor = connection.cursor()
    sql_call = str("SELECT id FROM circle C WHERE C.owner_id = " + user_id +
                   " UNION SELECT circle_id FROM circle C INNER JOIN " +
                   "memberofcircle A ON C.id = A.circle_id WHERE " +
                   "A.cust_id = " + str(user_id))
    # sql_call = str("SELECT circle_id FROM memberofcircle WHERE cust_id="
    #               + user_id)
    cursor.execute(sql_call)
    return cursor.fetchall()


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
    sql_call = str(
        "Insert into person Values (NULL, " +
        firstname +
        ", " +
        lastname +
        "," +
        password +
        "," +
        gender +
        ", " +
        address +
        "," +
        city +
        ", " +
        state +
        ", " +
        telephone +
        ")")
    cursor.execute(sql_call)
    sql_call = str(
        "select id from person where lastname = " +
        lastname +
        " and " +
        "firstname = " +
        firstname +
        " address = " +
        address)
    cursor.execute(sql_call)
    id_val = cursor.fetchone()
    sql_call = str(
        "Insert into employee Values (" +
        id_val +
        ", " +
        ssn +
        "," +
        start_date +
        ", " +
        hourly_rate +
        " , " +
        role +
        " )")

    cursor.execute(sql_call)


def get_employee_id(firstname, lastname, address):
    sql_call = str(
        "select id from person where lastname = " +
        lastname +
        " and " +
        "firstname = " +
        firstname +
        " address = " +
        address)
    cursor = connection.cursor()
    cursor.execute(sql_call)
    id_val = cursor.fetchone()
    return id_val


def delete_employee(ssn):
    sql_call = str("Delete from employee Where ssn = " + ssn)
    cursor = connection.cursor()
    cursor.execute(sql_call)


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
        ssn,
        start_date,
        hourly_rate,
        role):

    # Update Person
    # Set PhoneNumber = 6314136666
    # Where SSN= 123456789

    cursor = connection.cursor()
    sql_call = str("update person  " + firstname + ", " +
                   lastname + "," + password + "," + gender + ", " + address +
                   "," + city + ", " + state + ", " + telephone + ")")
    cursor.execute(sql_call)

    sql_call = str(
        "Insert into employee Values (NULL, " +
        ssn +
        "," +
        start_date +
        ", " +
        hourly_rate +
        " , " +
        role +
        " )")
    cursor.execute(sql_call)


def obtain_sales_report_by_month(date):

    cursor = connection.cursor()
    # emp_id INT,
    # adv_id INT,
    sql_call = str(
        "SELECT  A.adv_id,  A.item_name , E.emp_id, " +
        "SUM(P.num_units) as TSaleOnItem, SUM(P.num_units * A.unit_price) " +
        " FROM employee E INNER JOIN buy P INNER JOIN advertisement A ON " +
        "P.adv_id =A.adv_id AND A.Employee = E.emp_id  " +
        "WHERE MONTH(P.Date) = " +
        date +
        " GROUP BY A.adv_id")
    cursor.execute(sql_call)
    val = cursor.fetchone()
    return val


def produce_list_of_all_items_advertised():
    cursor = connection.cursor()
    sql_call = str(
        "SELECT A.item_name,A.unit_price,A.num_aval_units FROM advertisement A")

    cursor.execute(sql_call)
    val = cursor.fetchone()
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
    val = cursor.fetchone()
    return val