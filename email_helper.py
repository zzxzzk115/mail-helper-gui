from datetime import datetime
from gophish import Gophish
from gophish.models import Group, User, SMTP, Template, Page, Campaign
import threading


class SendEmailProfile:
    def __init__(self, sender_name : str, sender_email : str, subject : str, 
            recipient_first_name : str, recipient_last_name : str, recipient_email : str,
            email_content: str, email_attachment, smtp_host : str, smtp_user_name : str, smtp_user_password : str, smtp_ignore_cert_errors : bool) -> None:
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.subject = subject
        self.recipient_first_name = recipient_first_name
        self.recipient_last_name = recipient_last_name
        self.recipient_email = recipient_email
        self.email_content = email_content
        self.email_attachment = email_attachment
        self.smtp_host = smtp_host
        self.smtp_user_name = smtp_user_name
        self.smtp_user_password = smtp_user_password
        self.smtp_ignore_cert_errors = smtp_ignore_cert_errors


def send_email(gophish : Gophish, profile : SendEmailProfile, callback):
    t = threading.Thread(target=_send_email_proc, args=(gophish, profile, callback))
    t.start()


def _send_email_proc(gophish : Gophish, profile : SendEmailProfile, callback):
    # Get Date time now
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a new Sending Profile
    new_sending_profile = SMTP(name='SMTP:' + now)
    new_sending_profile.host = profile.smtp_host
    if profile.sender_name:
        new_sending_profile.from_address = profile.sender_name + ' <' + profile.sender_email + '>'
    else:
        new_sending_profile.from_address = profile.sender_email
    new_sending_profile.interface_type = 'SMTP'
    new_sending_profile.ignore_cert_errors = profile.smtp_ignore_cert_errors
    new_sending_profile.username = profile.smtp_user_name
    new_sending_profile.password = profile.smtp_user_password
    gophish.smtp.post(new_sending_profile)

    # Create a new Group
    new_group = Group(name='Group:' + now, 
                        targets=[User(first_name=profile.recipient_first_name, 
                                        last_name=profile.recipient_last_name,
                                        email=profile.recipient_email)])
    gophish.groups.post(new_group)

    # Create a new Email Template
    new_email_template = Template(name='Template:' + now, html=profile.email_content, 
        subject=profile.subject, attachments=[profile.email_attachment])
    gophish.templates.post(new_email_template)

    # Create a new empty Landing Page
    new_landing_page = Page(name='Page:' + now, html='')
    gophish.pages.post(new_landing_page)

    # Create a new Campaign and schedule it
    new_campaign = Campaign(name='Campaign:' + now, groups=[new_group], page=new_landing_page,
        template=new_email_template, smtp=new_sending_profile)
    gophish.campaigns.post(new_campaign)
    callback()