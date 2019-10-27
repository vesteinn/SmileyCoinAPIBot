from django.urls import include, path
from django.contrib import admin
from rest_framework import routers

from block.api import views


class Router(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        root_view = super(Router, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__name__ = "SmileyCoin API"
        root_view.cls.__doc__ = "Navigate and search the SmileyCoin blockchain"
        return root_view


router = Router()
router.register(r'blocks', views.BlockViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'vouts', views.VoutViewSet)
router.register(r'vins', views.VinViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'op_returns', views.OpReturnViewSet)


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
