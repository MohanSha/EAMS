#import libraries
import smtplib
import MySQLdb
import getpass
from calendar import monthrange
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_emailatt(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    #function for mail
    def py_mail(SUBJECT, BODY, TO, FROM):
        """With this function we send out our html email"""
        bcc="sathishkumar.k@qubecinema.com"
        #bcc="mohansha@qubecinema.com"
        # Create message container - the correct MIME type is multipart/alternative here!
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = "HR Desk"
        MESSAGE.preamble = """
    Your mail reader does not support the report format.
    Please visit us <a href="login.php">online</a>!"""
    
        # Record the MIME type text/html.
        HTML_BODY = MIMEText(BODY, 'html')
    
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        MESSAGE.attach(HTML_BODY)
    
        # The actual sending of the e-mail
        server = smtplib.SMTP('postman.realimage.co.in:25')
    
        # Print debugging output when testing
        if __name__ == "__main__":
            server.set_debuglevel(1)
    
        # Credentials (if needed) for sending the mail
        password = userpass
        #password = "2011Ppc@1056"
    
        server.starttls()
        server.login(FROM,password)
        server.sendmail(FROM, [TO,bcc], MESSAGE.as_string())
        server.quit()


    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    # Get the cursor, which is used to traverse the database, line by line
    att_read_cursor = database.cursor()

    tbl1_name="att_report"
    tbl2_name="erp_report"
    tbl3_name="email"


    #mh=int(raw_input("Enter Month: "))
    #yr=int(raw_input("Enter Year: "))
    mh=int(inp_mh.get())
    yr=int(inp_yr.get())

    startdate = datetime(yr,mh,21)
    #print startdate.strftime('%Y-%m-%d')
    no_of_days = monthrange(yr, mh)
    tday = no_of_days[1]+1

    #testid = raw_input("Enter Employee ID to generate email : [Enter 0 for all] ")
    testid = str(inp_tid.get())
    #testid=0
    #test_to_email= raw_input("Enter test mail recepient : [Enter 0 for all] ")
    test_to_email = str(inp_teid.get())
    #userid = raw_input("Enter From Email ID: ")
    userid = str(inp_se.get())
    #userpass = getpass.getpass() #raw_input("Enter Password: ")
    userpass = str(inp_sepass.get())
    if testid==0:
        # Create the Select sql query
        att_query = """SELECT A.ID,B.Employee_Name,A.Date,A.Leave_status,C.Email_Id FROM `att_report` A,`erp_report` B, `email` C WHERE A.ID=B.E_code AND A.ID=C.Emp_Code;"""
    else:
        att_query = """SELECT A.ID,B.Employee_Name,A.Date,A.Leave_status,C.Email_Id FROM `att_report` A,`erp_report` B, `email` C WHERE A.ID=B.E_code AND A.ID=C.Emp_Code AND A.ID='"""+testid+"""';"""

    # Execute sql Query
    att_read_cursor.execute(att_query)
    att_count = att_read_cursor.rowcount
    att_row = att_read_cursor.fetchone()
    ic=0

    content="""
    """
    att_date_list=[]
    att_ls_list=[]
    dt=[];
    i=0
    htmlstr1 = """<th>"""
    htmlstr2 = """<br>"""
    htmlstr3 = """</th>"""
    #foot1="""<td align='center'>"""   
    foot2="""</td>"""   

    #each attendance row create the html
    while att_row is not None:
        print att_row
        prev_id = att_row[0]
        prev_name = att_row[1]
        prev_email = att_row[4]
        header=""
        footer=""
        for day in range(1,tday):
            att_date_list.insert(day,att_row[2]);
            dt.insert(day,datetime.strptime(att_date_list[day-1], '%d-%m-%Y'));
            #print dt[day-1]
            header = header+htmlstr1+str(datetime.strftime(dt[day-1],'%d'))+htmlstr2+str(datetime.strftime(dt[day-1],'%b'))+htmlstr2+str(datetime.strftime(dt[day-1],'%a'))+htmlstr3
            att_ls_list.insert(day,att_row[3]); 
            if str(datetime.strftime(dt[day-1],'%a'))=="Sat" or str(datetime.strftime(dt[day-1],'%a'))=="Sun":
                foot1="<td class='workoff' align='center'>";
            else:
                        if att_row[3]=="A":
                                foot1= "<td class='absent' align='center'>";
                                pass;
                        elif att_row[3]=="PH":
                                foot1= "<td class='ph' align='center'>";
                                pass;
                        elif att_row[3]=="CL" or att_row[3]=="SL" or att_row[3]=="HSL" or att_row[3]=="HCL" \
                        or att_row[3]=="PL" or att_row[3]=="CO" or att_row[3]=="ML" or att_row[3]=="MATRL" \
                        or att_row[3]=="PTL" or att_row[3]=="TL1" or att_row[3]=="TL2" or att_row[3]=="BL" \
                        or att_row[3]=="EL":
                                foot1= "<td class='cl' align='center'>";
                                pass;
                        elif att_row[3]=="LOP":
                                foot1= "<td class='absent' align='center'>";
                                pass;
                        elif att_row[3]=="HOD":
                                foot1= "<td class='od' align='center'>";
                                pass;
                        elif att_row[3]=="OD":
                                foot1= "<td class='od' align='center'>";
                                pass;
                        else:
                                foot1= "<td align='center'>";
                                pass;

            footer = footer+foot1+att_ls_list[day-1]+foot2
            att_row = att_read_cursor.fetchone() 

            if att_row is None:
                curr_id = ""
                curr_name = ""
                curr_email = ""
            else:
                curr_id = att_row[0]
                curr_name = att_row[1]
                curr_email = att_row[4] 
            if curr_id != prev_id:
                #before calculating next empolyee send mail for current employee
                if __name__ == "__main__":
                    """Executes if the script is run as main script (for testing purposes)"""         
                    email_content = """
                    <html>
                    <head>
                        <title>Employee Attendance</title>
                        <!-- This is developed by Mohan Sha -->
                        <style>
            body
            {
                font-family: Verdana, Geneva, Tahoma, sans-serif;
            }
            table,tr
            {
                border-collapse: collapse;
                border: 1px solid black;
            
            }
            th
            {
                border-collapse: collapse;
                border: 1px solid black;
                font-size: 12;
                font: verdana;
                background-color: lightgrey;
            }
            td
            {
                border-collapse: collapse;
                border: 1px solid black;
                align-content:center;
                font-size: 12;
                font: verdana;
            }
            td.workoff
            {
                background-color: cyan;
                align-content:center;
                font-size: 12;
                font: verdana;
            }
            td.cl
            {
                background-color: lightsalmon;
                align-content:center;
                font-size: 12;
                font: verdana;
            }
            td.od
            {
                background-color: lightgreen;
                align-content:center;
                font-size: 12;
                font: verdana;
            }
            td.ph
            {
                background-color: greenyellow;
                align-content:center;
                font-size: 12;
                font: verdana;
            }
            td.absent
            {
                background-color: red;
                align-content:center;
                font-size: 12;
                font: verdana;
            }

            td.noday
            {
                background-color: lightslategray;
                align-content:center;
                align:'center';
            }
            td.diagonalFalling
            {
            background: linear-gradient(to right top, #fff 0%,#fff 49.9%,#000000    
            50%,#000000 51%,#fff 51.1%,#fff 100%);
            }
        </style>
                    </head>
                    <body>
                        Dear """+prev_name+""", <br><br>
                        Your attendance information from 21st """+str(datetime.strftime(dt[0],'%b %Y'))+""" to 20th """+str(datetime.strftime(dt[tday-3],'%b %Y'))+"""<br><br>
                        <table>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>"""+header+"""
                            </tr>
                            <tr>
                                <td align="center">"""+prev_id+"""</td>
                                <td align="center">"""+prev_name+"""</td>"""+footer+"""
                            </tr>
                        </table>
                        <p><p>Leave Type:</p>
                        <table border="1">
                        <tr>
                            <td class='absent'> A </td>
                            <td> Not swipe/Not apply in ERP/Reporting officer not authorize </td>
                            <td class='ph'> PH </td>
                            <td> Paid holiday </td>   
                        <tr>
                            <td class='workoff'> WO </td>
                            <td> Weekly off </td>
                            <td class='cl'> MATRL </td>
                            <td> Maternity Leave </td>
                        </tr>  
                        <tr>  
                            <td class='cl'>CL</td>
                            <td>Casual Leave</td>
                            <td class='cl'>PTL</td>
                            <td>Paternity Leave</td>
                        </tr>
                        <tr>
                            <td class='cl'>HSL</td>
                            <td>Half-day sick Leave</td>
                            <td class='cl'>TL1</td>
                            <td>Tenure Leave 1</td>
                        </tr>  
                        <tr>  
                            <td class='cl'>HCL</td>
                            <td>Half-day Casual Leave</td>
                            <td class='cl'>TL2</td>
                            <td>Tenure Leave 2</td>
                        </tr>
                        <tr>
                            <td class='cl'>SL</td>
                            <td>Sick Leave</td>
                            <td class='cl'>BL</td>
                            <td>Bereavement Leave</td>
                        </tr>
                        <tr>    
                            <td class='cl'>PL</td>
                            <td>Privilege Leave</td>
                            <td class='cl'>EL</td>
                            <td>Education Leave</td>
                        </tr>
                        <tr>
                            <td class='workoff'>CO</td>
                            <td>Compensatory off</td>
                            <td class='absent'>LOP</td>
                            <td>Loss of Pay</td>
                        </tr>
                        <tr>    
                            <td class='cl'>ML</td>
                            <td>Marriage Leave</td>
                            <td class='od'>HOD/OD</td>
                            <td>Half Day OD<strong>/</strong>On Duty</td>
                        </tr>
                </table>
                <p>Note: If any date mentioned as &#34;A&#34; need to be apply in ERP ASAP Else it will be considered as &#34;Loss of pay&#34; in next month. If you have any clarification please revert to sathishkumar.k@qubecinema.com. </p> 
                <p>
                Regards<br>
                Team-Payroll</p>
        </body>
        </html>"""
                    if test_to_email==0:
                        TO = prev_email
                    else:
                        TO = test_to_email
                    #TO = 'mohansha@qubecinema.com'
                    #FROM ='mohansha@qubecinema.com'
                    FROM = userid
                    SUBJECT = "Your Attendance from "+str(datetime.strftime(dt[0],'%b %Y'))+" to "+str(datetime.strftime(dt[tday-3],'%b %Y'))
                    #print "mail sent for "+prev_id
                    #print att_date_list
                    #print att_ls_list
                    py_mail(SUBJECT, email_content, TO, FROM)
                    att_date_list=[]
                    att_ls_list=[]
                    dt=[]
                    ic = ic+1
                break

        
        #att_row = att_read_cursor.fetchone()

    # Close the cursor
    att_read_cursor.close()
    #insert_cursor.close()
    #xexit()


    # Commit the transaction
    #database.commit()

    # Close the database connection
    database.close()


    # Print results
    print ""
    print "All Done!"
    print "I just sent "  + str(ic) + " Emails!"
    emain.destroy()

def checkMonthOnly(event):
    #print inp_mh.get()
    if inp_mh.get()=="" or inp_mh.get().isdigit() and int(inp_mh.get()) > 0 and int(inp_mh.get()) < 13:
        #print "corrent"
        return True
    else:
        showerror('Error', 'Enter valid Input')
        inp_mh.delete(0, END)
        inp_mh.focus()
        return False

def checkYearOnly(event):
    #print inp_yr.get()
    if inp_yr.get()=="" or inp_yr.get().isdigit() and int(inp_yr.get()) > 2016 and int(inp_yr.get()) < 2019:
        return True
    else:
        showerror('Error', 'Enter valid Input')
        inp_yr.delete(0, END)
        inp_yr.focus()
        return False

def send():
    #print inp_yr.get()
    if inp_yr.get()!="" and inp_yr.get()!="" \
    and inp_tid.get()!="" and inp_teid.get()!="" \
    and inp_se.get()!="" and inp_sepass.get()!="":
        emain.withdraw()
        exec_emailatt()
        return True
    else:
        showerror('Error', 'Input values can not be blank')
        inp_mh.focus()
        return False

emain = Tk()
emain.title('Input')

Label(emain, text="Enter Month: ").grid(row=1,column=2,sticky=W,pady=4)
Label(emain, text="Enter Year: ").grid(row=2,column=2,sticky=W,pady=4)
Label(emain, text="Enter Employee ID to generate email or Enter 0 for all: ").grid(row=3,column=2,sticky=W,pady=4)
Label(emain, text="Enter test mail recepient or Enter 0 for all: ").grid(row=4,column=2,sticky=W,pady=4)
Label(emain, text="Enter Sender Email ID: ").grid(row=5,column=2,sticky=W,pady=4)
Label(emain, text="Enter Sender Password: ").grid(row=6,column=2,sticky=W,pady=4)
Button(text='   Send   ', command=send).grid(row=7,column=2,sticky=E,pady=12)
inp_mh = Entry(emain)
inp_mh.grid(row=1,column=4,padx=12)
inp_mh.bind('<FocusOut>', checkMonthOnly)
inp_yr = Entry(emain)
inp_yr.grid(row=2,column=4,padx=12)
inp_yr.bind('<FocusOut>', checkYearOnly)
inp_mh.focus()
inp_tid = Entry(emain)
inp_tid.grid(row=3,column=4,padx=12)
inp_teid = Entry(emain)
inp_teid.grid(row=4,column=4,padx=12)
inp_se = Entry(emain)
inp_se.grid(row=5,column=4,padx=12)
inp_sepass = Entry(emain, show='*')
inp_sepass.grid(row=6,column=4,padx=12)

emain.mainloop()