import os
import unittest

from reportlab.lib import colors

from src.pydf_invoice.models import ClientInfo, Item, InvoiceInfo, CompanyInfo
from src.pydf_invoice.pdf_invoice import PDFInvoice


class TestPDFInvoice(unittest.TestCase):

    def setUp(self) -> None:
        self.files_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_generated')

    def test_PDFInvoice(self):
        file_path = os.path.join(self.files_directory, 'pdf_invoice.pdf')

        if os.path.exists(file_path):
            os.remove(file_path)

        client_info = ClientInfo(
            "Wassim CHAGUETMI",
            "0799136332",
            "Sidi Embarek El Harrach",
            "FR01256413564",
            "QSDAZ65465132",
            "SDQSDFQFSQ654981",
            "145875646123534213"
        )

        items = [
            Item("Produit1", "12", "15.00", "600.00"),
            Item("Produit1", "12", "15.00", "600.00"),
            Item("Produit1", "12", "15.00", "600.00"),
            Item("Produit1", "12", "15.00", "600.00"),
        ]

        invoice_info = InvoiceInfo(
            "22/123",
            "28/07/2022 14:06",
            items,
            ["Designation", "Quantité", "Prix Unitaire", "Total"],
            "150.00",
            "50.00",
            "250.00",
            [colors.darkgrey, colors.lightgrey],
            "Colissimo",
            "50.00"
        )
        company_info = CompanyInfo(
            "Bandido",
            "Ecole sidi embarek batiment B N°7 El Harrach, Alger, 16051",
            "0899458554",
            "Bandidofrance@google.com",
            "123654789",
            "654231654",
            "654789654"
            "654987654",
            "654654894",
            "65432165465",
            "65749876546465",
            "assets/logo-blanc.png",
            "assets/qr_code.png",
        )

        invoice = PDFInvoice(
            file_path,
            client_info,
            invoice_info,
            company_info,
            "Test Title",
            watermark="assets/logo-blanc-not-transp.png"
        )

        invoice.create()
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
