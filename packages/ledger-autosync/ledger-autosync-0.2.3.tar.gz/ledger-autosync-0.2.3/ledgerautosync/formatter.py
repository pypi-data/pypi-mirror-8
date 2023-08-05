# Copyright (c) 2013, 2014 Erik Hetzner
# 
# This file is part of ledger-autosync
#
# ledger-autosync is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# ledger-autosync is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ledger-autosync. If not, see
# <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from decimal import Decimal
from ofxparse.ofxparse import Transaction, InvestmentTransaction
from ledgerautosync import EmptyInstitutionException

AUTOSYNC_INITIAL = "autosync_initial"
ALL_AUTOSYNC_INITIAL = "all.%s"%(AUTOSYNC_INITIAL)

def clean_ofx_id(ofxid):
    ofxid = ofxid.replace('/', '_')
    ofxid = ofxid.replace('$', '_')
    ofxid = ofxid.replace(' ', '_')
    return ofxid

class Formatter(object):
    def __init__(self, account, name, indent=4, ledger=None, fid=None):
        self.acctid=account.account_id
        if fid is not None:
            self.fid = fid
        else:
            if account.institution is None:
                raise EmptyInstitutionException("Institution provided by OFX is empty and no fid supplied!")
            else:
                self.fid=account.institution.fid
        self.name = name
        self.lgr = ledger
        self.indent = indent
        self.currency = account.statement.currency
        self.currency = self.currency.upper()
        if self.currency == "USD": self.currency = "$"

    def mk_ofxid(self, txnid):
        return clean_ofx_id("%s.%s.%s"%(self.fid, self.acctid, txnid))

    def mk_dynamic_account(self, txn, exclude):
        if self.lgr is None:
            return "Expenses:Misc"
        else:
            payee = self.format_payee(txn)
            account = self.lgr.get_account_by_payee(payee, exclude)
            if account is None:
                return "Expenses:Misc"
            else:
                return account

    def format_amount(self, amount, reverse=False, unlimited=False):
        if unlimited:
            amt = str(abs(amount))
        else:
            amt = "%0.2f"%(abs(amount))
        if amount.is_signed() != reverse:
            return "-%s%s"%(self.currency, amt)
        else:
            return "%s%s"%(self.currency, amt)

    def format_payee(self, txn):
        payee = None
        memo = None
        if (hasattr(txn, 'payee')): payee = txn.payee
        if (hasattr(txn, 'memo')): memo = txn.memo
        
        if (payee is None) and (memo is None):
            return "UNKNOWN"
        if (payee is None) or txn.memo.startswith(payee):
            return memo
        elif (memo is None) or payee.startswith(memo):
            return payee
        else:
            return "%s %s"%(payee, memo)

    def format_date(self, date):
        return date.strftime("%Y/%m/%d")

    def format_balance(self, statement):
        retval = ""
        if (hasattr(statement, 'balance_date')):
            date = statement.balance_date
        else:
            date = statement.end_date
        if (hasattr(statement, 'balance')):
            retval += "%s * --Autosync Balance Assertion\n"%(self.format_date(date))
            retval += self.format_txn_line(self.name, self.format_amount(Decimal("0")), " = %s"%(self.format_amount(statement.balance)))
        return retval

    def format_initial_balance(self, statement):
        retval = ""
        if (hasattr(statement, 'balance')):
            initbal = statement.balance
            for txn in statement.transactions:
                initbal -= txn.amount
            retval += "%s * --Autosync Initial Balance\n"%(self.format_date(statement.start_date))
            retval += "%s; ofxid: %s\n"%(" "*self.indent, self.mk_ofxid(AUTOSYNC_INITIAL))
            retval += self.format_txn_line(self.name, self.format_amount(initbal))
            retval += self.format_txn_line("Assets:Equity", self.format_amount(initbal, reverse=True))
        return retval

    def format_txn_line(self, acct, amt, suffix=""):
        space_count = 52 - self.indent - len(acct) - len(amt)
        if space_count < 2:
            space_count = 2
        return "%s%s%s%s%s\n"%(" "*self.indent, acct, " "*space_count, amt, suffix)

    def format_txn(self, txn):
        retval = ""
        ofxid = self.mk_ofxid(txn.id)
        if isinstance(txn, Transaction):
            retval += "%s %s\n"%(self.format_date(txn.date), self.format_payee(txn))
            retval += "%s; ofxid: %s\n"%(" "*self.indent, ofxid)
            retval += self.format_txn_line(self.name, self.format_amount(txn.amount))
            retval += self.format_txn_line(self.mk_dynamic_account(txn, exclude=self.name), self.format_amount(txn.amount, reverse=True))
        elif isinstance(txn, InvestmentTransaction):
            if txn.settleDate is not None:
                retval = "%s=%s %s\n"%(txn.tradeDate.strftime("%Y/%m/%d"), txn.settleDate.strftime("%Y/%m/%d"), txn.memo)
            else:
                retval = "%s %s\n"%(txn.tradeDate.strftime("%Y/%m/%d"), self.format_payee(txn))
            retval += "%s; ofxid: %s\n"%(" "*self.indent, ofxid)
            retval += self.format_txn_line(acct=self.name, amt=str(txn.units), 
                                           suffix=" %s @ %s"%(txn.security, self.format_amount(txn.unit_price, unlimited=True)))
            retval += self.format_txn_line(self.name, self.format_amount(txn.units * txn.unit_price, reverse=True))
        return retval
