
import pandas as pd
import json
import datetime

class ExpenseList:
    def __init__(self):
        f = open(r'test_case.json')
        content = f.read()
        a = json.loads(content)
        self.df = pd.DataFrame(a)
        self.records = self.df.to_dict('records')
        self.length = len(self.records)
        self.global_count = self.length

    def add_new_item(self, item_name, amount, category):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        self.records.append({
            'Index': str(self.global_count),
            'Item Name': item_name,
            'Amount': '$ ' + amount,
            'Category': category,
            'Timestamp': timestamp
        })
        self.length += 1
        self.global_count += 1
        return self.records
        