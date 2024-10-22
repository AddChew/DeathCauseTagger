import pytest


@pytest.mark.django_db
class TestTag:
    tag_endpoint = "/api/v1/tag"
        
    def test_tag_single_tag(self, client):
        response = client.get(
            self.tag_endpoint, 
            query_params = {"death_cause": "PARATYPHOID FEVER A", "period": 365}
        )
        body = response.json()

        assert response.status_code == 200
        assert body == {
            "description": "PARATYPHOID FEVER A",
            "period": 365,
            "tag": {
                "code": "A011",
                "death_cause": "PARATYPHOID FEVER A"
            }
        }

    def test_tag_single_tag_period(self, client):
        response = client.get(
            self.tag_endpoint, 
            query_params = {"death_cause": "stroke", "period": 1}
        )
        body = response.json()

        assert response.status_code == 200
        assert body == {
            "description": "stroke",
            "period": 1,
            "tag": {
                "code": "I64X",
                "death_cause": "STROKE NOT SPECIFIED AS HAEMORRHAGE OR INFARCTION"
            }
        }

        response = client.get(
            self.tag_endpoint, 
            query_params = {"death_cause": "stroke", "period": 365}
        )
        body = response.json()

        assert response.status_code == 200
        assert body == {
            "description": "stroke",
            "period": 365,
            "tag": {
                "code": "I694",
                "death_cause": "SEQUELAE OF STROKE NOT SPECIFIED AS HAEMORRHAGE OR INFARCTION"
            }
        }

    def test_tag_single_options(self, client):
        response = client.get(
            self.tag_endpoint, 
            query_params = {"death_cause": "ischaemic hear disease", "period": 1}
        )
        body = response.json()

        assert response.status_code == 200
        assert body == {
            "description": "ischaemic hear disease",
            "period": 1,
            "options": [
                {
                    "code": "I259",
                    "death_cause": "CHRONIC ISCHAEMIC HEART DISEASE UNSPECIFIED",
                    "score": 0.88
                },
                {
                    "code": "I249",
                    "death_cause": "ACUTE ISCHAEMIC HEART DISEASE UNSPECIFIED",
                    "score": 0.7096774
                },
                {
                    "code": "K559",
                    "death_cause": "VASCULAR DISORDER OF INTESTINE UNSPECIFIED",
                    "score": 0.62068963
                },
                {
                    "code": "I119",
                    "death_cause": "HYPERTENSIVE HEART DISEASE WITHOUT CONGESTIVE HEART FAILURE",
                    "score": 0.5365854
                },
                {
                    "code": "I248",
                    "death_cause": "OTHER FORMS OF ACUTE ISCHAEMIC HEART DISEASE",
                    "score": 0.4888889
                }
            ]
        }
