from rest_framework import serializers


class CardData(serializers.Serializer):
    full_name = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='get_full_name')
    birth_date = serializers.DateField(source='userprofile.birth_date')
    active = serializers.BooleanField(source='is_active')
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()

        return representation

    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('worldwide_gross cannot be bigger than us_gross')
        return data

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 1 and 10.')
        return value




    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['key'] = self.context['key']

            return representation


class MP4NFT(CardType):
    '''
    A serializer for the JSON data for cards of this type

    This goes into the value field of the card, perhaps call it data
    '''
    small = serializers.FileField(help_text='The MP4 file scaled down to a thumbnail size for phones.')
    medium = serializers.FileField(help_text='The MP4 file scaled down to the size of a laptop screen.')
    full = serializers.FileField(help_text='The MP4 file without any scaling.')
    overlay = serializers.ChoiceField(
        help_text='How should this file be expanded to fill the screen?',
        choices=(
            ('cover', 'Cover'),
            ('stretch', 'Stretch'),
        )
    )


class NameCard(CardType):
    pass


class CardCompositor(CardType):
    left = CardType()
    right = CardType()


class Profile(CardType):
    pass


class VideoCallCard(CardType):
    pass


class AuthRole(CardType):
    pass


class PermissionCompositor(CardType):
    permission1 = JSONField({})
    permission2 = JSONField({})

    '''
    this subtree of nodes requires permissions 1 and 2 from the coders guild and the shamans guild
    '''

# A card for the AnonymousUser, anyone anonymous can post as the AnonymousUser

class DistributedTaskQueue:
    '''
    Doing work for the good of all beings in this 
    If we trust each other enough we can mirror each others databasesa and run each others code jobs
    If you have 10 people, you can shard in that group,
    heterogeneous mirroring

    You get money for running jobs == crypto mining

    load balancing
    backups

    '''

    
