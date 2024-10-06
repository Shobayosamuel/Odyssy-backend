# from datetime import datetime, timedelta
# import jwt
# from django.conf import settings
# from django.core.mail import send_mail
# from django.utils import timezone

# from authentication import models

# class UserVerifier:
#     encoding_algorithm = settings.ENCODING_ALGORITHM

#     def __init__(self, user: models.CustomUser = None):
#         self.user = user
#         self.is_admin = user.is_superuser if user else False

#     def get_path(self, action):
#         if action == "reset_password":
#             return f"{settings.HOST_CLIENT_URL}/reset-password" if self.is_admin else f"{settings.CLIENT_URL}/new-password"
#         elif action == "verification":
#             return f"{settings.CLIENT_URL}/signup/verification"

#     def generate_encryption_payload(self):
#         return {
#             "email": self.user.email,
#             "expiresAt": datetime.strftime(
#                 timezone.now() + timedelta(days=1), "%Y-%m-%dT%H:%M"
#             ),
#         }

#     def generate_token(self):
#         payload = self.generate_encryption_payload()
#         encoded_jwt = jwt.encode(
#             payload, settings.SECRET_KEY, algorithm=self.encoding_algorithm
#         )
#         return encoded_jwt

#     def generate_verification_email_message(self, email, token):
#         verification_path = self.get_path("verification")
#         query_parameters = f"?token={token}&email={email}"
#         full_link = verification_path + query_parameters
#         message = f"Hello {self.user.first_name}!\nPlease click the link below to verify your account.\nLink: {full_link}"
#         subject = "Let's Get You Verified"
#         return message, subject

#     def generate_password_reset_email_message(self, email, token):
#         reset_path = self.get_path("reset_password")
#         query_parameters = f"?token={token}&email={email}"
#         full_link = reset_path + query_parameters
#         message = f"Hello {self.user.first_name}!\nPlease click the link below to reset your password.\nLink: {full_link}"
#         subject = "Reset Your Password"
#         return message, subject

#     def send_token_to_mail(self, token, purpose=None):
#         if purpose == "reset_password":
#             message, subject = self.generate_password_reset_email_message(self.user.email, token)
#         else:
#             message, subject = self.generate_verification_email_message(self.user.email, token)

#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[self.user.email],
#             fail_silently=False,
#         )

#     def check_expired(self):
#         token_date_str = self.payload["expiresAt"]
#         format = "%Y-%m-%dT%H:%M"
#         token_date = datetime.strptime(token_date_str, format)
#         day_difference = timezone.now() - timezone.make_aware(token_date)
#         return day_difference.days > 1

#     def decode_token(self, token):
#         try:
#             resulting_payload = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms=[self.encoding_algorithm]
#             )
#         except jwt.exceptions.ImmatureSignatureError:
#             return False, "Invalid signature"
#         else:
#             self.payload = resulting_payload
#             return True, "Token validated"

#     def verify_user(self, email):
#         if self.check_expired():
#             return False, "Token expired"
#         try:
#             claiming_user = models.User.objects.get(email=email)
#             encrypted_user = models.User.objects.get(email=self.payload["email"])
#             if claiming_user.pk == encrypted_user.pk:
#                 self.user = encrypted_user
#                 return True, "User matches"
#             else:
#                 return False, "Claiming user does not match encrypted user"
#         except models.User.DoesNotExist:
#             return False, "User does not exist"
