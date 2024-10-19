import pytest

from mappings.models import Mapping


@pytest.mark.django_db
class TestMappings:
    mappings_endpoint = "/api/v1/mappings"
        
    def test_read_mappings_unauth(self, client):
        response = client.get(self.mappings_endpoint)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Unauthorized"
        }

    def test_read_mappings_auth_limit(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?limit=5", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 11066
        assert len(body["items"]) == 5
        assert body["items"] == [
            {
                "code": "A000",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR CHOLERAE",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A001",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR ELTOR",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A009",
                "death_cause": "CHOLERA UNSPECIFIED",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A010",
                "death_cause": "TYPHOID FEVER",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A011",
                "death_cause": "PARATYPHOID FEVER A",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_mappings_auth_active(self, client, access_token):
        Mapping.objects.filter(code__description__icontains = "A00").update(is_active = False)

        response = client.get(
            f"{self.mappings_endpoint}?active=false", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 3
        assert body["items"] == [
            {
                "code": "A000",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR CHOLERAE",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A001",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR ELTOR",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A009",
                "death_cause": "CHOLERA UNSPECIFIED",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_mappings_auth_death_cause(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?death_cause=cholera", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 4
        assert body["items"] == [
            {
                "code": "A000",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR CHOLERAE",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A001",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR ELTOR",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A009",
                "death_cause": "CHOLERA UNSPECIFIED",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "XXXX",
                "death_cause": "CHOLERA VACCINE",
                "category": "UNKNOWN"
            }
        ]

    def test_read_mappings_auth_category(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?category=unknown&limit=5", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            },
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 1596
        assert body["items"] == [
            {
                "code": "XXXX",
                "death_cause": "4 AMINOPHENOL DERIVATIVES",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "ACCIDENT ON BOARD WATERCRAFT WITHOUT ACCIDENT TO WATERCRAFT NOT CAUSING DROWNING AND SUBMERSION",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "ACCIDENT ON BOARD WATERCRAFT WITHOUT ACCIDENT TO WATERCRAFT NOT CAUSING DROWNING AND SUBMERSION CANOE OR KAYAK",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "ACCIDENT ON BOARD WATERCRAFT WITHOUT ACCIDENT TO WATERCRAFT NOT CAUSING DROWNING AND SUBMERSION FISHING BOAT",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "ACCIDENT ON BOARD WATERCRAFT WITHOUT ACCIDENT TO WATERCRAFT NOT CAUSING DROWNING AND SUBMERSION INFLATABLE CRAFT NONPOWERED",
                "category": "UNKNOWN"
            }
        ]

    def test_read_mappings_auth_option(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?option=true&limit=3", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 7213
        assert body["items"] == [
            {
                "code": "A000",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR CHOLERAE",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A001",
                "death_cause": "CHOLERA DUE TO VIBRIO CHOLERAE 01 BIOVAR ELTOR",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "A009",
                "death_cause": "CHOLERA UNSPECIFIED",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_mappings_auth_open(self, client, access_token):
        Mapping.objects.filter(code__description__icontains = "B00").update(is_open = True)

        response = client.get(
            f"{self.mappings_endpoint}?open=true&limit=3", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 9
        assert body["items"] == [
            {
                "code": "B000",
                "death_cause": "ECZEMA HERPETICUM",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "B001",
                "death_cause": "HERPESVIRAL VESICULAR DERMATITIS",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "B002",
                "death_cause": "HERPESVIRAL GINGIVOSTOMATITIS AND PHARYNGOTONSILLITIS",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_mappings_auth_code_ordering(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?ordering=-code__description&limit=3", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 11066
        assert body["items"] == [
            {
                "code": "XXXX",
                "death_cause": "UNKNOWN",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "PEDESTRIAN INJURED IN COLLISION WITH PEDAL CYCLE",
                "category": "UNKNOWN"
            },
            {
                "code": "XXXX",
                "death_cause": "PEDESTRIAN INJURED IN COLLISION WITH PEDAL CYCLE NONTRAFFIC ACCIDENT",
                "category": "UNKNOWN"
            }
        ]

    def test_read_mappings_auth_death_cause_ordering(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?ordering=-death_cause__description&limit=3", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 11066
        assert body["items"] == [
            {
                "code": "B469",
                "death_cause": "ZYGOMYCOSIS UNSPECIFIED",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "B029",
                "death_cause": "ZOSTER WITHOUT COMPLICATION",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            },
            {
                "code": "B022",
                "death_cause": "ZOSTER WITH OTHER NERVOUS SYSTEM INVOLVEMENT",
                "category": "CERTAIN INFECTIOUS AND PARASITIC DISEASES"
            }
        ]

    def test_read_mappings_auth_category_ordering(self, client, access_token):
        response = client.get(
            f"{self.mappings_endpoint}?ordering=code__category__description&limit=3", 
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
        )
        body = response.json()

        assert response.status_code == 200
        assert body["count"] == 11066
        assert body["items"] == [
            {
                "code": "P000",
                "death_cause": "FETUS AND NEWBORN AFFECTED BY MATERNAL HYPERTENSIVE DISORDERS",
                "category": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"
            },
            {
                "code": "P001",
                "death_cause": "FETUS AND NEWBORN AFFECTED BY MATERNAL RENAL AND URINARY TRACT DISEASES",
                "category": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"
            },
            {
                "code": "P002",
                "death_cause": "FETUS AND NEWBORN AFFECTED BY MATERNAL INFECTIOUS AND PARASITIC DISEASES",
                "category": "CERTAIN CONDITIONS ORIGINATING IN THE PERINATAL PERIOD"
            }
        ]
