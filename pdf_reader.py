"""
Created by: 2017 Hacker Hostel Fellows
Version: Python 2.17.13
Description:
	* Open a pdf file, create a png file for each page and
	  extract the information needed from each page
	  to populate a csv file.
"""
from wand.image import Image
from PIL import Image as PI
from PIL import ImageEnhance,ImageStat,ImageFilter
import pyocr
import pyocr.builders
import io
import argparse
import optparse
import os
import time
from threading import Thread

## Miscellanous Functions
def vary_img_options(img,option):
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

def create_images(png_list):
	"""
	description: Given the png_list passed in the parameter this function
	will apply image filter to improve the pdf page images
	parameters: a list of png files
	returns: a list of image blobs
	"""
	blob_list = []
	if not os.path.exists("./update_pngFiles"):
		os.system("mkdir update_pngFiles")
	for index,png_file in enumerate(png_list):
		img = PI.open(png_file)
		# update_img = apply_filters(img)
		img.save("./update_pngFiles/png_file{}.png".format(index+1))
		blob_list.append("./update_pngFiles/png_file{}.png".format(index+1))
	return blob_list

#multi-threading
def create_png_files(filename):
	"""
	description: Creates a png_file for each page in the specified pdf file
	parameters: string
	returns: list of png files
	"""
	png_list = []
	image_pdf = Image(filename="./{}".format(filename), resolution=300)
	image_png = image_pdf.convert('png')
	if not os.path.exists('./png_files'):
		os.system("mkdir ./png_files")
	for index,img in enumerate(image_png.sequence):
	    img_page = Image(image=img)
	    img_page.save(filename="./png_files/image_{}.png".format(index+1))
	    png_list.append("./png_files/image_{}.png".format(index+1))
	return png_list

## multi-threading
def make_blob(blob_list):
	"""
	description: Given the list of png files this function will create image
	blobs which converts the image into byte string and appends them to a list
	parameters: a list of png files
	returns: a list of byte strings
	"""
	req_image = []
	for blob in blob_list:
		img_page = Image(filename=blob)
		req_image.append(img_page.make_blob('png'))
	return req_image

def main():
	# tool to create image to string
	tool = pyocr.get_available_tools()[0]
	# english is the chosen language
	lang = tool.get_available_languages()[0]
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
	png_list = create_png_files(pdf_file)
	blob_list = create_images(png_list)
	req_image = make_blob(blob_list)
	final_text = [ ]
	for img in req_image:
		txt = tool.image_to_string(
	        PI.open(io.BytesIO(img)),
	        lang=lang,
	        builder=pyocr.builders.TextBuilder())
		final_text.append(txt)
	print(final_text)

if __name__ == "__main__":
	main()
