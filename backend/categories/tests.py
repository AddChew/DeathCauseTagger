import pytest
from categories.models import Category


@pytest.mark.django_db
class TestCategories:
    categories_endpoint = "/api/v1/categories"
        
    def test_read_categories_unauth(self, client):
        response = client.get(self.categories_endpoint)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Unauthorized"
        }

    def test_read_categories_auth_all(self, client, access_token):
        response = client.get(
            self.categories_endpoint, 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 19
        assert body["items"] == [
            {"description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"},
            {"description": "NEOPLASMS"},
            {"description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"},
            {"description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"},
            {"description": "MENTAL AND BEHAVIOURAL DISORDERS"},
            {"description": "DISEASES OF THE NERVOUS SYSTEM"},
            {"description": "DISEASES OF THE EYE AND ADNEXA"},
            {"description": "DISEASES OF THE EAR AND MASTOID PROCESS"},
            {"description": "DISEASES OF THE CIRCULATORY SYSTEM"},
            {"description": "DISEASES OF THE RESPIRATORY SYSTEM"},
            {"description": "DISEASES OF THE DIGESTIVE SYSTEM"},
            {"description": "DISEASES OF THE SKIN AND SUBCUTANEOUS TISSUE"},
            {"description": "DISEASES OF THE MUSCULOSKELETAL SYSTEM AND CONNECTIVE TISSUE"},
            {"description": "DISEASES OF THE GENITOURINARY SYSTEM"},
            {"description": "PREGNANCY, CHILDBIRTH AND THE PUERPERIUM"},
            {"description": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"},
            {"description": "CONGENITAL MALFORMATIONS, DEFORMATIONS AND CHROMOSOMAL ABNORMALITIES"},
            {"description": "SYMPTOMS, SIGNS AND ABNORMAL CLINICAL AND LABORATORY FINDINGS, NOT ELSEWHERE CLASSIFIED"},
            {"description": "UNKNOWN"}
        ]

    def test_read_categories_auth_active(self, client, access_token):
        Category.objects.filter(description__icontains = "diseases").update(is_active = False)

        response = client.get(
            f"{self.categories_endpoint}?active=true", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 7
        assert body["items"] == [
            {"description": "NEOPLASMS"},
            {"description": "MENTAL AND BEHAVIOURAL DISORDERS"},
            {"description": "PREGNANCY, CHILDBIRTH AND THE PUERPERIUM"},
            {"description": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"},
            {"description": "CONGENITAL MALFORMATIONS, DEFORMATIONS AND CHROMOSOMAL ABNORMALITIES"},
            {"description": "SYMPTOMS, SIGNS AND ABNORMAL CLINICAL AND LABORATORY FINDINGS, NOT ELSEWHERE CLASSIFIED"},
            {"description": "UNKNOWN"}
        ]

    def test_read_categories_auth_diseases(self, client, access_token):
        response = client.get(
            f"{self.categories_endpoint}?description=disease", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 12
        assert body["items"] == [
            {"description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"}, 
            {"description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"}, 
            {"description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"}, 
            {"description": "DISEASES OF THE NERVOUS SYSTEM"}, 
            {"description": "DISEASES OF THE EYE AND ADNEXA"}, 
            {"description": "DISEASES OF THE EAR AND MASTOID PROCESS"}, 
            {"description": "DISEASES OF THE CIRCULATORY SYSTEM"}, 
            {"description": "DISEASES OF THE RESPIRATORY SYSTEM"}, 
            {"description": "DISEASES OF THE DIGESTIVE SYSTEM"}, 
            {"description": "DISEASES OF THE SKIN AND SUBCUTANEOUS TISSUE"}, 
            {"description": "DISEASES OF THE MUSCULOSKELETAL SYSTEM AND CONNECTIVE TISSUE"}, 
            {"description": "DISEASES OF THE GENITOURINARY SYSTEM"}
        ]

    def test_read_categories_auth_ordering(self, client, access_token):
        response = client.get(
            f"{self.categories_endpoint}?ordering=description", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 19
        assert body["items"] == [
            {"description": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"},
            {"description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"},
            {"description": "CONGENITAL MALFORMATIONS, DEFORMATIONS AND CHROMOSOMAL ABNORMALITIES"},
            {"description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"},
            {"description": "DISEASES OF THE CIRCULATORY SYSTEM"},
            {"description": "DISEASES OF THE DIGESTIVE SYSTEM"},
            {"description": "DISEASES OF THE EAR AND MASTOID PROCESS"},
            {"description": "DISEASES OF THE EYE AND ADNEXA"},
            {"description": "DISEASES OF THE GENITOURINARY SYSTEM"},
            {"description": "DISEASES OF THE MUSCULOSKELETAL SYSTEM AND CONNECTIVE TISSUE"},
            {"description": "DISEASES OF THE NERVOUS SYSTEM"},
            {"description": "DISEASES OF THE RESPIRATORY SYSTEM"},
            {"description": "DISEASES OF THE SKIN AND SUBCUTANEOUS TISSUE"},
            {"description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"},
            {"description": "MENTAL AND BEHAVIOURAL DISORDERS"},
            {"description": "NEOPLASMS"},
            {"description": "PREGNANCY, CHILDBIRTH AND THE PUERPERIUM"},
            {"description": "SYMPTOMS, SIGNS AND ABNORMAL CLINICAL AND LABORATORY FINDINGS, NOT ELSEWHERE CLASSIFIED"},
            {"description": "UNKNOWN"}
        ]

    def test_read_categories_auth_limit(self, client, access_token):
        response = client.get(
            f"{self.categories_endpoint}?limit=5", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 19
        assert len(body["items"]) == 5
        assert body["items"] == [
            {"description": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"},
            {"description": "NEOPLASMS"},
            {"description": "DISEASES OF THE BLOOD AND BLOOD-FORMING ORGANS AND CERTAIN DISORDERS INVOLVING THE IMMUNE MECHANISM"},
            {"description": "ENDOCRINE, NUTRITIONAL AND METABOLIC DISEASES"},
            {"description": "MENTAL AND BEHAVIOURAL DISORDERS"}
        ]