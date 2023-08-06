# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PushMessage.message'
        db.alter_column('scarface_pushmessage', 'message', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'PushMessage.message'
        db.alter_column('scarface_pushmessage', 'message', self.gf('django.db.models.fields.TextField')())

    models = {
        'scarface.pushmessage': {
            'Meta': {'object_name': 'PushMessage'},
            'badge_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "'default'"}),
            'context_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "'none'"}),
            'extra_payload': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_new_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'default': "''"}),
            'message_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'receiver_arn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sound': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['scarface']