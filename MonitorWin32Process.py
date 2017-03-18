#!-*- encoding: utf-8 -*- 
import wmi,os,time,smtplib
import logging 
from ConfigParser import ConfigParser
from email.mime.text import MIMEText
 
CONFIGFILE='./config.ini'
config = ConfigParser() 
config.read(CONFIGFILE)

mailHost = config.get('mailHost', 'Host')
mailUser = config.get('mailUser','User') 
mailPass = config.get('mailPass','Pass') 
mailPostfix = config.get('mailPostfix','Postfix') 
mailToList = config.get('mailToList','toList')
subject = config.get('subject','subject')

def send_mail(mailToList, subject, content):
    RealTime = time.strftime("%Y-%m-%d %X",time.localtime()) 
    content = RealTime + " " + content 
    me="Monitor"+"<"+mailUser+"@"+mailPostfix+">" 
    msg = MIMEText(content,'plain','gb2312') 
    msg['Subject'] = subject 
    msg['From'] = me 
    msg['To'] = mailToList 
    try: 
        s = smtplib.SMTP() 
        s.connect(mailHost) 
        s.login(mailUser,mailPass) 
        s.sendmail(me, mailToList, msg.as_string()) 
        s.close() 
        return True 
    except Exception, e: 
        print str(e) 
        return False

dirName = "d:\MonitorWin32Process\\" 
logSuffix = ".log" 
logErrorSuffix = ".error.log" 
config = ConfigParser() 
config.read(CONFIGFILE) 
 
ProgramPath = config.get('MonitorProgramPath','ProgramPath') 
ProcessName = config.get('MonitorProcessName','ProcessName')  
SleepTime = config.get('ProcessSleepTime','SleepTime')

if not os.path.isdir(dirName): 
    os.makedirs(dirName) 

c = wmi.WMI() 
def main(): 
    ProList = []             #如果在main()函数之外ProList 不会清空列表内容.
    time_time_day = time.strftime("%Y-%m-%d", time.localtime())
    time_time_log = time.strftime("%Y-%m-%d %X", time.localtime())
    log_file_name = dirName + time_time_day + logSuffix
    log_file_name_error = dirName + time_time_day + logErrorSuffix
    if  not os.path.isfile(log_file_name): 
        file(log_file_name,'a')

    for process in c.Win32_Process():
        ProList.append(str(process.Name)) 

    if ProcessName in ProList:
        content = time_time_log + " Service " + ProcessName + " is running...!!!\n"
        print "Service " + ProcessName + " is running...!!!"
        logFile = open(log_file_name,'a+')
        logFile.write(content)
        logFile.close()
 
    else:
        content = time_time_log + " Service " + ProcessName + " is error !!!" + "\n"
        logFile = open(log_file_name_error,'a+') 
        print "Service " + ProcessName + " error ...!!!"
        logFile.write(content) 
        logFile.close() 
        os.startfile(ProgramPath) 
        send_mail(mailToList,subject,content)
 
if __name__ == "__main__": 
    while True: 
        main() 
        time.sleep(int(SleepTime)) 
