from rest_framework import serializers


class AtestadoSerializer(serializers.Serializer):
    doctor_name = serializers.CharField(max_length=255)
    crm = serializers.CharField(max_length=50)
    patient_name = serializers.CharField(max_length=255)
    cpf = serializers.CharField(max_length=14)
    data_atendimento = serializers.DateField()
    dias_afastamento = serializers.IntegerField(min_value=1)
    motivo = serializers.CharField()
    cid = serializers.CharField(required=False, allow_blank=True)


class DeclaracaoAcompanhamentoSerializer(serializers.Serializer):
    acompanhante_nome = serializers.CharField(max_length=255)
    relacao = serializers.CharField(max_length=100)
    inicio = serializers.DateTimeField()
    fim = serializers.DateTimeField()
    observacoes = serializers.CharField(required=False, allow_blank=True)


class DeclaracaoComparecimentoSerializer(serializers.Serializer):
    paciente = serializers.CharField(max_length=255)
    horario_comparecimento = serializers.DateTimeField()
    motivo = serializers.CharField()
    duracao = serializers.CharField()


class PrescricaoSerializer(serializers.Serializer):
    medicamentos = serializers.ListField(child=serializers.CharField(max_length=255))
    posologia = serializers.CharField()
    orientacoes = serializers.CharField(required=False, allow_blank=True)
    data = serializers.DateField()
