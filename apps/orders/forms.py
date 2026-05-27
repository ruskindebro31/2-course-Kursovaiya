from django import forms


class OrderCreateForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        min_length=2,
        label="ФИО",
        widget=forms.TextInput(attrs={"placeholder": "Иванов Иван Иванович"}),
    )
    phone = forms.CharField(
        max_length=30,
        label="Телефон",
        widget=forms.TextInput(attrs={"placeholder": "+7 (900) 000-00-00"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email (необязательно)",
        widget=forms.EmailInput(attrs={"placeholder": "name@example.com"}),
    )
    address = forms.CharField(
        max_length=255,
        label="Адрес",
        widget=forms.TextInput(attrs={"placeholder": "Город, улица, дом, квартира"}),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Уточнения по заказу"}),
        label="Комментарий (необязательно)",
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        # Honeypot field: must stay empty for real users.
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Подозрительная активность обнаружена.")
        return value
