from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ["available", "sold", "pending"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200
    pets = response.json()
    assert isinstance(pets, list), "Validate the output is a list"
    for pet in pets:
        assert_that(pet["status"], is_(status), 
            f"Pet {pet.get('id')} has incorrect status")
    valid_statuses = ["available", "sold", "pending"]
    for pet in pets:
        # Validate the status property is one of the valid status options
        assert pet["status"] in valid_statuses, \
            f"Pet {pet.get('id')} has invalid status: {pet.get('status')}"
        # validate each item returns in the expected schema
        validate(instance=pet, schema=schemas.pet)


'''
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("id", ["9999999999", ".9", "-1", "abc", "@#$%"])
def test_get_by_id_404(id):
    params = {
        "id": id
    }
    test_endpoint = "/pets/{id}"
    response = api_helpers.get_api_data(test_endpoint)
    assert response.status_code == 404

    '''
    Noticed the swagger doc had that the response for a 404 would be "Pet not found", but the actual response was different.
    assert_that(response.text, contains_string("Pet not found"))
    '''