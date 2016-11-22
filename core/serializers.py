from rest_framework import serializers

class CompanyModelSerializer(serializers.Serializer):
    # owner = serializers.ForeignKey(User)
    company_name = serializers.CharField(max_length=150)
    company_email = serializers.CharField(max_length=150)
    # company_phone_no = serializers.CharField(max_length=10)
    # ad_reference = serializers.CharField(max_length=1)
    # is_claimed = serializers.BooleanField()
    # is_approved = serializers.BooleanField()

    #Company Subscription
    # sub_plan = serializers.ForeignKey(SubscriptionPlan)
    # sub_begin_date =  serializers.DateField()
    # sub_end_date = serializers.DateField()
    # is_sub_active = serializers.BooleanField()

    #Requirement subscription
    # req_sub_begin_date =  serializers.DateField()
    # req_sub_end_date = serializers.DateField()
    # is_req_sub_active = serializers.BooleanFiseld()



    # email = serializers.EmailField()
    # content = serializers.CharField(max_length=200)
    # created = serializers.DateTimeField()
