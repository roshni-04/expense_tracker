from rest_framework import serializers
from . models import Category,Activity

#company model serializer
class CatSerializer(serializers.HyperlinkedModelSerializer):
    cat_id=serializers.ReadOnlyField()#display read only fields
    class Meta:
        model=Category
        fields="__all__"#serialize all fields of company models
        #('name','location','active') serialise only these 3 fields
        
#in this serialiser category is treated as a link
class ActSerializer(serializers.HyperlinkedModelSerializer):
    ac_id=serializers.ReadOnlyField()#display read only fields
   
    class Meta:
        model=Activity
        fields="__all__"#serialize all fields of company models
        #('name','location','active') serialise only these 3 fields


#in this serializer category is treated as a nested object
class ActCatLinkedSerializer(serializers.HyperlinkedModelSerializer):
    ac_id=serializers.ReadOnlyField()#display read only fields
    a_cat=CatSerializer()  #use a nested serializer to include the related category data
    class Meta:
        model=Activity
        fields="__all__"