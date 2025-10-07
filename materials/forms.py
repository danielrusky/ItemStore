from django import forms
from materials.models import Material, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("title", "description")


class RecordForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ("title", "content", "image")

    def clean_name(self):
        cleaned_data = self.cleaned_data["title"]
        ban_words = [
            "казино",
            "криптовалюса",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in ban_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Запретка в названии продукта")

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data["description"]
        ban_words = [
            "казино",
            "криптовалюса",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]
        for word in ban_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Запретка в описании продукта")

        return cleaned_data

