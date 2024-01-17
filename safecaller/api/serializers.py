from rest_framework import serializers
from .models import Contact, RegisteredUser, SpamReport


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact

        fields = "__all__"

        read_only_fields = ["spam_reports", "is_spam"]


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser

        fields = "__all__"

        read_only_fields = ["is_logged_in", "personal_contacts"]

    def create(self, validated_data):
        user = RegisteredUser.objects.create(
            name=validated_data["name"],
            number=validated_data["number"],
            email=validated_data.get("email", ""),
            hashed_password=validated_data["hashed_password"]
        )

        return user


class RegisteredUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser

        fields = ["number", "hashed_password"]


class RegisteredUserLogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser

        fields = []


class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport

        fields = ["reported_number"]

    def create(self, validated_data):
        # Extract the 'reported_number' from the validated data
        reported_number = validated_data.get("reported_number")

        # Create the SpamReport object
        spam_report = SpamReport.objects.create(
            reported_number=reported_number,
            # Assign the reporter from the request user
            reporter=self.context['request'].user
        )

        return spam_report
