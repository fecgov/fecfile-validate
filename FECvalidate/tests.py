from django.test import TestCase

# Create your tests here.
class CommitteeTest(TestCase):
    """ Test module for Committee model """

    def setUp(self):
        Committee.objects.create(
            committeeid='C01234567', committeename = 'Test Committee 1', street1='Street1 ',
            street2 = 'Street 2', city='Washington DC', state='DC', zipcode='912853', 
            treasurerfirstname='John', treasurerlastname='Smith', treasurerprefix='Mr')
            
        save_data = {
                "committeeid": "C11234567",
                "committeename": "Test Committee 2",
                "street1": "Street 1",
                "street2": "Street 2",
                "city": "Washington",
                "state": "DC",
                "zipcode": 20001,
                "treasurerprefix": "Mr",
                "treasurerfirstname": "John",
                "treasurermiddlename": "Doe",
                "treasurerlastname": "Smith",
                "treasurersuffix": "IV"
            }
        Committee.objects.create(**save_data)
        
    def test_committee_create(self):
        comm = Committee.objects.get(committeeid='C01234567')
        
        self.assertEqual(comm.committeename, "Test Committee 1")

class Validate_F99(TestCase):
    """docstring for Validate_F99"TestCase def __init__(self, arg):
        super(Validate_F99,TestCase.__init__()
        self.arg = arg
    """

    def validate_f99_post_json1(self):
        json_data = { "committeeid": "C01234567", "committeename": "Test Committee 1", "street1": "Street1 ", "street2": "Street 2", "city": "Washington DC", "state": "DC", "zipcode": 912853, "treasurerprefix": "Mr", "treasurerfirstname": "John", "treasurermiddlename": "", "treasurerlastname": "Smith", "treasurersuffix": "", "text": "abcde", "reason": "MST"}
        resp = self.client.post('/f99/validate_f99', json.dumps(json_data), content_type="application/json")
        self.assertEqual(resp.status_code, 201)


    def validate_f99_post_json2(self):
        json_data = { "committeeid": "C01234567", "committeename": "Test Committee 1", "street1": "Street1 ", "street2": "Street 2", "city": "Washington DC", "state": "DC", "zipcode": 912853, "treasurerprefix": "Mr", "treasurerfirstname": "John", "treasurermiddlename": "", "treasurerlastname": "Smith", "treasurersuffix": "", "text": "abcde", "reason": "MS"}
        resp = self.client.post('/f99/validate_f99', json.dumps(json_data), content_type="application/json")
        self.assertEqual(resp.status_code, 204)