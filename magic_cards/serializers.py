#API for cards serilizers

from rest_framework import serializers
from .models import SetObjects, CoreCardFields, GameplayFields

class SetObjectsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return SetObjects.objects.create(**validated_data)

    class Meta:
        model = SetObjects
        fields = ('id', 'code', 'mtgo_code', 'tcgplayer_id', 'name', 'set_type', 'released_at', 'parent_set_code', 'card_count', 'digital', 'foil_only', 'scryfall_uri', 'uri')

class CoreCardFieldsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CoreCardFields.objects.create(**validated_data)
    
    class Meta:
        model = CoreCardFields 
        fields = ('arena_id', 'id', 'lang', 'mtgo_id', 'mtgo_foil_id', 'tcgplayer_id', 'object', 'oracle_id', 'prints_search_uri', 'rulings_uri', 'scryfall_uri', 'uri')
      
class GameplayFieldsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return GameplayFields.objects.create(**validated_data)
    
    class Meta:
        model = GameplayFields 
        fields = ('cmc', 'colors', 'color_identity', 'color_indicator', 'foil', 'hand_modifier', 'layout', 'legalities', 'life_modifier', 'loyalty', 'mana_cost', 'name', 'nonfoil', 'oracle_text', 'oversized', 'power', 'reserved', 'toughness', 'type_line')



