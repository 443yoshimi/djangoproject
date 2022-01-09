from django.db import models

class Workplan(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sskcd = models.CharField(db_column='SSKCD', max_length=10)  # Field name made lowercase.
    ktncd = models.CharField(db_column='KTNCD', max_length=10)  # Field name made lowercase.
    ckmcd = models.CharField(db_column='CKMCD', max_length=10)  # Field name made lowercase.
    catcd = models.CharField(db_column='CATCD', max_length=10)  # Field name made lowercase.
    hincd = models.CharField(db_column='HINCD', max_length=20)  # Field name made lowercase.
    hinnm = models.CharField(db_column='HINNM', max_length=50)  # Field name made lowercase.
    callcd = models.IntegerField(db_column='CALLCD')  # Field name made lowercase.
    size = models.CharField(db_column='SIZE', max_length=10)  # Field name made lowercase.
    tray = models.CharField(db_column='TRAY', max_length=20)  # Field name made lowercase.
    baitnk = models.IntegerField(db_column='BAITNK')  # Field name made lowercase.
    gozen = models.IntegerField(db_column='GOZEN')  # Field name made lowercase.
    hradd = models.IntegerField(db_column='HRADD')  # Field name made lowercase.
    ggadd = models.IntegerField(db_column='GGADD')  # Field name made lowercase.
    tsadd = models.IntegerField(db_column='TSADD')  # Field name made lowercase.
    yobi1 = models.CharField(db_column='YOBI1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yobi2 = models.CharField(db_column='YOBI2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yobi3 = models.CharField(db_column='YOBI3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yobi4 = models.CharField(db_column='YOBI4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yobi5 = models.CharField(db_column='YOBI5', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sizdate = models.IntegerField(db_column='SIZDATE')  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WORKPLAN'
        


class Hincatmst(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sskcd = models.CharField(db_column='SSKCD', max_length=10)  # Field name made lowercase.
    catcd = models.CharField(db_column='CATCD', max_length=10)  # Field name made lowercase.
    catname = models.CharField(db_column='CATNAME', max_length=50)  # Field namemade lowercase.
    pcatcd = models.IntegerField(db_column='PCATCD', blank=True, null=True)  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HINCATMST'
        unique_together = (('id', 'catcd'),)

    def __str__(self):
        return f"{self.catcd} : {self.catname}" 


class Ckmmst(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sskcd = models.CharField(db_column='SSKCD', max_length=10)  # Field name made lowercase.
    ckmcd = models.CharField(db_column='CKMCD', max_length=10)  # Field name made lowercase.
    ckmname = models.CharField(db_column='CKMNAME', max_length=50)  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CKMMST'
        unique_together = (('id', 'ckmcd'),)

    def __str__(self):
        return f"{self.ckmcd} : {self.ckmname}"


class Sskmst(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sskcd = models.CharField(db_column='SSKCD', max_length=10)  # Field name made lowercase.
    sskname = models.CharField(db_column='SSKNAME', max_length=50)  # Field namemade lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SSKMST'
        unique_together = (('id', 'sskcd'),)

    def __str__(self):
        return f"{self.sskcd} : {self.sskname}"


class Ktnmst(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sskcd = models.CharField(db_column='SSKCD', max_length=10)  # Field name made lowercase.
    ktncd = models.CharField(db_column='KTNCD', max_length=10)  # Field name made lowercase.
    ktnname = models.CharField(db_column='KTNNAME', max_length=50)  # Field namemade lowercase.
    egstrtm = models.IntegerField(db_column='EGSTRTM')  # Field name made lowercase.
    egendtm = models.IntegerField(db_column='EGENDTM')  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTNMST'
        unique_together = (('id', 'ktncd'),)

    def __str__(self):
        return f"{self.ktncd} : {self.ktnname}"

class DateModel(models.Model):
    date_field = models.DateField()


class Hikmeilog(models.Model):
    store_cd = models.IntegerField(db_column='STORE_CD')  # Field name made lowercase.
    jancd = models.CharField(db_column='JANCD', max_length=20)  # Field name made lowercase.
    hikdt = models.DateField(db_column='HIKDT')  # Field name made lowercase.
    hiksu = models.BigIntegerField(db_column='HIKSU')  # Field name made lowercase.
    hikgaku = models.BigIntegerField(db_column='HIKGAKU')  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HIKMEILOG'

class Timesalesmeilog(models.Model):
    deal_date = models.DateField(db_column='DEAL_DATE')  # Field name made lowercase.
    yobi = models.IntegerField(db_column='YOBI')  # Field name made lowercase.
    store_cd = models.IntegerField(db_column='STORE_CD')  # Field name made lowercase.
    jancd = models.CharField(db_column='JANCD', max_length=13)  # Field name made lowercase.
    jancd_2 = models.CharField(db_column='JANCD_2', max_length=13)  # Field name made lowercase.
    hinnm = models.CharField(db_column='HINNM', max_length=50)  # Field name made lowercase.
    seltmzncd = models.IntegerField(db_column='SELTMZNCD')  # Field name made lowercase.
    classcd = models.IntegerField(db_column='CLASSCD')  # Field name made lowercase.
    bmncd = models.IntegerField(db_column='BMNCD')  # Field name made lowercase.
    gentnk = models.BigIntegerField(db_column='GENTNK', blank=True, null=True)  # Field name made lowercase.
    sales_itm = models.BigIntegerField(db_column='SALES_ITM', blank=True, null=True)  # Field name made lowercase.
    sales_amt = models.BigIntegerField(db_column='SALES_AMT', blank=True, null=True)  # Field name made lowercase.
    item_dis_amt = models.BigIntegerField(db_column='ITEM_DIS_AMT', blank=True, null=True)  # Field name made lowercase.
    nebikiritu0 = models.IntegerField(db_column='NebikiRitu0', blank=True, null=True)  # Field name made lowercase.
    nebikiritu10 = models.IntegerField(db_column='NebikiRitu10', blank=True, null=True)  # Field name made lowercase.
    nebikiritu20 = models.IntegerField(db_column='NebikiRitu20', blank=True, null=True)  # Field name made lowercase.
    nebikiritu30 = models.IntegerField(db_column='NebikiRitu30', blank=True, null=True)  # Field name made lowercase.
    nebikiritu40 = models.IntegerField(db_column='NebikiRitu40', blank=True, null=True)  # Field name made lowercase.
    nebikiritu50 = models.IntegerField(db_column='NebikiRitu50', blank=True, null=True)  # Field name made lowercase.
    nebikiritu99 = models.IntegerField(db_column='NebikiRitu99', blank=True, null=True)  # Field name made lowercase.
    lastseltmzncd = models.IntegerField(db_column='LASTSELTMZNCD')  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIMESALESMEILOG'

class Hinmst(models.Model):
    jancd = models.CharField(db_column='JANCD', max_length=13)  # Field name made lowercase.
    hinnm = models.CharField(db_column='HINNM', max_length=100)  # Field name made lowercase.
    ckmcd = models.IntegerField(db_column='CKMCD')  # Field name made lowercase.
    bmncd = models.IntegerField(db_column='BMNCD', blank=True, null=True)  # Field name made lowercase.
    linecd = models.IntegerField(db_column='LINECD', blank=True, null=True)  # Field name made lowercase.
    classcd = models.IntegerField(db_column='CLASSCD', blank=True, null=True)  # Field name made lowercase.
    catcd = models.CharField(db_column='CATCD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    syokbn = models.CharField(db_column='SYOKBN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tankakng = models.BigIntegerField(db_column='TANKAKNG', blank=True, null=True)  # Field name made lowercase.
    baitnk = models.BigIntegerField(db_column='BAITNK', blank=True, null=True)  # Field name made lowercase.
    gentnk = models.DecimalField(db_column='GENTNK', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    yobi1 = models.CharField(db_column='YOBI1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yobi2 = models.CharField(db_column='YOBI2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yobi3 = models.CharField(db_column='YOBI3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yobi4 = models.CharField(db_column='YOBI4', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yobi5 = models.CharField(db_column='YOBI5', max_length=20, blank=True, null=True)  # Field name made lowercase.
    makdt = models.DateTimeField(db_column='MAKDT')  # Field name made lowercase.
    updt = models.DateTimeField(db_column='UPDT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HINMST'
        