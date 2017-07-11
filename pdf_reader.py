"""
Created by: 2017 Hacker Hostel Fellows
Version: Python 2.17.13
Description:
	* Open a pdf file, create a png file for each page and
	  extract the information needed from each page
	  to populate a csv file.
"""
from wand.image import Image
from wand.sequence import Sequence
from wand.sequence import SingleImage
from PIL import Image as PI
from PIL import ImageEnhance,ImageStat,ImageFilter
import pyocr
import pyocr.builders
import io
import argparse
import optparse
import os
from time import time
from multiprocessing import Pool , cpu_count
import random as rand

rand.seed(42)
page_info = "page_info.txt"

# class Image_Page(SingleImage):
# 	def __init__(self):
# 		pass
# 	def image_save(self, wand_image):
# 		index = rand.randint(0,1000)
# 		img_page = Image(image=wand_image)
# 		filename = "./png_folder/png_file{}.png".format(index)
# 		img_page.save(filename=filename)
# 		return filename
# 	def go(self,image_sequence):
# 		p = Pool(4)
# 		png_list = p.map(self, image_sequence)
# 		return png_list
# 	def __call__(self, wand_image):
# 		return self.image_save(wand_image)
#
# 	def __del__(self):
# 		pass


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

# def create_images(png_list):
# 	"""
# 	description: Given the png_list passed in the parameter this function
# 	will apply image filter to improve the pdf page images
# 	parameters: a list of png files
# 	returns: a list of image blobs
# 	"""
# 	blob_list = []
# 	if not os.path.exists("./update_pngFiles"):
# 		os.system("mkdir update_pngFiles")
# 	for index,png_file in enumerate(png_list):
# 		img = PI.open(png_file)
# 		# update_img = apply_filters(img)
# 		img.save("./update_pngFiles/png_file{}.png".format(index+1))
# 		blob_list.append("./update_pngFiles/png_file{}.png".format(index+1))
# 	return blob_list

def create_png_files(filename,pool):
	"""
	description: Creates a png_file for each page in the specified pdf file
	parameters: string
	returns: list of png files
	"""
	png_list = []
	print(5*" " + "Reading PDF file")
	image_pdf = Image(filename="./{}".format(filename), resolution=300)
	print(5*" " + "Finish Reading PDF file")
	print(5*" " + "Converting PDF to list of PNG files")
	image_png = image_pdf.convert('png')
	print(5*" " + "Finished converting PDF file to list of PNG files")
	if not os.path.exists('./png_folder'):
		os.system("mkdir ./png_folder")
	start_time = time()
	for index,img in enumerate(image_png.sequence):
		img_page = Image(image=img)
		img_page.save(filename="./png_folder/png_file{}.png".format(index+1))
		png_list.append("./png_folder/png_file{}.png".format(index+1))
	print(5*" " + "Creating png_files took about {} seconds ".format(time()-start_time))
	return png_list

# def save_image(wand_image):
# 	index = rand.randint(0,1000)
# 	img_page = Image(image=wand_image)
# 	filename = "./png_folder/png_file{}.png".format(index)
# 	img_page.save(filename=filename)
# 	return filename

## multi-threading
def make_imageBlob(png_file):
	"""
	description:
	parameters:
	returns:
	"""
	img_page = Image(filename=png_file)
	string_text = img_page.make_blob('png')
	return string_text

def populate_file(req_image):
	# tool to create image to string
	tool = pyocr.get_available_tools()[0]
	# english is the chosen language
	lang = tool.get_available_languages()[0]
	txt = tool.image_to_string(PI.open(io.BytesIO(req_image)),
	        lang=lang,
	        builder=pyocr.builders.TextBuilder())
	return txt.encode('ascii', 'ignore')

def write_content(page_line):
	with open(page_info,"a") as fout:
		if page_line != "":
			fout.write("{}\n".format(page_line))


def main():
	total_time = 0
	#clears page_info.txt
	with open(page_info,"w") as fout:
		fout.write("")

	print("Your machine has {} computer processor units (CPU)".format(cpu_count()))
	pool = Pool(processes = cpu_count())
	image_textFile = "image_textFile.txt"
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
	# blob_list = create_images(png_list) ## Uncomment if need image processing
	req_image = []
	print("Making image blobs")
	start_time = time()
	req_image = pool.map(make_imageBlob,png_list)
	print("This make_imageBlob function took about {} seconds ".format(time()-start_time))
	total_time = total_time + time()-start_time
	print("Changing the image to text")
	final_text = []
	start_time = time()
	final_text = pool.map(populate_file,req_image)
	print("This populate_file function took about {} seconds ".format(time()-start_time))
	total_time = total_time + time()-start_time
	print("Your program runtime was {} seconds".format(total_time))
	for page_text in final_text:
		pool.map(write_content, page_text.split("\n"))
	print("Finish writing image content to page_info.txt")
	pool.close()
	pool.join()

if __name__ == "__main__":
	main()
