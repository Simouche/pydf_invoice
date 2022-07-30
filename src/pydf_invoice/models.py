from dataclasses import dataclass
from io import BytesIO
from typing import Union


@dataclass
class ClientInfo:
    """
    Client information
    """
    name: str
    phone: str = None
    address: str = None
    tva: str = None
    nif: str = None
    nis: str = None
    rc: str = None


@dataclass
class Item:
    """
    Product/Item information
    """
    name: str
    quantity: str
    unit_price: str
    total: str

    def to_row_data(self):
        return [self.name, self.quantity, self.unit_price, self.total]


@dataclass
class InvoiceInfo:
    number: str
    date: str
    data: list[Item]
    table_cols: list[str]
    total_ht: str
    total_tva: str
    total_ttc: str
    rows_colors: list = None
    delivery_company: str = None
    delivery_cost: str = None


@dataclass
class BankAccount:
    rib: str
    bank_name: str
    bank_address: str = None


@dataclass
class CompanyInfo:
    name: str
    address: str
    phone: list[str]
    email: str
    siret: str = None
    tva: str = None
    nif: str = None
    nis: str = None
    rc: str = None
    rcs: str = None
    logo: Union[str, BytesIO] = None
    qr_code: Union[str, BytesIO] = None
    bank_account: BankAccount = None
