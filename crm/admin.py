from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

class PackageInclusionAndExclusionInline(admin.TabularInline):
	model = PackageInclusionAndExclusion


class MainInclusionInline(admin.TabularInline):
	model = MainInclusion


class PackageItineraryInline(admin.StackedInline):
	model = PackageItinerary
	extra = 1

class PackageHotelInline(admin.StackedInline):
	model = PackageHotel
	extra = 0

class PackageAdmin(admin.ModelAdmin):
	inlines = [ PackageInclusionAndExclusionInline,MainInclusionInline,PackageItineraryInline,PackageHotelInline,]


admin.site.register(Package, PackageAdmin)

admin.site.register([Destination,Supplier,AgentLeadStatus,AssignedAgentLead,AspnetrolePermission,Permission,DestinationCity,Category,PackageInclusionAndExclusion,Leads,Aspnetusers,Attendance,Leaditems,Company,
                     Aspnetroles,MainInclusion,ItineryInclusion,PackageItinerary,Leadstatus,Profilepics,Agent,Project,AskQuotation,Quotation,Hotel,Itinerary,InclusionAndExclusion])

