from django.db import models

# Create your models here.
class Member(models.Model):
    EDIT_OPTION = {
                    'Member Email Edit' : 0,
                    'Member phone Edit' : 1,
                    'Member name Edit':2,
                    'Member contact_address Edit':3,
                    'Member contact_area Edit':4
                    }
    name = models.CharField(max_length = 150)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    created_on = models.DateTimeField(default = datetime.datetime.now, blank=True)

    def membereditfunction(self, location_id = None, new_value='', action=None):
        member = self

        if action == EDIT_OPTION['Member Email Edit']:
            member.email = new_value
        elif action == EDIT_OPTION['Member phone Edit']:
            member.phoneno = new_value
        elif action == EDIT_OPTION['Member name Edit']:
            member.name = new_value
        member.save()
        else:
            if not location_id:
                messages.error("Sorry operation unsuccessful. Please select members location")
            else:
                location = Location.objects.get(id=location_id)
                if action == EDIT_OPTION['Member contact_area Edit']:
                    location.contact_area = new_value
                elif action == EDIT_OPTION['Member contact_address Edit']:
                    location.contact_address = new_value
                location.save()

class Location(models.Model):
    contact_address = models.CharField(("House no & details"), max_length=250)
    contact_area = models.CharField(("Area"), max_length=250)
    member = models.ForeignKey(Member, related_name='location_member', on_delete=models.CASCADE)
    pincode = models.IntegerField(("Pin Code"))
    


