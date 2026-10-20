from django.shortcuts import render

def ver_contrato(request):
    """
    View para exibir informações de um contrato.
    """
    # Aqui você pode buscar o contrato no banco de dados e passar para o template
    # Por exemplo:
    # contrato = Contrato.objects.get(id=1)
    # return render(request, 'contrato.html', {'contrato': contrato})
    
    return render(request, 'contrato.html')
