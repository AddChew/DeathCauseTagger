from django.contrib.postgres.search import SearchVector
from django.db import migrations


# def compute_search_vector(apps, schema_editor):
#     Mapping = apps.get_model("tagger", "Mapping")
#     Mapping.objects.update(
#         search_vector=SearchVector("description", "icd__description", "icd__code", "icd__category__description")
#     )


class Migration(migrations.Migration):

    dependencies = [
        ("tagger", "0004_mapping_tagger_mapp_search__3cf9c6_gin"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE FUNCTION update_mapping_search_vector()
            RETURNS TRIGGER
            LANGUAGE plpgsql AS $$
            BEGIN
                SELECT
                    to_tsvector(coalesce(NEW.description, '')) ||
                    to_tsvector(
                        (SELECT coalesce(description, '')
                         FROM tagger_icd WHERE id = NEW.icd_id)
                    ) ||
                    to_tsvector(
                        (SELECT coalesce(code, '')
                         FROM tagger_icd WHERE id = NEW.icd_id)
                    ) ||
                    to_tsvector(
                        (SELECT coalesce(b.description, '')
                         FROM tagger_icd a
                         INNER JOIN tagger_category b
                         ON a.category_id = b.id
                         WHERE a.id = NEW.icd_id)
                    )
                INTO NEW.search_vector;
                RETURN NEW;
            END;
            $$;

            CREATE TRIGGER mapping_update_trigger
            BEFORE INSERT OR UPDATE OF description, icd_id, search_vector
            ON tagger_mapping
            FOR EACH ROW EXECUTE PROCEDURE
            update_mapping_search_vector();

            UPDATE tagger_mapping SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS mapping_update_trigger
            ON tagger_mapping;

            DROP FUNCTION update_mapping_search_vector();
            """,
        ),
        # migrations.RunPython(
        #     compute_search_vector, reverse_code=migrations.RunPython.noop
        # ),
    ]