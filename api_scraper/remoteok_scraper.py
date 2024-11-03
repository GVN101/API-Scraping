# import requests
# import xlwt
# from xlwt import Workbook
# import smtplib
# from os.path import basename
# from email.mime.application import MIMEApplication
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.utils import COMMASPACE,formatdate

# BASE_URL = 'https://remoteok.com/api'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
# REQUEST_HEADER = {
#     'User-Agent': USER_AGENT,
#     'Accept-Language': 'en-US,en;q=0.5'
# }
# def get_job_postings():
#     res = requests.get(url=BASE_URL,headers=REQUEST_HEADER)
#     return res.json()

# def output_jobs_to_cls(data):
#     wb = Workbook()
#     job_sheet = wb.add_sheet('Jobs')
#     headers = list(data[0].keys())
#     for i in range(len(headers)):
#         job_sheet.write(0, i, headers[i])
#     for i in range(len(data)):
#         job = data[i]
#         values = list(job.values())
#         for j in range(len(values)):
#             job_sheet.write(i+1, j, values[j])    
#     wb.save('remote_jobs.xls')    


# if __name__ ==  '__main__':
#     json=get_job_postings()[1:]
#     output_jobs_to_cls(json)

import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# https://myaccount.google.com/lesssecureapps
BASE_URL = 'https://remoteok.com/api/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}
MAX_EXCEL_CHAR_LIMIT = 32760


def get_job_postings():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
    return res.json()


def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())
    for i in range(0, len(headers)):
        job_sheet.write(0, i, headers[i])
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            value = values[x]
            if isinstance(value, str) and len(value) > MAX_EXCEL_CHAR_LIMIT:
                value = value[:MAX_EXCEL_CHAR_LIMIT]
            job_sheet.write(i+1, x, value)
    wb.save('remote_jobs.xls')


def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()
    smtp.login(send_from, 'Enter Password Here')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)
    send_email('chn21cs062@ceconline.edu', ['contact@preneure.com'],
               'Jobs Posting', 'Please, find attached a list of job posting to this email',
               files=['remote_jobs.xls'])