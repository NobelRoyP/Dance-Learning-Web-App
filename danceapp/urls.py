from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('userregister/',views.userregister,name='userregister'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('userhome/',views.userhome,name='userhome'),
    path('mark_attendance/',views.mark_attendance,name='mark_attendance'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('usereditprofile/',views.usereditprofile,name='usereditprofile'), 
    path('trainerregister/',views.trainerregister,name='trainerregister'), 
    path('trainerlogin/',views.trainerlogin,name='trainerlogin'), 
    path('trainerhome/',views.trainerhome,name='trainerhome'), 
    path('trainerprofile/',views.trainerprofile,name='trainerprofile'), 
    path('trainereditprofile/<int:id>/',views.trainereditprofile,name='trainereditprofile'), 
    path('trainer_student_list/', views.trainer_student_list, name='trainer_student_list'),

    path('institutionregister/',views.institutionregister,name='institutionregister'),
    path('logout/',views.logout,name='logout'), 
    path('institutionlogin/',views.institutionlogin,name='institutionlogin'),
    path('institutiondashboard/',views.institutiondashboard,name='institutiondashboard'),
    path('institutionprofile/',views.institutionprofile,name='institutionprofile'),
    path('institutioneditprofile/',views.institutioneditprofile,name='institutioneditprofile'),
    path('artistregister/', views.artistregister, name='artistregister'),
    path('artistlogin/', views.artistlogin, name='artistlogin'),
    path('artistprofile/', views.artistprofile, name='artistprofile'),
    path('artistdashboard/', views.artistdashboard, name='artistdashboard'),
    path('artisteditprofile/', views.artisteditprofile, name='artisteditprofile'),
    path('shopregister/', views.shopregister, name='shopregister'),
    path('shoplogin/', views.shoplogin, name='shoplogin'),
    path('shopdashboard/', views.shopdashboard, name='shopdashboard'),
    path('shopprofile/', views.shopprofile, name='shopprofile'),
    path('shopeditprofile/', views.shopeditprofile, name='shopeditprofile'),
    path('deleteprofile/<int:id>',views.deleteprofile,name="deleteprofile"),
    path('trainerdeleteprofile/<int:id>',views.trainerdeleteprofile,name="trainerdeleteprofile"),
    path('shopdeleteprofile/<int:id>',views.shopdeleteprofile,name="shopdeleteprofile"),
    path('artistdeleteprofile/<int:id>',views.artistdeleteprofile,name="artistdeleteprofile"),
    path('userlist/', views.user_list, name='userlist'),
    path('admindashboard/',views.admindashboard,name="admindashboard"),
    path('get_batch_attendance/', views.get_batch_attendance, name='get_batch_attendance'),
    path('trainerlist/', views.trainer_list, name='trainerlist'),
    path('shoplist/', views.shop_list, name='shoplist'), 
    path('artistlist/', views.artist_list, name='artistlist'),
    
    path('deleteuser/<int:id>/', views.deleteuser, name='deleteuser'),
    path('approveuser/<int:id>/', views.approveuser, name='approveuser'),
    path('rejectuser/<int:id>/', views.rejectuser, name='rejectuser'),

    path('deletetrainer/<int:id>/', views.deletetrainer, name='deletetrainer'),
    path('deleteshop/<int:id>/', views.deleteshop, name='deleteshop'),
    path('deleteartist/<int:id>/', views.deleteartist, name='deleteartist'),

    path('usertrainers/', views.usertrainers, name='usertrainers'), 
    path('deleteinstitution/<int:id>/', views.deleteinstitution, name='deleteinstitution'),

    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('institutionlist/', views.institution_list, name='institutionlist'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productlist/', views.productlist, name='productlist'),
    path('editproductlist/<int:id>/', views.editproductlist, name='editproductlist'),
    path('deleteproductlist/<int:id>/', views.deleteproductlist, name='deleteproductlist'),
    path('userartist/', views.userartist, name='userartist'),
    path('userinstitution/', views.userinstitution, name='userinstitution'),
    path('usershop/', views.usershop, name='usershop'),
    path('addphotos/', views.addphotos, name='addphotos'),
    path('photolist/',views.photolist,name='photolist'),
    path('ViewProducts/<int:id>/',views.ViewProducts,name="ViewProducts"),
    
    path('approveinstitution/<int:id>/', views.approveinstitution, name='approveinstitution'),
    path('rejectinstitution/<int:id>/', views.rejectinstitution, name='rejectinstitution'),

    path('add_feedback/', views.add_feedback, name='add_feedback'),
    path('feedback_list/', views.feedback_list, name='feedback_list'),

    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<int:id>/', views.edit_course, name='edit_course'),
    path('course_list/', views.course_list, name='course_list'),
    path('delete_course/<int:id>/', views.delete_course, name='delete_course'),

    path('trainerlist_institution/', views.trainerlist_institution, name='trainerlist_institution'),
    path('add_trainer_institution/', views.add_trainer_institution, name='add_trainer_institution'),
    path('delete_trainer_institution/<int:id>/', views.delete_trainer_institution, name='delete_trainer_institution'),
    path('join-institution/<int:id>/', views.join_institution, name='join_institution'),

    path('userlist_institution/', views.userlist_institution, name='userlist_institution'),
    path('approve_request/<int:id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:id>/', views.reject_request, name='reject_request'),
    path('cancel-application/<int:id>/', views.cancel_application, name='cancel_application'),
    path('delete_application/<int:id>/', views.delete_user_application, name='delete_user_application'),


    path('add_reel/', views.add_reel, name='add_reel'),
    path('reel_list/', views.reel_list, name='reel_list'),
    path('delete_reel/<int:id>/', views.delete_reel, name='delete_reel'),
    path('edit_reel/<int:id>/', views.edit_reel, name='edit_reel'),
    path('view_trainer_reels/<int:trainer_id>/', views.view_trainer_reels, name='view_trainer_reels'),

    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),


    # Chat – student side
    path('chat/user/list/',views.user_chat_list,name='user_chat_list'),
    path('chat/user/room/<int:trainer_id>/', views.user_chat_room,  name='user_chat_room'),
    path('chat/user/send/<int:trainer_id>/', views.user_send_message, name='user_send_message'),
    path('chat/user/poll/<int:trainer_id>/', views.user_poll_messages, name='user_poll_messages'),

    # Chat – trainer side
    path('chat/trainer/list/',views.trainer_chat_list,name='trainer_chat_list'),
    path('chat/trainer/room/<int:user_id>/', views.trainer_chat_room,name='trainer_chat_room'),
    path('chat/trainer/send/<int:user_id>/', views.trainer_send_message, name='trainer_send_message'),
    path('chat/trainer/poll/<int:user_id>/', views.trainer_poll_messages, name='trainer_poll_messages'),


    path('product_list_user/', views.product_list_user, name='product_list_user'),
    path('book-costume/<int:product_id>/',views.book_costume,name='book_costume'),
    path('user/bookings/',views.user_bookings,name='user_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/payment/<int:booking_id>/', views.initiate_booking_payment, name='initiate_booking_payment'),
    path('booking/payment/success/', views.booking_payment_success, name='booking_payment_success'),

    # Institution side
    path('institution/bookings/',views.institution_booking_requests,  name='institution_booking_requests'),
    path('institution/bookings/returned/<int:booking_id>/',views.mark_costume_returned,name='mark_costume_returned'),

]








