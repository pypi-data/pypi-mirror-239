from .base_model import *


class HltDispResultType(BaseModel):
    """
    Тип результатов заключения
    """

    id = models.AutoField(db_column="disp_ResultTypeID", primary_key=True)
    code = models.CharField(db_column="Code", max_length=100)
    date_begin = models.DateTimeField(db_column="DateBegin")
    date_end = models.DateTimeField(db_column="DateEnd")
    flags = models.IntegerField(db_column="Flags")
    guid = models.CharField(db_column="Guid", max_length=36)
    name = models.TextField(db_column="Name")
    rf_disp_type_guid = models.CharField(db_column="rf_DispTypeGuid", max_length=36)
    is_main = models.BooleanField(db_column="IsMain")
    is_show_ctrl = models.SmallIntegerField(db_column="IsShowCtrl")
    age_from = models.IntegerField(db_column="AgeFrom")
    age_to = models.IntegerField(db_column="AgeTo")
    sex_id = models.IntegerField(db_column="rf_kl_SexID")
    rf_result_type_display_id = models.IntegerField(db_column="rf_ResultTypeDisplayID")
    rf_disp_question_type_id = models.IntegerField(db_column="rf_disp_QuestionTypeID")
    rf_mkbid = models.IntegerField(db_column="rf_MKBID")
    rf_question_guid = models.CharField(db_column="rf_QuestionGuid", max_length=36)

    class Meta:
        managed = False
        db_table = "hlt_disp_ResultType"
