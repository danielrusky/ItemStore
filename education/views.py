from django.shortcuts import render


def education(requests):
    context = {
        'title': 'Образование'
    }
    return render(requests, 'education/education.html', context)