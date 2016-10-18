from django.contrib.auth.models import User

from django.db.models import Manager


class CompanyModelManager(Manager):
    def create_company(self, **kaargs):
        user = None
        try:
            user = User.objects.get(id=kaargs.get("user_id"))
        except User.DoesNotExist:
            user = User.objects.create_user(kaargs.get("company_email"), kaargs.get("company_email"),
                                            kaargs.get("password"))
            user.first_name = kaargs.get("username").split()[0]
            try:
                if kaargs.get("username").split()[1]:
                    user.last_name = kaargs.get("username").split()[1]
            except:
                pass
            user.save()
            # return  False, "User Does Not exist", None
        company = self.create(company_name=kaargs.get("company_name"), email=kaargs.get("company_email"),
                              ad_reference=kaargs.get("ad_reference"),
                              owner=user)
        return True, "Company Created Successfully", company
