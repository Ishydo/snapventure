import models

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = (
            'id',
            'bio',
            'location',
        )


class JourneySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Journey
        fields = (
            'id',
            'name',
            'created',
            'last_updated',
            'description',
            'img_description',
            'img_ambiance',
            'start_time',
            'end_time',
            'private',
            'active',
            'deleted',
        )


class InscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inscription
        fields = (
            'id',
            'name',
            'created',
            'last_updated',
        )


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Type
        fields = (
            'id',
            'name',
            'created',
            'last_updated',
            'description',
        )


class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Step
        fields = (
            #'id',
            'name',
            'created',
            'last_updated',
            'content_text',
            'content_url',
            'journey',
            'qrcode_uuid',
            'final',
        )


class ScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Scan
        fields = (
            'id',
            'name',
            'created',
            'last_updated',
        )
