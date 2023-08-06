# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from facebook_api.admin import FacebookModelAdmin
from models import User


class UserAdmin(FacebookModelAdmin):
    list_display = ('name','first_name','last_name','gender')
    list_display_links = ('name',)
    list_filter = ('gender',)
    search_fields = ('name',)

#    def get_readonly_fields(self, *args, **kwargs):
#        fields = super(UserAdmin, self).get_readonly_fields(*args, **kwargs)
#        return fields + ['likes']


if 'facebook_posts' in settings.INSTALLED_APPS:
    from facebook_posts.models import PostOwner, Comment

    class PostInline(generic.GenericTabularInline):
        model = PostOwner
        ct_field = 'owner_content_type'
        ct_fk_field = 'owner_id'
        fields = ('post',)
        readonly_fields = fields
        extra = False
        can_delete = False

    class CommentInline(generic.GenericTabularInline):
        model = Comment
        ct_field = 'author_content_type'
        ct_fk_field = 'author_id'
        fields = ('message','likes_count')
        readonly_fields = fields
        extra = False
        can_delete = False

    UserAdmin.inlines = [PostInline, CommentInline]

admin.site.register(User, UserAdmin)
