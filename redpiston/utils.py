from django.db.models import get_model

def load_generic_object(model_name, pk):
    model = get_model('redpiston', model_name)
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
