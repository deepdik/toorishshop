from __future__ import print_function
from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect
from django.shortcuts import render

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
from werkzeug.utils import secure_filename
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from bunch import bunchify
import pyexcel
from django.db.models import Q
import os.path
from datetime import datetime
import pprint
from django.http import HttpResponse
from .authtoken import *

from django.core.paginator import Paginator
import pandas as pd
import xlrd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework import status

from django_filters import rest_framework as filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,

    )
import psycopg2
import json
from psycopg2.extras import RealDictCursor

con = psycopg2.connect(dbname='touristshop', user='postgres', host='localhost', password='Bismillah@123')
#con = psycopg2.connect(dbname='LeadPolice', user='postgres', host='50.63.167.106', password='Modinagar@7')




token = 'zzzzz'



class SupplierListAPIView(APIView):
 
    def get(self, request, format=None):
        agentid   = request.GET.get('agentid')
        supplier = Supplier.objects.filter(agentid=agentid)
        serializer = SupplierListSerializer(supplier,many=True) 
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = SupplierAddSerializer(data=request.data)      
        if serializer.is_valid():       
            serializer.save()
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AgentleadsAPIView(APIView):

    def get(self, request, format=None):
        statusid = request.GET.get('statusid')
        agentid   = request.GET.get('agentid')
        leads = AssignedAgentLead.objects.filter(agentid=agentid,AgentLeadStatus = statusid)
        serializer = AgentLeadsByStatusListSerializer(leads,many=True) 
        return Response(serializer.data)
        


class PackageFilter(django_filters.FilterSet):
    
    price_per_persion = django_filters.RangeFilter(field_name='offeredpriceperperson')
    package_days = django_filters.RangeFilter(field_name='packagedays')
    # hotel__stars = django_filters.NumberFilter(field_name=hotel_package)
    class Meta:
        model = Package
        fields = {'category','package_days','price_per_persion','destination__destination_type',
            }

class PackageListFilterAPIView(ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PackageFilter


class PackageListAPIView(APIView):
    def get(self, request, format=None):
        agentid   = request.GET.get('agentid')
        package = Package.objects.filter(agentid=agentid)
        serializer = PackageListSerializer(package,many=True) 
        return Response(serializer.data)


class PackageDetailAPIView(RetrieveAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageDetailSerializer
    lookup_field = "id"

class PackageAddAPIView(APIView):

    def post(self, request, format=None):

        serializer = PackageAddSerializer(data=request.data)      
        if serializer.is_valid():       
            serializer.save()
            serialized_data = serializer.validated_data                              
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class QuotationAddAPIView(APIView):

	def get(self, request, format=None):
		leadid = request.GET.get('leadid')
		
		agentid = request.GET.get('agentid')
	
		if leadid and agentid:
			quotobj = Quotation.objects.filter(leadid=leadid, agentid=agentid)
				
			serializer = QuotationListSerializer(quotobj,many=True)		
			return Response(serializer.data,status=HTTP_200_OK)
		if leadid:	
			QuerySet = Quotation.objects.filter(leadid=leadid)		
			serializer = QuotationListSerializer(QuerySet,many=True)		
			return Response(serializer.data)
		return Response('pls provide leadid', status=status.HTTP_400_BAD_REQUEST)



	def post(self, request, format=None):

		serializer = QuotationAddSerializer(data=request.data)		
		if serializer.is_valid():		
			serializer.save()
			serialized_data = serializer.validated_data
			leadid = serialized_data.get('leadid')
			agentid = serialized_data.get('agentid')
			obj = AskQuotation.objects.get(leadid=leadid,agentid=agentid)
			obj.isquotsent = True
			obj.save()
					
			return Response(request.data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

	def put(self, request, format=None):
		quotid = request.GET.get('id')
		if quotid:		
			Quotation.objects.get(id=quotid).delete()
			serializer = QuotationAddSerializer(data=request.data)		
			if serializer.is_valid():		
				serializer.save()			
				return Response(request.data, status=HTTP_200_OK)
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		quotid = request.GET.get('id')
		if quotid:
			obj =	Quotation.objects.get(id=quotid)
			leadid = obj.leadid
			agentid = obj.agentid
			obj.delete()
			askquotobj = AskQuotation.objects.get(leadid=leadid,agentid=agentid)
			askquotobj.isquotsent = False
			askquotobj.save()
			return Response(status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DocumentsList(APIView):
    def get(self,request):
        records = Document.objects.all()
        serializer = UploadDocSerializer(records,many=True)
        return Response(serializer.data)


class Documents_of_project(APIView):
    def get(self,request, project_id):
        records = Document.objects.filter(projectid=project_id)
        serializer = UploadDocSerializer(records,many=True)
        return Response(serializer.data)


class Cretae_document(APIView):
    def post(self,request):
        serializer = UploadDocSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Get_project_document(APIView):
    def get(self,request,project_id):
        record = Document.objects.filter(projectid=project_id)
        serializer = UploadDocSerializer(record,many=True)
        return Response(serializer.data)

class Profile_pics(APIView):
    def post(self,request):
        user_name = request.GET.get('username')
        image = request.FILES['image']
        Profilepics.objects.filter(username=user_name).update(pics=image)
        # serializer = UploadProfilepics(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('success')
    def get(self,request):
        user_name= request.GET.get('username')
        print('abc',user_name)
        record = Profilepics.objects.get(username=user_name)
        serializer = UploadProfilepics(record)
        return Response(serializer.data)


class Document_with_projectid_documentid(APIView):
    def get(self,request, project_id,document_id):
        records = Document.objects.filter(projectid= project_id,id=document_id)
        serializer = DocumentsSerializer(records,many=True)
        return Response(serializer.data)

#@decorator
@api_view(['get'])
def getcmp(request):
    #perm=Auth(request)
    param = True
    if(param==True):
        records = Company.objects.all()
        serializer = CompanySerializer(records, many=True)
        return Response(serializer.data)
    else:
        return "Wrong Token"

@api_view(['get'])
def getcmpWithPaging(request):
    user_name = request.GET.get('username')
    company_id = request.GET.get('companyId')
    page_number = request.GET.get('pageNumber')
    status_id = request.GET.get('statusId')
    project_id = request.GET.get('projectId')
    assignedTo = request.GET.get('assignedTo')
    assignedTo = request.GET.get('assignedTo')
    lead_name = request.GET.get('leadName')
    lead_number = request.GET.get('leadNumber')
    date_from = request.GET.get('DateFrom')
    date_to = request.GET.get('DateTo')
    '''
    filter.companyid, filter.pageSize, 
                filter.pageNumber, filter.statusID,filter.projectId,filter.assignedTo,filter.leadName,
                filter.leadNumber,filter.DateFrom,filter.DateTo
    '''
    param = True
    if(param==True):
        records = Company.objects.all()
        serializer = CompanySerializer(records, many=True)
        return Response(serializer.data)
    else:
        return "Wrong Token"


@api_view(['post'])
def postcmp(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyList(APIView):
    def get(self,request):
        records = Company.objects.all()
        serializer = CompanySerializer(records,many=True)
        #my_header(request.META['HTTP_TOKEN'])
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentList(APIView):
    def get(self,request):
        companyid= request.GET.get('companyid')
        records = Agent.objects.filter(allocatedcid=companyid)
        serializer = AgentsSerializer(records,many=True)
        #my_header(request.META['HTTP_TOKEN'])
        return Response(serializer.data)

    def post(self, request):
        serializer = AgentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data['agentid'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AskQuotationAgent(APIView):
    def get(self,request):
        agent_id = request.GET.get('agentid')
        user_name = request.GET.get('username')
        if(agent_id):
            records = AskQuotation.objects.filter(agentid=agent_id)
        else:
            agentid = Agent.objects.get(username = user_name).agentid
            records = AskQuotation.objects.filter(agentid=agentid)

        serializer = AskQuotationSerializer(records,many=True)
        #my_header(request.META['HTTP_TOKEN'])
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = AskQuotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data['quotationid'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Company_company_id_get_update_delete(APIView):
    def get(self,request,company_id, Format=None):
        records = Company.objects.get(pk=company_id)
        serializer = CompanySerializer(records)
        return Response(serializer.data)

    def put(self,request,company_id, Format=None):
        records = Company.objects.get(pk=company_id)
        serializer = CompanySerializer(records,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, format=None):
        user = Company.objects.get(pk=company_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AspnetusersList(APIView):
    def get(self,request):
        documents = Aspnetusers.objects.all()
        serializer = AspnetusersSerializer(documents,many=True)
        return Response(serializer.data)

@api_view(['post'])
def post(request):
        data = request.data
        print('create user',data)
        now = datetime.now()
        format_iso_now = now.isoformat()
        newdate = now + timedelta(days=365)
        data['createddatetime'] = format_iso_now
        data['lockoutenddateutc']= newdate.isoformat()
        data['twofactorenabled']= "1"
        data['lockoutenabled']= "1"
        data['accessfailedcount'] =1
        data['securitystamp'] = "victor"
        data['emailconfirmed'] = "1"
        data['phonenumberconfirmed'] = "1"
        data['token'] = "asd"
        #print(data['lockoutenddateutc'])
        serializer = AspnetusersSerializer(data = data)
        #print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Aspnetusers_update_user(APIView):
    def put(self, request):
        data = request.data
        user = Aspnetusers.objects.get(pk=data['id'])
        print(user.username)
        serializer = AspnetusersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Aspnetusers_get_update_delete(APIView):
    def get(self, request, user_id, format=None):
        user = Aspnetusers.objects.get(pk=user_id)
        serializer = AspnetusersSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user = Aspnetusers.objects.get(pk=user_id)
        print(request.data)
        serializer = AspnetusersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        user = Aspnetusers.objects.get(pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Aspnetusers_of_company(APIView):
    def get(self,request):
        username = request.GET.get('username')
        company_id = Aspnetusers.objects.get(username=username).companyid
        cursor = open()
        join_query = "Select * from AspNetUsers u join AspNetRoles r on CAST(u.roleid AS INTEGER) = r.id " \
                     "where u.companyid  =" + str(company_id)
        cursor.execute(join_query)
        records = cursor.fetchall()
        dump_records = json.dumps(records, sort_keys=True, default=str)
        loaded_records = json.loads(dump_records)
        return Response(loaded_records)
        # documents = Aspnetusers.objects.filter(companyid=company_id)
        # serializer = AspnetusersSerializer(documents,many=True)
        # return Response(serializer.data)


class AspnetusersWrole(APIView):
    def get(self,request):
        documents = Aspnetusers.objects.all()
        serializer = AspnetusersWrolesSerializer(documents,many=True)
        return Response(serializer.data)


class AspnetusersWithrole(APIView):
    def get(self,request):
        my_dict = dict(request.GET)
        for key in my_dict:
            if str(key.lower()) == 'username':
                username = my_dict[key][0]
        #username = request.GET.get('username')
        company_id = Aspnetusers.objects.get(username=username).companyid
        documents = Aspnetusers.objects.filter(companyid=company_id)
        serializer = AspnetusersWithrolesSerializer(documents,many=True)
        r = json.dumps(serializer.data)
        loaded_r = json.loads(r)
        new_res = list()
        for info in loaded_r:
            mydict = info
            mydict1=mydict['role'][0]
            mydict['role']=mydict1
            new_res.append(mydict)
        #pprint.pprint(new_res, width=4)
        #print(loaded_r[0]['role'][0])
        return Response(new_res)

class users_by_projectid(APIView):
    def get(self,request,project_id):
        users = Aspnetusers.objects.filter(projectid=project_id)
        serializer = AspnetusersSerializer(users, many=True)
        return Response(serializer.data)

class Aspnetusers_of_username(APIView):
    def get(self,request,user_name):
        documents = Aspnetusers.objects.filter(username=user_name)
        serializer = AspnetusersSerializer(documents,many=True)
        return Response(serializer.data)


class Reporting(APIView):
    def get(self, request, project_id, user_id):
        cursor = open()
        query = "Select y.* from (Select Row_Number() over (order by l.leadid desc) as RowNumber, u.Id as " \
                "Id,(u.FirstName || ' ' || u.LastName) as username,li.BuilderInterest,li.cmpctlabel," \
                "l.companyid,l.CreateDateTimeOffset,l.createuserid,l.EditDateTimeOffset,l.EditUser_ID," \
                "l.Email,l.leadid,l.name,l.phonenumber,li.ProjName,li.QueryRemarks,li.RangeFrom," \
                "li.RangeTo,li.receivedon,l.Status,li.StatusDate,li.statusid,li.TypeOfProperty,li.assignedto," \
                "li.LeadItemId from Leads l join LeadItems li on li.leadid = l.leadid join AspNetUsers u " \
                "on u.Id::varchar = li.assignedto join Project p on u.projectid = p.projectid " \
                "join company c on p.projectid = c.companyid where p.projectid =COALESCE({}) and " \
                "u.id = COALESCE({}))as y".format(project_id, user_id)
        print(query)
        cursor.execute(query)
        records = cursor.fetchall()
        print(records)
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        print(loaded_r)
        con.close()
        return Response(loaded_r)

class AspnetrolesList(APIView):
    def get(self,request):
        documents = Aspnetroles.objects.all()
        serializer = AspnetrolesSerializer(documents,many=True)
        return Response(serializer.data)

    def post(self, request, Format=None):
        serializer = AspnetrolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectList(APIView):
    def get(self, request, user_name):
        print(user_name)
        records = Project.objects.all()
        serializer = ProjectSerializer(records,many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Project_project_id_get_update_delete(APIView):
    def get(self,request,project_id,Format=None):
        records = Project.objects.get(pk=project_id)
        serializer = ProjectSerializer(records)
        return Response(serializer.data)

    def put(self,request,project_id, Format=None):
        record = Project.objects.get(pk=project_id)
        serializer = ProjectSerializer(record,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, format=None):
        record = Project.objects.get(pk=project_id)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Projects_of_company(APIView):
    def get(self,request):
        my_dict = dict(request.GET)
        for key in my_dict:
            if str(key.lower()) == 'username':
                username = my_dict[key][0]
        #username = request.GET.get('username')
        company_id = Aspnetusers.objects.get(username=username).companyid
        records = Project.objects.filter(companyid=company_id)
        serializer = ProjectSerializer(records,many=True)
        return  Response(serializer.data)


class Projects_of_company_ById(APIView):
    def get(self,request):
        company_id = request.GET.get('companyid')
        records = Project.objects.filter(companyid=company_id)
        serializer = ProjectSerializer(records, many=True)
        return Response(serializer.data)

class Projects_Create(APIView):
    def post(self,request):
        print(request.data)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersJoinList(APIView):
    def get(self,request):
        cursor = open()
        query = "SELECT documents.projectid FROM documents INNER JOIN project on documents.projectid = project.projectid"
        cursor.execute(query)
        records = cursor.fetchall()
        r = json.dumps(records)
        loaded_r = json.loads(r)
        return Response(loaded_r)


class Aspnetusers_join_aspnetroles(APIView):
    def get(self,request, user_name):
        cursor = open()
        join_query = "select r.name, U.* from (select * from aspnetusers where companyid in " \
                "(select companyid from aspnetusers where username=" + "'" + user_name + "'" + "limit 1)) as U " \
                "join aspnetroles r on CAST(U.roleid AS INTEGER)=r.id;"
        cursor.execute(join_query)
        records = cursor.fetchall()
        dump_records = json.dumps(records,sort_keys=True, default=str)
        loaded_records = json.loads(dump_records)
        return Response(loaded_records)


class function_of_postgres(APIView):
    def get(self,request):
        cursor = open()
        function_query = "select * from dataget1()"
        cursor.execute(function_query)
        records = cursor.fetchall()
        dump_records = json.dumps(records,sort_keys=True, default=str)
        loaded_records = json.loads(dump_records)
        return Response(loaded_records)


class complex_join_of_postgres(APIView):
    def get(self,request,company_id,status_id):
        cursor = open()
        function_query = "Select u.Id as  Id,(u.FirstName || ' ' || u.LastName) as assignedto," \
                         "li.BuilderInterest,li.cmpctlabel,l.companyid, l.CreateDateTimeOffset," \
                         "l.createuserid,l.EditDateTimeOffset,l.EditUser_ID,l.Email,l.leadid," \
                         "l.name,l.phonenumber, li.ProjName,li.QueryRemarks,li.RangeFrom,li.RangeTo," \
                         "li.receivedon,l.Status, li.StatusDate,li.statusid,li.TypeOfProperty," \
                         "li.LeadItemId from Leads l join LeadItems li on li.leadid = l.leadid" \
                         " join AspNetUsers u on u.Id = li.assignedto" \
                         " where li.statusid =" + str(status_id) + " and u.companyId =" + str(company_id)
        #print(function_query)
        cursor.execute(function_query)
        records = cursor.fetchall()
        dump_records = json.dumps(records,sort_keys=True, default=str)
        loaded_records = json.loads(dump_records)

        return Response(loaded_records)

class LeadsListAll(APIView):
    def get(self,request):
        documents = Leads.objects.all()
        serializer = LeadsSerializer(documents,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeadsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.

class LeadsOneLeads(APIView):
    def get(self,request,lead_id):
        documents = Leads.objects.get(pk=lead_id)
        serializer = LeadsSerializer(documents)
        return Response(serializer.data)

class LeadsListAllCmp(APIView):
    def get(self,request,company_id):
        documents = Leads.objects.filter(companyid=company_id)
        serializer = LeadsSerializer(documents,many=True)
        return Response(serializer.data)

class OtherLeadsByUsernameStatusId(APIView):
    def get(self,request):
        username = request.GET.get('username')
        status_id = request.GET.get('statusId')
        #company_id = Aspnetusers.objects.get(username=username).companyid
        cursor = open()
        queryset = "Select y.* from (Select Row_Number() over (order by l.leadid desc) " \
                   "as RowNumber, u.Id as  Id,(u.FirstName || ' ' ||  u.LastName) as username,li.BuilderInterest," \
                   "li.cmpctlabel,l.companyid,l.CreateDateTimeOffset,l.createuserid, l.EditDateTimeOffset,l.EditUser_ID," \
                   "l.Email,l.leadid,l.name,l.phonenumber,li.ProjName,li.QueryRemarks,li.RangeFrom,li.RangeTo," \
                   "li.receivedon,l.Status,li.StatusDate,li.statusid,li.TypeOfProperty,li.assignedto,li.LeadItemId" \
                   " from Leads l join LeadItems li on li.leadid = l.leadid join AspNetUsers u on u.Id::varchar = li.assignedto" \
                   " where u.UserName = '{}' and li.Statusid= {})as y".format(username,status_id)
        cursor.execute(queryset)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)

        loaded_r = json.loads(r)
        result = get_other_leads(loaded_r)

        return Response(result)

class OtherLeadsByUsername(APIView):
    def get(self,request):
        user_name = request.GET.get('userName')
        status_id = request.GET.get('statusID')
        project_id = request.GET.get('projectid')
        lead_name = request.GET.get('leadname')
        lead_id = request.GET.get('leadid')
        date_from = request.GET.get('datefrom')
        date_to = request.GET.get('dateto')
        #company_id = Aspnetusers.objects.get(username=username).companyid
        if ((date_from == '' and date_to !='') or (date_from!='' and date_to=='')):
            errors = 'Must give both date'
            print('error', errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        cursor = open()
        additional_query= ""
        if (user_name != None and status_id != None):
            additional_query = " u.username=\'" + user_name + "\' and li.statusid= " + status_id
        if (project_id != None and project_id != ''):
            print('projectid', project_id)
            additional_query = additional_query + " and u.projectid=" + project_id
        if (lead_name != None and lead_name != ''):
            additional_query = additional_query + " and l.name=\'" + lead_name + "\'"
        if (lead_id != None and lead_id != ''):
            additional_query = additional_query + " and l.leadid=" + lead_id
        if (date_from != None and date_from != '' and date_to != None and date_to != ''):
            additional_query = additional_query + " and li.statusdate > \'"\
                               + date_from + "\' and li.statusdate < \'" + date_to + "\'"

        print('xyz',additional_query)
        queryset = "Select y.* from (Select Row_Number() over (order by l.leadid desc) " \
                   "as RowNumber, u.userid as  id,(u.firstname || ' ' ||  u.lastname) as username,li.builderinterest," \
                   "li.cmpctlabel,l.companyid,l.createdatetimeoffset,l.createuserid, l.editdatetimeoffset,l.edituserid," \
                   "l.email,l.leadid,l.name,l.phonenumber,li.projname,li.queryremarks,li.rangefrom,li.rangeto," \
                   "li.receivedon,l.statusid,li.statusdate,li.statusid,li.typeofproperty,li.assignedto,li.leaditemid" \
                   " from Leads l join LeadItems li on li.leadid = l.leadid join Aspnetusers u on" \
                   " u.userid::varchar = li.assignedto" \
                   " where " + additional_query + " )as y"
        # queryset = "select * from aspnetusers"
        cursor.execute(queryset)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)

        loaded_r = json.loads(r)
        pprint.pprint(loaded_r, width=8)
        #print('current leads',loaded_r)
        result = get_other_leads(loaded_r)

        return Response(result)


class OtherLeadsByCompanyId(APIView):
    def get(self,request):
        my_dict = dict(request.GET)
        for key in my_dict:
            if str(key.lower()) == 'companyid':
                company_id = my_dict[key][0]
            else:
                status_id = my_dict[key][0]

        cursor = open()
        queryset = "Select u.userid as  id,(u.firstname || ' ' || u.lastname) as assignedto,li.builderinterest,li.cmpctlabel," \
                   "l.companyid," \
                   "l.createdatetimeoffset,l.createuserid,l.editdatetimeoffset,l.edituserid," \
                   "l.email,l.leadid,l.name,l.phonenumber,li.projname,li.queryremarks,li.rangefrom," \
                   "li.rangeto,li.receivedon,l.statusid,li.statusdate,li.statusid,li.typeofproperty,li.leaditemid" \
                   " from leads l join leaditems li on li.leadid = l.leadid join aspnetusers u on " \
                   "u.userid::varchar = li.assignedto " \
                   "where li.statusid = {} and u.companyid ={} ".format(status_id,company_id)
        cursor.execute(queryset)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)

        loaded_r = json.loads(r)
        result = get_other_leads(loaded_r)

        return Response(result)

class OtherLeadsC(APIView):
    def get(self,request):
        company_id = request.GET.get('companyid')
        result = other_leads_company_id(company_id)

        return Response(result)

class Add_token(APIView):
    def put(self,request,user_name,token):
        #data = request.data['token']
        new_token = token.replace("COLON",":")
        Aspnetusers.objects.filter(username = user_name).update(token=new_token)
        return Response('success')

class getattendance(APIView):
    def get(self,request,date,username):
        print(date)
        cursor = open()
        query = "Select (u.FirstName || '' || u.LastName) as name,a.DistanceIn,a.Attendence," \
                "a.DateIn,a.DateOut,a.Date,a.DistanceOut,a.AttendanceId from Attendance a join AspNetUsers u" \
                " on a.userid = u.id where a.Date = '{}' and u.UserName ='{}'".format(date,username)
        print(query)
        cursor.execute(query)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        con.close()
        return Response(loaded_r)

class Leadsitemss(APIView):
    def get(self,request):
        user_name = request.GET.get('userName')
        print(user_name)
        pagesize = request.GET.get('pageSize')
        pagenumber = request.GET.get('pageNumber')
        company_id = Aspnetusers.objects.get(username= user_name).companyid
        status_id = 16
        documents = Leads.objects.filter(companyid=company_id, statusid=status_id)
        #serializer = Leads_with_itemsSerializer(documents,many=True)
        # r = json.dumps(serializer.data)
        # loaded_r = json.loads(r)
        serializers = LeadsSerializer(documents, many=True)
        leads_json = json.dumps(serializers.data)
        final_json_leads= json.loads(leads_json)
        user_documents = Aspnetusers.objects.filter(Q(roleid='3') | Q(roleid='4'),companyid= company_id)
        user_serializer = AspnetusersSerializer(user_documents, many=True)
        user_json = json.dumps(user_serializer.data)
        user_json_list = json.loads(user_json)
        print('items user',len(user_json_list))
        #user_len = len(user_json_list)
        #new_res = list(user_len)
        items = list()
        leads_list =list()
        for info in final_json_leads:
            #info = dict()
            info['nextlink'] = ''
            info['assignees'] = ''
            info['leadSource']= 'raw'
            info['pageNumber'] = '0'
            info['pageSize'] = '0'
            info['totalCount'] = '0'
            info['assignedUsers'] = []
            items_list = list()
            for new_user in user_json_list:
                item= dict()
                item['leaditemid']= 0
                item['leadid']= 0
                item['queryremarks']= "testdata"
                item['typeofproperty']= 2
                item['status']= 10
                item['rangefrom']= 2
                item['rangeto']= 3
                item['cmpctlabel']= "test"
                item['receivedon']= "2018-10-10T00:00:00Z"
                item['projname']= "Himan"
                item['assignedto']= new_user['userid']
                item['builderinterest']= "1"
                item['statusid']= 10
                item['statusdate']= "2018-10-10T00:00:00Z"
                item['companyid']= 1
                item['isassigned'] = False
                item['token'] = ''
                item['username'] = new_user['firstname'] + new_user['lastname']
                item['leaditemid'] = 0


                # item['lead_id'] = 0
                # item['queryremarks'] = ''
                # item['typeofproperty'] = 0
                # item['status'] = 0
                # item['rangefrom'] = 0
                # item['rangeto'] = 0
                # item['cmpctlabel'] = ''
                # item['receivedon'] = ''
                # item['projname'] = ''
                # item['assignedto'] = new_user['id']
                # item['builderinterest'] = ''
                # item['statusid'] = 0
                # item['statusdate'] = ''
                # item['isAssigned'] = False
                # item['token'] = ''
                # item['username'] = new_user['firstname'] + new_user['lastname']
                # item['companyid'] = 0
                # item['leaditemid'] = 0
                items_list.append(item)
            info['items']= items_list
            leads_list.append(info)
        paginator = Paginator(leads_list, pagesize)
        page = paginator.page(pagenumber)
        g = page.object_list
        return Response(g)

class LeadsList(APIView):
    def get(self,request,company_id, page_num, status):
        documents = Leads.objects.filter(companyid=company_id, status=status)
        serializer = Leads_with_itemsSerializer(documents,many=True)
        r = json.dumps(serializer.data)
        loaded_r = json.loads(r)
        new_res = list()
        for info in loaded_r:
            #mydict = info
            #mydict1 = mydict['role'][0]
            info['nextlink'] = 'vc.com/abv'
            info['assignees'] = ''
            info['leadSource']= 'raw'
            info['pageNumber'] = '0'
            info['pageSize'] = '0'
            info['totalCount'] = '0'
            info['assignedUsers'] = []
            new_info_item = list()
            for item in info['items']:
                item['companyId'] = 0
                item['isAssigned'] = False
                item['token'] = ''
                item['username'] = 'Alok Kumar'
                new_info_item.append(item)
            new_res.append(info)
        paginator = Paginator(new_res, 10)
        page = paginator.page(page_num)
        g = page.object_list
        return Response(g)

    def post(self, request, format=None):
        serializer = LeadsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.

class LeadsWithStatus(APIView):
    def get(self, request, company_id, status_id):
        records = Leads.objects.filter(companyid=company_id, status = status_id)
        serializer = LeadsWithItemsSerializer(records, many=True)
        return Response(serializer.data)



class Leads_items_List(APIView):
    def get(self,request):
        documents = Leaditems.objects.all()
        serializer = LeaditemsSerializer(documents,many=True)
        return  Response(serializer.data)

    def post(self, request, format=None):
        serializer = LeaditemsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.

class Upload_excel_file(APIView):
    def post(self,request):
        #print(request.GET.get('username'))
        f = request.FILES['file']
        #my_dict = dict(request.GET)
        username = request.GET.get('userName')
        # for key in my_dict:
        #     if str(key.lower()) == 'username':
        #         username = my_dict[key][0]
        company_id = Aspnetusers.objects.get(username=username).companyid
        print(f.name)
        myfile = pd.read_excel(f)
        leads = myfile.to_json(orient='records')
        leads= json.loads(leads)
        for lead in leads:
            lead['companyid'] = company_id
            lead['cmpctlabel'] = lead['remarks']
            lead['statusid'] = 16
            lead['isassigned'] = False

            #print(leads)
        serializer = LeadsExcelSerializer(data=leads, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response('success')
# Create your views here.
#select * from leaditems;
from django.shortcuts import render


class Integration_of_company(APIView):
    def get(sself, request ,ccompany_id):
        records = Integrations.objects.filter(companyid=ccompany_id)
        serializer = IntegrationsSerializer(records,many=True)
        return Response(serializer.data)


class Integration_by_integrationid(APIView):
    def get(self, request ,integration_id):
        records = Integrations.objects.filter(id=integration_id)
        serializer = IntegrationsSerializer(records,many=True)
        return Response(serializer.data)


class Recordingsleadid(APIView):
    def get(self, request ,lead_id):
        records = Recordings.objects.filter(id=lead_id)
        serializer = RecordingsSerializer(records,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class Recordingsusername(APIView):
    def get(self, request ,lead_id):
        records = Recordings.objects.filter(id=lead_id)
        serializer = RecordingsSerializer(records,many=True)
        return Response(serializer.data)
    def post(self):
        pass

class AddRecordings(APIView):
    def get(self, request):
        records = Recordings.objects.all()
        serializer = RecordingsSerializer(records,many=True)
        return Response(serializer.data)


    def post (self,request):
        serializer = RecordingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getattendance(APIView):
    def get(self,request):
        username = request.GET.get('username')
        date = request.GET.get('attendanceDate')
        cursor = open()
        query = "Select (u.FirstName + '' + u.LastName) as name,a.DistanceIn,a.Attendence,a.DateIn," \
                "a.DateOut,a.Date,a.DistanceOut,a.AttendanceId from Attendence a" \
                " join AspNetUsers u on a.userid = u.UserName where a.Date =" +(date) +" and u.UserName ="+(username)
        cursor.execute(query)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        con.close()
        return Response(loaded_r)


class Token(APIView):
    def post(self, request):
        global token
        token=login(request)
        return HttpResponse(json.dumps(token))


def check_token(func):
   def inner(received_token):
      global token
      print("I am going to check token")
      if received_token != token:
         print("Whoops! Not Authorized")
         return

      return func(token)
   return inner



@api_view(['get'])
def login_with_google(request):
    #print(request.META)
    google_token = request.GET.get('token')

    return Response(google_token)



@api_view(['post'])
def login(request):
    #print(request.META)
    if (request.META['CONTENT_TYPE'] == 'application/x-www-form-urlencoded' and request.data['grant_type']=='password'):
        user_name = request.data['username']
        #print(user_name)
        
        try:
            user = Aspnetusers.objects.get(username=user_name)
        except:
            user = None

        if user:            
            if(user.passwordhash==request.data['password']):
                response = dict()
                response['companyid'] = user.companyid
                response['roleid'] = user.roleid
                response['rolename'] = Aspnetroles.objects.get(pk=response['roleid']).name
                response['username'] = user.username
                response['token_type'] = 'bearer'
                response['access_token'] = create_token(user.username,user.companyid,user.roleid)
                print(response['access_token'])
        else:
            user_name = request.data['username']
            user = Agent.objects.get(username=user_name)
            if (user.passwordhash == request.data['password']):
                response = dict()
                response['companyname'] = user.companyname
                response['roleid'] = user.roleid
                response['rolename'] = 'agent'
                response['agentid']  = user.agentid
                response['username'] = user.username
                response['token_type'] = 'bearer'
                response['access_token'] = create_token(user.username, user.companyname, user.roleid)
                print(response['access_token'])
                
    return Response(response)




from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


class LeadstatusCountAPIView(APIView):
    def get(self,request):
        my_dict = dict(request.GET)
        for key in my_dict:
            if str(key.lower()) == 'username':
                user_name = my_dict[key][0]

        #username= request.GET.get('username')
        company_id = Aspnetusers.objects.get(username=user_name).companyid
        cursor = open()
        query = "Select n.phonenumbercount, s.name,s.statusid from(Select COUNT(li.statusid) " \
                "as phonenumbercount,li.statusid from Leads l join LeadItems li on li.leadid = l.leadid  where " \
                "l.companyid in ({}) Group by li.statusid) as n join LeadStatus s on n.statusid = s.statusid UNION Select" \
                " count(leadid) as phonenumbercount,'Raw Leads' as name,{} as statusid from Leads where companyid = {} and" \
                " isassigned ={}".format(company_id, 16, company_id, False)
        #print(query)
        cursor.execute(query)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        j = len(loaded_r)
        #print(loaded_r)
        #print(j)
        response = dict()
        response['currentleadscount'] = 0
        response['noworkcount'] = 0
        response['notconnectedcount'] = 0
        response['followupscount'] = 0
        response['visitoncounts'] = 0
        response['visitdonecount'] = 0
        response['visitdeadcount'] = 0
        response['otherprojectscount'] = 0
        response['resalecount'] = 0
        response['alreadybookedcount'] = 0
        response['bookeddone'] = 0
        response['deadcount'] = 0
        response['rentcount'] = 0
        response['plotcount'] = 0
        response['duplicatecount'] = 0
        response['rawleadscount'] = 0
        #print('working')
        #print('next working')
        i = 0
        while i <= j - 1:
            if loaded_r[i]['statusid'] == 16:
                print(loaded_r[i])
                response['rawleadscount'] = loaded_r[i]['phonenumbercount']
                print(response['rawleadscount'])
            elif loaded_r[i]['statusid'] == 1:
                print(loaded_r[i])
                response['currentleadscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 2:
                response['noworkcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 3:
                response['notconnectedcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 4:
                response['followupscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 5:
                response['visitoncounts'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 6:
                response['visitdonecount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 7:
                response['visitdeadcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 8:
                response['otherprojectscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 9:
                response['resalecount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 10:
                response['alreadybookedcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 11:
                response['bookeddone'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 12:
                response['deadcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 13:
                response['rentcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 14:
                response['plotcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 15:
                response['duplicatecount'] = loaded_r[i]['phonenumbercount']
            i = i + 1
        con.close()
        print('end')
        print(type(response))
        return Response(response)


class MobileLeadstatusCountAPIView(APIView):
    def get(self,request):
        username= request.GET.get('username')
        cursor = open()
        query = "Select n.phonenumbercount, s.name,s.statusid from (Select COUNT(DISTINCT l.leadid) " \
                "as phonenumbercount,statusid from Leads l join LeadItems li on li.leadid = l.leadid join " \
                "AspNetUsers u on u.Id::varchar = li.assignedto where u.UserName = '{}' Group by statusid) as" \
                " n join LeadStatus s on n.statusid = s.statusid".format(username)
        print(query)
        cursor.execute(query)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        j = len(loaded_r)
        print(loaded_r)
        print(j)
        response = dict()
        response['currentleadscount'] = 0
        response['noworkcount'] = 0
        response['notconnectedcount'] = 0
        response['followupscount'] = 0
        response['visitoncounts'] = 0
        response['visitdonecount'] = 0
        response['visitdeadcount'] = 0
        response['otherprojectscount'] = 0
        response['resalecount'] = 0
        response['alreadybookedcount'] = 0
        response['bookeddone'] = 0
        response['deadcount'] = 0
        response['rentcount'] = 0
        response['plotcount'] = 0
        response['duplicatecount'] = 0
        response['rawleadscount'] = 0
        print('working')
        print('next working')
        i = 0
        while i <= j - 1:
            if loaded_r[i]['statusid'] == 16:
                print(loaded_r[i])
                response['rawleadscount'] = loaded_r[i]['phonenumbercount']
                print(response['rawleadscount'])
            elif loaded_r[i]['statusid'] == 1:
                print(loaded_r[i])
                response['currentleadscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 2:
                response['noworkcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 3:
                response['notconnectedcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 4:
                response['followupscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 5:
                response['visitoncounts'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 6:
                response['visitdonecount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 7:
                response['visitdeadcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 8:
                response['otherprojectscount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 9:
                response['resalecount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 10:
                response['alreadybookedcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 11:
                response['bookeddone'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 12:
                response['deadcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 13:
                response['rentcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 14:
                response['plotcount'] = loaded_r[i]['phonenumbercount']
            elif loaded_r[i]['statusid'] == 15:
                response['duplicatecount'] = loaded_r[i]['phonenumbercount']
            i = i + 1
        con.close()
        print('end')
        print(type(response))
        return Response(response)
@api_view(['get'])
def lead_status_count(request,company_id):
    cursor = open()
    query = "Select n.phonenumbercount, s.name,s.statusid from(Select COUNT(DISTINCT l.leadid) " \
            "as phonenumbercount,statusid from Leads l join LeadItems li on li.leadid = l.leadid  where " \
            "l.companyid in ({}) Group by statusid) as n join LeadStatus s on n.statusid = s.statusid UNION Select" \
            " count(leadid) as phonenumbercount,'Raw Leads' as name,{} as statusid from Leads where companyid = {} and" \
            " isassigned ={}".format(company_id, 16, company_id, False)
    print(query)
    cursor.execute(query)
    records = cursor.fetchall()
    r = json.dumps(records, indent=4, sort_keys=True, default=str)
    loaded_r = json.loads(r)
    j = len(loaded_r)
    print(loaded_r)
    print(j)
    response = dict()
    response['currentleadscount'] = 0
    response['noworkcount'] = 0
    response['notconnectedcount'] = 0
    response['followupscount'] = 0
    response['visitoncounts'] = 0
    response['visitdonecount'] = 0
    response['visitdeadcount'] = 0
    response['otherprojectscount'] = 0
    response['resalecount'] = 0
    response['alreadybookedcount'] = 0
    response['bookeddone'] = 0
    response['deadcount'] = 0
    response['rentcount'] = 0
    response['plotcount'] = 0
    response['duplicatecount'] = 0
    response['rawleadscount'] = 0
    print('working')
    print('next working')
    i = 0
    while i <= j - 1:
        if loaded_r[i]['statusid'] == 16:
            print(loaded_r[i])
            response['rawleadscount'] = loaded_r[i]['phonenumbercount']
            print(response['rawleadscount'])
        elif loaded_r[i]['statusid'] == 1:
            print(loaded_r[i])
            response['currentleadscount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 2:
            response['noworkcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 3:
            response['notconnectedcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 4:
            response['followupscount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 5:
            response['visitoncounts'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 6:
            response['visitdonecount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 7:
            response['visitdeadcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 8:
            response['otherprojectscount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 9:
            response['resalecount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 10:
            response['alreadybookedcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 11:
            response['bookeddone'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 12:
            response['deadcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 13:
            response['rentcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 14:
            response['plotcount'] = loaded_r[i]['phonenumbercount']
        elif loaded_r[i]['statusid'] == 15:
            response['duplicatecount'] = loaded_r[i]['phonenumbercount']
        i = i + 1
    con.close()
    print('end')
    print(type(response))
    return Response(response)


@api_view(['get'])
def mobile_status_count(request, company_id):
    response = 'mobile_status_count: ' + str(company_id)
    return Response(response)

class Leads_update_delete(APIView):
    def put(self, request, lead_id, format=None):
        # record = Leads.objects.get(pk=lead_id)
        # item12=
        leads_serializer = LeadsUpdataSerializer(data=request.data)
        # leads_item_serializer = LeaditemsSerializer(record)
        # leads = json.dumps(request.data)
        # leads_list = json.loads(leads)
        # if leads_serializer.is_valid():
        #     print('working',leads_serializer.data)
        #
        # items_list = leads_list['items']
        # for item in items_list:
        #     if(item['lead_id'] != 0):
        #         #print('item',item)
        #         item_serializer = LeaditemsSerializer(data=item)
        #         if item_serializer.is_valid():
        #             #print('items_ser',item_serializer.data)
        #             #item_serializer.validated_data
        #             item_serializer.save()
        if leads_serializer.is_valid():
            leads_serializer.save()
            return Response(leads_serializer.data)
        return Response(leads_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
def create_lead(request, company_id):
    response = 'new lead: ' + str(company_id)
    return Response(response)


@api_view(['put'])
def Leads_update(request, lead_id):
    #print('type',type(request.data))
    leads = json.dumps(request.data)
    leads_json = json.loads(leads)
    record = Leads.objects.get(pk=lead_id)
    lead_serializer = LeadsSerializer(record, data=leads_json)
    print('received items',leads_json['items'])
    print('items length',len(leads_json['items']))
    lead_items = leads_json['items']
    #item_serializer = LeaditemsSerializer(data=leads_json['items'])
    token = ''
    for item in lead_items:
        print('leaditems',item)
        if(item['leadid'] != 0):
            token = item['token']
            item_serializer = LeaditemsSerializer(data=item)
            if item_serializer.is_valid():
                item_serializer.save()
                print('success item inserted')
    print('type=',type(leads_json))
    if lead_serializer.is_valid():
        lead_serializer.save()
        send_firebase_push_notification = firebase_push_notification(token)
        return Response(lead_serializer.data)
    return Response(lead_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class locationsbyuser(APIView):
    def get(self,request):
        username = request.GET.get('username')
        cursor = open()
        function_query = "Select * from Location where companyid in " \
                         "(Select  companyid from AspNetUsers where username = '{}' LIMIT 1 )".format(username)
        cursor.execute(function_query)
        records = cursor.fetchall()
        dump_records = json.dumps(records,sort_keys=True, default=str)
        loaded_records = json.loads(dump_records)
        print(loaded_records)
        final_output = list()

        for item in loaded_records:
            newd = dict()
            newd['locationid'] = item['locationid']
            newd['title'] = item['username']
            newd['lat'] = item['lattitude']
            newd['lng'] = item['longitude']
            newd['companyID'] = item['companyid']
            newd['description'] = item['username']
            final_output.append(newd)
        return Response(final_output)

class CreateLocation(APIView):
    def post(self,request):
        serializer = LocationSerializer(data=request.data)
        username = request.data['username']
        cursor = open()
        queryset = "Select *  from Location l join AspNetUsers u on u.userid::varchar = l.userid " \
                   "where u.username = '{}' LIMIT(1)".format(username)
        cursor.execute(queryset)
        records = cursor.fetchall()
        r = json.dumps(records, indent=4, sort_keys=True, default=str)
        loaded_r = json.loads(r)
        con.close()
        return Response(loaded_r)

@api_view(['get'])
def gtest(request, username):
    response = 'mobile_status_count: ' + username
    return Response(response)



class LeadSms(APIView):
    def post(self, request, *args, **kwargs):
        cursor = open()
        data = request.body
        data = data.decode("utf-8")
        # print('data received',data.decode("utf-8"))
        print('received data = ', data)
        import re
        r1 = re.findall(r"\(?\d{3}\)?-? *\d{3}-? *-?\d{4}", data)
        print(r1)
        split = [x.strip() for x in data.split(',')]
        username = request.GET.get('UserName')
        print(username)
        portalType = request.GET.get('portalType')
        cid = Aspnetusers.objects.get(username=username).companyid
        UserID = Aspnetusers.objects.get(username=username).userid
        name = split[0]
        print(name)
        phonenumber = r1[0]
        print(phonenumber)
        cmpctlabel = data
        print('sdds', phonenumber, cmpctlabel, name)
        if (phonenumber):
            if (portalType.lower() == "mgcbrk"):
                Status = 1
            elif (portalType.lower() == "nnacre"):
                Status = 2
        query = "Insert into Leads(createuserid,CreateDateTimeOffset,EditUser_ID,EditDateTimeOffset," \
                "name,email,phonenumber,isassigned,companyid,cmpctlabel,receivedon,status) Values ({}," \
                "CURRENT_TIMESTAMP,null,null,'{}',null,{},'False',{},'{}'," \
                "CURRENT_TIMESTAMP,{})".format(UserID, name, phonenumber, cid, cmpctlabel, Status)

        try:
            cursor.execute(query)
            print("queryexecuted")
        except Exception as e:
            print("Sorry someerror " + str(e))
        #con.commit()
        print(query)
        con.close()
        return Response('success')

class apiLeadsTest(APIView):
    def get(self,request):
        username = request.GET.get('username')
        statusId = request.GET.get('statusId')
        projectId = request.GET.get('projectid')
        leadName = request.GET.get('leadname')
        leadId = request.GET.get('lead_id')
        dateFrom = request.GET.get('datefrom')
        dateTo = request.GET.get('dateto')
        #company_id = Aspnetusers.objects.get(username=username).companyid
        cursor = open()
        additional_query= "myleads:"
        if(username!=None and statusId!=None):
            additional_query = " u.UserName=\'" + username + "\' and li.Statusid= " + statusId
        if(projectId!=None and projectId!=''):
            print('projectid',projectId)
            additional_query = additional_query + " and u.projectid="+projectId
        if(leadName != None and leadName!=''):
            additional_query = additional_query + " and l.name=\'" + leadName + "\' "
        if(leadId != None and leadId!=''):
            additional_query = additional_query + " and l.lead_id=" + leadId
        if(dateFrom != None and dateFrom != '' and dateTo != None and dateTo !='' and dateTo > dateFrom ):
            additional_query = additional_query + " and li.StatusDate > \'" + dateFrom + "\' and li.statusDate < \'" + dateTo +"\'"


        print('xyz',additional_query)
        return Response(additional_query)

def send_email_client():
    SCOPES = 'https://mail.google.com/'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    return Response('success')

