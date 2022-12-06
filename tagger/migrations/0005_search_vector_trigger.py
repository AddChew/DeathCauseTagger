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

            CREATE OR REPLACE FUNCTION update_icd()
            RETURNS TRIGGER
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tagger_mapping SET search_vector = NULL
                WHERE icd_id = NEW.id;
                RETURN NEW;
            END;
            $$;

            CREATE OR REPLACE FUNCTION delete_icd()
            RETURNS TRIGGER
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tagger_mapping SET search_vector = NULL
                WHERE icd_id = OLD.id;
                RETURN OLD;
            END;
            $$;

            CREATE OR REPLACE FUNCTION update_category()
            RETURNS TRIGGER
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tagger_mapping
                SET search_vector = NULL
                FROM tagger_mapping a
                INNER JOIN tagger_icd b
                ON a.icd_id = b.id
                WHERE b.category_id = NEW.id;
                RETURN NEW;
            END;
            $$;

            CREATE OR REPLACE FUNCTION delete_category()
            RETURNS TRIGGER
            LANGUAGE plpgsql AS $$
            BEGIN
                UPDATE tagger_mapping a 
                SET search_vector = NULL
                FROM tagger_mapping a
                INNER JOIN tagger_icd b
                ON a.icd_id = b.id
                WHERE b.category_id = OLD.id;
                RETURN OLD;
            END;
            $$;

            CREATE TRIGGER mapping_update_trigger
            BEFORE INSERT OR UPDATE OF description, icd_id, search_vector
            ON tagger_mapping
            FOR EACH ROW EXECUTE PROCEDURE
            update_mapping_search_vector();

            CREATE TRIGGER icd_update_trigger
            AFTER UPDATE OF code, description, category_id 
            ON tagger_icd
            FOR EACH ROW EXECUTE PROCEDURE 
            update_icd();

            CREATE TRIGGER icd_delete_trigger
            AFTER DELETE
            ON tagger_icd
            FOR EACH ROW EXECUTE PROCEDURE 
            delete_icd();

            CREATE TRIGGER category_update_trigger
            AFTER UPDATE OF description
            ON tagger_category
            FOR EACH ROW EXECUTE PROCEDURE 
            update_category();

            CREATE TRIGGER category_delete_trigger
            AFTER DELETE
            ON tagger_category
            FOR EACH ROW EXECUTE PROCEDURE 
            delete_category();

            UPDATE tagger_mapping SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS mapping_update_trigger
            ON tagger_mapping;

            DROP TRIGGER IF EXISTS icd_update_trigger
            ON tagger_icd;   

            DROP TRIGGER IF EXISTS icd_delete_trigger
            ON tagger_icd;

            DROP TRIGGER IF EXISTS category_update_trigger
            ON tagger_category;   

            DROP TRIGGER IF EXISTS category_delete_trigger
            ON tagger_category;     

            DROP FUNCTION update_mapping_search_vector();
            DROP FUNCTION update_icd();
            DROP FUNCTION delete_icd();
            DROP FUNCTION update_category();
            DROP FUNCTION delete_category();
            """,
        ),
        # migrations.RunPython(
        #     compute_search_vector, reverse_code=migrations.RunPython.noop
        # ),
    ]