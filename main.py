import json
from os import path
from gophish import Gophish
import PySimpleGUI as sg     
import template_helper as tp
import email_helper as em
from email_helper import SendEmailProfile


# Set the theme of this GUI program
sg.theme('dark grey 9')

# Load gophish settings from config file
gophish_setting_config_file = 'gophish_settings.json'
if not path.exists(gophish_setting_config_file):
    with open(gophish_setting_config_file, 'w') as f:
        f.write('''
{
    "gophish_api_key" : "",
    "gophish_host" : "",
    "smtp_host" : "",
    "smtp_user_name" : "",
    "smtp_user_password" : "",
    "ignore_certificate_errors" : true
}
''')

with open(gophish_setting_config_file, 'r') as f:
    gophish_settings = json.loads(f.read())

layout = [  [sg.Text('Gophish Settings:')],
            [sg.Text('  Gophish API_KEY', size=(30,1)), sg.InputText(key='IT_GAPIKEY', password_char='*', default_text=gophish_settings['gophish_api_key'])],
            [sg.Text('  Gophish HOST', size=(30,1)), sg.InputText(key='IT_GHOST', default_text=gophish_settings['gophish_host'])],
            [sg.Text('  SMTP HOST', size=(30,1)), sg.InputText(key='IT_SMTPHOST', default_text=gophish_settings['smtp_host'])],
            [sg.Text('  SMTP User Name', size=(30,1)), sg.InputText(key='IT_SMTPUN', default_text=gophish_settings['smtp_user_name'])],
            [sg.Text('  SMTP User Password', size=(30,1)), sg.InputText(key='IT_SMTPUP', default_text=gophish_settings['smtp_user_password'])],
            [sg.Checkbox('  Ignore Certificate Errors', key='CB_ICE', default=gophish_settings['ignore_certificate_errors'])],
            [sg.Text('From:')],
            [sg.Text('  Sender Name', size=(30,1)), sg.InputText(key='IT_SN')],
            [sg.Text('  Sender Email Address', size=(30,1)), sg.InputText(key='IT_SEA')],
            [sg.Text('To:')],
            [sg.Text('  Recipient First Name (Optional)', size=(30,1)), sg.InputText(key='IT_RFN')],
            [sg.Text('  Recipient Last Name (Optional)', size=(30,1)), sg.InputText(key='IT_RLN')],
            [sg.Text('  Recipient Email Address', size=(30,1)), sg.InputText(key='IT_REA')],
            [sg.Text('Email Content Settings:')],
            [sg.Text('  Subject:', size=(30,1)), sg.InputText(key='IT_SUBJECT')],
            [sg.Text('  Email Template HTML File', size=(30,1)), sg.InputText(key='IT_ET'), sg.FileBrowse()],
            [sg.Text('  Email Template Config File', size=(30,1)), sg.InputText(key='IT_ETRC'), sg.FileBrowse()],
            [sg.Text('  Attachment File (Optional)', size=(30,1)), sg.InputText(key='IT_ATMT'), sg.FileBrowse()],
            [sg.Button('Send Email')]] 


window = sg.Window('Mail Helper GUI v0.1.4', layout)    


def email_proc_callback(state):
    window.write_event_value('email_sent', state)

while True:
    event, values = window.read() 
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Send Email':
        try:
            window['Send Email'].update('Sending...')
            window['Send Email'].update(disabled=True)
            email_content = tp.get_rendered_html(values['IT_ET'], values['IT_ETRC'])
            gophish = Gophish(api_key=values['IT_GAPIKEY'], host=values['IT_GHOST'])
            send_profile = SendEmailProfile(values['IT_SN'], values['IT_SEA'], values['IT_SUBJECT'], values['IT_RFN'],
                values['IT_RLN'], values['IT_REA'], email_content, tp.get_attachment(values['IT_ATMT']), values['IT_SMTPHOST'], values['IT_SMTPUN'],
                values['IT_SMTPUP'],  values['CB_ICE'])
            em.send_email(gophish, send_profile, email_proc_callback)
        except Exception as e:
            print(e)
            sg.popup('Error! Please check your configs and inputs then try again. Error: ' + str(e), title='Error')
            window['Send Email'].update(disabled=False)
            window['Send Email'].update('Send Email')
    if event == 'email_sent':
        result = values['email_sent']
        window['Send Email'].update(disabled=False)
        window['Send Email'].update('Send Email')
        if result['sent']:
            gophish_settings['gophish_api_key'] = values['IT_GAPIKEY']
            gophish_settings['gophish_host'] = values['IT_GHOST']
            gophish_settings['smtp_host'] = values['IT_SMTPHOST']
            gophish_settings['ignore_certificate_errors'] = values['CB_ICE']
            with open(gophish_setting_config_file, 'w') as f:
                f.write(json.dumps(gophish_settings, indent=4))
            sg.popup('Email Sent!', title=result['msg'])
        else:
            err = result['msg']
            print(err)
            sg.popup('Email Sent Failed! Please check your configs and inputs then try again. Error: ' + err, title='Error')
window.close()