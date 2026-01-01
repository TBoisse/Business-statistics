class Transaction():
    def __init__(self, title, date, status, price, tr_type = "unknown"):
        self.title = title
        self.date = date
        self.status = status
        self.price = price
        self.type = tr_type

    def __repr__(self):
        return f"{self.date} : {self.title} [{self.price}]"
    

def write_transaction(f, transactions : list[Transaction]):
    for transaction in transactions:
        f.write(f"{transaction.date};{transaction.title};{transaction.price};{transaction.type}\n")
    