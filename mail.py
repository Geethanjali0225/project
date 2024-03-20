# Email configuration
#geetanjali.c2k@gmail.com
#geethanjali.c2000@gmail.com
#miyp yibf gzel nubt



import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
email_sender = "geetanjali.c2k@gmail.com"
email_password = "miyp yibf gzel nubt"
email_receiver = "geethanjali.c2000@gmail.com"

# Thresholds for memory and CPU usage
cpu_threshold_5 = 5
cpu_threshold_10 = 10
memory_threshold_5 = 5
memory_threshold_10 = 10

# Function to send an email with a table of grouped commands
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Read the CSV file and group similar commands by thresholds
grouped_commands = {}

with open('performance_log.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row

    for row in csvreader:
        cpu = float(row[0])
        memory = float(row[1])
        command = row[3].strip()
        notification = ""

        if cpu > cpu_threshold_10 or memory > memory_threshold_10:
            notification = "<font color='red'>Exceeds 10%</font>"
        elif cpu > cpu_threshold_5 or memory > memory_threshold_5:
            notification = "<font color='orange'>Exceeds 5%</font>"

        if notification and command not in grouped_commands:
            grouped_commands[command] = {'cpu_sum': 0, 'memory_sum': 0, 'notifications': []}
            grouped_commands[command]['cpu_sum'] += cpu
            grouped_commands[command]['memory_sum'] += memory
            grouped_commands[command]['notifications'].append(notification)

# Prepare HTML email content with a table of grouped commands
message = "<html><body><table border='1' style='border-collapse: collapse;'><tr><th>Command</th><th>Total Cpu %</th><th>Total Memory %</th><th>Notifications</th></tr>"

for command, data in grouped_commands.items():
    message += f"<tr><td>{command}</td><td>{data['cpu_sum']}</td><td>{data['memory_sum']}</td><td>{', '.join(data['notifications'])}</td></tr>"

message += "</table></body></html>"

# Send the email with the grouped commands in a table format
if grouped_commands:
    send_email("Performance Alert", message)
