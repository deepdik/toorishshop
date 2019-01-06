from rest_framework import serializers
from .models import *
import json
from rest_framework.response import Response
from rest_framework.serializers import SerializerMethodField


class DestinationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            'id',
            'name'

        ]


# supplier serializer

class SupplierListSerializer(serializers.ModelSerializer):
    destination =   DestinationDetailSerializer()
    class Meta:
        model = Supplier
        fields =[
            'supplierid',
            'agentid',
            'name',
            'email',
            'phonenumber',
            'companyname',
            'destination',
            'createddatetime',
            'city',
            'state',
            'landmark',
            'pin',
            'address'

        ]
class SupplierAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# agent leads by status

class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'

class AgentLeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = [
            'leadid',
            'name',
            'email',
            'phonenumber',
            ]


class AgentLeadsByStatusListSerializer(serializers.ModelSerializer):
    
    lead   =    SerializerMethodField()

    def get_lead(self,instance):
        lead = Leads.objects.get(leadid = instance.leadid)
        data = AgentLeadsSerializer(lead).data
        return data
        
    class Meta:
        model = AssignedAgentLead
        fields = [
            'id',
            'lead',
            'agentid',
            'AgentLeadStatus'
        ]    


# package serializer start---------------------

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'catimg',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'catimg'

        ]




class PackageHotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageHotel
        fields = [
            'name',
            'facilities',
            'address',
            'about',
            'stars',
            'image_one',
            'image_two',
            'image_three'

        ]

class PackageHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageHotel
        fields = '__all__'



class PackageItineraryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItinerary
        fields = [
            'day',
            'title',
            'description',
            'itinery_inclusion',
            'labels',
            'image_one',
            'image_two',
            'image_three'
        ]

class PackageItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItinerary
        fields = '__all__'


class MainInclusionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainInclusion
        fields = [
            'name',
            'inclimg',           

        ]
class MainInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainInclusion
        fields = '__all__'



class PackageInclusionAndExclusionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclusionAndExclusion
        fields = [
            'name',
            'description',
            'isinclusion',
            'isexclusion'
        ]

class PackageInclusionAndExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclusionAndExclusion
        fields = '__all__'



class PackageListSerializer(serializers.ModelSerializer):
    maininclusion = SerializerMethodField()
    category   =    CategoryDetailSerializer()
    destination =   DestinationDetailSerializer()



    def get_maininclusion(self,instance):
        maininclusion = MainInclusion.objects.filter(package=instance.id)
        data = MainInclusionSerializer(maininclusion,many=True).data
        return data
    
    class Meta:
        model = Package
        fields = [
            'id',
            'destination',
            'packagedays',
            'packagenights',
            'packagename',
            'category',           
            'actualpriceperperson',
            'offeredpriceperperson',
            'bannerimage',            
            'maininclusion',
            
            ]

class PackageDetailSerializer(serializers.ModelSerializer):
    maininclusion = SerializerMethodField()
    category   =    CategoryDetailSerializer(many=True)

    def get_maininclusion(self,instance):
        maininclusion = MainInclusion.objects.filter(package=instance.id)
        data = MainInclusionSerializer(maininclusion,many=True).data
        return data
    
    class Meta:
        model = Package
        fields = [
            'id',
            'destination',
            'packagedays',
            'packagenights',
            'packagename',
            'category',           
            'actualpriceperperson',
            'offeredpriceperperson',
            'bannerimage',            
            'maininclusion',
            
            ]











class PackageAddSerializer(serializers.ModelSerializer):

    hotel = PackageHotelListSerializer(many=True)
    itinerary = PackageItineraryListSerializer(many=True)
    inclusionandexclusion = PackageInclusionAndExclusionListSerializer(many=True)
    maininclusion = MainInclusionListSerializer(many=True)
   
    class Meta:
        model = Package
        fields = [

            'destination',
            'packagedays',
            'packagenights',
            'packagename',
            'category',
            'overview',
            'actualpriceperperson',
            'offeredpriceperperson',
            'bannerimage',
            'inclusionandexclusion',
            'maininclusion',
            'itinerary',
            'hotel',

            ]

    def create(self, validated_data):
        hotels = validated_data.pop('hotel')
        itinerarys = validated_data.pop('itinerary')
        inclusionandexclusions = validated_data.pop('inclusionandexclusion')
        maininclusions = validated_data.pop('maininclusion')

        package = Package.objects.create(**validated_data)

        hotel_list = [ PackageHotel(package=package, **hotel) for hotel in hotels]     
        PackageHotel.objects.bulk_create(hotel_list)

        itinerary_list = [ PackageItinerary(package=package, **itinerary) for itinerary in itinerarys]     
        PackageItinerary.objects.bulk_create(itinerary_list)

        inclusionandexclusion_list = [ PackageInclusionAndExclusion(package=package, **inclusionandexclusion) for inclusionandexclusion in inclusionandexclusions]
        PackageInclusionAndExclusion.objects.bulk_create(inclusionandexclusion_list) 

        maininclusion_list = [ MainInclusion(package=package, **maininclusion) for maininclusion in maininclusions]     
        MainInclusion.objects.bulk_create(maininclusion_list)

        return package








# quotation ---------------------------

class HotelListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Hotel
		fields = [

			'nights',
			'hotelname',
			'roomtype',
			'city',
			'stars',
			'comment'
		]

class ItineraryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Itinerary
		fields = [

			'day',
			'title',
			'description',

		]
class InclusionAndExclusionListSerializer(serializers.ModelSerializer):
	class Meta:
		model = InclusionAndExclusion
		fields = [

			'name',
			'description',
			'isinclusion',		
		]
class QuotationListSerializer(serializers.ModelSerializer):

	hotel = SerializerMethodField()
	itinerary = SerializerMethodField()
	inclusionandexclusion = SerializerMethodField()

	def get_hotel(self,instance):
		hotel = Hotel.objects.filter(quotation = instance.id)
		data = HotelListSerializer(hotel,many=True).data
		return data

	def get_itinerary(self,instance):
		itinerary = Itinerary.objects.filter(quotation = instance.id)
		data = ItineraryListSerializer(itinerary,many=True).data
		return data

	def get_inclusionandexclusion(self,instance):
		inclusionandexclusion = InclusionAndExclusion.objects.filter(quotation = instance.id)
		data = InclusionAndExclusionListSerializer(inclusionandexclusion,many=True).data
		return data

	class Meta:
		model = Quotation
		fields = [
			'id',
            'leadid',
            'agentid',
			'days',
			'nights',
			'ispriceperperson',
			'istotalprice',
			'currency',
			'flightcost',
			'visacost',
			'landpackagecost',
			'quottotalprice',
			'ishotel',
			'hotel',
			'isflight',
			'flightdetail',
			'iscab',
			'cabdetail',
			'inclusionandexclusion',
			'itinerarystartday',
			'itinerary',
			'termscond',
			'otherenfo',

			]
class QuotationAddSerializer(serializers.ModelSerializer):
	
	hotel = HotelListSerializer(many=True)
	itinerary = ItineraryListSerializer(many=True)
	inclusionandexclusion = InclusionAndExclusionListSerializer(many=True)

	class Meta:
		model = Quotation
		fields = [
            'leadid',
            'agentid',
			'days',
			'nights',
			'ispriceperperson',
			'istotalprice',
			'currency',
			'flightcost',
			'visacost',
			'landpackagecost',
			'quottotalprice',
			'ishotel',
			'hotel',
			'isflight',
			'flightdetail',
			'iscab',
			'cabdetail',
			'inclusionandexclusion',
			'itinerarystartday',
			'itinerary',
			'termscond',
			'otherenfo'
			]

	def create(self, validated_data):
		hotels = validated_data.pop('hotel')
		itinerarys = validated_data.pop('itinerary')
		inclusionandexclusions = validated_data.pop('inclusionandexclusion')
		quotation = Quotation.objects.create(**validated_data)
		hotel_list = [ Hotel(quotation=quotation, **hotel) for hotel in hotels]		
		Hotel.objects.bulk_create(hotel_list)
		itinerary_list = [ Itinerary(quotation=quotation, **itinerary) for itinerary in itinerarys]		
		Itinerary.objects.bulk_create(itinerary_list)
		inclusionandexclusion_list = [ InclusionAndExclusion(quotation=quotation, **inclusionandexclusion) for inclusionandexclusion in inclusionandexclusions]
		InclusionAndExclusion.objects.bulk_create(inclusionandexclusion_list)			
		return quotation


	def update(self, validated_data):
		hotels = validated_data.pop('hotel')
		itinerarys = validated_data.pop('itinerary')
		inclusionandexclusions = validated_data.pop('inclusionandexclusion')
		quotation = Quotation.objects.create(**validated_data)
		hotel_list = [ Hotel(quotation=quotation, **hotel) for hotel in hotels]		
		Hotel.objects.bulk_create(hotel_list)
		itinerary_list = [ Itinerary(quotation=quotation, **itinerary) for itinerary in itinerarys]		
		Itinerary.objects.bulk_create(itinerary_list)
		inclusionandexclusion_list = [ InclusionAndExclusion(quotation=quotation, **inclusionandexclusion) for inclusionandexclusion in inclusionandexclusions]
		InclusionAndExclusion.objects.bulk_create(inclusionandexclusion_list)			
		return quotation



class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        #fields = ('name',)


class AspnetrolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspnetroles
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanytypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companytype
        fields = '__all__'

class AspnetusersSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    # def get_role(self, instance):
    #     #print('dfsgds',instance.roleid)
    #     data= Aspnetroles.objects.filter(id= int(instance.roleid))
    #     #print('data',data)
    #     return AspnetrolesSerializer(data,many=True).data

    class Meta:
        model = Aspnetusers
        fields = '__all__'
        # fields = [
        #     'id',
        #     'username',
        #     'email',
        #     'passwordhash',
        #     'companyid',
        #     'roleid'
        #     'role'
        # ]


class AspnetusersWrolesSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    def get_role(self, instance):
        data= Aspnetroles.objects.filter(id= int(instance.roleid))
        return AspnetrolesSerializer(data,many=True).data
    class Meta:
        model = Aspnetusers
        fields = [
            'id',
            'username',
            'email',
            'passwordhash',
            'companyid',
            'roleid',
            'role'
        ]

class AspnetusersWithrolesSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    def get_role(self, instance):
        data= Aspnetroles.objects.filter(id= int(instance.roleid))
        # for d in data:
        #     print(d.name)
        return AspnetrolesSerializer(data,many=True).data
    class Meta:
        model = Aspnetusers
        fields = [
            'userid',
            'username',
            'email',
            'passwordhash',
            'companyid',
            'roleid',
            'projectid',
            'createddatetime',
            'accessfailedcount',
            'firstname',
            'lastname',
            'lockoutenabled',
            'lockoutenddateutc',
            'twofactorenabled',
            'phonenumberconfirmed',
            'phonenumber',
            'emailconfirmed',
            'securitystamp',
            'token',
            'role'
        ]




class LeadsSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = [
            'createuserid',
            'edituser_id',
            'name',
            'phonenumber',
            'companyid',
            'cmpctlabel',
            'status',

        ]

class LeadsWithItemsSerializer(serializers.ModelSerializer):
    items= SerializerMethodField()
    def get_items(self,instance):
        items= Leaditems.objects.filter(lead_id=instance.lead_id)
        data = LeaditemsSerializer(items,many=True).data
        return data

    class Meta:
        model = Leads
        fields = [
            'lead_id',
            'createuserid',
            'edituser_id',
            'createdatetimeoffset',
            'editdatetimeoffset',
            'name',
            'email',
            'phonenumber',
            'isassigned',
            'companyid',
            'cmpctlabel',
            'receivedon',
            'status',
            'id',
            'items'
        ]


class LeadsUpdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = '__all__'
    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        lead_id= self.context['request'].data['lead_id']
        lead = Leads.objects.get(pk=lead_id)
        leads_serializer = LeadsSerializer(lead, data=self.context['request'].data)
        if leads_serializer.is_valid():
            leads_serializer.save()
        print('items',items)
        return lead

class UploadDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class UploadProfilepics(serializers.ModelSerializer):

    class Meta:
        model = Profilepics
        fields = '__all__'

class Leads_with_itemsSerializer(serializers.ModelSerializer):
    items= serializers.SerializerMethodField()
    def get_items(self,instance):
        data = Leaditems.objects.filter(lead_id=int(instance.lead_id))
        return LeaditemsSerializer(data,many=True).data
    class Meta:
        model = Leads
        fields = [
            'leadid',
            'createuserid',
            'edituserid',
            'createdatetimeoffset',
            'editdatetimeoffset',
            'name',
            'email',
            'phonenumber',
            'isassigned',
            'companyid',
            'cmpctlabel',
            'receivedon',
            'statusid',
            'id',
            'items'
        ]

class LeadsExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads
        fields = [
            'name',
            'email',
            'phonenumber',
            'companyid',
            'cmpctlabel',
            'statusid'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class IntegrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integrations
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AskQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskQuotation
        fields = '__all__'

class LeaditemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaditems
        fields = '__all__'



class RecordingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recordings
        fields = '__all__'


class AgentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
