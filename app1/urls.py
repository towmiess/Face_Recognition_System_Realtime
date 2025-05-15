from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard Views
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employe-dashboard/', views.employe_dashboard, name='employe_dashboard'),
    
    # this is for object detection
    path('ppe-page', views.ppe, name='ppe-page'),  # URL to the YoloPage

    # Employe Registration and Attendance
    path('register_employe/', views.register_employe, name='register_employe'),
    path('mark_attendance', views.mark_attendance, name='mark_attendance'),
    path('register_success/', views.register_success, name='register_success'),
    path('employes/', views.employe_list, name='employe-list'),
    path('employe/<int:pk>/', views.employe_detail, name='employe-detail'),
    path('employes/attendance/', views.employe_attendance_list, name='employe_attendance_list'),
    path('employes/<int:pk>/authorize/', views.employe_authorize, name='employe-authorize'),
    path('employes/<int:pk>/delete/', views.employe_delete, name='employe-delete'),
    path('employes/edit/<int:pk>/', views.employe_edit, name='employe-edit'),
    
    # Capture and Recognize Views
    path('capture-and-recognize/', views.capture_and_recognize, name='capture_and_recognize'),
    path('recognize_with_cam/', views.capture_and_recognize_with_cam, name='capture_and_recognize_with_cam'),
    
    # User Authentication Views
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Attendance Notifications
    path('send_attendance_notifications', views.send_attendance_notifications, name='send_attendance_notifications'),
    
    # Late Check-in Policies
    path('late_checkin_policy_list/', views.late_checkin_policy_list, name='late_checkin_policy_list'),
    path('late-checkin-policies/create/', views.create_late_checkin_policy, name='create_late_checkin_policy'),
    path('late-checkin-policies/<int:policy_id>/update/',views.update_late_checkin_policy, name='update_late_checkin_policy'),
    path('delete-late-checkin-policy/<int:policy_id>/', views.delete_late_checkin_policy, name='delete_late_checkin_policy'),
    
    ########################################################### Camera Configurations
    path('camera-config/', views.camera_config_create, name='camera_config_create'),
    path('camera-config/list/', views.camera_config_list, name='camera_config_list'),
    path('camera-config/update/<int:pk>/', views.camera_config_update, name='camera_config_update'),
    path('camera-config/delete/<int:pk>/', views.camera_config_delete, name='camera_config_delete'),
    
    # Attendance (General View)
    path('attendance/', views.employe_attendance, name='employe_attendance'),
    # For email adding and upateing and editing
    path('email-configs/', views.view_email_configs, name='view_email_configs'),
    path('email-configs/add/', views.add_email_config, name='add_email_config'),
    path('email-configs/edit/<int:email_config_id>/', views.edit_email_config, name='edit_email_config'),
    path('email-configs/delete/<int:email_config_id>/', views.delete_email_config, name='delete_email_config'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/update/<int:pk>/', views.department_update, name='department_update'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),

    # This url is for check out time policy settings
    path('settings-list/', views.settings_list, name='settings_list'),
    path('settings/create/', views.create_settings, name='create_settings'),
    path('settings/<int:pk>/update/', views.update_settings, name='update_settings'),
    path('settings/<int:pk>/delete/', views.delete_settings, name='delete_settings'),
    #######################################
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/<int:pk>/delete/', views.leave_delete, name='leave_delete'),
    path('leaves/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leaves/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
    ###########################################
    path('employe_leave_list/', views.employe_leave_list, name='employe_leave_list'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),


    path('salaries/', views.salary_list, name='salary_list'),
    path('salary/add/', views.add_salary, name='add_salary'),
    path('salary/detail/<int:salary_id>/', views.salary_detail, name='salary_detail'),  # URL for Salary Detail
    path('salary/detail/<int:salary_id>/', views.salary_detail, name='salary_detail'),  # URL for Salary Detail
    path('salary/detail/<int:salary_id>/', views.salary_detail, name='salary_detail'),  # URL for Salary Detail
    path('salary/update/<int:salary_id>/', views.update_salary, name='update_salary'),
    path('salary/delete/<int:salary_id>/', views.delete_salary, name='delete_salary'),

    path('emp_salary_detail/', views.employe_salary_detail, name='employe_salary_detail'),
    path('upload_face_image/', views.upload_face_image, name='upload_face_image'),


]
