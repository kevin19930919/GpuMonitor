import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpumonitoring.settings')
django.setup()

from mail_sender import send_mail, get_text_from_records, get_text_from_crawllogs
import config

def main():
    send_mail(config.from_sender, "weiyen_lin@leadtek.com.tw", config.tw_notifiation_subject, "Test Mail")

if __name__ == '__main__':
    main()