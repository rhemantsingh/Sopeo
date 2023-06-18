"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Inventory.views import home, show, all_items, view_item, sell_item, new_item,\
    order_item, edit_item, show_order, receive_order, cancel_order, received_orders, \
    cancelled_orders, sold_items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('show', show),
    path('items', all_items),
    path('item/<int:id>', view_item),
    path('sell/<int:id>', sell_item),
    path('create', new_item),
    path('item/order/<int:id>', order_item),
    path('item/edit/<int:id>', edit_item),
    path('item/showOrder/<int:id>', show_order),
    path('item/showOrder/receive/<int:id>', receive_order),
    path('item/showOrder/cancel/<int:id>', cancel_order),
    path('item/received/<int:id>', received_orders),
    path('item/cancelled/<int:id>', cancelled_orders),
    path('item/sold/<int:id>', sold_items),
]
