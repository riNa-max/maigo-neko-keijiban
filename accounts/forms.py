from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

Account = get_user_model()

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tanaka'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '090-1234-5678'}),
        }
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'phone_number': '電話番号',
        }
    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"placeholder": "tanaka"}),
        help_text="※半角英数字と@ . + - _ のみ使用可能"
    )
    email = forms.CharField(
        label="メールアドレス",
        widget=forms.TextInput(attrs={"placeholder": "example@gmail.com"}),
        help_text="",
        error_messages={
            'required': "メールアドレスを入力してください。",
            'invalid': "有効なメールアドレスを入力してください。",
            'unique': "このメールアドレスは既に登録されています。",
        }
    )
    phone_number = forms.CharField(
        label="電話番号",
        widget=forms.TextInput(attrs={"placeholder": "000-0000-0000"}),
        error_messages={
            'required': "電話番号を入力してください。",
            'invalid': "有効な電話番号を入力してください。",
            'unique': "この電話番号は既に登録されています。",
        }
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ユーザー名'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '電話番号'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '確認用パスワード'}),
        }

    error_messages = {
        'password_mismatch': "パスワードが一致しません。",
        'duplicate_username': "このユーザー名は既に使用されています。",
        'password_too_short': "パスワードは8文字以上にしてください。",
        'password_too_common': "このパスワードは一般的すぎます。",
        'password_entirely_numeric': "パスワードを数字だけにすることはできません。",
    }

    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(),
        help_text=(
            "※最低8文字以上<br>"
            "※半角英数字と@ . + - _ のみ使用可能<br>"
            "※英字と数字を組み合わせてください"
        ),
    )

    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput(),
        help_text=""
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        
        return password2

    username = forms.CharField(
        label="ユーザー名",
        widget=forms.TextInput(attrs={"placeholder": "タナカ"}),
        help_text="",
        error_messages={
            'required': "ユーザー名を入力してください。",
            'unique': "このユーザー名は既に使用されています。",
            'invalid': "有効なユーザー名を入力してください。半角英数字と @/./+/-/_ のみ使用できます。",
        }
    )

    email = forms.CharField(
        label="メールアドレス",
        widget=forms.TextInput(attrs={"placeholder": "example@gmail.com"}),
        help_text="",
        error_messages={
            'required': "メールアドレスを入力してください。",
            'invalid': "有効なメールアドレスを入力してください。",
            'unique': "このメールアドレスは既に登録されています。",
        }
    )

    phone_number = forms.CharField(
        label="電話番号",
        widget=forms.TextInput(attrs={"placeholder": "000-0000-0000"}),
        error_messages={
            'required': "電話番号を入力してください。",
            'invalid': "有効な電話番号を入力してください。",
            'unique': "この電話番号は既に登録されています。",
        }
    )

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="メールアドレス",  # ログインをメールアドレスに変更する場合
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'パスワード'})
    )

    error_messages = {
        'invalid_login': "メールアドレスまたはパスワードが正しくありません。",
        'inactive': "このアカウントは無効です。",
    }