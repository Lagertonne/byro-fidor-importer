from byro.bookkeeping.signals import process_csv_upload, process_transaction

from byro.bookkeeping.models import (
    Account, AccountCategory, Booking, Transaction,
)

from byro.members.models import Member

from django.dispatch import receiver
from django.utils.timezone import now
from byro.bookkeeping.special_accounts import SpecialAccounts
from datetime import datetime
from decimal import Decimal
import csv
import re


@receiver(process_csv_upload)
def process_fidor_csv(sender, **kwargs):
    source = sender
    sender.source_file.open(mode='r')
    csv_reader = csv.DictReader(sender.source_file, delimiter=";")
    line_count = 0
    transactions = []
    booking_timestamp = now()
    for row in csv_reader:
        # Filter relevant details from csv
        memo = re.split('BIC: \w+ ', row["Beschreibung"])[-1]
        value_datetime = datetime.strptime(row["Datum"], '%d.%m.%Y')
        amount = Decimal(row["Wert"].replace('.', '').replace(',', '.'))
        if (row["Beschreibung"] == "Kontofuehrung" or row["Beschreibung"] == "Aktivitaetsbonus"):
            receiver_or_sender = "Fidor"
        else:
            receiver_or_sender = re.split("((Absender)|(Empfaenger))(.*)(, IBAN.)\s+", row["Beschreibung2"])[2]

        account = SpecialAccounts.bank

        # Negative = outgoing = c(redit)
        # Positive = incoming = d(ebit)

        if amount < 0:
            amount = -amount
            booking_type = 'c'
        else:
            booking_type = 'd'

        params = dict(
            memo=memo,
            amount=amount,
            importer='fidor_csv_importer'
        )

        if booking_type == 'c':
            params['credit_account'] = account
        else:
            params['debit_account'] = account


        data = {
            'csv_line': row,
            'other_party': receiver_or_sender,
        }

        # Does the booking already exist?
        booking = account.bookings.filter(
            transaction__value_datetime=value_datetime,
            **params
        ).first()

        # Noooo? Then create one.
        if not booking:
            t = Transaction.objects.create(
                value_datetime=value_datetime,
                user_or_context='Fidor CSV import'
            )
            Booking.objects.create(
                transaction=t,
                booking_datetime=booking_timestamp,
                source=source,
                data=data,
                **params
            )

    return True

@receiver(process_transaction)
def match_transaction(sender, signal, **kwargs):
    transaction = sender

    if transaction.is_read_only:
        return False
    if transaction.is_balanced:
        return False

    match = re.search("NLL[0-9]{3}", transaction.find_memo().upper())
    
    if match:
        uid = match.group(0).upper()
    else:
        return False

    member = None

    try:
        member = Member.objects.get(number=uid)
    except Member.DoesNotExist:
        return False
    
    balances = transaction.balances
    data = {
        'amount': abs(balances['debit'] - balances['credit']),
        'account': SpecialAccounts.fees_receivable,
        'user_or_context': 'Fidor Auto-Matcher',
        'member': member,
    }
    if balances['debit'] > balances['credit']:
        transaction.credit(**data)
    else:
        transaction.debit(**data)

    return True
