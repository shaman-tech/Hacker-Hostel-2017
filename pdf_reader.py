"""
Created by: 2017 Hacker Hostel Fellows
Version: Python 2.17.13
Description:
	* Open a pdf file, create a png file for each page and
	  extract the information needed from each page
	  to populate a csv file.
"""
from wand.image import Image as wand_image
from PIL import Image as pillow_image
from PIL import ImageEnhance,ImageStat,ImageFilter
import argparse
import os
from time import time
from multiprocessing import Pool , cpu_count
import re
import datetime
import pytesseract

resolution = 350
page_info = "page_info.txt"
caricom_heading = r'CARICOM[\s+]?\(CARIBBEAN[\s+]?COMMON[\s+]?MARKET\)'
bill_ladding_heading = r'BILL[\s+]?OF[\s+]?LADING'
time_date = datetime.datetime.now()
report_time = "{}/{}/{}".format(time_date.day,time_date.month,time_date.year)
supplier_regex = r""
content_regex = r""
bill_ladding_regex = r'BO[LI]-[0-9]+'
shipping_line_regex =r'[Cc]arrier[\s+]?[Nn]ame[\s+]?[.]+[\s+]?:[\s+].*[\s+]?[\n+]?Truck[\s+]?No:'
container_regex = r'[Cc]ontainer number[\s+]?[.]:[\s+]?[A-Z]+[\s+]?[0-9]+-[0-9]'
product_number_regex = r'P0[\s+]?#[\s+]?[0-9]+'
invoice_number_regex = r'[0-9]+/[0-9]+/[0-9]+[\s+]?[A-Za-z0-9_]+'

## Miscellanous Functions
def vary_img_options(img, option):
	"""
	description: Performs digital image processing on the image passed in the
	arguements with a option that is also passed as a parameter. The acceptable
	options are color, contrast, bright ( brightness), sharp ( sharpness )
	parameters: Pillow.Image instance and string
	returns: Nothing
	"""
	if option.lower() == "color":
		enhancer = ImageEnhance.Color(img)
	elif option.lower() == "contrast":
		enhancer = ImageEnhance.Contrast(img)
	elif option.lower() == "bright":
		enhancer = ImageEnhance.Brightness(img)
	elif option.lower() == "sharp":
		enhancer = ImageEnhance.Sharpness(img)
	for i in range(5):
		factor = i / 4.0
		try:
			enhancer.enhance(factor).show("Contrast %f" % factor)
		except:
			break

def print_stats(img):
	"""
	description:  prints out the statistic of an image
	parameters:	PIL.Image.Stat object
	returns: Nothing
	"""
	img_stat = ImageStat.Stat(img)
	print(img_stat.extrema)#Min/max values for each band in the image.
	print(img_stat.count)#Total number of pixels for each band in the image.
	print(img_stat.sum)#Sum of all pixels for each band in the image.
	print(img_stat.sum2)#Squared sum of all pixels for each band in the image.
	#Average (arithmetic mean) pixel level for each band in the image.
	print(img_stat.mean)
	print(img_stat.median)#Median pixel level for each band in the image.
	print(img_stat.rms)#RMS (root-mean-square) for each band in the image.
	print(img_stat.var)#Variance for each band in the image.
	print(img_stat.stddev)#Standard deviation for each band in the image.

def apply_filters(img):
	"""
	description: Performs image filtering on specified Image
	Type of Filters:
		* BLUR
		* CONTOUR
		* DETAIL
		* EDGE_ENHANCE
		* EDGE_ENHANCE_MORE
		* EMBOSS
		* FIND_EDGES
		* SMOOTH
		* SMOOTH_MORE
		* SHARPEN
	parameters: Pillow.Image instance
	returns: Filtered Pillow.Image
	"""
	img2 = img.filter(ImageFilter.MinFilter(3))
	img2 = img2.filter(ImageFilter.SHARPEN)
	img2 = img2.filter(ImageFilter.DETAIL)
	return img2

def create_png_files(filename,pool):
	"""
	description: Creates a png_file for each page in the specified pdf file
	parameters: string
	returns: list of png files
	"""
	png_list = []
	print(5*" " + "Reading PDF file")
	image_pdf = wand_image(filename="./{}".format(filename), resolution=resolution)
	print(5*" " + "Finish Reading PDF file")
	print(5*" " + "Converting PDF to list of PNG files")
	image_png = image_pdf.convert('png')
	print(5*" " + "Finished converting PDF file to list of PNG files")
	if not os.path.exists('./png_folder'):
		os.system("mkdir ./png_folder")
	for index,img in enumerate(image_png.sequence):
		img_page = wand_image(image=img,resolution=resolution)
		img_page.save(filename="./png_folder/png_file{}.png".format(index+1))
		png_list.append("./png_folder/png_file{}.png".format(index+1))
	return png_list

def image_to_text(png_file):
	caricom_matches = []
	ladding_matches = []
	txt = pytesseract.image_to_string(pillow_image.open(png_file))
	caricom_matches = re.findall(caricom_heading,txt)
	ladding_matches = re.findall(bill_ladding_heading,txt)
	if len(caricom_matches) > 0:
		print("This page contains the caricom heading")
		print("##############################\n\n")
		print(txt)
	elif len(ladding_matches) > 0:
		print("This page contains the bill ladding heading")
		print("##############################\n\n")
		print(txt)
	else:
		print("Does not contain the caricom heading or bill ladding heading")

def main():
	total_time = 0
	final_text = []
	#clears page_info.txt
	with open(page_info,"w") as fout:
		fout.write("")
	print("Your machine has {} computer processor units (CPU)".format(cpu_count()))
	pool = Pool(processes = cpu_count())
	try:
		parser = argparse.ArgumentParser(description= 'pdf file used to \
		populate tgg csv file')
		parser.add_argument('pdf_file', type=str,
		                    help='a pdf that contains shipping information')

		command_args = parser.parse_args()
	except:
		print("Try this "+ 10*"-" + "> python pdf_reader.py <pdf_file>")
		return -1
	pdf_file = command_args.pdf_file
	start_time = time()
	print("Creating png files")
	png_list = create_png_files(pdf_file,pool)
	print("This create_png_files function took about {} seconds ".format(time()-start_time))
	total_time = total_time + time()-start_time
	start_time = time()
	final_text = pool.map(image_to_text,png_list[0:5])
	print("This populate_file function took about {} seconds ".format(time()-start_time))
	total_time = total_time + time()-start_time
	print("Your program runtime was {} seconds".format(total_time))
	pool.close()
	pool.join()

if __name__ == "__main__":
	main()
