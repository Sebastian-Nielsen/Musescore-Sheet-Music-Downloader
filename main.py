from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

from PyPDF2 import PdfFileMerger         # pip install PyPDF2
from svglib.svglib import svg2rlg        # pip install svglib
from reportlab.graphics import renderPDF # pip install reportlab

import requests, re                      # pip install requests

############################################
##### ALTER THESE PARAMETERS ###############
############################################

DEBUG = True # Whether debug-focused comments should be printed to terminal not
PATH = 'C:/Users/sebas/PycharmProjects/andet/downloads'
FULL_PATH_TO_CHROMDRIVER_EXE = 'C:/Users/sebas/OneDrive/Dokumenter/chromedriver.exe'

URL_OF_MUSESCORE_PAGE = 'https://musescore.com/mysteryblackman/scores/5156653'  # Example 1
# URL_OF_MUSESCORE_PAGE = 'https://musescore.com/user/27048071/scores/4845903'  # Example 2

############################################
############################################
############################################


def getScoreLinks(url):
	browser = webdriver.Chrome(FULL_PATH_TO_CHROMDRIVER_EXE)
	document = browser.get(url)

	input("press enter when website has loaded")

	numOfPages = len(browser.find_elements_by_css_selector('body > '
	                                                   'div.js-page.react-container > '
	                                                   'div > section > section > '
	                                                   'main > div > :nth-child(3) > '
	                                                   'div > div > *'))

	linkTemplate = browser.find_elements_by_css_selector('img')[0].get_attribute('src')

	parts = re.split(r'score_\d\.svg', linkTemplate)

	links = []
	for i in range(numOfPages):
		links.append( f"{parts[0]}score_{i}.svg" )

	print(f"Links found: {links}")
	browser.close()

	return links

def downloadSVGs(links: [str]) -> [str]:
	"""
	:param links: List of SVG links
	:return: List of FULL-PATH-filenames that the links are stored under
	"""
	assert links, "Bad parameter: 'links' is empty."

	filenames = []

	for i, link in enumerate(links):   # 'i' is going to be the filename
		r = requests.get(link)
		filename = f"{PATH}/{i}.svg"
		with open(filename, "wb") as f:
			f.write(r.content)

		filenames.append(filename)

	return filenames

def convertSVGsToPDFs(filenames: [str]) -> [str]:
	"""
	:param filenames: list of FULL-PATH svg filenames
	:return: list of FULL-PATH pdf filenames
	"""
	print(f"Converting SVGs to PDFs ..\n")

	if DEBUG: print(f"SVGs to convert: {filenames}")

	pdfNames = []
	for filename in filenames:
		drawing = svg2rlg(filename)
		filename_withoutExt = filename[:-4] # Remove svg fileextension
		renderPDF.drawToFile(drawing, f"{filename_withoutExt}.pdf")
		pdfNames.append(f"{filename_withoutExt}.pdf")

	if DEBUG: print(f"Converted SVGs: {filenames}\n")

	return pdfNames

def mergePDFs(pdfName: str, pdfFilenames: [str]) -> None:
	print(f"Merging PDFs into one ..")

	merger = PdfFileMerger()

	for pdf in pdfFilenames:
		merger.append(pdf)

	merger.write(f"{PATH}/{pdfName}.pdf")
	merger.close()

if __name__ == '__main__':

	links: [str] = getScoreLinks(URL_OF_MUSESCORE_PAGE)

	# list of FULL-PATH filenames for the downloaded and stored SVGs
	SVG_filenames: [str] = downloadSVGs(links)

	# list of FULL-PATH pdf-filenames
	PDF_filenames: [str] = convertSVGsToPDFs(SVG_filenames)

	mergePDFs(pdfName='result', pdfFilenames=PDF_filenames)






#    Alternative, though less efficient, way of extracting the score_svg links:

# 	input("press enter when ready")
# 	print(browser.find_elements_by_css_selector(cssSelector_classNameOfContainerDiv))
# 	print()
# 	print()
# 	print()
# 	print()
#
# 	for el in browser.find_elements_by_css_selector(cssSelector_classNameOfContainerDiv):
# 		ActionChains(browser).move_to_element(el).perform()
# 		sleep(2)
# 		try:
# 			img = el.find_element_by_css_selector('img')
# 			print(img.get_attribute('src'))
# 		except:
# 			...
#
# main('https://musescore.com/user/27048071/scores/4845903', 'body > '
#                                                            'div.js-page.react-container > '
#                                                            'div > section > section > '
#                                                            'main > div > :nth-child(3) > '
#                                                            'div > div > *')
