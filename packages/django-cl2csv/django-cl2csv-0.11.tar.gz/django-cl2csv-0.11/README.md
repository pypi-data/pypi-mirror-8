django-cl2csv
===

cl2csv is a tiny Django app for adding export functionality to the built-in admin list views. Fields can be hidden from export. The name is short for "Change list to Comma Separated Values".

Installation
---

1. Install via pip:

`$ pip install django-cl2csv`

2. Add "cl2csv" to your INSTALLED_APPS setting like this:

```python
	INSTALLED_APPS = (
        ...
        'cl2csv',
    )
```

Usage
--

```python
from cl2csv.options import ExportModelAdmin

class DVDAdmin(ExportModelAdmin):
    hide_from_export = ('secret_vote',)
```
