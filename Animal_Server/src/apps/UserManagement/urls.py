from django.urls import path

from .views import Common_userBatchActivationView
from .views import Common_userUserView, AdminUserView
from .views import Common_userLoginView, AdminLoginView
from .views import Common_userChangePasswordView, AdminChangePasswordView,Common_userRegistrationView, AdminRegistrationView
from .views import UploadFileForCommon_userView

urlpatterns = [
    path('common_user/', Common_userUserView.as_view(), name='Common_userOpts'),
    path('common_user/<str:id>/', Common_userUserView.as_view(), name='Common_userDetail'),
    path('admin/', AdminUserView.as_view(), name='AdminOpts'),
    path('admin/<str:id>/', AdminUserView.as_view(), name='AdminDetail'),
    path('adminLogin/', AdminLoginView.as_view(), name='AdminLogin'),
    path('common_userLogin/', Common_userLoginView.as_view(), name='Common_userLogin'),
    path('common_userRegister/',Common_userRegistrationView.as_view(), name='Common_userRegister'),
    path('adminRegister/',AdminRegistrationView.as_view(), name='AdminRegister'),
    path('common_userBatchActivation/', Common_userBatchActivationView.as_view(), name='Common_userBatchActivation'),
    path('common_userChangePassword/<str:user_id>/', Common_userChangePasswordView.as_view(), name='Common_userChangePassword'),
    path('adminChangePassword/<str:user_id>/', AdminChangePasswordView.as_view(), name='AdminChangePassword'),
    path('uploadFileForCommon_user/', UploadFileForCommon_userView.as_view(), name='UploadFileForCommon_user'),
]


if __name__ == '__main__':
    pass
