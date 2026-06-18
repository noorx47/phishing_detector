import csv
import random

random.seed(42)

companies = ["PayPal", "Amazon", "Netflix", "Chase Bank", "Apple",
             "Microsoft", "DHL", "Bank of America", "eBay", "Google"]

names = ["Sarah", "John", "Priya", "Marcus", "Elena", "Tom", "David", "Laura"]

fake_links = [
    "http://secure-login-update.com/verify",
    "http://account-confirm-now.net/login",
    "http://192.168.5.23/login.php",
    "http://bit.ly/3xKqL9",
    "http://paypal-security-check.info",
]

normal_links = [
    "https://docs.google.com/document/d/abc123",
    "https://github.com/myteam/project",
    "https://zoom.us/j/123456789",
]

phishing_templates = [
    "Dear Customer, your {company} account has been suspended due to unusual activity. Click here immediately to verify your identity: {link}. Failure to act within 24 hours will result in permanent account closure.",
    "URGENT: We detected a login attempt to your {company} account from an unrecognized device. Verify your account now at {link} or your account will be locked.",
    "Congratulations! You have been selected to receive a $500 {company} gift card. To claim your prize confirm your details here: {link}. Offer expires in 12 hours!",
    "Your {company} payment information could not be verified. Please update your billing details immediately by clicking {link} to avoid suspension.",
    "Security Alert: Someone tried to access your {company} account. Please confirm it was you by logging in here: {link}. This is your final warning.",
    "Your {company} account has a pending invoice of $249.99 that could not be processed. Click {link} now to update your payment method.",
    "Dear user, your {company} subscription will be cancelled unless you confirm your card details within 24 hours. Click here: {link}",
    "ATTENTION: Your mailbox has exceeded its storage limit. Click {link} now to verify your {company} account or your emails will be deleted.",
]

legit_templates = [
    "Hi {name}, just checking in to see if you had a chance to review the project document I sent yesterday. Let me know if you have any questions.",
    "Hi {name}, the meeting tomorrow has been moved to 10am instead of 9am. Same conference room. See you there.",
    "Hey {name}, thanks for your help with the report last week. Looking forward to working with you again.",
    "Hi {name}, attached is the agenda for Thursday's team meeting. Please add any topics you'd like to discuss.",
    "Hi {name}, here is the link to the shared document we talked about: {link}. Let me know what you think.",
    "Hi {name}, just a reminder that your subscription renews next month. No action needed, this is just a heads up.",
    "Hi {name}, I reviewed the budget spreadsheet and left some comments. Could we set up a quick call this week?",
    "Hi {name}, welcome to the team! Your laptop and login details will be ready on your first day.",
]


def build_dataset():
    rows = []

    for template in phishing_templates:
        for _ in range(8):
            company = random.choice(companies)
            link = random.choice(fake_links)
            text = template.format(company=company, link=link)
            rows.append((text, "phishing"))

    for template in legit_templates:
        for _ in range(8):
            name = random.choice(names)
            link = random.choice(normal_links)
            try:
                text = template.format(name=name, link=link)
            except KeyError:
                text = template.format(name=name)
            rows.append((text, "legitimate"))

    random.shuffle(rows)
    return rows


def save_to_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email_text", "label"])
        for text, label in rows:
            writer.writerow([text, label])


if __name__ == "__main__":
    dataset = build_dataset()
    save_to_csv(dataset, "data/emails.csv")
    print(f"Created data/emails.csv with {len(dataset)} emails.")