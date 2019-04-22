import poplib
from time import sleep,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
raw_n=''
record_n=0
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
def decode_str(s):
    if not s:
        return None
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def recieve_email():
    global raw_n,record_n
    time_start=time()
    sleep(2)
    host = 'pop.qq.com'  
    username = '2691399914@qq.com'  
    password = 'dpwjsmmafegnddag'  
    server = poplib.POP3_SSL(host,port=995)
    server.user(username)
    server.pass_(password)
    # 获得邮件
    '''messages = [server.retr(i) for i in range(1, len(server.list()[1]) + 1)]  
    messages = [b'\r\n'.join(mssg[1]).decode() for mssg in messages]  
    messages = [Parser().parsestr(mssg) for mssg in messages]  
    #print("===="*10)'''
    resp, mails, octets = server.list()
    index = len(mails)
    resp, lines, octets = server.retr(index)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    message = msg
    time_consume=time()-time_start
    if time_consume>8:
        print(time_consume)
    time_start=time()
    subject = message.get('Subject')
    subject = decode_str(subject)
    if subject :
        msg_n=int(subject.split('#'*8)[1])
        ctn_split=subject.split('#'*8)[0]
    if raw_n=='':
        raw_n=msg_n
        record_n=msg_n
        return
    if record_n!=msg_n and raw_n!='':
        #如果标题匹配
        if subject and subject.startswith('download_annex'):
            value = message.get('From')
            if value:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
            #print("发件人: %s" % value)
            #print("标题:%s" % subject)
            for part in message.walk():
                contentType = part.get_content_type()
                fileName = part.get_filename()  
                fileName = decode_str(fileName)
                # 保存附件  
                if fileName:  
                    with open(fileName, 'wb') as fEx:
                        data = part.get_payload(decode=True) 
                        fEx.write(data)  
                        print("附件%s已保存" % fileName)
                    record_n=msg_n
                    return 'download_annex'
                '''elif contentType == 'text/plain' or contentType == 'text/html':
                    # 保存正文
                    data = part.get_payload(decode=True)
                    charset = guess_charset(part)
                    if charset:
                        charset = charset.strip().split(';')[0]
                        #print ('charset:', charset)
                        data = data.decode(charset)
                    content = data
                    print(content)'''
        
        elif subject.startswith('to_wechat'):
            record_n=msg_n
            return (ctn_split)
        elif subject.startswith('to_mp3'):
            record_n=msg_n
            return (ctn_split)
            
        else:
            record_n=msg_n
            return (ctn_split)
        #print(time()-time_start)
        
    
