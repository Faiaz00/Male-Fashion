from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [ 
    path('', views.home, name = 'home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='showcart'),

    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

    path('search/', views.search, name='search'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('about/', views.about, name = 'about'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('details/', views.shopdetails, name = 'shopdetails'),
    path('blog/', views.blog, name = 'blog'),
    path('blogdetails/', views.blogdetails, name = 'blogdetails'),
    path('contact/', views.contact, name = 'contact'),
    path('shop/', views.shop, name = 'shop'),
    path('acccategory/', views.accessories_category_view, name = 'accessoriescategory'),


    path('clothings/', views.clothing, name='clothing'),
    path('accessories', views.accessories, name='accessories'),
    path('shoes', views.shoes, name='shoes'),


    path('clothings/tshirt/', views.tshirt_view, name='tshirts'),
    path('clothings/pant/', views.pant_view, name='pants'),
    path('clothings/jacket/', views.jacket_view, name='jackets'),
    path('clothings/hoodie/', views.hoodie_view, name='hoodies'),


    path('accessories/watches/', views.watches_view, name='watches'),
    path('accessories/bags/', views.bags_view, name='bags'),
    path('accessories/belts/', views.belts_view, name='belts'),
    path('accessories/sunglasses/', views.sunglasses_view, name='sunglasses'),


    path('shoes/sandals/', views.sandals_view, name='sandals'),
    path('shoes/boots/', views.boots_view, name='boots'),
    path('shoes/loafers/', views.loafers_view, name='loafers'),
    path('shoes/sneakers/', views.sneakers_view, name='sneakers'),



    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='shop/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name = 'passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='shop/passwordchangedone.html'), name = 'passwordchangedone'),
    #path('checkout/process/', views.process_checkout, name='process_checkout'),
    path('order-success/', views.order_success, name='order_success'),

    path('password-reset', auth_views.PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'),name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)