def parse_model_form_data(request, model):
    model_fields = [f.attname for f in model._meta.fields]
    parsed_form_data = dict()
    for field in request.POST:
        if field in model_fields:
            parsed_form_data[field] = request.POST[field]
    return parsed_form_data
