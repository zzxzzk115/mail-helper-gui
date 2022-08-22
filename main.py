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
    "ignore_certificate_errors" : true
}
''')

with open(gophish_setting_config_file, 'r') as f:
    gophish_settings = json.loads(f.read())

layout = [  [sg.Text('Gophish Settings:')],
            [sg.Text('  Gophish API_KEY', size=(30,1)), sg.InputText(key='IT_GAPIKEY', password_char='*', default_text=gophish_settings['gophish_api_key'])],
            [sg.Text('  Gophish HOST', size=(30,1)), sg.InputText(key='IT_GHOST', default_text=gophish_settings['gophish_host'])],
            [sg.Text('  SMTP HOST', size=(30,1)), sg.InputText(key='IT_SMTPHOST', default_text=gophish_settings['smtp_host'])],
            [sg.Checkbox('  Ignore Certificate Errors', key='CB_ICE', default=gophish_settings['ignore_certificate_errors'])],
            [sg.Text('From:')],
            [sg.Text('  Sender Name', size=(30,1)), sg.InputText(key='IT_SN')],
            [sg.Text('  Sender Email Address', size=(30,1)), sg.InputText(key='IT_SEA')],
            [sg.Text('To:')],
            [sg.Text('  Recipient First Name (Optional)', size=(30,1)), sg.InputText(key='IT_RFN')],
            [sg.Text('  Recipient Last Name (Optional)', size=(30,1)), sg.InputText(key='IT_RLN')],
            [sg.Text('  Recipient Email Address', size=(30,1)), sg.InputText(key='IT_REA')],
            [sg.Text('Template Settings:')],
            [sg.Text('  Subject:', size=(30,1)), sg.InputText(key='IT_SUBJECT')],
            [sg.Text('  Email Template HTML File', size=(30,1)), sg.InputText(key='IT_ET'), sg.FileBrowse()],
            [sg.Text('  Email Template Config File', size=(30,1)), sg.InputText(key='IT_ETRC'), sg.FileBrowse()],
            [sg.Button('Send Email')]] 


window = sg.Window('Mail Helper GUI v0.1.0', layout)    


while True:
    event, values = window.read() 
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Send Email':
        try:
            window['Send Email'].update('Sending...')
            window['Send Email'].update(disabled=True)
            email_content = tp.get_rendered_html(open(values['IT_ET']).read(), tp.get_config_dict(values['IT_ETRC']))
            gophish = Gophish(api_key=values['IT_GAPIKEY'], host=values['IT_GHOST'])
            send_profile = SendEmailProfile(values['IT_SN'], values['IT_SEA'], values['IT_SUBJECT'], values['IT_RFN'],
                values['IT_RLN'], values['IT_REA'], email_content, values['IT_SMTPHOST'],  values['CB_ICE'])
            em.send_email(gophish, send_profile)
            window['Send Email'].update(disabled=False)
            window['Send Email'].update('Send Email')
            sg.popup('Email Sent!', title='Sucess')
            gophish_settings['gophish_api_key'] = values['IT_GAPIKEY']
            gophish_settings['gophish_host'] = values['IT_GHOST']
            gophish_settings['smtp_host'] = values['IT_SMTPHOST']
            gophish_settings['ignore_certificate_errors'] = values['CB_ICE']
            with open(gophish_setting_config_file, 'w') as f:
                f.write(json.dumps(gophish_settings, indent=4))
        except Exception as e:
            print(e)
            sg.popup('Error! Please check your configs and inputs then try again.', title='Error')
            window['Send Email'].update(disabled=False)
            window['Send Email'].update('Send Email')
window.close()