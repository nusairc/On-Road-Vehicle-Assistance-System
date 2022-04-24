import demjson
from flask import Flask, render_template, request, redirect, session
from DBconnection import Db
app = Flask(__name__)

from email.mime import image
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
mymail="nuzairnuz141@gmail.com"
mypswd="virtualrealist1!2@3#"

app.secret_key="key"

@app.route('/')
def start():
    return render_template('home.html')

@app.route('/log')
def login():
    return render_template('loginindex.html')

@app.route('/logout')
def logout():
    session.clear
    session['lg']=""
    return render_template('loginindex.html')

@app.route('/login1',methods=['post'])
def login1():
    db=Db()
    user=request.form['textfield']
    passwrd=request.form['textfield2']
    qry=db.selectOne("select * from login where user_name='"+user+"' and password='"+passwrd+"'")
    if qry:
        typ=qry['type']
        session['lg']='ln'
        if typ=="admin":
            return redirect("/adminhome")
        elif typ=="workshop":
            session['login_id']=qry['login_id']
            return redirect("/workshophome")

        elif typ=="service_center":
            session['login_id']=qry['login_id']
            return redirect("/service_centerhome")

        else:
            return 'ok'
    return 'invalid user'


@app.route('/forget_pswd')
def forget_pswd():
    return render_template("forget_password.html")

@app.route('/forget_pswd1',methods=['post'])
def forget_pswd1():
    db = Db()
    mail=request.form['textfield']
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

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))

    return '''<script>alert("Email sent");window.location="/log"</script>'''


@app.route('/adminhome')
def adminhome():
    if session['lg']=='ln':
        return render_template("ADMIN/admin_home.html")
    else:
        return render_template('loginindex.html')


@app.route('/viewwrkshp')
def viewwrkshp():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.select("select * from workshop,login where login.login_id=workshop.workshop_id and login.type='pending'")
        return render_template("ADMIN/approve_workshop.html",data=qry)
    else:
        return render_template('loginindex.html')

@app.route('/workshop_approve/<id>')
def workshop_approve(id):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.update("update login set type='workshop' where login_id='"+id+"'")
        q=db.insert("insert into payment values('','"+id+"','','pending',curdate())")

        return '''<script>alert("approved");window.location="/viewwrkshp"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/workshop_reject/<id>')
def workshop_reject(id):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.update("update login set type='Rejected' where login_id='"+id+"'")
        return '''<script>alert("rejected");window.location="/viewwrkshp"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/view_apprved_wrkshp')
def view_apprved_wrkshp():
    if session['lg'] == 'ln':

        db=Db()
        qry=db.select("select * from workshop,login where login.login_id=workshop.workshop_id and login.type='workshop'")
        return render_template("ADMIN/view_approved_workshop.html",data=qry)
    else:
        return render_template('loginindex.html')
@app.route('/set_location/<id>')
def set_location(id):
    if session['lg'] == 'ln':
        db=Db()
        return render_template("ADMIN/loccation.html",d=id)
    else:
        return render_template('loginindex.html')
@app.route('/set_location1/<id>',methods=['post'])
def set_location1(id):
    if session['lg'] == 'ln':
        db=Db()
        lat=request.form['textfield']
        long=request.form['textfield2']
        p=request.form['p']
        q=db.insert("insert into location values('','"+long+"','"+lat+"','"+p+"','"+id+"')")
        return render_template("ADMIN/loccation.html")
    else:
        return render_template('loginindex.html')

@app.route('/manage_complaint')
def manage_complaint():
    if session['lg'] == 'ln':
        return render_template("ADMIN/Manage_complaint.html")
    else:
        return render_template('loginindex.html')

@app.route('/manage_complaint1',methods=['post'])
def manage_complaint1():
    if session['lg'] == 'ln':
        db=Db()
        sub=request.form['ch']
        if sub=="workshop":
            qry=db.select("select * from complaint,customer,workshop where complaint.customer_id=customer.customer_id and complaint.w_sc_id=workshop.workshop_id and complaint.subject='"+sub+"'")
            return render_template("ADMIN/Manage_complaint.html",data=qry)
        else:
            qry = db.select("select * from complaint,customer,service_center_info where complaint.customer_id=customer.customer_id and complaint.w_sc_id=service_center_info.service_center_id and complaint.subject='" + sub + "'")
            return render_template("ADMIN/Manage_complaint.html", data1=qry)
    else:
        return render_template('loginindex.html')


@app.route('/reply/<id>')
def reply(id):
    if session['lg'] == 'ln':
        return render_template("ADMIN/reply_complaint.html", cid=id)
    else:
        return render_template('loginindex.html')


@app.route('/reply1/<id>',methods=['post'])
def reply1(id):
    if session['lg'] == 'ln':
        db=Db()
        re=request.form['re']
        qry=db.update("update complaint set reply='"+re+"',reply_date=curdate() where complaint_id='"+id+"'")
        return '''<script>alert("reply sent");window.location="/manage_complaint"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/manage_rating')
def manage_rating():
    if session['lg'] == 'ln':
        return render_template("ADMIN/rating.html")
    else:
        return render_template('loginindex.html')

@app.route('/view_rating',methods=['post'])
def view_rating():
    if session['lg'] == 'ln':
        db = Db()
        sub = request.form['ch']
        if sub == "workshop":
            qry = db.select(
                "select * from rating,customer,workshop where rating.customer_id=customer.customer_id and rating.w_s_id=workshop.workshop_id and rating.subject='" + sub + "'")
            return render_template("ADMIN/rating.html", data=qry)
        else:
            qry1 = db.select("select * from rating,customer,service_center_info where rating.customer_id=customer.customer_id and rating.w_s_id=service_center_info.service_center_id and rating.subject='" +  sub + "'")

        return render_template("ADMIN/rating.html",data1=qry1)
    else:
        return render_template('loginindex.html')


@app.route('/manage_feedback')
def manage_feedback():
    if session['lg'] == 'ln':
        return render_template("ADMIN/feedback.html")
    else:
        return render_template('loginindex.html')


@app.route('/view_feedback',methods=['post'])
def view_feedback():
    if session['lg'] == 'ln':
        db = Db()
        sub = request.form['ch']
        if sub == "workshop":
            qry = db.select(
                "select * from feedback,customer,workshop where feedback.customer_id=customer.customer_id and feedback.w_s_id=workshop.workshop_id and feedback.subject='" + sub + "'")
            return render_template("ADMIN/feedback.html", data=qry)
        else:
            qry1 = db.select(
                "select * from feedback,customer,service_center_info where feedback.customer_id=customer.customer_id and feedback.w_s_id=service_center_info.service_center_id and feedback.subject='" +  sub + "'")

            return render_template("ADMIN/feedback.html",data1=qry1)
    else:
        return render_template('loginindex.html')

@app.route('/manage_service_center_admin')
def manage_service_center_admin():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.select("select * from service_center_info,login where login.login_id=service_center_info.service_center_id and login.type='pending'")
        return render_template("ADMIN/approve_reject_servicecenter.html",data=qry)
    else:
        return render_template('loginindex.html')
@app.route('/viewservicefun')
def viewservicefun():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.select("select * from service_center_info,service_function where service_function.service_center_id=service_center_info.service_center_id and service_function.service_center_id='"+str(session['login_id'])+"'")
        return render_template("service center/view_service.html",data=qry)
    else:
        return render_template('loginindex.html')

@app.route('/delete_serv/<fid>')
def delete_serv(fid):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.delete("delete from service_function where service_fun_id='"+fid+"'")
        return '''<script>alert("Deleted");window.location="/viewservicefun"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/view_service_center')
def view_service_center():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.select("select * from service_center_info,login where login.login_id=service_center_info.service_center_id and login.type='service_center'")
        return render_template("ADMIN/approved_reject_servicecenter.html",data=qry)

    else:
        return render_template('loginindex.html')
@app.route('/service_center_approve/<id>')
def service_center_approve(id):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.update("update login set type='service_center' where login_id='"+id+"'")
        return '''<script>alert("approved");window.location="/manage_service_center_admin"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/service_center_reject/<id>')
def service_center_reject(id):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.update("update login set type='Rejected' where login_id='"+id+"'")
        return '''<script>alert("rejected");window.location="/manage_service_center_admin"</script>'''
    else:
        return render_template('loginindex.html')
@app.route('/set_location11/<id>')
def set_location11(id):
    if session['lg'] == 'ln':
        db=Db()
        return render_template("ADMIN/location.html",d=id)
    else:
        return render_template('loginindex.html')
@app.route('/set_location111/<id>',methods=['post'])
def set_location111(id):
    if session['lg'] == 'ln':
        db=Db()
        lat=request.form['textfield']
        long=request.form['textfield2']
        p=request.form['p']
        q=db.insert("insert into location values('','"+long+"','"+lat+"','"+p+"','"+id+"')")
        return render_template("ADMIN/location.html")
    else:
        return render_template('loginindex.html')

@app.route('/view_customer')
def view_customer():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.select("select * from customer")
        return render_template("ADMIN/customer.html",data=qry)
    else:
        return render_template('loginindex.html')


#############################################################





@app.route('/workshophome')
def workshophome():
    if session['lg'] == 'ln':
        return render_template("workshop/ws_home.html")
    else:
        return render_template('loginindex.html')


@app.route('/manage_worker_details')
def manage_worker_details():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from mechanic_info where workshop_id='"+str(session['login_id'])+"'"
        res=db.select(qry)
        return render_template("workshop/view_workers.html",data=res)
    else:
        return render_template('loginindex.html')

@app.route('/add_worker_details')
def add_worker_details():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from workshop"
        res=db.select(qry)
        return render_template("workshop/Worker_details(workshop).html",data=res)
    else:
        return render_template('loginindex.html')

@app.route('/add_worker_details1',methods=['post'])
def add_worker_details1():
    if session['lg'] == 'ln':
        db=Db()
        mec_name=request.form['textfield']
        place=request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        state= request.form['select']
        district = request.form['textfield5']
        email = request.form['textfield6']
        contact = request.form['textfield7']
        specification = request.form['select2']
        type = request.form['select3']
        # workshop=request.form['select5']
        qry="insert into mechanic_info values('','"+mec_name+"','"+str(session['login_id'])+"','"+place+"','"+post+"','"+pin+"','"+district+"','"+state+"','"+contact+"','"+email+"','"+specification+"','"+type+"')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/workshophome"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/edit_worker/<id>')
def edit_worker(id):
    if session['lg'] == 'ln':
        db=Db()
        qry = "select * from workshop"
        result = db.select(qry)
        qry="select * from mechanic_info where mechanic_id='"+id+"'"
        res=db.selectOne(qry)
        return render_template("workshop/edit_worker.html",data=res,d=result)
    else:
        return render_template('loginindex.html')

@app.route('/edit_worker1/<id>',methods=['post'])
def edit_worker1(id):
    if session['lg'] == 'ln':
        db=Db()
        mec_name = request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        state = request.form['select']
        district = request.form['textfield5']
        email = request.form['textfield6']
        contact = request.form['textfield7']
        specification = request.form['select2']
        type = request.form['select3']
        workshop = request.form['select5']
        qry="update mechanic_info set mechanic_name='"+mec_name+"',workshop_id='"+workshop+"',place='"+place+"',post='"+post+"',pin='"+pin+"',district='"+district+"',state='"+state+"',contact_no='"+contact+"',email_id='"+email+"',specification='"+specification+"',type='"+type+"' where mechanic_id='"+id+"'"
        db.update(qry)
        return '''<script>alert("success");window.location="/manage_worker_details"</script>'''
    else:
        return render_template('loginindex.html')
@app.route('/delete_worker1/<id>',)
def delete_worker1(id):
    if session['lg'] == 'ln':

        db=Db()
        qry="delete from mechanic_info where mechanic_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/manage_worker_details"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/manage_crane_deatils')
def manage_crane_details():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from workshop"
        res=db.select(qry)
        return render_template("ADMIN/Crane.html",d=res)
    else:
        return render_template('loginindex.html')

@app.route('/manage_crane_deatils1',methods=['post'])
def manage_crane_details1():
    if session['lg'] == 'ln':
        db=Db()
        owner=request.form['textfield']
        crane=request.form['textfield2']
        # workshop=request.form['select']
        qry="insert into crane values('','"+str(session['login_id'])+"','"+owner+"','"+crane+"')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/workshophome"</script>'''
    else:
        return render_template('loginindex.html')
@app.route('/view_crane_deatils')
def view_crane_deatils():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from crane where workshop_id='"+str(session['login_id'])+"'"
        res=db.select(qry)
        return render_template("workshop/view_crane.html",d=res)
    else:
        return render_template('loginindex.html')

@app.route('/delete_crane/<id>')
def delete_crane(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from crane where crane_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_crane_deatils"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/manage_spare_info')
def manage_spare_info():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from workshop"
        res=db.select(qry)
        return render_template("workshop/Spare_info.html",d=res)
    else:
        return render_template('loginindex.html')

@app.route('/manage_spare_info1',methods=['post'])
def manage_spare_info1():
    if session['lg'] == 'ln':
        db=Db()
        spare=request.form['textfield2']
        # workshop=request.form['select']
        qry="insert into spare_info values('','"+spare+"','"+str(session['login_id'])+"')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/workshophome"</script>'''

    else:
        return render_template('loginindex.html')
@app.route('/view_spare_deatils')
def view_spare_deatils():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from spare_info where workshop_id='"+str(session['login_id'])+"'"
        res=db.select(qry)
        return render_template("workshop/spare.html",d=res)
    else:
        return render_template('loginindex.html')

@app.route('/delete_spare/<id>')
def delete_spare(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from spare_info where spare_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_spare_deatils"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/manage_account')
def manage_account():
    if session['lg'] == 'ln':
        return render_template("ADMIN/Manage_account.html")
    else:
        return render_template('loginindex.html')
@app.route('/manage_account1',methods=['post'])
def manage_account1():
    if session['lg'] == 'ln':
        db=Db()
        acno=request.form['textfield']
        name=request.form['textfield2']
        ifsc=request.form['textfield3']
        vali=request.form['textfield4']
        qr=db.insert("insert into account_info values('','"+acno+"','"+name+"','"+ifsc+"','"+vali+"','"+str(session['login_id'])+"')")
        return render_template("ADMIN/Manage_account.html")
    else:
        return render_template('loginindex.html')

@app.route('/view_account')
def view_account():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from account_info where account_holder_id='"+str(session['login_id'])+"'"
        res=db.select(qry)
        return render_template("workshop/view_acco.html",d=res)
    else:
        return render_template('loginindex.html')


@app.route('/delete_account/<id>')
def delete_account(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from account_info where account_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_account"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/request1')
def request1():
    if session['lg'] == 'ln':
        db=Db()
        qry="select * from workshop_request,customer,workshop,location where workshop_request.customer_id=customer.customer_id and workshop.workshop_id=workshop_request.workshop_id and workshop_request.workshop_id='"+str(session['login_id'])+"' and customer.customer_id=location.id"
        res=db.select(qry)
        return render_template("workshop/Request(WORK) .html",data=res)
    else:
        return render_template('loginindex.html')
@app.route('/approve_request/<id>')
def approve_request(id):
    if session['lg'] == 'ln':
        db = Db()
        qry=db.update("update workshop_request set  status='approved' where request_id='"+id+"'" )
        q=db.insert("insert into payment values('','"+id+"','','pending',curdate())")
        return '''<script>alert("success");window.location="/request1"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/view_payment/<id>')
def view_payment(id):
    if session['lg'] == 'ln':
        db = Db()
        qry = db.selectOne("select * from workshop_request,payment where payment.id='" + id + "' and workshop_request.request_id=payment.id")
        res = db.select(qry)
        return render_template("workshop/payment.html", data=res)
    else:
        return render_template('loginindex.html')


@app.route('/reject_request/<id>')
def reject_request(id):
    if session['lg'] == 'ln':
        db = Db()
        qry=db.update("update workshop_request set  status='rejected' where request_id='"+id+"'" )
        return '''<script>alert("success");window.location="/request1"</script>'''
    else:
        return render_template('loginindex.html')



@app.route('/rating')
def rating():
    if session['lg'] == 'ln':
         return render_template("workshop/view_rating.html")
    else:
            return render_template('loginindex.html')


@app.route('/workshop_view_rating')
def workshop_view_rating():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.select("select * from rating,customer,workshop where rating.customer_id=customer.customer_id and rating.w_s_id=workshop.workshop_id and rating.w_s_id='"+str(session['login_id'])+"'")
        return render_template("workshop/view_rating.html", data=qry)
    else:
            return render_template('loginindex.html')


@app.route('/vprofile')
def vprofile():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.selectOne("select * from workshop,login where workshop.workshop_id='" + str(session['login_id']) + "' and workshop.workshop_id=login.login_id and login.type='workshop'")
        # res = db.select(qry)
        return render_template("workshop/wsprofile.html", data=qry)
    else:
        return render_template('loginindex.html')


@app.route('/view_feedback1')
def view_feedback1():
    if session['lg'] == 'ln':
        db=Db()
        q=db.select("select * from feedback,workshop,customer where customer.customer_id=feedback.customer_id and feedback.w_s_id=workshop.workshop_id and feedback.w_s_id='"+str(session['login_id'])+"' and feedback.subject='workshop'")
        return render_template("workshop/feedback(service).html",data=q)
    else:
        return render_template('loginindex.html')

###################################################################################################



@app.route('/service_centerhome')
def service_centerhome():
    if session['lg'] == 'ln':
        return render_template("service center/ss_home.html")
    else:
        return render_template('loginindex.html')


@app.route('/edit_profile')
def edit_profile():
    if session['lg'] == 'ln':
        db=Db()
        qry=db.selectOne("select * from service_center_info where service_center_id='"+str(session['login_id'])+"'")
        return render_template("service center/Service_Center_details(edit).html",data=qry )
    else:
        return render_template('loginindex.html')

@app.route('/edit_profile11',methods=['post'])
def edit_profile11():
    if session['lg'] == 'ln':
        db = Db()
        scenter = request.form['textfield']
        place = request.form['textfield2']
        post = request.form['textfield3']
        pin = request.form['textfield4']
        state = request.form['select']
        district = request.form['textfield5']
        email = request.form['textfield6']
        contact = request.form['textfield7']
        license = request.form['textfield8']
        qry="update service_center_info set service_center_name='"+scenter+"',place='"+place+"',post='"+post+"',pincode='"+pin+"',district='"+district+"',state='"+state+"',contact_no='"+contact+"',email_id='"+email+"',license_no='"+license+"' where service_center_id='"+str(session['login_id'])+"'"
        db.update(qry)
        return '''<script>alert("success");window.location="/edit_profile"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/manage_service_function')
def manage_service_function():
    if session['lg'] == 'ln':
        return render_template("service center/service-function.html")
    else:
        return render_template('loginindex.html')
@app.route('/manage_service_function1',methods=['post'])
def manage_service_function1():
    if session['lg'] == 'ln':
        db=Db()
        fun=request.form['textarea']
        qry="insert into service_function values('','"+str(session['login_id'])+"','"+fun+"')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/manage_service_function"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/update_status')
def update_status():
    if session['lg'] == 'ln':
        return render_template("service center/updatestatus.html")
    else:
        return render_template('loginindex.html')

@app.route('/view_request')
def view_request():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.select("select * from sc_request,service_function ,customer,location where sc_request.customer_id=customer.customer_id and sc_request.service_fun_id=service_function.service_fun_id and service_function.service_center_id='"+str(session['login_id'])+"' and customer.customer_id=location.id")
        return render_template("service center/updatestatus.html",data=qry)
    else:
        return render_template('loginindex.html')


@app.route('/update_status1/<id>')
def update_status1(id):
    if session['lg'] == 'ln':
        db = Db()
        qry=db.update("update sc_request set  status='approved' where request_id='"+id+"'" )
        q=db.insert("insert into payment values('','"+id+"','','pending',curdate())")
        return '''<script>alert("success");window.location="/view_request"</script>'''
    else:
        return render_template('loginindex.html')



@app.route('/update_status2/<id>')
def update_status2(id):
    if session['lg'] == 'ln':
        db = Db()
        qry=db.update("update sc_request set  status='rejected' where request_id='"+id+"'" )
        return '''<script>alert("success");window.location="/view_request"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/view_payment1/<id>')
def view_payment1(id):
    if session['lg'] == 'ln':
        db = Db()
        qry = db.selectOne("select * from sc_request,payment where payment.id='" + id + "' and workshop_request.request_id=payment.id")
        res = db.select(qry)
        return render_template("workshop/payment.html", data=res)
    else:
        return render_template('loginindex.html')



@app.route('/manage_offers')
def manage_offers():
    if session['lg'] == 'ln':
        return render_template("service center/offer.html")
    else:
        return render_template('loginindex.html')


@app.route('/manage_offers1',methods=['post'])
def manage_offers1():
    if session['lg'] == 'ln':
        db = Db()
        fun = request.form['textarea']
        qry = "insert into offer_info values('','" + fun + "',curdate(),'" + str(session['login_id']) + "')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/service_centerhome"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/view_offers')
def view_offers():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.select("select * from offer_info where offer_info.service_center_id ='"+str(session['login_id'])+"' ")
        return render_template("service center/offer(view).html",data=qry)
    else:
        return render_template('loginindex.html')
# @app.route('/edit_offers')
# def edit_offers():
#     db = Db()
#     qry = db.select("select * from offer_info where offer_info.service_center_id ='"+str(session['login_id'])+"' ")
#     return render_template("service center/offer(view).html",data=qry)
#


@app.route('/delete_offers1/<id>')
def delete_offers1(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from offer_info where offer_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_offers"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/manage_employee')
def manage_employee():
    if session['lg'] == 'ln':
        return render_template("service center/employee(service)1.html")
    else:
        return render_template('loginindex.html')


@app.route('/manage_employee1',methods=['post'])
def manage_employee1():
    if session['lg'] == 'ln':
        db = Db()
        emp_no =request.form['textfield']
        emp_name = request.form['textfield2']
        desig=request.form['textfield3']
        contact=request.form['textfield4']
        photo=request.files['textfield5']
        email=request.form['textfield6']
        import datetime
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(r"E:\final\Project\static\images\\" + date + '.jpg')
        path="/static/images/"+ date +".jpg"
        qry = "insert into employee values('','" +emp_no  + "','"+emp_name+"','"+desig+"','"+contact+"','"+str(path)+"','"+email+"','" + str(session['login_id']) + "')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/service_centerhome"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/view_employee')
def view_employee():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.select("select * from employee where service_center_id='"+str(session['login_id'])+"'")
        return render_template("service center/emlpoyee(editdel).html",data=qry)
    else:
        return render_template('loginindex.html')




@app.route('/delete_employee1/<id>')
def delete_employee1(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from employee where employee__id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_employee"</script>'''
    else:
        return render_template('loginindex.html')
@app.route('/edit_employee/<id>')
def edit_employee(id):
    if session['lg'] == 'ln':
        db=Db()
        q=db.selectOne("select * from employee where employee__id='"+id+"'")
        return render_template("service center/employee_edit.html",data=q)
    else:
        return render_template('loginindex.html')


@app.route('/edit_employee1/<id>',methods=['post'])
def edit_employee1(id):
    if session['lg'] == 'ln':
        db = Db()
        emp_no =request.form['textfield']
        emp_name = request.form['textfield2']
        desig=request.form['textfield3']
        contact=request.form['textfield4']
        photo=request.files['textfield5']
        email=request.form['textfield6']
        if request.files is not None:
            if photo.filename!="":
                import datetime
                date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                photo.save(r"E:\final\Project\static\images\\" + date + '.jpg')
                path="/static/images/"+ date +".jpg"
                qry = "update employee set employee_no='" +emp_no  + "',employee_name='"+emp_name+"',designation='"+desig+"',contact_no='"+contact+"',photo='"+str(path)+"',email_id='"+email+"' where employee__id='"+id+"'"
                db.update(qry)
                return '''<script>alert("success");window.location="/view_employee"</script>'''
            else:
                qry = "update employee set employee_no='" + emp_no + "',employee_name='" + emp_name + "',designation='" + desig + "',contact_no='" + contact + "',email_id='" + email + "' where employee__id='" + id + "'"
                db.update(qry)
                return '''<script>alert("success");window.location="/view_employee"</script>'''
        else:
            qry = "update employee set employee_no='" + emp_no + "',employee_name='" + emp_name + "',designation='" + desig + "',contact_no='" + contact + "',email_id='" + email + "' where employee__id='" + id + "'"
            db.update(qry)
            return '''<script>alert("success");window.location="/view_employee"</script>'''
    else:
        return render_template('loginindex.html')

@app.route('/view_feedback11')
def view_feedback11():
    if session['lg'] == 'ln':
        db=Db()
        q=db.select("select * from feedback,service_center_info,customer where customer.customer_id=feedback.customer_id and feedback.w_s_id=service_center_info.service_center_id and feedback.w_s_id='"+str(session['login_id'])+"' and feedback.subject='service_center'")
        return render_template("service center/feedback(service).html",data=q)
    else:
        return render_template('loginindex.html')

@app.route('/view_rating1')
def view_rating11():
    if session['lg'] == 'ln':
        db = Db()
        q = db.select(
            "select * from rating,service_center_info,customer where rating.w_s_id=service_center_info.service_center_id and rating.w_s_id='" + str(
                session['login_id']) + "' and rating.subject='service_center' and customer.customer_id=rating.customer_id")

        return render_template("service center/rating.html",data=q)
    else:
        return render_template('loginindex.html')
@app.route('/manage_worker')
def manage_worker():
    if session['lg'] == 'ln':
        return render_template("service center/worker(service).html")
    else:
        return render_template('loginindex.html')

@app.route('/manage_worker1',methods=['post'])
def manage_worker1():
    if session['lg'] == 'ln':
        db = Db()
        # w_no = request.form['textfield']
        w_name = request.form['textfield2']
        dept = request.form['textfield3']
        contact = request.form['textfield4']
        photo = request.files['textfield5']
        email = request.form['textfield6']
        import datetime
        date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        photo.save(r"E:\final\Project\static\images\\" + date + '.jpg')
        path = "/static/images/" + date + ".jpg"
        qry = "insert into worker values('','" + w_name + "','"+dept+"','"+email+"','"+contact+"','"+str(path)+"','" + str(session['login_id']) + "')"
        db.insert(qry)
        return '''<script>alert("success");window.location="/service_centerhome"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/view_worker')
def view_worker():
    if session['lg'] == 'ln':
        db = Db()
        qry = db.select("select * from worker where worker.service_center_id='"+str(session['login_id'])+"'")
        return render_template("service center/worker(editdel).html",data=qry)
    else:
        return render_template('loginindex.html')


#
#

@app.route('/delete_worker11/<id>')
def delete_worker11(id):
    if session['lg'] == 'ln':
        db=Db()
        qry="delete from worker where worker_id='"+id+"'"
        db.delete(qry)
        return '''<script>alert("success");window.location="/view_worker"</script>'''
    else:
        return render_template('loginindex.html')
@app.route('/edit_worker111/<id>')
def edit_worker111(id):
    if session['lg'] == 'ln':
        db=Db()
        qry=db.selectOne("select * from worker where worker_id='"+id+"'")
        return render_template("service center/edit_worker.html",data=qry)
    else:
        return render_template('loginindex.html')

@app.route('/edit_worker11/<id>',methods=['post'])
def edit_worker11(id):
    if session['lg'] == 'ln':
        db = Db()
        # w_no = request.form['textfield']
        w_name = request.form['textfield2']
        dept = request.form['textfield3']
        contact = request.form['textfield4']
        photo = request.files['textfield5']
        email = request.form['textfield6']
        if request.files is not None:
            if photo.filename!="":
                import datetime
                date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                photo.save(r"E:\final\Project\static\images\\" + date + '.jpg')
                path = "/static/images/" + date + ".jpg"
                qry = "update worker set worker_name='" + w_name + "',department='"+dept+"',email_id='"+email+"',contact_no='"+contact+"',photo='"+str(path)+"' where worker_id='"+id+"'"
                db.update(qry)
                return '''<script>alert("success");window.location="/view_worker"</script>'''
            else:
                qry = "update worker set worker_name='" + w_name + "',department='" + dept + "',email_id='" + email + "',contact_no='" + contact + "' where worker_id='" + id + "'"
                db.update(qry)
                return '''<script>alert("success");window.location="/view_worker"</script>'''
        else:
            qry = "update worker set worker_name='" + w_name + "',department='" + dept + "',email_id='" + email + "',contact_no='" + contact + "' where worker_id='" + id + "'"
            db.update(qry)
            return '''<script>alert("success");window.location="/view_worker"</script>'''
    else:
        return render_template('loginindex.html')


@app.route('/ss_reg')
def ss_reg():
    return render_template('ss_reg.html')


@app.route('/ss_reg1',methods=['post'])
def ss_reg1():
    db=Db()
    name=request.form['textfield']
    place=request.form['textfield2']
    post=request.form['textfield3']
    pin=request.form['textfield4']
    dis=request.form['textfield5']
    email=request.form['textfield6']
    phn=request.form['textfield7']
    lno=request.form['textfield8']
    p=request.form['p']
    pp=request.form['pp']
    state=request.form['select']
    q=db.selectOne("select * from login where user_name='"+email+"' and type='service_center'")
    if q is not None:
        return '''<script>alert("already exist");window.location="/"</script>'''
    else:
        if p==pp:
            qq=db.insert("insert into login values('','"+email+"','"+p+"','pending')")
            q1=db.insert("insert into service_center_info values('"+str(qq)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+dis+"','"+state+"','"+phn+"','"+email+"','"+lno+"')")
            return '''<script>alert("success");window.location="/"</script>'''
        else:
            return '''<script>alert("failed");window.location="/"</script>'''

@app.route('/ws_reg')
def ws_reg():
    return render_template('ws_reg.html')


@app.route('/ws_reg1',methods=['post'])
def ws_reg1():
    db=Db()
    name=request.form['textfield']
    place=request.form['textfield2']
    post=request.form['textfield3']
    pin=request.form['textfield4']
    dis=request.form['textfield5']
    email=request.form['textfield6']
    phn=request.form['textfield7']
    lno=request.form['textfield8']
    p=request.form['p']
    pp=request.form['pp']
    state=request.form['select']
    q=db.selectOne("select * from login where user_name='"+email+"' and type='workshop'")
    if q is not None:
        return '''<script>alert("already exist");window.location="/"</script>'''
    else:
        if p==pp:
            qq=db.insert("insert into login values('','"+email+"','"+p+"','pending')")
            q1=db.insert("insert into workshop values('"+str(qq)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+dis+"','"+state+"','"+phn+"','"+email+"','"+lno+"')")
            return '''<script>alert("success");window.location="/"</script>'''
        else:
            return '''<script>alert("failed");window.location="/"</script>'''



@app.route('/chat')
def chat():
    if session['lg'] == "ln":
        return render_template("workshop/workshop_user_chat.html")
    else:
        return render_template('loginindex.html')


@app.route('/company_staff_chat',methods=['post'])
def company_staff_chat():
    if session['lg'] == "ln":
        db=Db()
        a=session['login_id']
        # q1="SELECT `user`.* FROM `pharmacy`,`user`,`booking`,`p_medicine` WHERE `pharmacy`.`pid`=`p_medicine`.`pharmacyid` AND `p_medicine`.`p_medid`=`booking`.`p_medicineid` AND `booking`.`userid`=`user`.`userid` AND `pharmacy`.`pid`='"+str(session['lid'])+"' group by user.userid"
        q1="select * from workshop_request,customer,workshop,location where workshop_request.status='approved' and workshop_request.customer_id=customer.customer_id and workshop.workshop_id=workshop_request.workshop_id and workshop_request.workshop_id='"+str(session['login_id'])+"' and customer.customer_id=location.id"
        res = db.select(q1)
        v={}
        if len(res)>0:
            v["status"]="ok"
            v['data']=res
        else:
            v["status"]="error"

        rw=demjson.encode(v)
        print(rw)
        return rw
    else:
        return render_template('loginindex.html')


@app.route('/chatsnd',methods=['post'])
def chatsnd():
    if session['lg'] == "ln":
        db=Db()
        c = session['login_id']
        b=request.form['n']
        print(b)
        m=request.form['m']

        q2="insert into chat values(null,'"+str(c)+"','"+str(b)+"','"+m+"',curdate(),'workshop')"
        res=db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return render_template('loginindex.html')


@app.route('/chatrply',methods=['post'])
def chatrply():
    if session['lg'] == "ln":
        print("...........................")
        c = session['login_id']
        b=request.form['n']
        print("<<<<<<<<<<<<<<<<<<<<<<<<")
        print(b)
        t = Db()
        qry2 = "select * from chat where type='workshop' ORDER BY cid ASC ";
        res = t.select(qry2)
        print(res)

        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
            v['id']=c
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        return rw
    else:
        return render_template('loginindex.html')


@app.route('/chat1')
def chat1():
    if session['lg'] == "ln":
        return render_template("service center/sc_user_chat.html")
    else:
        return render_template('loginindex.html')


@app.route('/company_staff_chat1',methods=['post'])
def company_staff_chat1():
    if session['lg'] == "ln":
        db=Db()
        a=session['login_id']
        # q1="SELECT `user`.* FROM `pharmacy`,`user`,`booking`,`p_medicine` WHERE `pharmacy`.`pid`=`p_medicine`.`pharmacyid` AND `p_medicine`.`p_medid`=`booking`.`p_medicineid` AND `booking`.`userid`=`user`.`userid` AND `pharmacy`.`pid`='"+str(session['lid'])+"' group by user.userid"
        q1="select * from sc_request,service_function,customer,service_center_info,location where sc_request.status='approved' and sc_request.customer_id=customer.customer_id and service_center_info.service_center_id=service_function.`service_center_id` and sc_request.service_fun_id=service_function.service_fun_id and service_function.`service_center_id`='"+str(session['login_id'])+"' and customer.customer_id=location.id"
        res = db.select(q1)
        v={}
        if len(res)>0:
            v["status"]="ok"
            v['data']=res
        else:
            v["status"]="error"

        rw=demjson.encode(v)
        print(rw)
        return rw
    else:
        return render_template('loginindex.html')


@app.route('/chatsnd1',methods=['post'])
def chatsnd1():
    if session['lg'] == "ln":
        db=Db()
        c = session['login_id']
        b=request.form['n']
        print(b)
        m=request.form['m']

        q2="insert into chat values(null,'"+str(c)+"','"+str(b)+"','"+m+"',curdate(),'service_center')"
        res=db.insert(q2)
        v = {}
        if int(res) > 0:
            v["status"] = "ok"

        else:
            v["status"] = "error"

        r = demjson.encode(v)

        return r
    else:
        return render_template('loginindex.html')


@app.route('/chatrply1',methods=['post'])
def chatrply1():
    if session['lg'] == "ln":
        print("...........................")
        c = session['login_id']
        b=request.form['n']
        print("<<<<<<<<<<<<<<<<<<<<<<<<")
        print(b)
        t = Db()
        qry2 = "select * from chat where type='service_center' ORDER BY cid ASC ";
        res = t.select(qry2)
        print(res)

        v = {}
        if len(res) > 0:
            v["status"] = "ok"
            v['data'] = res
            v['id']=c
        else:
            v["status"] = "error"

        rw = demjson.encode(v)
        return rw
    else:
        return render_template('loginindex.html')


if __name__ == '__main__':
    app.run(port=4000)
