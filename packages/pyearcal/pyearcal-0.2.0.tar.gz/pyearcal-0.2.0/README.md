pyearcal
========
Generate your year calendar in Python. The result is a PDF file with 12 pages containing an image and a grid of days.

### Requirements
* reportlab
* DejaVu fonts (if you want pyearcal work out of the box)
* BeautifulSoup (optional)
* Python 2.7

### Usage

1. Prepare a directory with 12 images (different image providers are planned)
2. Initialize calendar with all options.
3. Render it to PDF

### Example code

```python
# Import important modules
from pyearcal import YearCalendar
from pyearcal.image_sources import UnsortedImageDirectory
from datetime import date
from pyearcal.l10n import CzechLocale

# Use all pictures from "images" directory
image_source = UnsortedImageDirectory("images")

# Use Czech locale and holidays
locale = CzechLocale()

# Set a few special days
special_days = [
    date(2014, 1, 31) # Guido van Rossum's birthday
]

calendar = YearCalendar(2014, image_source, locale, special_days)
calendar.render("calendar.pdf")
```

You can take **FlickrDownloader** as an inspiration for developing a more sophisticated image source.

### Example with real pictures

[India Faces Calendar 2014 (80 MB)](http://pyearcal.vzdusne.cz/calendar.pdf)
