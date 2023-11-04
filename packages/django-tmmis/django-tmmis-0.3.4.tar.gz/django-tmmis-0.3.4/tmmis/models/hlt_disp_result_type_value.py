from .base_model import *


class HltDispResultTypeValue(BaseModel):
    """
    Значения типов результата
    """

    id = models.AutoField(db_column="disp_ResultTypeValueID", primary_key=True)
    code = models.CharField(db_column="Code", max_length=100)
    date_begin = models.DateTimeField(db_column="DateBegin")
    date_end = models.DateTimeField(db_column="DateEnd")
    flags = models.IntegerField(db_column="Flags")
    guid = models.CharField(db_column="Guid", max_length=36)
    name = models.TextField(db_column="Name")
    rf_disp_type_guid = models.CharField(db_column="rf_DispTypeGuid", max_length=36)
    result_type = models.ForeignKey(
        "HltDispResultType",
        models.DO_NOTHING,
        to_field="Guid",
        db_column="rf_ResultTypeGuid",
        max_length=36,
    )
    rf_variant_guid = models.CharField(db_column="rf_VariantGuid", max_length=36)
    point = models.DecimalField(db_column="Point", max_digits=18, decimal_places=2)

    class Meta:
        managed = False
        db_table = "hlt_disp_ResultTypeValue"
