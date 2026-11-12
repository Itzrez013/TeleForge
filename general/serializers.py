from rest_framework import serializers
from .models import Notification,Security_and_Privacy
from persiantools import jdatetime

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['title', 'text', 'created_at']

    def get_created_at(self, obj):
        date = obj.created_at

        jalali_date = jdatetime.JalaliDate(date)

        return jalali_date.strftime('%Y/%m/%d')



class Security_and_PrivacySerializer(serializers.ModelSerializer):
    last_update = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['title', 'text', 'last_update']

    def get_last_update(self, obj):
        date = obj.last_update

        jalali_date = jdatetime.JalaliDate(date)

        return jalali_date.strftime('%Y/%m/%d')

