import re


supplier_regex = r""
content_regex = r""
bill_ladding_regex = r'BO[LI]-[0-9]+'
shipping_line_regex =r'[Cc]arrier[\s+]?[Nn]ame[\s+]?[.]+[\s+]?:[\s+].*[\s+]?[\n+]?Truck[\s+]?No:'
container_regex = r'[Cc]ontainer number[\s+]?[.]:[\s+]?[A-Z]+[\s+]?[0-9]+-[0-9]'
product_number_regex = r'P0[\s+]?#[\s+]?[0-9]+'
invoice_number_regex = r'[0-9]+/[0-9]+/[0-9]+[\s+]?[A-Za-z0-9_]+'


supplier_sample = "SELLER (Name, full address. country)\n\
S.M.JALEEL AND CO. LTD\n\
OTAHEITE INDUSTRIAL ESTATE,\n\
SOUTH OROPOUCHE.\n\
TRINIDAD W.|.\n\n\n\`
CONSiGNEE (Name, full address, country)"
supplier_sample2 = "SELLER (Name. full address, country)\nS.M.JALEEL AND CO. LTD\n\
OTAHEITE INDUSTRIAL ESTATE,\nSOUTH OROPOUCHE.\nTRINIDAD WJ.\n\n\n\
CONSIGNEE (Name, full address, country)\n"

content_sample = "NO 8 KIND SPECIFlCATION 0F COMMODITIES NET QUANTITY UNIT PRICE\n\
OF PKGE. ( IN CODE AND] OR IN FULL) WEiGHT USD\n\
Kg.\n\
2 X 40 FT CONTAINER\n\
7938 cs. 24 X ZOOML FRUTA K/KIDZ ASSORTED FLAVOUR 4238832 7938_000 , 24.290.28\n\n\n\
IT [8 HEREBY CERTIFIED THAT THIS INVOICE SHOWS"
content_sample2 = "No & KIND SPECIFICATION 0F COMMODITIES NET QUANTITY UNIT PRICE AMOUNT\n\
OF PKGE. ( EN CODEAND.‘ OR IN FULL) WEIGHT USD\n\
Kg.\n\
2 X 40 FT CONTAINER\n\
7938 cs. 24 X ZOOML FRUTA K/KIDZ ASSORTED FLAVOUR 4233392 7933000 24,290.28\n\
24,290.28\n\
EX-FACTORY 24,290.28\n
'ACKAGING 1,007.50\n\
IT iS HEREBY CERTIFIED THAT THIS INVOICE SHOWS"

bl_sample = "Bill of lading numben: BOL—00049475"
bl_sample2 = "Bill of lading number: BOL-00049591"

ship_line_sample = "SHIP TO > Carrier name ' SeaBoard Marine"
ship_line_sample2 = "Carrier name ...... : SeaBoard Marine"

contain_sample = "Container number .: SMLU 792387-7"
contain_sample2 = "' T. Geddes Grant Container number .: SMLU 786320-6"

po_sample = "P0 # 23246"
po_sample2 = "PO # 23246"

invoice_sample = "2017/06/22 SMJPM19588J"
invoice_sample2 = "2017106I22 SMJPM19588J"
