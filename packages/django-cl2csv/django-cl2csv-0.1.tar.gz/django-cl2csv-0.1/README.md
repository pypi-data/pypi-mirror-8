django-cl2csv
===================

CL2CSV (Change List to CSV) is a Django app (pluggable) that makes change lists (in the admin) exportable. The resulting CSV looks EXACTLY like what's on your screen. Certain fields can be hidden from export. This app is lightweight.

Usage
-----

```python
from cl2csv.options import ExportModelAdmin

class DVDAdmin(ExportModelAdmin):
    hide_from_export = ('secret_vote',)
```
