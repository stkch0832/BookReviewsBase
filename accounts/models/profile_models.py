from django.db import models
from django.contrib.auth import get_user_model
import os, random, string
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from datetime import date

User = get_user_model()


BIO_CHOICES = [
    ( 0, "未選択" ),
    ( 1, "男性" ),
    ( 2, "女性" ),
    ( 3, "その他" )
]

WORKPLACE_CHOICES = [
    ( 0, "未選択" ),
    ( 1, "北海道" ),
    ( 2, "青森県" ),
    ( 3, "岩手県" ),
    ( 4, "宮城県" ),
    ( 5, "秋田県" ),
    ( 6, "山形県" ),
    ( 7, "福島県" ),
    ( 8, "茨城県" ),
    ( 9, "栃木県" ),
    ( 10, "群馬県" ),
    ( 11, "埼玉県" ),
    ( 12, "千葉県" ),
    ( 13, "東京都" ),
    ( 14, "神奈川県" ),
    ( 15, "新潟県" ),
    ( 16, "富山県" ),
    ( 17, "石川県" ),
    ( 18, "福井県" ),
    ( 19, "山梨県" ),
    ( 20, "長野県" ),
    ( 21, "岐阜県" ),
    ( 22, "静岡県" ),
    ( 23, "愛知県" ),
    ( 24, "三重県" ),
    ( 25, "滋賀県" ),
    ( 26, "京都府" ),
    ( 27, "大阪府" ),
    ( 28, "兵庫県" ),
    ( 29, "奈良県" ),
    ( 30, "和歌山県" ),
    ( 31, "鳥取県" ),
    ( 32, "島根県" ),
    ( 33, "岡山県" ),
    ( 34, "広島県" ),
    ( 35, "山口県" ),
    ( 36, "徳島県" ),
    ( 37, "香川県" ),
    ( 38, "愛媛県" ),
    ( 39, "高知県" ),
    ( 40, "福岡県" ),
    ( 41, "佐賀県" ),
    ( 42, "長崎県" ),
    ( 43, "熊本県" ),
    ( 44, "大分県" ),
    ( 45, "宮崎県" ),
    ( 46, "鹿児島県" ),
    ( 47, "沖縄県" )
    ]

OCCAPATION_CHOICES = [
    ( 0, "未選択" ),
    ( 1, "会社役員" ),
    ( 2, "会社員(管理職)" ),
    ( 3, "会社員(一般職)" ),
    ( 4, "公務員" ),
    ( 5, "団体職員" ),
    ( 6, "有資格業" ),
    ( 7, "自営業" ),
    ( 8, "派遣・契約社員" ),
    ( 9, "パート・アルバイト" ),
    ( 10, "主婦" ),
    ( 11, "学生" ),
    ( 12, "退職者" ),
    ( 13, "無職" ),
    ( 14, "その他" )
]

INDUSTRY_CHOICES = [
    ( 0, "未選択" ),
    ( 1, "農林水産畜産・鉱業" ),
    ( 2, "土木・建設業" ),
    ( 3, "製造業" ),
    ( 4, "不動産業" ),
    ( 5, "サービス業" ),
    ( 6, "卸売・小売" ),
    ( 7, "飲食業" ),
    ( 8, "運輸業" ),
    ( 9, "金融保険業" ),
    ( 10, "情報通信業" ),
    ( 11, "教育・医療" ),
    ( 12, "出版印刷" ),
    ( 13, "電気・ガス・水道・熱供給" ),
    ( 14, "公務・団体" ),
    ( 15, "その他" )
]

POSITION_CHOICES = [
    ( 0, "未選択" ),
    ( 1, "ITエンジニア" ),
    ( 2, "WEB・インターネット・ゲーム" ),
    ( 3, "クリエイティブ" ),
    ( 4, "コンサルタント・金融・不動産専門職" ),
    ( 5, "企画・経営" ),
    ( 6, "保育・教育・通訳" ),
    ( 7, "公共サービス" ),
    ( 8, "医療・福祉" ),
    ( 9, "医薬・食品・化学・素材" ),
    ( 10, "営業" ),
    ( 11, "建築・土木" ),
    ( 12, "技能工・設備・配送・農林水産・他" ),
    ( 13, "管理・事務" ),
    ( 14, "美容・ブライダル・ホテル・交通" ),
    ( 15, "販売・フード・アミューズメント" ),
    ( 16, "電気・電子・機械・半導体" ),
    ( 17, "主婦" ),
    ( 18, "学生" ),
    ( 19, "無職" ),
    ( 20, "その他" )
]


def generate_unique_username():
    chars = string.ascii_letters + string.digits + '_'
    length = 16

    def create_username():
        return ''.join(random.choices(chars, k=length))

    username = create_username()
    while Profile.objects.filter(username=username).exists():
        username = create_username()

    return username


def upload_image_to(instance, filename):
    image_id = str(instance.user_id)

    return os.path.join('accounts', 'user_image', image_id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True
    )
    username = models.CharField(
        verbose_name='ユーザーID',
        max_length=30,
        default=generate_unique_username,
        unique=True,
        validators=[
            MinLengthValidator(5),
            RegexValidator(
                regex=r'^[a-zA-Z0-9\_]+$',
                message='半角英字(小文字・大文字)、数字、アンダースコア(_)を組み合わせて作成してください'
                )
            ],
        )

    name = models.CharField(
        verbose_name='名前',
        max_length=30,
        default='名無し',
    )
    introduction = models.CharField(
        verbose_name="自己紹介",
        max_length=255,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name='アイコン画像',
        upload_to=upload_image_to,
        default='',
        blank=True,
    )
    bio = models.IntegerField(
        verbose_name="性別",
        choices=BIO_CHOICES,
        default=0
    )
    birth = models.DateField(
        verbose_name="生年月日",
        null=True,
        blank=True,
    )
    age = models.PositiveIntegerField(
        verbose_name="年齢",
        null=True,
        blank=True,
    )
    workplace = models.IntegerField(
        verbose_name="勤務地",
        choices=WORKPLACE_CHOICES,
        default=0
    )
    occapation = models.IntegerField(
        verbose_name="職業",
        choices=OCCAPATION_CHOICES,
        default=0
    )
    industry = models.IntegerField(
        verbose_name="業種",
        choices=INDUSTRY_CHOICES,
        default=0
    )
    position = models.IntegerField(
        verbose_name="職種",
        choices=POSITION_CHOICES,
        default=0
    )

    created_at = models.DateTimeField(
        verbose_name="登録日時",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        if self.birth:
            today = date.today()
            self.age = today.year - self.birth.year - ((today.month, today.day) < (self.birth.month, self.birth.day))
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'profiles'
        app_label = 'accounts'

    def __str__(self):
        return self.username
