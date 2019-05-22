from django.http import HttpResponse
from clips.models import Clip
from datetime import datetime
from django.utils.dateparse import parse_duration
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def insert(request):
    timestamp = datetime.fromtimestamp(int(request.POST["timestamp"]))
    duration = parse_duration(request.POST["duration"])
    clip = Clip(timestamp=timestamp, anomaly=request.POST["anomaly"],
                duration=duration, file_name=request.POST["filename"])
    clip.save()
    return HttpResponse('Inserted')
