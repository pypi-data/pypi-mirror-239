import csv
import re
import random

from decimal import Decimal as D

from ofxstatement import statement
from ofxstatement.statement import generate_transaction_id
from ofxstatement.statement import generate_unique_transaction_id

from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin

class BsicLyPlugin(Plugin):
    """BSIC Plugin
    """

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=self.settings.get("charset", "UTF-8"))
        parser = BsicLyParser(f)
        return parser

class BsicLyParser(CsvStatementParser):
    date_format = "%d/%m/%Y"
    mappings = {
        # 'check_no': 3,
        'date': 0,
        # 'refnum': 3,
        'memo': 2,
        'amount': 3,
        #'id': 3
    }
    unique_id_set = set()

    def parse(self):
        """Main entry point for parsers

        super() implementation will call to split_records and parse_record to
        process the file.
        """

        stmt = super(BsicLyParser, self).parse()
        total_amount = sum(sl.amount for sl in stmt.lines)
        stmt.end_balance = D(stmt.start_balance) + total_amount
        stmt.start_date = min(sl.date for sl in stmt.lines)
        statement.recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """

        reader = csv.reader(self.fin, delimiter=',')
        return reader

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        if not self.statement.currency:
            # We probably are on the first line
            self.statement.currency = re.search(r'\((.*?)\)', line[5]).group(1)
            return None

        if line[0] == "Date" or line[0] == "Total":
            # Header line
            return None

        amount = ""
        line[3] = line[3].replace(' ', '')
        line[4] = line[4].replace(' ', '')
        line[5] = line[5].replace(' ', '')
        if len(line[3]):
            tx_type = "DEBIT"
            amount = "-" + line[3]
        elif len(line[4]):
            tx_type = "CREDIT"
            amount = line[4]

        if not self.statement.start_balance:
            self.statement.start_balance = D(line[5]) - D(amount)

        if amount:
            line[3] = amount

        stmtline = super(BsicLyParser, self).parse_record(line)
        stmtline.trntype = tx_type
        stmtline.id = generate_unique_transaction_id(stmtline, self.unique_id_set)

        return stmtline