import os
import pytest


token_endpoint = "/api/v1/token/pair"
categories_endpoint = "/api/v1/categories"


@pytest.fixture
def access_token(client):
    data = {
        "username": os.getenv("DEFAULT_USER", "admin"),
        "password": os.getenv("DEFAULT_PASSWORD", "admin")
    }
    response = client.post(token_endpoint, data, content_type = "application/json")
    json_response = response.json()
    return json_response["access"]


@pytest.mark.django_db
class TestCategories:

    def test_read_categories_unauth(self, client):
        response = client.get(categories_endpoint)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Unauthorized"
        }

    def test_read_categories_auth_all(self, client, access_token):
        response = client.get(
            categories_endpoint, 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "description": "NEOPLASMS"
            },
            {
                "description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"
            },
            {
                "description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"
            },
            {
                "description": "MENTAL AND BEHAVIOURAL DISORDERS"
            },
            {
                "description": "DISEASES OF THE NERVOUS SYSTEM"
            },
            {
                "description": "DISEASES OF THE EYE AND ADNEXA"
            },
            {
                "description": "DISEASES OF THE EAR AND MASTOID PROCESS"
            },
            {
                "description": "DISEASES OF THE CIRCULATORY SYSTEM"
            },
            {
                "description": "DISEASES OF THE RESPIRATORY SYSTEM"
            },
            {
                "description": "DISEASES OF THE DIGESTIVE SYSTEM"
            },
            {
                "description": "DISEASES OF THE SKIN AND SUBCUTANEOUS TISSUE"
            },
            {
                "description": "DISEASES OF THE MUSCULOSKELETAL SYSTEM AND CONNECTIVE TISSUE"
            },
            {
                "description": "DISEASES OF THE GENITOURINARY SYSTEM"
            },
            {
                "description": "PREGNANCY, CHILDBIRTH AND THE PUERPERIUM"
            },
            {
                "description": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"
            },
            {
                "description": "CONGENITAL MALFORMATIONS, DEFORMATIONS AND CHROMOSOMAL ABNORMALITIES"
            },
            {
                "description": "SYMPTOMS, SIGNS AND ABNORMAL CLINICAL AND LABORATORY FINDINGS, NOT ELSEWHERE CLASSIFIED"
            },
            {
                "description": "UNKNOWN"
            }
        ]

    def test_read_categories_auth_diseases(self, client, access_token):
        response = client.get(
            f"{categories_endpoint}?description=diseases", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "description": "DISEASES OF THE GENITOURINARY SYSTEM"
            },
            {
                "description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"
            },
            {
                "description": "DISEASES OF THE SKIN AND SUBCUTANEOUS TISSUE"
            },
            {
                "description": "DISEASES OF THE MUSCULOSKELETAL SYSTEM AND CONNECTIVE TISSUE"
            },
            {
                "description": "DISEASES OF THE NERVOUS SYSTEM"
            },
            {
                "description": "DISEASES OF THE EYE AND ADNEXA"
            },
            {
                "description": "DISEASES OF THE EAR AND MASTOID PROCESS"
            },
            {
                "description": "DISEASES OF THE CIRCULATORY SYSTEM"
            },
            {
                "description": "DISEASES OF THE RESPIRATORY SYSTEM"
            },
            {
                "description": "DISEASES OF THE DIGESTIVE SYSTEM"
            },
            {
                "description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"
            },
            {
                "description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_categories_auth_unknown(self, client, access_token):
        response = client.get(
            f"{categories_endpoint}?description=unknown", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "description": "UNKNOWN"
            }
        ]