# core/views.py
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import ContactMessageSerializer

class ContactAPIView(APIView):
    """
    Contact form API with reCAPTCHA validation, message saving,
    admin notification, and user confirmation email.
    """

    def post(self, request):
        # 1. Verify reCAPTCHA
        recaptcha_token = request.data.get("recaptcha_token")
        if not recaptcha_token:
            return Response({"error": "Missing reCAPTCHA token."}, status=status.HTTP_400_BAD_REQUEST)

        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        verify_data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": recaptcha_token
        }
        r = requests.post(verify_url, data=verify_data)
        result = r.json()

        if not result.get("success") or result.get("score", 0) < 0.5:
            return Response({"error": "reCAPTCHA validation failed."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate and save form
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            name = serializer.validated_data["name"]
            email = serializer.validated_data["email"]
            subject = serializer.validated_data["subject"]
            message = serializer.validated_data["message"]

            # 3. Send admin notification
            admin_subject = f"[fbnotes Contact] {subject}"
            admin_message = (
                f"New message received from fbnotes contact form:\n\n"
                f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}\n\n"
                f"-- fbnotes Contact System"
            )

            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=False,
            )

            # 4. Send user confirmation
            user_subject = "Thanks for contacting fbnotes!"
            user_message = (
                f"Hi {name},\n\n"
                f"Thank you for contacting fbnotes. We’ve received your message:\n\n"
                f"\"{message}\"\n\n"
                f"Our team will get back to you soon.\n\n"
                f"Best,\nfbnotes Support Team"
            )

            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )

            return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
