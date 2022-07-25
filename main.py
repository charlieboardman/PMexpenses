#This project will check the an email inbox which is set up to watch for emails from people with pictures of their receipts and their descriptions of the expense. The program is set up to watch for emails that are sent as SMS messages.

import time

class expense:
    def __init__(self,photo,description,USD_or_MXN,amount_spent,exchange_rate,account):
        self.photo = photo
        self.description = description
        self.USD_or_MXN = USD_or_MXN
        self.amount_spent = amount_spent
        self.exchange_rate = exchange_rate
        self.account = account

while True:
    time.sleep(60) #This program will run once every minute to check the email inbox
    unreads = get_unread_messages() #Check for any messages flagged as unread and return them as a list
    if unreads: #If there are any unread message objects recieved from the get_unread_messages() function
        for message in unreads:
            user = get_user(message) #get_user() checks the email address the message was sent from and uses a dictionary to identify the person who sent the expense
            message_type = ID_message_type(message) #determine if the message coming in is reporting a transaction or requesting a copy of the user's report to date
            if message_type == 'report':
                photo = get_photo(message) #get_photo returns an image object of the photo of the receipt taken by the person who sent the email
                description = get_description(message) #get_description gets the description of the expense taken from the text attachment of the message
                USD_or_MXN = get_currency(message) #get_currency flags if the expense is in USD or MXN from the text attachment of the message
                amount_spent = get_amount(message) #get_ammount grabs the number in pesos or dollars from the text attachment of the message
                exchange_rate = get_exchange_rate(message,USD_or_MXN) #gets the exchange rate from the text attachment of the message if the purchase was in pesos
                account = get_account(message) #gets the account from the message body
                validity = check_valid(photo,description,USD_or_MXN,amount_spent,exchange_rate) #Check that all parameters were identified correctly
                if validity == 'good':
                    write_to_report(user,photo,description,USD_or_MXN,amount_spent,exchange_rate, account) #writes the expense to the last line on the user's active report. If no current report exists, initate one. account may be blank 
                elif validity == 'errors_present':
                    send_error_message(validity,user) #send the user an error message email based on the validity report
                    mark_message_read(message) #mark the message read so that it will not error out again and a new message must be sent
            elif message_type == 'request_simple':
                send_report(user) #Send the user a copy of their report and reciepts so far
            elif message_type == 'request_and_archive':
                send_report(user) #Send the user a copy of their report and reciepts so far
                archive_report(user) #archive the user's current report, clearing if off of current status
            elif message_type == 'replace': #if a user makes edits to their expense report, replace the current version stored on the server with the updated version
                replace_current_report(user,message) #pull the new expense report from the message
            mark_message_read(message) #marks the message as read in the inbox
    user = message_type = photo = description = USD_or_MXN = amount_spent = exchange_rate = 0

    #idea, make one get_data() function that returns photo, description, USD_or_MXN, etc