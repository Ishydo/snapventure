import models
import serializers
from rest_framework import viewsets, permissions


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for the Profile class"""

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated] # Here are the difinitions of permissions


class JourneyViewSet(viewsets.ModelViewSet):
    """ViewSet for the Journey class"""

    queryset = models.Journey.objects.all()
    serializer_class = serializers.JourneySerializer
    permission_classes = [permissions.IsAuthenticated]


class InscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Inscription class"""

    queryset = models.Inscription.objects.all()
    serializer_class = serializers.InscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Type class"""

    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class StepViewSet(viewsets.ModelViewSet):
    """ViewSet for the Step class"""

    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScanViewSet(viewsets.ModelViewSet):
    """ViewSet for the Scan class"""

    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
