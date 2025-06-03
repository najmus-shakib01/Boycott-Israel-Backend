from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactFormSerializer
from django.core.mail import EmailMessage
import logging
logger = logging.getLogger(__name__)
import os

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = f"New message from {name} ({email})"
            email_message = f"""
            You have received a new message from your website :

            Name :- {name}
            Email :- {email}
            Message :-
            {message}
            """
            from_email=os.environ.get("EMAIL")
           
            try:
                admin_email_obj = EmailMessage(
                    subject=subject,
                    body=email_message,
                    from_email=from_email,
                    to=[from_email],
                    reply_to=[email]
                )
                admin_email_obj.send(fail_silently=False)

                user_email_obj = EmailMessage(
                    subject="ধন্যবাদ আপনাকে আপনার মতামত জানানোর জন্য!",
                    body=f"হাই {name},\n\nযোগাযোগের জন্য ধন্যবাদ। আমরা আপনার বার্তা পেয়েছি।\n\nআপনার মেসেজটি ছিল : \n{message}",
                    from_email=from_email,
                    to=[email]
                )
                user_email_obj.send(fail_silently=False)

                return Response({"message": "Email sent successfully! Please Check Your Email"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
