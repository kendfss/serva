import smtplib, os


smtp_info = {
    "gmail": {
        "host": "smtp.gmail.com",
        "port": 465,
    },
}

def quick_mail(
               msg:str, 
               receiver:str, 
               sender:str, 
               password:str, 
               subj:str="IP Address", 
               head:str="IP Address", 
               extra:str=os.path.split(os.path.expanduser('~'))[1], 
               att:str=None
              ) -> None:
    """
    Sends a short email to the given receiver using gmail's smtp configuration with default sender/receiver info taken from user environment variables
    Dependencies: os.environ.get [func], smtplib [mod], email.message.EmailMessage [obj]
    Arguments: message, **destination
    Output: None
    """
    message = EmailMessage()
    message['Subject'] = f'{subj if subj!=None else head if head!=None else ""}'
    message['From'] = sender
    message['To'] = receiver
    message.set_content(msg)
    if any([subj!=None,head!=None,extra!=None]):
        message.add_alternative(f"""\
        <!DOCTYPE html>
        <html style='font-family:courier new;'>
            <body>
                <h1 style="color:SlateGray;">{head if head!=None else ''}</h1>
                <p>{msg}</p>
                <P>from {extra if extra else ''}
            </body>
        </html>
        """, subtype='html')
    if att != None:
        for file in att.split('*'):
            with open(file, "rb") as f:
                fileData = f.read()
                fileName = f.name.split(os.sep)[-1]
                fileType = (os.path.splitext(f.name)[1]).replace(".","")
                message.add_attachment(fileData, maintype="image", subtype=fileType, filename=fileName)
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    target = sender.split('@')[1].split('.')[0]
    with smtplib.SMTP_SSL(
                          smtp_info[target]['host'], 
                          smtp_info[target]['port'],
                          ) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)