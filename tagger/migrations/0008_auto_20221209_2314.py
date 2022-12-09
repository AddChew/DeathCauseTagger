# Generated by Django 3.2.9 on 2022-12-09 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tagger', '0007_auto_20221209_2313'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF description, search_vector
            ON tagger_newcategory
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', description
            );
            UPDATE tagger_newcategory SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON tagger_newcategory;
            """
        )
    ]