
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from product_images import views


app_name = 'product-images'


urlpatterns = [

    path('upload/', views.upload_image, name='upload'),

    path('remove/<int:image_id>/', views.remove_image, name='remove')

]


app_urls = i18n_patterns(
    path('product-images/', include((urlpatterns, app_name))),
)
