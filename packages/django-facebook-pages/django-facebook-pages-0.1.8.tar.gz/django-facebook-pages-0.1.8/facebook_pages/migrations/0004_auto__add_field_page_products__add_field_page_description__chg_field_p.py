# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.products'
        db.add_column('facebook_pages_page', 'products',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Page.description'
        db.add_column('facebook_pages_page', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'Page.website'
        db.alter_column('facebook_pages_page', 'website', self.gf('django.db.models.fields.CharField')(max_length=300))
    def backwards(self, orm):
        # Deleting field 'Page.products'
        db.delete_column('facebook_pages_page', 'products')

        # Deleting field 'Page.description'
        db.delete_column('facebook_pages_page', 'description')


        # Changing field 'Page.website'
        db.alter_column('facebook_pages_page', 'website', self.gf('django.db.models.fields.CharField')(max_length=100))
    models = {
        'facebook_pages.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'can_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'checkins': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'company_overview': ('django.db.models.fields.TextField', [], {}),
            'cover': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'location': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posts_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'products': ('django.db.models.fields.TextField', [], {}),
            'talking_about_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['facebook_pages']