# start Meike
from django.contrib import admin
#start Alina: For matching User and Account
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
#end Alina

from .models import Account, Plz
from .models import Category
from .models import IntervalConstraint
from .models import Query
from .models import Resource
from .models import Watchlist

#admin.site.register(Account)
admin.site.register(Category)
admin.site.register(IntervalConstraint)
admin.site.register(Query)
admin.site.register(Resource)
admin.site.register(Watchlist)
admin.site.register(Plz)

# end Meike

#start Alina: For matching User and Account
from Cith2.models import Account
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'account'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#end Alina