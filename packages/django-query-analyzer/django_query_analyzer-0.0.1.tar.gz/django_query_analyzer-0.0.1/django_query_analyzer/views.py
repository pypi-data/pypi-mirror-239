from django.shortcuts import render
from .models import QueryAnalyzer


def query_analyzer_list(request):
    query_analyzers = QueryAnalyzer.objects.all()
    return render(request, 'query_analyzer_list.html', {'query_analyzers': query_analyzers})
