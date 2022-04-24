from flask import Flask, request, session, redirect, jsonify
from DBconnection import Db
import random
import demjson


from email.mime import image
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
mymail="nuzairnuz141@gmail.com"
mypswd="virtualrealist1!2@3#"


app = Flask(__name__)


@app.route('/login', methods=['post'])
def login():
    db = Db()
    username = request.form['username']
    password = request.form['password']
    lati = request.form['lati']
    longi = request.form['longi']
    place = request.form['place']
    qry = "SELECT * FROM `login` WHERE `user_name`='" + username + "' AND `password`='" + password + "'"
    res = db.selectOne(qry)
    print(res)
    res1 = {}
    if res != None:
        type = res['type']
        id = res['login_id']
        if type == "admin":
            res1['status'] = "none"
            return demjson.encode(res1)
        elif type == "customer":

            q = "select * from location where id='" + str(id) + "'"
            r = db.selectOne(q)
            if r is not None:
                q1 = "update location set latitude='" + lati + "',longitude='" + longi + "',place='" + place + "' where id='" + str(
                    id) + "'"
                db.update(q1)
                # r1={}
                # r1['status'] = "ok"
                res1['status'] = "ok"
                res1['type1'] = type
                res1['id1'] = id
                return demjson.encode(res1)
                # return demjson.encode(r1)
            else:
                qry1 = "insert into location values('','" + lati + "','" + longi + "','" + place + "','" + str(
                    id) + "')"
                db.insert(qry1)
                r2 = {}
                r2['status'] = "ok"
                return demjson.encode(r2)
            return demjson.encode(res1)

        else:
            res1['status'] = 'none'
            return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route('/location', methods=['post'])
def location():
    db = Db()
    lid = request.form['lid']
    lati = request.form['lati']
    longi = request.form['longi']
    place = request.form['place']

    res1 = {}

    q = "select * from location where id='" + str(lid) + "'"
    r = db.selectOne(q)
    print(q,"q")
    if r is not None:
        q1 = "update location set latitude='" + lati + "',longitude='" + longi + "',place='" + place + "' where id='" + str(
            id) + "'"
        print("q1",q1)
        db.update(q1)
        # r1={}
        res1['status'] = "ok"

    else:
        qry1 = "insert into location values('','" + lati + "','" + longi + "','" + place + "','" + str(
            id) + "')"
        print(qry1)
        db.insert(qry1)
        res1['status'] = "ok"
    return demjson.encode(res1)

@app.route('/cust_register', methods=['post'])
def cust_register():
    db = Db()
    name = request.form['name']
    lati = request.form['lati']
    longi = request.form['longi']
    place = request.form['place']

    phone = request.form['phone']
    email = request.form['email']
    uname = request.form['username']
    password = request.form['password']
    cp = request.form['password1']
    import datetime
    img = request.files['pic']
    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    img.save(r"E:\final\Project\static\\" + date + ".jpg")
    path = "/static/" + date + ".jpg"
    res = db.selectOne("select * from login where user_name='" + uname + "'")
    res2 = {}
    if res is not None:
        res2['status'] = 'Already exist'
        return demjson.encode(res2)
    else:
        if password == cp:
            qry = "insert into login values('','" + uname + "','" + str(password) + "','customer')"
            res = db.insert(qry)
            qry1 = "insert into customer values('" + str(res) + "','" + name + "','" + str(path) + "','" + phone + "','" + email + "')"
            db.insert(qry1)
            qry2 = db.insert(
                "insert into location values('','" + lati + "','" + longi + "','" + place + "','" + str(res) + "')")
            res2['status'] = 'ok'
            return demjson.encode(res2)
        else:
            res2['status'] = 'none'
            return demjson.encode(res2)

@app.route('/feedback', methods=['get', 'post'])
def sendfeedback():
    db = Db()
    user_id = request.form['lid']
    feedback = request.form['feedback']
    sid = request.form['id']

    qry = "INSERT INTO feedback VALUES(NULL ,'" + feedback + "','" + user_id + "','" + sid + "',curdate(),'service_center')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'feedback send successfully'
    return demjson.encode(res1)


@app.route('/rating', methods=['get', 'post'])
def rating():
    db = Db()
    user_id = request.form['lid']
    rating = request.form['rating']
    id = request.form['id']

    qry = "INSERT INTO rating VALUES(NULL ,'" + rating + "','" + user_id + "','"+id+"',curdate(),'service_center')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'rating send successfully'
    return demjson.encode(res1)


@app.route('/view_reply', methods=['post'])
def view_reply():
    d = Db()
    lid = request.form['lid']
    id = request.form['id']

    qr = "SELECT * FROM complaint,service_center_info,customer WHERE complaint.customer_id='" + lid + "' and complaint.customer_id=customer.customer_id and complaint.w_sc_id=service_center_info.service_center_id and complaint.w_sc_id='"+id+"'"
    res = d.select(qr)
    print(res,lid,id)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        res1['lid'] = lid
        return demjson.encode(res1)

    else:
        res1['status'] = 'none'
        res1['lid'] = lid
        return demjson.encode(res1)
@app.route('/view_rating', methods=['post'])
def view_rating():
    d = Db()
    id = request.form['id']
    qr = "SELECT * FROM rating,customer,service_center_info WHERE rating.customer_id=customer.customer_id and rating.w_s_id=service_center_info.service_center_id and rating.w_s_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)
@app.route('/view_feed', methods=['post'])
def view_feed():
    d = Db()
    id = request.form['id']
    qr = "SELECT * FROM feedback,customer,service_center_info WHERE feedback.customer_id=customer.customer_id and feedback.w_s_id=service_center_info.service_center_id and feedback.w_s_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    res1['status'] = 'ok'
    res1['data'] = res
    return demjson.encode(res1)

@app.route('/view_sc', methods=['post'])
def view_sc():
    db = Db()
    lati = request.form['lati']
    print(lati)
    longi = request.form['longi']
    print(longi)
    place = request.form['place']
    qry = "select service_center_info.*,location.*, (3959 * ACOS ( COS ( RADIANS('" + str(
        lati) + "') ) * COS( RADIANS( location.latitude) ) * COS( RADIANS( location.longitude ) - RADIANS('" + str(
        longi) + "') ) + SIN ( RADIANS('" + str(
        lati) + "') ) * SIN( RADIANS( location.latitude ) ))) AS user_distance FROM location,service_center_info HAVING user_distance  < 1000.2137 and  service_center_info.service_center_id=location.id "
    # qry = "select * from driver,vehicle where driver.driver_id=vehicle.driver_id and driver.longitude LIKE and driver.longitude like '%longi%' and driver.place like '%place%'"
    # qry="SELECT driver_id, (6371 * ACOS (COS ( RADIANS(latitude) )* COS( RADIANS( lati ))* COS( RADIANS( longi ) - RADIANS($longitude) )+ SIN ( RADIANS(latitude) )* SIN( RADIANS( lati ) )) AS distance FROM driver HAVING distance < 30 ORDER BY distance LIMIT 0 , 20;"
    res = db.select(qry)
    print(res)

    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route('/view_sc_fun', methods=['post'])
def view_sc_fun():
    d = Db()
    id = request.form['id']
    qr = "SELECT * FROM service_center_info,service_function WHERE service_center_info.service_center_id=service_function.service_center_id and service_function.service_center_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    if qr is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route('/complaint', methods=['get', 'post'])
def complaint():
    db = Db()
    user_id = request.form['lid']
    id = request.form['id']

    complaint = request.form['complaint']
    qry = "INSERT INTO complaint VALUES(NULL ,'service_center','" + complaint + "','"+user_id+"','"+id+"',curdate(),'pending','pending')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'complaint Send successfully'
    return demjson.encode(res1)


@app.route('/Send_request', methods=['post'])
def help():
    db = Db()
    user_id = request.form['lid']
    did = request.form['id']
    latitude = request.form['lati']
    longitude = request.form['longi']
    place = request.form['place']
    qry = "insert into sc_request values('','" + user_id + "','" + did + "',curdate(),'pending')"
    res = db.insert(qry)
    # qry1 = "insert into user_location values('','" + user_id + "','" + latitude + "','" + longitude + "')"
    # res2 = db.insert(qry1)
    res1 = {}
    res1['status'] = 'ok'
    return demjson.encode(res1)


@app.route('/chat', methods=['post'])
def chat():
    db=Db()
    from_id=request.form['lid']
    to_id=request.form['toid']
    message=request.form['message']
    # /type=request.form['ty']
    qry="insert into chat values(null,'"+from_id+"','"+to_id+"','"+message+"',curdate(),'service_center')"
    res=db.insert(qry)
    res1={}
    if res is not None:
        res1['status']='ok'
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)




@app.route("/viw_chat_msg", methods=['post'])
def viw_chat_msg():
    db=Db()
    toid = request.form["toid"]
    fid = request.form["lid"]
    lmid = request.form["lastid"]
    print(lmid)
    # ty = request.form["ty"]

    qry = "select fid,msg,date,cid from chat where   chat.type='service_center' and cid>'" + str(lmid) + "' AND ((toid='" + str(toid) + "' and  fid='" + str(fid) + "' ) or (toid='" + str(fid) + "' and fid='" + str(toid) + "' )  )   order by cid asc"
    print(qry)
    res=db.select(qry)
    print(res)
    # con, cu = connection();
    # cu.execute(qry);
    # results = cu.fetchall();
    res1={}
    if res is not None:
        # row_headers = [x[0] for x in cu.description]
        # json_data = []
        # for result in results:
        #     json_data.append(dict(zip(row_headers, result)))
        # con.commit()
        # print(results, json_data)
        res1['status'] = 'ok'
        res1['data']=res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route("/and_send_msg", methods=['post'])
def and_send_msg():
    db = Db()
    from_id = request.form['lid']
    to_id = request.form['toid']
    message = request.form['message']
    # /type=request.form['ty']
    qry = "insert into chat values(null,'" + from_id + "','" + to_id + "','" + message + "',curdate(),'service_center')"
    res = db.insert(qry)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route("/and_send_msg1", methods=['post'])
def and_send_msg1():
    db = Db()
    from_id = request.form['lid']
    to_id = request.form['toid']
    message = request.form['message']
    # /type=request.form['ty']
    qry = "insert into chat values(null,'" + from_id + "','" + to_id + "','" + message + "',curdate(),'workshop')"
    res = db.insert(qry)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)
@app.route("/and_view_msg",methods=['post'])
def and_view_msg():
    db = Db()
    toid = request.form["toid"]
    fid = request.form["lid"]
    lmid = request.form["lastid"]
    print(lmid)
    # ty = request.form["ty"]

    qry = "select fid,msg,date,cid from chat where   chat.type='service_center' and cid>'" + str(
        lmid) + "' AND ((toid='" + str(toid) + "' and  fid='" + str(fid) + "' ) or (toid='" + str(
        fid) + "' and fid='" + str(toid) + "' )  )   order by cid asc"
    print(qry)
    res = db.select(qry)
    print(res)
    # con, cu = connection();
    # cu.execute(qry);
    # results = cu.fetchall();
    res1 = {}
    if res is not None:
        # row_headers = [x[0] for x in cu.description]
        # json_data = []
        # for result in results:
        #     json_data.append(dict(zip(row_headers, result)))
        # con.commit()
        # print(results, json_data)
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)

@app.route("/and_view_msg1",methods=['post'])
def and_view_msg1():
    db = Db()
    toid = request.form["toid"]
    fid = request.form["lid"]
    lmid = request.form["lastid"]
    print(lmid)
    # ty = request.form["ty"]

    qry = "select fid,msg,date,cid from chat where   chat.type='workshop' and cid>'" + str(
        lmid) + "' AND ((toid='" + str(toid) + "' and  fid='" + str(fid) + "' ) or (toid='" + str(
        fid) + "' and fid='" + str(toid) + "' )  )   order by cid asc"
    print(qry)
    res = db.select(qry)
    print(res)
    # con, cu = connection();
    # cu.execute(qry);
    # results = cu.fetchall();
    res1 = {}
    if res is not None:
        # row_headers = [x[0] for x in cu.description]
        # json_data = []
        # for result in results:
        #     json_data.append(dict(zip(row_headers, result)))
        # con.commit()
        # print(results, json_data)
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)


@app.route('/view_wc', methods=['post'])
def view_wc():
    db = Db()
    lati = request.form['lati']
    print(lati)
    longi = request.form['longi']
    print(longi)
    place = request.form['place']
    qry = "select workshop.*,location.*, (3959 * ACOS ( COS ( RADIANS('" + str(
        lati) + "') ) * COS( RADIANS( location.latitude) ) * COS( RADIANS( location.longitude ) - RADIANS('" + str(
        longi) + "') ) + SIN ( RADIANS('" + str(
        lati) + "') ) * SIN( RADIANS( location.latitude ) ))) AS user_distance FROM location,workshop HAVING user_distance  < 1000.2137 and  workshop.workshop_id=location.id "
    # qry = "select * from driver,vehicle where driver.driver_id=vehicle.driver_id and driver.longitude LIKE and driver.longitude like '%longi%' and driver.place like '%place%'"
    # qry="SELECT driver_id, (6371 * ACOS (COS ( RADIANS(latitude) )* COS( RADIANS( lati ))* COS( RADIANS( longi ) - RADIANS($longitude) )+ SIN ( RADIANS(latitude) )* SIN( RADIANS( lati ) )) AS distance FROM driver HAVING distance < 30 ORDER BY distance LIMIT 0 , 20;"
    res = db.select(qry)
    print(res)

    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)


@app.route('/Send_request_ws', methods=['post'])
def Send_request_ws():
    db = Db()
    user_id = request.form['lid']
    did = request.form['id']
    # latitude = request.form['lati']
    # longitude = request.form['longi']
    req = request.form['req']
    qry = "insert into workshop_request values('','"+req+"','" + user_id + "','" + did + "',curdate(),'pending')"
    res = db.insert(qry)
    # qry1 = "insert into user_location values('','" + user_id + "','" + latitude + "','" + longitude + "')"
    # res2 = db.insert(qry1)
    res1 = {}
    res1['status'] = 'ok'
    return demjson.encode(res1)

@app.route('/feedback_ws', methods=['get', 'post'])
def feedback_ws():
    db = Db()
    user_id = request.form['lid']
    feedback = request.form['feedback']
    sid = request.form['id']

    qry = "INSERT INTO feedback VALUES(NULL ,'" + feedback + "','" + user_id + "','" + sid + "',curdate(),'workshop')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'feedback send successfully'
    return demjson.encode(res1)

@app.route('/view_feed_ws', methods=['post'])
def view_feed_ws():
    d = Db()
    id = request.form['id']
    qr = "SELECT * FROM feedback,customer,workshop WHERE feedback.customer_id=customer.customer_id and feedback.w_s_id=workshop.workshop_id and feedback.w_s_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    res1['status'] = 'ok'
    res1['data'] = res
    return demjson.encode(res1)



@app.route('/rating_ws', methods=['get', 'post'])
def rating_ws():
    db = Db()
    user_id = request.form['lid']
    rating = request.form['rating']
    id = request.form['id']

    qry = "INSERT INTO rating VALUES(NULL ,'" + rating + "','" + user_id + "','"+id+"',curdate(),'workshop')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'rating send successfully'
    return demjson.encode(res1)
@app.route('/view_rating_ws', methods=['post'])
def view_rating_ws():
    d = Db()
    id = request.form['id']
    qr = "SELECT * FROM rating,customer,workshop WHERE rating.customer_id=customer.customer_id and rating.w_s_id=workshop.workshop_id and rating.w_s_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        return demjson.encode(res1)
    else:
        res1['status'] = 'none'
        return demjson.encode(res1)


@app.route('/complaint_ws', methods=['get', 'post'])
def complaint_ws():
    db = Db()
    user_id = request.form['lid']
    id = request.form['id']

    complaint = request.form['complaint']
    qry = "INSERT INTO complaint VALUES(NULL ,'workshop','" + complaint + "','"+user_id+"','"+id+"',curdate(),'pending','pending')"
    res = db.insert(qry)
    res1 = {}
    res1['status'] = 'complaint Send successfully'
    return demjson.encode(res1)

@app.route('/view_reply_ws', methods=['post'])
def view_reply_ws():
    d = Db()
    lid = request.form['lid']
    id = request.form['id']

    qr = "SELECT * FROM complaint,workshop,customer WHERE complaint.customer_id='" + lid + "' and complaint.customer_id=customer.customer_id and complaint.w_sc_id=workshop.workshop_id and complaint.w_sc_id='"+id+"'"
    res = d.select(qr)
    print(res)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        res1['lid'] = lid
        return demjson.encode(res1)

    else:
        res1['status'] = 'none'
        res1['lid'] = lid
        return demjson.encode(res1)


@app.route('/status_ws', methods=['post'])
def status_ws():
    d = Db()
    lid = request.form['lid']
    id = request.form['id']

    qr = "SELECT * FROM workshop_request,workshop,customer WHERE workshop_request.customer_id='" + lid + "' and workshop_request.customer_id=customer.customer_id and workshop_request.workshop_id=workshop.workshop_id "
    res = d.select(qr)
    print(res)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        res1['lid'] = lid
        return demjson.encode(res1)

    else:
        res1['status'] = 'none'
        res1['lid'] = lid
        return demjson.encode(res1)

@app.route('/status_ss', methods=['post'])
def status_ss():
    d = Db()
    lid = request.form['lid']
    id = request.form['id']

    qr = "SELECT * FROM sc_request,service_center_info,customer,service_function WHERE sc_request.customer_id='" + lid + "' and sc_request.customer_id=customer.customer_id and sc_request.service_fun_id=service_function.service_fun_id and service_center_info.service_center_id=service_function.service_center_id "
    res = d.select(qr)
    print(res)
    res1 = {}
    if res is not None:
        res1['status'] = 'ok'
        res1['data'] = res
        res1['lid'] = lid
        return demjson.encode(res1)

    else:
        res1['status'] = 'none'
        return demjson.encode(res1)


# @app.route('/paymentdonee', methods=['post'])
# def paymentdonee():
#     db=Db()
#     # lid=request.form['lid']
#     id=request.form['id']
#     amount = request.form['amount']
#     qr="update payment set amount='"+amount+"', p_status='paid', date=curdate() where id='"+str(id)+"'"
#     res=db.update(qr)
#     hqr="update workshop_request set status='paid' where request_id='"+str(id)+"'"
#     rens=db.update(hqr)
#     # qr2="insert into payment VALUES ('','"+id+"','"+amount+"','paid',curdate())"
#     # res2=db.insert(qr2)
#     res1={}
#     res1['status']='ok'
#     return demjson.encode(res1)




@app.route('/paymentdone', methods=['post'])
def paymentdone():
    db=Db()
    rid=request.form['rid']
    id=request.form['lid']
    amount = request.form['amount']
    qr="update payment set amount='"+amount+"', p_status='paid', date=curdate() where id='"+str(rid)+"'"
    res=db.update(qr)
    hqr = "update workshop_request set status='paid' where request_id='" + str(rid) + "'"
    rens = db.update(hqr)
    res1={}
    res1['status']='ok'
    return demjson.encode(res1)






@app.route('/add_chat',methods=['post'])
def add_chat():
    db=Db()
    lid = request.form['lid']
    toid = request.form['toid']
    message = request.form['message']
    q2="insert into chat values('','"+lid+"','"+toid+"','"+message+"',curdate(),'workshop')"
    res = db.insert(q2)
    res1 = {}
    res1['status'] = "Inserted"
    return demjson.encode(res1)

@app.route('/view_chat',methods=['post'])
def view_chat():
    db=Db()
    lid = request.form['lid']
    toid = request.form['toid']
    lastid = request.form['lastid']
    print(lid,toid,lastid)
    q2="select chat.* from chat where cid>'"+lastid+"' and ((fid='"+lid+"' and toid='"+toid+"') or (fid='"+toid+"' and toid='"+lid+"' and type='workshop'))"
    res = db.select(q2)
    print(res)
    res1 = {}
    res1['status'] = "ok"
    res1['data'] = res
    return demjson.encode(res1)

@app.route('/add_chat1',methods=['post'])
def add_chat1():
    db=Db()
    lid = request.form['lid']
    toid = request.form['toid']
    message = request.form['message']
    q2="insert into chat values('','"+lid+"','"+toid+"','"+message+"',curdate(),'service_center')"
    res = db.insert(q2)
    res1 = {}
    res1['status'] = "Inserted"
    return demjson.encode(res1)

@app.route('/view_chat1',methods=['post'])
def view_chat1():
    db=Db()
    lid = request.form['lid']
    toid = request.form['toid']
    lastid = request.form['lastid']
    print(lid,toid,lastid)
    q2="select chat.* from chat where cid>'"+lastid+"' and ((fid='"+lid+"' and toid='"+toid+"') or (fid='"+toid+"' and toid='"+lid+"' and type='service_center'))"
    res = db.select(q2)
    print(res)
    res1 = {}
    res1['status'] = "ok"
    res1['data'] = res
    return demjson.encode(res1)
# @app.route('/view_staff',methods=['post'])
# def view_chatcouncillor():
#     lid = request.form['lid']
#     print(lid)
#     qry = db.selectOne("select * from student,course where student.stud_course_id=course.course_id and student.stud_id='" + str(lid) + "'")
#     print(qry)
#     cid = qry['stud_course_id']
#     y = qry['batch']
#     q = db.select("select * from subect_alloc,staff,subject,suballoctocourse where  suballoctocourse.suballoccourseid=subect_alloc.csuballocid and suballoctocourse.ssubid=subject.sub_id and staff.Staff_id=subect_alloc.staff_name and suballoctocourse.scid='"+str(cid)+"' group by staff.Staff_id ")
#     # print(q, cid)
#     res1 = {}
#     res1['status'] = "ok"
#     res1['data'] = q
#     return demjson.encode(res1)


@app.route('/forget_pswd1',methods=['post'])
def forget_pswd1():
    db = Db()
    mail=request.form['email']
    qry=db.selectOne("select * from login where user_name='"+mail+"'")
    res=qry['password']
    print(res)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login(mymail, mypswd)

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText("Your Password is " + str(res))

    msg['Subject'] = 'Verification'

    msg['To'] = mail

    msg['From'] = mymail

    try:
        gmail.send_message(msg)
        res1 = {}
        res1['status'] = "ok"
        return demjson.encode(res1)

    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
        res1 = {}
        res1['status'] = "none"
        return demjson.encode(res1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
