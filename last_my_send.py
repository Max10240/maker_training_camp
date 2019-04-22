import smtplib,json
from time import sleep
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
with open('record.txt','r')as f:
    record_n=json.load(f)[0]
_user = "1346990364@qq.com"
_pwd = "vnnelvdhymomiaib"
_to  = "2691399914@qq.com"
def send_email(subject,file_name='',email_file_name='email.mp3'):
    global record_n
    #如名字所示Multipart就是分多个部分 # 构造一个MIMEMultipart对象代表邮件本身 
    msg = MIMEMultipart() 
    msg["Subject"] = subject+'#'*8+str(record_n) 
    msg["From"]  = _user 
    msg["To"]   = _to 
    '''#---这是文字部分--- 
    part = MIMEText('背景########24','plain', 'utf-8') 
    msg.attach(part) '''
    '''#---这是附件部分--- 
    #xlsx类型附件 
    part = MIMEApplication(open('foo.xlsx','rb').read()) 
    part.add_header('Content-Disposition', 'attachment', filename="foo.xlsx") 
    msg.attach(part) 
       
    #jpg类型附件 
    part = MIMEApplication(open('foo.jpg','rb').read()) 
    part.add_header('Content-Disposition', 'attachment', filename="foo.jpg") 
    msg.attach(part) 
       
    #pdf类型附件 
    part = MIMEApplication(open('foo.pdf','rb').read()) 
    part.add_header('Content-Disposition', 'attachment', filename="foo.pdf") 
    msg.attach(part) '''
    if file_name:
        #mp3类型附件 
        part = MIMEApplication(open(file_name,'rb').read()) 
        part.add_header('Content-Disposition', 'attachment', filename=email_file_name) 
        msg.attach(part) 
    s = smtplib.SMTP("smtp.qq.com", timeout=30)#连接smtp邮件服务器,端口默认是25 
    s.login(_user, _pwd)#登陆服务器 
    s.sendmail(_user, _to, msg.as_string())#发送邮件
    record_n+=1
    with open('record.txt','w')as f:
        json.dump([record_n],f)
    print('发送成功')
    sleep(4)
