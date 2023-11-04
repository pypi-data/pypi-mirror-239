from .base_model import *


class HltDispResultValue(BaseModel):
    """
    Результат прохождения обследования
    """

    id = models.AutoField(db_column="disp_ResultValueID", primary_key=True)
    code = models.CharField(db_column="Code", max_length=100)
    flags = models.IntegerField(db_column="Flags")
    guid = models.CharField(db_column="Guid", max_length=36)
    name = models.TextField(db_column="Name")
    rf_card_guid = models.CharField(db_column="rf_CardGuid", max_length=36)
    result_type = models.ForeignKey(
        "HltDispResultType",
        models.DO_NOTHING,
        to_field="Guid",
        db_column="rf_ResultTypeGuid",
        max_length=36,
    )
    result_type_value = models.ForeignKey(
        "HltDispResultTypeValue",
        models.DO_NOTHING,
        to_field="guid",
        db_column="rf_ResultTypeValueGuid",
        max_length=36,
    )
    value1 = models.TextField(db_column="Value1")
    value2 = models.DecimalField(db_column="Value2", max_digits=9, decimal_places=4)
    document_id = models.IntegerField(db_column="DocumentId")
    doc_type_guid = models.CharField(db_column="DocTypeGuid", max_length=36)
    tap = models.ForeignKey("HltTap", models.DO_NOTHING, db_column="rf_TAPID", related_name="+")
    is_auto = models.BooleanField(db_column="IsAuto")
    rf_exam_guid = models.CharField(db_column="rf_ExamGuid", max_length=36)

    class Meta:
        managed = False
        db_table = "hlt_disp_ResultValue"
