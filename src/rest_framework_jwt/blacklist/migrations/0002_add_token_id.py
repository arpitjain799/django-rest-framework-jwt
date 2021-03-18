# Generated by Django 3.1.4 on 2020-12-12 12:15

from django.db import migrations, models
from django import VERSION

import jwt


def add_token_id_values(apps, schema_editor):
    """Fill in token_id values for existing token records that have a token id
    """
    BlacklistedToken = apps.get_model('blacklist', 'BlacklistedToken')
    for row in BlacklistedToken.objects.filter(token_id=None):
        payload = jwt.decode(row.token)
        token_id = payload.get('orig_jti') or payload.get('jti')
        if token_id:
            row.token_id = token_id
            row.save(update_fields=['token_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklistedtoken',
            name='token_id',
            field=models.UUIDField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='token',
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.RunPython(add_token_id_values, reverse_code=migrations.RunPython.noop)
    ]
    if VERSION >= (2, 2):
        operations.append(
            migrations.AddConstraint(
                model_name='blacklistedtoken',
                constraint=models.CheckConstraint(
                    check=models.Q(token_id__isnull=False) | models.Q(token__isnull=False),
                    name='token_or_id_not_null',
                ),
            )
        )