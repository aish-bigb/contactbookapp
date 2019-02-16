from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from ..models import Location, Member

class PhoneBookTestCase(TestCase):
    def setUp(self):
        m=Member.objects.create(name='Aiswara', email="aishzzz@gmail.com",phone_number = '3423332323')
        Location.objects.create(contact_address="Jupiter", contact_area="Mars", pincode=232123)
        Location.objects.create(contact_address="Jupiter",member = m,  contact_area="Mars", pincode=232123)


    def test_retrieval(self):
        m = Member.objects.get(name="Aiswara")
        L = Location.objects.get(member=m)

    def test_edit(self):
        m = Member.objects.get(name="Aiswara")
        m.name='Akamsha'
        m.save()
        l=Location.objects.filter(member=m)
        for each in l:
            each.member = None
            each.save()


    def test_detele():
        m = Member.objects.get(name='Akamsha')
        m.delete()

        Location.objects.filter(member=m).delete()
