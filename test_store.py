from urllib import response
from jsonschema import validate
import pytest
import random
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

'''
Created a fixture that will create a new pet and order for the patch call so that the test is reusable.
If there was a delete call, I would include that to wrap at the end of the test
'''
@pytest.fixture
def order_data():
    pet_endpoint = "/pets/"
    petPayload = { 
        "id": random.randint(1, 10000),
        "name": "string",
        "type": "cat",
        "status": "available"
    }
    api_helpers.post_api_data(pet_endpoint, petPayload)
    pet_id = petPayload.get("id")

    post_endpoint = "/store/order"  
    payload = {
        "pet_id": pet_id
    }
    response = api_helpers.post_api_data(post_endpoint, payload)
    data = response.json()

    order_id  = data.get("id")
    return order_id

@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_patch_order_by_id(order_data, status):
    test_endpoint = f"/store/order/{order_data}"
    payload = {
        "status": status
    }
    response = api_helpers.patch_api_data(test_endpoint, payload)
    assert response.status_code == 200
    ''' created a schema for the outputted message and validated the response against it.'''
    validate(instance=response.json(), schema=schemas.order)
    assert_that(response.json().get("message"), contains_string("Order and pet status updated successfully"))
