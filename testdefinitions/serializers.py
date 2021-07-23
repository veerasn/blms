from rest_framework import serializers
from testdefinitions.models import TestDef, TestComposition


class TestCompositionSerializer(serializers.ModelSerializer):

    test = serializers.ReadOnlyField(source='to_test_def.component')
    description = serializers.ReadOnlyField(source='to_test_def.long_common_name')
    test_id = serializers.ReadOnlyField(source='to_test_def.loinc_num')

    class Meta:
        model = TestComposition
        fields = ['test', 'description', 'test_id']


class TestDefSerializer(serializers.ModelSerializer):

    components = TestCompositionSerializer(source='from_test_defs', many=True)

    class Meta:
        model = TestDef
        fields = ('loinc_num', 'component', 'long_common_name', 'PanelType', 'components')





