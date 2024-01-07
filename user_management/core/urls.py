from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import UserView
   

schema_view = get_schema_view(
    openapi.Info(
        title="NextGenAi",
        default_version='2.0',
        description="Me going again working on a NextGenAi project with a superb team😅😅",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="maestro@allcanlearn.me"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # url='https://laughing-computing-machine-gj696v7xvxw2wpw6-8000.app.github.dev' # comment this line. It's for my codespace
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('user', UserView.as_view(), name='user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)