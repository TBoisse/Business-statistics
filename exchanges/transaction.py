from _io import TextIOWrapper

class Transaction():
    """
    Transaction structure. Allow to effiently store a transaction.
    """
    def __init__(self, title : str, date : str, status : str, price : str, tr_type = "unknown"):
        """
        :param title: Title of the transaction.
        :type title: str
        :param date: Date of the transaction.
        :type date: str
        :param status: Status of the transaction (Processed, On going, ...)
        :type status: str
        :param price: Amount of the transaction.
        :type price: str
        :param tr_type: Type of transaction (Sale vs Purchase)
        """
        self.title = title
        self.date = date
        self.status = status
        self.price = price
        self.type = tr_type

    def __repr__(self):
        return f"{self.date} : {self.title} [{self.price}]"
    
def initiate_transaction(path : str):
    """
    Write the header of a csv file.
    
    :param path: Path to the csv file.
    :type path: str
    """
    with open(path, "w+") as f:
        f.write("date;title;price;type\n")

def write_transactions(f : TextIOWrapper, transactions : list[Transaction]):
    """
    Write transactions in a file.
    
    :param f: Text wrapper (Given by open)
    :type f: TextIOWrapper
    :param transactions: List of transactions.
    :type transactions: list[Transaction]
    """
    for transaction in transactions:
        f.write(f"{transaction.date};{transaction.title};{transaction.price};{transaction.type}\n")
    