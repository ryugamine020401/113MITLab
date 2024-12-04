from tortoise.models import Model
from tortoise import fields

class TortoiseItem(Model):
    """
    SQLite的
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    price = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)
    class Meta:
        """
        可定義在db內的table名稱
        """
        table = "TortoiseItem"


class StudentScoreItem(Model):
    """
    MySQL的
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    subject = fields.TextField(null=True)
    midterm_score = fields.FloatField(default=0.0, null=True, index=True)
    final_score = fields.FloatField(default=0.0, null=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        """
        可定義在db內的table名稱
        """
        table = "studentsExamScore"
