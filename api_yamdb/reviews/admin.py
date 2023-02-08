from django.contrib import admin

from reviews import models as m

admin.site.register(m.Category)
admin.site.register(m.Genre)
admin.site.register(m.Title)
admin.site.register(m.Review)
admin.site.register(m.Comment)
