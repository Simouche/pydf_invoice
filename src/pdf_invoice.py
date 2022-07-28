from copy import deepcopy

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, TableStyle, Table, Spacer

from .models import ClientInfo, InvoiceInfo, CompanyInfo
from src import CENTER_BODY_TEXT, RIGHT_BODY_TEXT, LEFT_BODY_TEXT, RIGHT_HEADER_TEXT, LEFT_HEADER_TEXT, \
    CENTER_HEADER_TEXT


class PDFInvoice:

    def __init__(self, filename: str, client_info: ClientInfo, invoice_info: InvoiceInfo,
                 company_info: CompanyInfo, title: str = "", text_styles: dict = None, watermark: str = None, ):
        self.page_size = A4
        self.page_width = self.page_size[0]
        self.page_height = self.page_size[1]

        self.document_class = SimpleDocTemplate
        self.top_margin = inch / 3
        self.left_margin = inch
        self.right_margin = inch

        self.document = self.document_class(
            filename,
            title=title,
            pagesize=self.page_size,
            topMargin=self.top_margin,
            leftMargin=self.left_margin,
            rightMargin=self.right_margin,
        )

        self.height_between_elements = inch / 3
        self.client_infos = client_info
        self.invoice_info = invoice_info
        self.company_info = company_info
        self.watermark = watermark

        if text_styles is None:
            self._text_samples = getSampleStyleSheet()
            self._text_styles = {
                CENTER_BODY_TEXT: ParagraphStyle(CENTER_BODY_TEXT, parent=self._text_samples.get('Normal'),
                                                 alignment=TA_CENTER),
                LEFT_BODY_TEXT: ParagraphStyle(LEFT_BODY_TEXT, parent=self._text_samples.get('Normal'),
                                               alignment=TA_LEFT),
                RIGHT_BODY_TEXT: ParagraphStyle(RIGHT_BODY_TEXT, parent=self._text_samples.get('Normal'),
                                                alignment=TA_RIGHT),
                RIGHT_HEADER_TEXT: ParagraphStyle(RIGHT_HEADER_TEXT, parent=self._text_samples.get('Heading1'),
                                                  alignment=TA_RIGHT, fontSize=10),
                LEFT_HEADER_TEXT: ParagraphStyle(LEFT_HEADER_TEXT, parent=self._text_samples.get('Heading1'),
                                                 alignment=TA_LEFT, fontSize=10),
                CENTER_HEADER_TEXT: ParagraphStyle(CENTER_HEADER_TEXT, parent=self._text_samples.get('Heading1'),
                                                   alignment=TA_CENTER, fontSize=10),
            }

        self.dark_grey_color = deepcopy(colors.darkgrey)
        self.dark_grey_color.alpha = 0.7
        self.grey_color = deepcopy(colors.lightgrey)
        self.grey_color.alpha = 0.5
        self.story = []

    def draw_watermark(self, canvas: Canvas, _):
        """
        setup background image on all pages
        :param canvas:
        :param _:
        :return:
        """
        if self.watermark:
            canvas.saveState()
            canvas.drawImage(self.watermark, 100, 100, width=self.page_width - 200, height=self.page_height - 200)
            canvas.restoreState()

    def all_pages(self, canvas: Canvas, doc):
        self.draw_watermark(canvas, doc)

    def add_header(self):
        header_elements = []

        if self.company_info.logo:
            img = Image(self.company_info.logo, height=50, width=50)
            header_elements.append(img)

        header_texts = [
            [Paragraph(self.company_info.name, style=self._text_styles[CENTER_HEADER_TEXT])],
            [Paragraph(self.invoice_info.date, style=self._text_styles[RIGHT_BODY_TEXT])],
            [Paragraph(self.client_infos.name, style=self._text_styles[RIGHT_BODY_TEXT])],
        ]
        header_texts_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
        header_texts_table = Table(header_texts, style=header_texts_table_style)
        header_elements.append(header_texts_table)

        header_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (1, 0), (1, 0), 'TOP'),
        ])
        header_table = Table(
            [header_elements],
            colWidths=[(self.page_width / 2) - inch / 3, (self.page_width / 2) - inch / 3],
            style=header_table_style,
        )

        self.story.append(header_table)
        self.add_space()

    def add_space(self, width=None, height=None):
        self.story.append(Spacer(width or 0, height or self.height_between_elements))

    def add_footer(self):
        footer_elements = []
        if self.company_info.qr_code:
            img = Image(self.company_info.qr_code, height=100, width=100, )
            footer_elements.append(img)

        company_details = [[Paragraph(self.company_info.name, self._text_styles[CENTER_HEADER_TEXT])]]

        # <editor-fold desc="company info breakdown">
        if self.company_info.siret:
            company_details.append([
                Paragraph("Siret:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.siret, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.tva:
            company_details.append([
                Paragraph("N° TVA:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.tva, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.rcs:
            company_details.append([
                Paragraph("RCS:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.rcs, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.nif:
            company_details.append([
                Paragraph("NIF:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.nif, style=self._text_styles[RIGHT_BODY_TEXT])
            ])
        if self.company_info.nis:
            company_details.append([
                Paragraph("NIS:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.nis, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.rc:
            company_details.append([
                Paragraph("RC:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.rc, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.address:
            company_details.append([
                Paragraph("Adresse:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.address, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.phone:
            company_details.append([
                Paragraph("Téléphone:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.phone, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.email:
            company_details.append([
                Paragraph("Email:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.email, style=self._text_styles[RIGHT_BODY_TEXT])
            ])

        if self.company_info.bank_account:
            company_details.append([
                Paragraph("RIB:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(self.company_info.bank_account.rib, style=self._text_styles[RIGHT_BODY_TEXT])
            ])
        # </editor-fold>

        company_info_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('LINEABOVE', (0, 1), (1, 1), 0.25, colors.lightgrey),
            ('SPAN', (0, 0), (1, 0)),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (0, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ])

        company_info_table = Table(company_details, style=company_info_table_style, rowHeights=inch / 3,
                                   )
        footer_elements.append(company_info_table)

        footer_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
        footer_table = Table(
            [footer_elements],
            colWidths=[(self.page_width / 2) - inch / 3, (self.page_width / 2) - inch / 3],
            style=footer_table_style,
        )
        self.story.append(footer_table)
        self.add_space()

    def add_title(self):
        title = Paragraph(f"Facture N°: {self.invoice_info.number}", style=self._text_styles[CENTER_HEADER_TEXT])
        self.story.append(title)
        self.add_space(height=inch / 4)

    def add_data_table(self):
        data_table_style = TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                 self.invoice_info.rows_colors or [self.dark_grey_color, self.grey_color]),
            ]
        )

        data = [self.invoice_info.table_cols, ]
        for item in self.invoice_info.data:
            data.append(item.to_row_data())

        col_width = self.page_width - (self.right_margin + self.left_margin)
        data_table = Table(
            data,
            [(col_width / 6) * 3, col_width / 6, col_width / 6, col_width / 6],
            style=data_table_style,
            repeatRows=[0],
        )
        self.story.append(data_table)
        self.add_space(height=inch / 4)

    def add_invoice_totals(self):
        totals_texts = [
            [
                Paragraph("Total HT:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(f"{self.invoice_info.total_ht}€", style=self._text_styles[RIGHT_BODY_TEXT]),
            ],
            [
                Paragraph("TVA 20%:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(f"{self.invoice_info.total_tva}€", style=self._text_styles[RIGHT_BODY_TEXT]),
            ],
            [
                Paragraph(f"Livraison ({self.invoice_info.delivery_company or ''}):",
                          style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(f"{self.invoice_info.delivery_cost or 0}€", style=self._text_styles[RIGHT_BODY_TEXT]),
            ],
            [
                Paragraph("Total a payer:", style=self._text_styles[LEFT_HEADER_TEXT]),
                Paragraph(f"{self.invoice_info.total_ttc}€", style=self._text_styles[RIGHT_BODY_TEXT]),
            ],
        ]

        totals_table_style = TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (0, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ('BACKGROUND', (0, -1), (-1, -1), self.dark_grey_color),
        ])

        totals_table = Table(
            totals_texts,
            style=totals_table_style,
            colWidths=[inch * 2, inch],
            hAlign='RIGHT',
        )
        self.story.append(totals_table)
        self.add_space()

    def create(self):
        self.add_header()
        self.add_title()
        self.add_data_table()
        self.add_invoice_totals()
        self.add_footer()
        self.document.build(self.story, onFirstPage=self.all_pages, onLaterPages=self.all_pages)
