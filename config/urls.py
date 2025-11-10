from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("greatKart.urls")),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('account/', include('accounts.urls')),
    
    # ORDERS
    path('orders/',include('orders.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
