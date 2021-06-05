from os import path

from flask_admin.contrib import sqla
from flask_admin_s3_upload import S3ImageUploadField

from flaskygram.database import db
from flaskygram.extensions import admin
from flaskygram.library.get_setting_value import get_setting_value
from flaskygram.library.prefix_file_utcnow import prefix_file_utcnow
from .models import Media


class MediaAdminView(sqla.ModelView):
    column_list = ('image',)
    form_excluded_columns = ('image_storage_type',
                             'image_storage_bucket_name')

    form_overrides = dict(
        image=S3ImageUploadField)

    form_args = dict(
        image=dict(
            base_path=get_setting_value('UPLOADS_FOLDER'),
            relative_path=get_setting_value('THINGY_IMAGE_RELATIVE_PATH'),
            url_relative_path=get_setting_value('UPLOADS_RELATIVE_PATH'),
            namegen=prefix_file_utcnow,
            storage_type_field='image_storage_type',
            bucket_name_field='image_storage_bucket_name',
        ))

    def scaffold_form(self):
        form_class = super(MediaAdminView, self).scaffold_form()
        static_root_parent = path.abspath(get_setting_value('PROJECT_ROOT'))

        if get_setting_value('USE_S3'):
            form_class.image.kwargs['storage_type'] = 's3'

        form_class.image.kwargs['bucket_name'] = get_setting_value('S3_BUCKET_NAME')
        form_class.image.kwargs['access_key_id'] = get_setting_value('AWS_ACCESS_KEY_ID')
        form_class.image.kwargs['access_key_secret'] = get_setting_value('AWS_SECRET_ACCESS_KEY')
        form_class.image.kwargs['static_root_parent'] = static_root_parent

        return form_class


admin.add_view(MediaAdminView(Media, session=db.session, name='Media', category='Media'))

