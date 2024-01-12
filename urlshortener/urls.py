from django.urls import path

from urlshortener.views import CreateURLMapRecordView, URLRedirectView, CreateTokenView


urlpatterns = [
    path('api/urlmap/', CreateURLMapRecordView.as_view(), name='create-urlmap-record'),
    path('api/auth/', CreateTokenView.as_view(), name='create-token'),
    path('<str:key>/', URLRedirectView.as_view(), name='redirecter'),
]
