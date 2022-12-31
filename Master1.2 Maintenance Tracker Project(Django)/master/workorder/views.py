import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import WorkOrder, Assets, WoEvents


# Home Page
def home(request):
    return render(request, 'index.html')


# Create Work Order
def createWorkOrder(request):
    areas = Assets.objects.values('area').distinct()

    if request.method == 'POST':
        area = request.POST['area']
        location = request.POST['location']
        asset = request.POST['asset']
        # createdTime = request.POST['createdTime']
        createdTime = datetime.datetime.now()
        createdBy = request.POST['createdBy']
        description = request.POST['description']
        status = request.POST['status']
        action = request.POST['action']
        # closedTime = request.POST['closedTime']
        closedTime = datetime.datetime.now()
        image = request.FILES.get('imagefile')

        WorkOrder(area=area,
                  location=location,
                  asset=asset,
                  createdTime=createdTime,
                  createdBy=createdBy,
                  description=description,
                  status=status,
                  action=action,
                  closedTime=closedTime,
                  image_file=image).save()

        return render(request, 'createworkorder.html')

    else:
        return render(request, 'createworkorder.html', {'areas': areas})


# Select Dropdown Location(Create)
def selectLocation(request):
    data = []
    _area = request.GET.get('area')
    assets = Assets.objects.filter(area=_area)

    for asset in assets:
        data.append(asset.location)
    data = tuple(set(data))
    if request.is_ajax():
        return JsonResponse({'data': data})

    return render(request, 'createsnag.html')


# Select Dropdown Assets(Create)
def selectAssets(request):
    data = []
    _area = request.GET.get('area')
    _location = request.GET.get('location')
    assets = Assets.objects.filter(area=_area, location=_location)

    for asset in assets:
        data.append(asset.asset)

    if request.is_ajax():
        return JsonResponse({'data': data})

    return render(request, 'createworkorder.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username exists')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(first_name=firstname,
                                                last_name=lastname,
                                                username=username,
                                                email=email,
                                                password=password1)
                user.save()
                return render(request, 'index.html')
        else:
            messages.info(request, 'Password not matching')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')


# Show all work orders
def showWorkOrders(request, snags={}):
    areas = []
    status = []
    createdby = []
    snags = WorkOrder.objects.all().values()
    for snag in snags:
        areas.append(snag['area'])
    areas = tuple(set(areas))

    for snag in snags:
        status.append(snag['status'])
    status = tuple(set(status))

    for snag in snags:
        createdby.append(snag['createdBy'])
    createdby = tuple(set(createdby))

    return render(request, 'showworkorders.html',
                  {'snags': snags,
                   'areas': areas,
                   'status': status,
                   'createdby': createdby})

# Click Area Dropdown


def selectArea(request):
    data = []
    locations = []
    parameters = getParameters(request)
    data = filterWorkOrders(**parameters)
    for wo in data:
        locations.append(wo['location'])
    locations = tuple(set(locations))
    if request.is_ajax():
        return JsonResponse([{'locations': locations}, {'data': data}], safe=False)
    return render(request, 'showworkorders.html')

# Filter by location


def filterByLocation(request):
    data = []
    assets = []
    parameters = getParameters(request)
    data = filterWorkOrders(**parameters)
    for item in data:
        assets.append(item['asset'])
    assets = tuple(set(assets))

    if request.is_ajax():
        return JsonResponse([{'assets': assets}, {'data': data}], safe=False)
    return render(request, 'showworkorders.html')

# Filter by createdby


def filterByCreatedby(request):
    data = []
    parameters = getParameters(request)
    data = filterWorkOrders(**parameters)
    if request.is_ajax():
        return JsonResponse({'data': data}, safe=False)
    return render(request, 'showworkorders.html')

# Filter by satus


def filterByStatus(request):
    data = []
    parameters = getParameters(request)
    data = filterWorkOrders(**parameters)
    if request.is_ajax():
        return JsonResponse({'data': data}, safe=False)
    return render(request, 'showworkorders.html')

# Display Work Order Details


def displayWo(request):
    data = []
    events = []
    wonumber = request.GET.get('wonumber')

    data = workOrderDetails(wonumber, "id")
    data[0]['createdTime'] = data[0]['createdTime'].strftime("%d/%m/%y-%H:%M")
    data[0]['closedTime'] = data[0]['closedTime'].strftime("%d/%m/%y-%H:%M")
    data[0]['image_file'] = "/media/"+data[0]['image_file']

    events = list(WoEvents.objects.filter(wonumber=wonumber).values())
    for event in events:
        event['editedTime'] = event['editedTime'].strftime("%d/%m/%y-%H:%M")

    return JsonResponse([{'events': events}, {'data': data}], safe=False)


def addEvent(request):
    _event = request.GET.get('_event')
    _wonumber = request.GET.get('wonumber')
    wonumber = int(_wonumber[3:])

    data = workOrderDetails(wonumber, "id")
    data[0]['createdTime'] = data[0]['createdTime'].strftime("%d/%m/%y-%H:%M")
    data[0]['closedTime'] = data[0]['closedTime'].strftime("%d/%m/%y-%H:%M")
    data[0]['image_file'] = "/media/"+data[0]['image_file']

    editedTime = datetime.datetime.now()
    editedBy = "Siyad"
    WoEvents(wonumber_id=wonumber,
             editedBy=editedBy,
             editedTime=editedTime,
             event=_event).save()

    events = list(WoEvents.objects.filter(wonumber=wonumber).values())
    for event in events:
        event['editedTime'] = event['editedTime'].strftime("%d/%m/%y-%H:%M")

    return JsonResponse([{'events': events}, {'data': data}], safe=False)


def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {'user': user})
        else:
            messages.info(request, 'Wrong Credentials..')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logOut(request):
    logout(request)
    return render(request, 'index.html')


def workOrderDetails(parameter, value):
    data = {}
    my_filter = {}
    my_filter[value] = parameter
    data = list(WorkOrder.objects.filter(**my_filter).values())
    return data


def filterWorkOrders(**values):
    data = {}
    my_filter = {}
    for key, value in values.items():
        if value != '':
            my_filter[key] = value
    data = list(WorkOrder.objects.filter(**my_filter).values())
    return data


def getParameters(request):
    parameter = {}
    if (request.GET.get('area') == 'Area') or (request.GET.get('area') == None):
        parameter['area'] = ''
    else:
        parameter['area'] = request.GET.get('area')
    if request.GET.get('location') == 'Location' or request.GET.get('location') == None:
        parameter['location'] = ''
    else:
        parameter['location'] = request.GET.get('location')
    if request.GET.get('asset') == 'Asset' or request.GET.get('asset') == None:
        parameter['asset'] = ''
    else:
        parameter['asset'] = request.GET.get('asset')
    if request.GET.get('createdby') == 'Created By' or request.GET.get('createdby') == None:
        parameter['createdby'] = ''
    else:
        parameter['createdBy'] = request.GET.get('createdby')
    if request.GET.get('status') == 'Status' or request.GET.get('status') == None:
        parameter['status'] = ''
    else:
        parameter['status'] = request.GET.get('status')
    return parameter
