# django-analysis


A reusable Django app to manage analyses.

Quick start
-----------

1. Add "django_analyses" to your INSTALLED_APPS setting:

<pre>
    INSTALLED_APPS = [  
        ...  
        'django_analyses',  
    ]  
</pre>

2. Include the `analysis` URLconf in your project urls.py:

<pre>
    path("api/", include("django_analyses.urls", namespace="analysis")),
</pre>

3. Run `python manage.py migrate` to create the analysis models.

4. Start the development server and visit http://127.0.0.1:8000/admin/.

5. Visit http://127.0.0.1:8000/api/analysis/.
