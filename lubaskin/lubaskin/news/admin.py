from django.contrib import admin
from .models import News, Category,Comment,Code
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from django import forms
# Register your models here.

class NewsAdminForm(forms.ModelForm):
    
    class Meta:
        model = News
        fields = '__all__' # для поля контент подключаем эдитор

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm # подключаем эдитор
    list_display = ('id','title','category','created_at','updated_at','is_published','get_photo')
    fields = ('photo','get_photo')
    list_display_links = ('id','title','category')
    search_fields = ('title','content')
    list_editable = ('is_published',)
    list_filter = ('is_published','category','id')
    fields = ('id','title','content','category','is_published','created_at','updated_at','photo','get_photo')
    readonly_fields = ('get_photo','created_at','updated_at','id')
    
    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('news','name','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','news')

class CodeAdmin(admin.ModelAdmin):
    list_display = ('id','user_name','user_code')
    search_fields = ('id','user_name')

admin.site.register(News, NewsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Code,CodeAdmin)
admin.site.site_header = 'Hi! LUBASKIN_CODE!'
admin.site.site_title = 'ADMIN'
