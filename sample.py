import re
import pytesseract
import argparse
from PIL import Image

##Product number
# regex = r"P0[\s+]?#[\s+]?[0-9]+"
# matches = re.findall(regex, "P0 # 2345 P0 #456")
# for match in matches:
#     print "Match: %s" % (match)

##Invoice number
# regex = r"[0-9]+/[0-9]+/[0-9]+[\s+]?[A-Za-z0-9_]+"
# matches = re.findall(regex, "S.M.JALEEL AND CO. LTD 2017/06/22 SMJPM19588J 40019588 the pop and mom shop")
# for match in matches:
#     print "Match: %s" % (match)

##Shipping line
# regex = r"[Cc]arrier[\s+]?[Nn]ame[\s+]?[.]+[\s+]?:[\s+].*[\s+]?[\n+]?Truck[\s+]?No:"
# matches = re.findall(regex, "carrier name ...... : SeaBoard Marine\n\nTruck No:")
# for match in matches:
#     print "Match: %s" % (match)
# tmp = match.split("\n")
# print("")
# shipping_line= tmp[0].split(" :")[1].lstrip(" ")
# print(shipping_line)

##Container Number
# regex = r"[Cc]ontainer number[\s+]?[.]:[\s+]?[A-Z]+[\s+]?[0-9]+-[0-9]"
# matches = re.findall(regex, "Container number .: SMLU 786320-6")
# for match in matches:
#     print "Match: %s" % (match)
# tmp = match.split(":")[-1].lstrip(" ")
# carrier_number = "".join(tmp.split(" "))
# print(carrier_number)


##Bill ladding number
# regex = r'[\s+]?["+]?[\s+]?.*BO[LI]-[0-9]+'
# regex = r'BO[LI]-[0-9]+'
# matches = re.findall(regex, '""""""" Bill of lading numbeI: BOL-00049475')
# for match in matches:
#     print "Match: %s" % (match)
# print(match)
#
# ##Supplier
# regex = r'SELLER.*?[\d+]/?[\d+]/?[\d+][\s+]?\n'
# matches = re.findall(regex, 'SELLER (Name, run address. country) INVOICE DATE ANDVNO. SMJ PROCUREMENT 8. MARKETING ORDER NO:\
# S.M.JALEEL AND CO. LTD \n')
# for match in matches:
#     print "Match: %s" % (match)
def main():
    try:
    	parser = argparse.ArgumentParser(description= 'png_file for parsing')
    	parser.add_argument('png_file' ,type=str, help='a page of the pdf file')
    	command_args = parser.parse_args()
    except:
    	print("Try this "+ 10*"-" + "> python pdf_reader.py <png_file>")
    	return -1
    png_file = "./png_folder/"+command_args.png_file

    image_text = pytesseract.image_to_string(Image.open(png_file))
    print(image_text)



if __name__ == "__main__":
    main()
