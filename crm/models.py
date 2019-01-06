from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

CURRENCY = (('rupees','Rupees'),('doller','Doller'))
ROOMTYPE = (('delux','Delux'),('economic','Economic'),('other','Other'))

class Aspnetroles(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'aspnetroles'
        verbose_name_plural = "Aspnetroles"

class AskQuotation(models.Model):
    quotationid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    leadid = models.IntegerField()
    agentid = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    isquotsent = models.BooleanField(default=False)
    companyname = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'askquotation'
        verbose_name_plural = "AskQuotation"

class Aspnetusers(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=256,unique=True)
    passwordhash = models.CharField(max_length=128, blank=True, null=True)
    securitystamp = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    emailconfirmed = models.NullBooleanField()
    phonenumber = models.CharField(max_length=15, blank=True, null=True)
    phonenumberconfirmed = models.BooleanField()
    twofactorenabled = models.NullBooleanField()
    lockoutenddateutc = models.DateTimeField(blank=True, null=True)
    lockoutenabled = models.NullBooleanField()
    accessfailedcount = models.IntegerField()
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=30)
    createddatetime = models.DateTimeField()
    companyid = models.IntegerField(blank=True, null=True)
    roleid = models.CharField(max_length=10, blank=True, null=True)
    projectid = models.IntegerField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'aspnetusers'
        verbose_name_plural = "Aspnetusers"


class Agent(models.Model):
    agentid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=256,unique=True)
    passwordhash = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    emailconfirmed = models.NullBooleanField(default=False)
    phonenumber = models.CharField(max_length=10, blank=True, null=True)
    phonenumberconfirmed = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    companyname = models.CharField(max_length=256)
    createddatetime = models.DateTimeField(auto_now_add=True, blank=True)
    roleid = models.SmallIntegerField(default=8)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    pin = models.PositiveIntegerField()
    address = models.TextField(blank=True)
    contactpersonname = models.CharField(max_length=50)
    contactpersonmobile = models.CharField(max_length=10)
    allocatedcid = models.PositiveIntegerField()


    class Meta:
        managed = True
        db_table = 'agent'
        verbose_name_plural = "Agents"


class Attendance(models.Model):
    attendanceid = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=100)
    distancein = models.FloatField()
    attendence = models.BooleanField(default=False)
    datein = models.DateTimeField(blank=True, null=True)
    dateout = models.DateTimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    distanceout = models.FloatField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'attendance'
        verbose_name_plural = "Attendance"


class Company(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=100)
    email = models.EmailField(max_length=70,blank=True,null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    companyaddress = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    contactpersonname = models.CharField(max_length=50)
    contactphone = models.CharField(max_length=10)
    contactemail = models.CharField(max_length=100)
    activatedtill = models.DateTimeField()
    isactivated = models.NullBooleanField()
    logopath = models.TextField(blank=True, null=True)
    companytype = models.IntegerField(blank=True, null=True)

    class Meta:

        db_table = 'company'
        verbose_name_plural = "Company"


class Companytype(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'companytype'

class Document(models.Model):
    documentid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    projectid = models.IntegerField()
    link = models.FileField()

    class Meta:
        managed = True
        db_table = 'document'
        verbose_name_plural = "Document"

class Profilepics(models.Model):
    username = models.CharField(primary_key=True,max_length=100)
    pics = models.ImageField()

    class Meta:
        managed = True
        db_table = 'profilepics'
        verbose_name_plural = "profilepics"


class Integrations(models.Model):
    sourceid = models.IntegerField(blank=True, null=True)
    integrationkey = models.CharField(max_length=50, blank=True, null=True)
    integrationvalue = models.CharField(max_length=500, blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'integrations'


class Jobruns(models.Model):
    jobrunid = models.AutoField(primary_key=True)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    noofleads = models.IntegerField()
    errormessage = models.TextField(blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'jobruns'


class Kwdelhi(models.Model):
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    emailaddress = models.CharField(max_length=100, blank=True, null=True)
    telephonenumber = models.CharField(max_length=100, blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'kwdelhi'


class Leaditems(models.Model):
    leaditemid = models.AutoField(primary_key=True)
    leadid = models.IntegerField(blank=True, null=True)
    queryremarks = models.CharField(max_length=200, blank=True, null=True)
    typeofproperty = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    rangefrom = models.IntegerField(blank=True, null=True)
    rangeto = models.IntegerField(blank=True, null=True)
    cmpctlabel = models.TextField(blank=True, null=True)
    receivedon = models.DateTimeField(blank=True, null=True)
    projname = models.CharField(max_length=100, blank=True, null=True)
    assignedto = models.CharField(max_length=128, blank=True, null=True)
    builderinterest = models.NullBooleanField()
    statusid = models.IntegerField(blank=True, null=True)
    statusdate = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'leaditems'
        verbose_name_plural = "Leaditems"


class Leads(models.Model):
    leadid = models.AutoField(primary_key=True)
    createuserid = models.CharField(max_length=128, blank=True, null=True)
    createdatetimeoffset = models.DateTimeField(blank=True, null=True)
    edituserid = models.CharField(max_length=128, blank=True, null=True)
    editdatetimeoffset = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    phonenumber = models.CharField(max_length=14, blank=True, null=True)
    isassigned = models.NullBooleanField(default=False)
    companyid = models.IntegerField(blank=True, null=True)
    cmpctlabel = models.TextField(blank=True, null=True)
    receivedon = models.DateTimeField(auto_now_add=True)
    statusid = models.IntegerField(blank=True, null=True)
    id = models.CharField(max_length=150, blank=True, null=True)
    projectname = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    locality = models.CharField(max_length=256, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'leads'
        verbose_name_plural = "Leads"


class Leadstatus(models.Model):
    statusid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'leadstatus'
        verbose_name_plural = "Leadstatus"


class Location(models.Model):
    locationid = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=100)
    lattitude = models.CharField(max_length=100)
    companyid = models.IntegerField()
    lastupdated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'location'


class Project(models.Model):
    projectid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)
    lattitude = models.CharField(max_length=100, blank=True, null=True)
    companyid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'project'
        verbose_name_plural = "Project"


class Recording(models.Model):
    record = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'recording'


class Recordings(models.Model):
    leadid = models.IntegerField()
    name = models.CharField(max_length=250)
    createdatetime = models.DateTimeField()
    createdby = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'recordings'


class Refreshtokens(models.Model):
    subject = models.CharField(max_length=50)
    clientid = models.CharField(max_length=50)
    issuedutc = models.DateTimeField()
    expiresutc = models.DateTimeField()
    protectedticket = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'refreshtokens'


class Sourcetypes(models.Model):
    source = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'sourcetypes'

# class Profileimage(models.Model):
#     username = models.CharField(primary_key=True, max_length=100)
#     userimage = models.BYT
#
#     class Meta:
#         managed = False
#         db_table = 'sprofileimage'


# Quotation Model Start

class Quotation(models.Model):
	leadid				= models.IntegerField()
	agentid				= models.CharField(max_length=100)
	days 				= models.PositiveSmallIntegerField()
	nights				= models.PositiveSmallIntegerField()
	ispriceperperson 	= models.BooleanField(default=False)
	istotalprice		= models.BooleanField(default=False)
	currency			= models.CharField(max_length=120, choices=CURRENCY,default=CURRENCY[1][1],)
	flightcost			= models.PositiveIntegerField(null=True, blank=True)
	visacost			= models.PositiveIntegerField(null=True, blank=True)
	landpackagecost		= models.PositiveIntegerField(null=True, blank=True)
	quottotalprice		= models.PositiveIntegerField()
	ishotel             = models.BooleanField(default=True)
	isflight			= models.BooleanField()
	flightdetail		= models.TextField(null=True, blank=True)
	iscab				= models.BooleanField()
	cabdetail			= models.TextField(null=True, blank=True)
	itinerarystartday   = models.DateField()
	termscond			= models.TextField(null=True, blank=True)
	otherenfo     		= models.TextField(null=True, blank=True)
	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __int__(self):
		return self.days

	class Meta:
		managed = True
		ordering = ('timestamp',)
		verbose_name_plural = "Quotations"



class Hotel(models.Model):
	quotation           = models.ForeignKey(Quotation, on_delete=models.CASCADE)
	nights 				= models.CharField(max_length=40)
	hotelname 			= models.CharField(max_length=30)
	roomtype 			= models.CharField(max_length=120, choices=ROOMTYPE)
	city				= models.CharField(max_length=30)
	stars 				= models.IntegerField(
							default=0,
							validators=[
							MaxValueValidator(5),
							MinValueValidator(0)
							]
							)
	comment 			= models.TextField(null=True, blank=True)
	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __int__(self):
		return self.nights

	class Meta:
		managed = True
		ordering = ('timestamp',)
		verbose_name_plural = "Hotels"

class Itinerary(models.Model):
	quotation           = models.ForeignKey(Quotation, on_delete=models.CASCADE)
	day 				= models.CharField(max_length=10)
	title				= models.CharField(max_length=100)
	description			= models.TextField()

	def __str__(self):
		return self.day

	class Meta:
		managed = True
		verbose_name_plural = "Itineraries"

class InclusionAndExclusion(models.Model):
	quotation           = models.ForeignKey(Quotation, on_delete=models.CASCADE)
	name 				= models.CharField(max_length=10)
	description			= models.TextField(null=True, blank=True)
	isinclusion 		= models.BooleanField()


	def __str__(self):
		return self.name

	class Meta:
		managed = True
		verbose_name_plural = "InclusionAndExclusions"


# Packages model start------------------------------------------

TYPE = (('1', 'Domestic'), ('2', 'International'))

def upload_location(instance, filename):
    return 'Package/%s-%s/%s' % (instance.packagename, instance.id, filename)

def itenery_img_location(instance,filename):
    return 'Itinerary/%s-%s/%s' % (instance.day, instance.id, filename)

class Destination(models.Model):
    destination_type = models.CharField(max_length=120, choices=TYPE)
    name = models.CharField(max_length =120,unique=True)

    def __str__(self):
        return self.name



    class Meta:
    
        verbose_name_plural = "Destinations"

class DestinationCity(models.Model):
    destination         = models.ForeignKey(Destination,on_delete=models.DO_NOTHING)
    city                = models.CharField(max_length = 120)

    def __str__(self):
        return self.city

    class Meta:    
        verbose_name_plural = "DestinationCities"

class Category(models.Model):

    name                = models.CharField(max_length=120, unique=True)
    catimg              = models.FileField(upload_to='CatImg/',default='CatImg/None/default.svg')
    timestamp           = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = "Categories"


class Package(models.Model):
    agentid                 = models.CharField(max_length=100)
    destination             = models.ForeignKey(Destination,on_delete=models.DO_NOTHING)
    packagedays             = models.PositiveSmallIntegerField()
    packagenights           = models.PositiveSmallIntegerField()
    packagename             = models.CharField(db_index = True, max_length = 120, unique = True)    
    category                = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    overview                = models.TextField(null=True, blank=True)  
    actualpriceperperson    = models.PositiveIntegerField()
    offeredpriceperperson   = models.PositiveIntegerField(null=True, blank=True)
    bannerimage             = models.ImageField(upload_to = upload_location,
                                    default ='Package/None/default.png',
                                    )       
    timestamp               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.packagename

    class Meta:
        ordering            = ('timestamp',)
        verbose_name_plural = "Packages"


class PackageInclusionAndExclusion(models.Model):
    package             = models.ForeignKey(Package, on_delete=models.CASCADE)
    name                = models.CharField(max_length=10)
    description         = models.TextField(null=True,blank=True)
    isinclusion         = models.BooleanField()
    isexclusion         = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        verbose_name_plural = "PackageInclusionAndExclusions"

class MainInclusion(models.Model):
    package             = models.ForeignKey(Package, on_delete=models.CASCADE)
    name                = models.CharField(max_length=30,unique=True)
    inclimg             = models.ImageField(upload_to='InclusionImg/',
                           default='InclusionImg/None/default.png',
                           )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('timestamp',)
        verbose_name_plural = "MainInclusions"

class ItineryInclusion(models.Model):
    name                = models.CharField(max_length=10)
    description         = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name

       
class PackageItinerary(models.Model):
    package             = models.ForeignKey(Package, on_delete=models.CASCADE)
    day                 = models.CharField(max_length=10)
    title               = models.CharField(max_length=100)
    description         = models.TextField()  
    itinery_inclusion   = models.ManyToManyField(ItineryInclusion ,blank=True)
    labels              = models.TextField(blank = True, null = True)
    image_one           = models.ImageField(upload_to = itenery_img_location,blank=True, null=True)
    image_two           = models.ImageField(upload_to = itenery_img_location,blank=True, null=True)
    image_three         = models.ImageField(upload_to = itenery_img_location,blank=True, null=True)

    def __int__(self):
        return self.day

    class Meta:
        ordering        = ('id',)
        verbose_name_plural = "PackageItinerary"



class PackageHotel(models.Model):  
    package             = models.ForeignKey(Package, on_delete=models.CASCADE)
    name                = models.CharField(max_length=100)
    facilities          = models.TextField(null=True,blank=True)
    address             = models.CharField(max_length=300)
    about               = models.TextField(null=True,blank=True)
    stars               = models.IntegerField(
                            default=0,
                            validators=[
                                MaxValueValidator(5),
                                MinValueValidator(0)
                            ]
                         )
    timestamp           = models.DateTimeField(auto_now_add=True)
    image_one           = models.ImageField(upload_to = 'package_img',blank=True, null=True)
    image_two           = models.ImageField(upload_to = 'package_img',blank=True, null=True)
    image_three         = models.ImageField(upload_to = 'package_img',blank=True, null=True)


    def __str__(self):
        return self.name
    class Meta:
        # ordering = ('timestamp')
        verbose_name_plural = "PackageHotel"

class UploadImage(models.Model):
    image               = models.ImageField()
    caption             = models.CharField(max_length = 50,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Images"



# user permissions models start --------------------------------- 

class Permission(models.Model):
    permission_id       = models.IntegerField(primary_key=True)
    permission_name     = models.CharField(max_length=150)

    def __str__(self):
        return self.permission_name

    class Meta:
        verbose_name_plural = "Permissions"

class AspnetrolePermission(models.Model):
    companyid           = models.IntegerField()
    roleid              = models.SmallIntegerField()
    Permissions         = models.ManyToManyField(Permission, blank =True)

    def __str__(self):
        return str(self.companyid)+ '-' +str(self.roleid)

    class Meta:
        verbose_name_plural = "AspnetrolePermissions"

# agents leads status

class AgentLeadStatus(models.Model):
    id                  = models.IntegerField(primary_key=True)
    name                =models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "AgentLeadStatus"

class AssignedAgentLead(models.Model):
    leadid              = models.IntegerField()
    agentid             = models.CharField(max_length=100)
    AgentLeadStatus     = models.ForeignKey(AgentLeadStatus, on_delete=models.CASCADE)

    def __int__(self):
        return self.leadid

    class Meta:
        verbose_name_plural = "AssignedAgentLead"

# vendor/supplier

class Supplier(models.Model):
    supplierid          = models.AutoField(primary_key=True)
    agentid             = models.CharField(max_length=100)
    name                = models.CharField(max_length=30)
    email               = models.CharField(max_length=256, blank=True, null=True)  
    phonenumber         = models.CharField(max_length=10, blank=True, null=True)    
    companyname         = models.CharField(max_length=256)
    destination         = models.ForeignKey(Destination,default=2,on_delete=models.DO_NOTHING)
    createddatetime     = models.DateTimeField(auto_now_add=True, blank=True)
    city                = models.CharField(max_length=30, blank=True, null=True)
    state               = models.CharField(max_length=30, blank=True, null=True)
    landmark            = models.CharField(max_length=100, blank=True, null=True)
    pin                 = models.PositiveIntegerField(blank=True, null=True)
    address             = models.TextField(null=True,blank=True) 

    def __int__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Suppliers"