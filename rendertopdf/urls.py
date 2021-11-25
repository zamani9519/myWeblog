from django.urls import path
from .views import topdf

name_app = "rendertopdf"
urlpatterns = [
    path('pdf/<slug:slug>',topdf, name="topdf"),
    # path('api', api ,name="api")
]
