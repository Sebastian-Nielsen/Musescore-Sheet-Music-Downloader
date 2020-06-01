# Musescore-Sheet-Music-Downloader :fire:
Musescore doesn't allow for free PDF download of sheet music; this script gets around that by automatically scraping the SVG files, and merging them into a single PDF.

# Instructions :book:
- Install Python 3 
- `pip install` 
  - PyPDF2
  - svglib
  - reportlab
  - requests
  - selenium
- Download chromedriver

- Alter the parameters in `main.py` to fit your environment

# Feeling generous ? :heart:
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XNWPMMDXSAMEY&source=url)

# TODO List :pencil:
- [ ] The script can be optimized by using Requests to scrape the SVG files instead of selenium chromedriver. 
