from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Member, Location
from django.contrib import messages
from django.db import transactions

# Create your views here.

def index(request):
    '''View to display the index page'''
    context = {
        'title' : 'PhoneBook',
        'text' : "This is a contact book App. "
    }
    render(request,'contactbookapp/index.html',context)

    #return HttpResponse("welcome to Contact Book")

class PhoneBookAdd():
    '''Phone Number addition class'''
    template_name = "phonebookapp/add.html"
    def get(self, request, *args, **kwargs):
        request_context_dict = {
            'title': 'Phone Book Add'
        }
    return self.render_to_response(request_context_dict)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            m_name = request.POST.get('m_name', None)
            email = request.POST.get('email', None)
            phoneno = request.POST.get('phoneno', None)
            if m_name and email:
                m = Member.objects.create(name = m_name, email=email)
            if phoneno:
                m.phone_number = phoneno
            m.save()

class PhoneBookEdit():
    '''Phone Number edit class'''
    template_name = "phonebookapp/edit.html"

    def dispatch(self, request, *args, **kwargs):
        return super(PhoneBookEdit, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        request_context_dict = {
            'title': 'Phone Book Edit',
            'message' : 'Which of the following members data you want to edit?'
            'member' : Member.objects.all()

        }
        return self.render_to_response(request_context_dict)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            m_id = request.POST.get('id', None)
            new_value = request.POST.get('new_value', None)
            location_id = request.POST.get('location_id', None)
            action = request.POST.get('action', None)
            if not m_id or new_value:
                messages.error(request,"Member id/ edit action should not be Empty")
                return HttpResponseRedirect('/phonebookapp/edit/')

            try:
                m = Member.objects.get(id=m_id)
                m.membereditfunction(location_id, new_value, action)
                messages.success(request, "Edit successful")
            except:
                messages.error(request,"Sorry operation unsuccessful")
                return HttpResponseRedirect('/phonebookapp/edit/')

class PhoneBookView():
    '''Phone Number view class'''
    template_name = "phonebookapp/search.html"

    def dispatch(self, request, *args, **kwargs):
        return super(PhoneBookView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request_context_dict = {
            'title': 'Phone Book Search',
        }
        return self.render_to_response(request_context_dict)


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email', None)
            phoneno = request.POST.get('phoneno', None)
            m = Member.objects.all()
            if email:
                m = m.filter(email = email)
            if phoneno:
                m = m.filter(phone_number = phoneno)
            location = Location.objects.filter(member= m)
            request_context_dict = {
                'title': 'Phone Book Search',
                'location': location,
                'members' : m
                    }
            return self.render_to_response(request_context_dict)

class PhoneBookDelete():
    '''Phone Number delete class'''
    template_name = "phonebookapp/delete.html"
    def get(self, request, *args, **kwargs):
        request_context_dict = {
            'title': 'Member deletion',
            'text' : 'Select the member to delete'
        }
        return self.render_to_response(request_context_dict)


    def dispatch(self, request, *args, **kwargs):
        return super(PhoneBookDelete, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            m_id = request.POST.get('id', None)
            
            if not m_id:
                messages.error(request,"Please provide member id to be deleted")
                return HttpResponseRedirect('/phonebookapp/delete/')
            try:
                with transactions.atomic:
                    m = Member.objects.get(id=m_id)
                    Location.objects.filter(member=m).delete()
                    m.delete()
                    messages.success(request, "Deletion successful")
                    
            except Member.DoesNotExist:
                messages.error(request,"The provided member is doesnot exist/or already deleted")
                return HttpResponseRedirect('/phonebookapp/delete/')
            except:
                messages.error("Some error occured while deleting member {}".format(m_id))
                return HttpResponseRedirect('/phonebookapp/delete')


            

            




