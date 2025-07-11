# alx_backend_graphql_crm/urls.py

from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from ..crm.schema import schema  # <-- Add this line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
]
