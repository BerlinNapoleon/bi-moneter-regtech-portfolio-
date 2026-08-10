# scripts/telegram_bot.py
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8801561226:AAFT2Hgho6NEQZigQse7PmRgeNH7fpNf6EU')
CHAT_ID = os.environ.get('CHAT_ID', '1907896409')

def send_compliance_alert(bank_name, report_type, status, message):
    text = (
        f'PERINGATAN KEPATUHAN REGULASI\n\n'
        f'Bank: {bank_name}\n'
        f'Jenis Laporan: {report_type}\n'
        f'Status: {status}\n'
        f'Catatan: {message}\n\n'
        f'Harap segera melakukan pengecekan pada Portal RegTech.'
    )
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == '__main__':
    # Test send alert
    send_compliance_alert('Bank Testing', 'LKP-01', 'LATE_SUBMISSION', 'Test message from GitHub Action')

