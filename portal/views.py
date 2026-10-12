from datetime import date, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    EventCertificateForm,
    EventForm,
    LoginForm,
    OrganizerProfileForm,
    StudentEventRequestForm,
    UserRegistrationForm,
    UserUpdateForm,
)
from .models import Event, EventCertificate, EventRegistration, EventRequest, OrganizerProfile


def organizer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not OrganizerProfile.objects.filter(user=request.user).exists():
            messages.error(request, 'You must be an organizer to access this page.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    wrapper.__name__ = view_func.__name__
    return wrapper


def ensure_demo_data():
    """No demo or placeholder events are created. Events must be created by organizers."""
    return


def home(request):
    event_queryset = Event.objects.filter(is_published=True, event_date__gte=date.today()).order_by('event_date')
    events = event_queryset[:3]
    return render(request, 'portal/home.html', {
        'events': events,
        'has_more_events': event_queryset.count() > 3,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account was created successfully.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'portal/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    organizer_profile = OrganizerProfile.objects.filter(user=request.user).first()
    user_registrations = EventRegistration.objects.filter(user=request.user).select_related('event').order_by('-registered_at')
    all_events = Event.objects.filter(is_published=True, event_date__gte=date.today()).order_by('event_date')[:5]
    organizer_events = Event.objects.filter(organizer=request.user).order_by('event_date') if organizer_profile else []
    my_event_requests = EventRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    my_certificates = EventCertificate.objects.filter(user=request.user).select_related('event')
    certificate_map = {certificate.event_id: certificate for certificate in my_certificates}

    for registration in user_registrations:
        registration.certificate = certificate_map.get(registration.event_id)

    registration_status_counts = {
        'selected': EventRegistration.objects.filter(user=request.user, status='selected').count(),
        'waitlist': EventRegistration.objects.filter(user=request.user, status='waitlist').count(),
        'cancelled': EventRegistration.objects.filter(user=request.user, status='cancelled').count(),
    }

    category_counts = []
    for category in Event.objects.values_list('category', flat=True).distinct():
        count = Event.objects.filter(category=category, is_published=True).count()
        if count:
            category_counts.append({'name': category, 'count': count})

    max_category_count = max((item['count'] for item in category_counts), default=1)
    for item in category_counts:
        item['width'] = round((item['count'] / max_category_count) * 100)

    return render(request, 'portal/dashboard.html', {
        'organizer_profile': organizer_profile,
        'user_registrations': user_registrations,
        'events': all_events,
        'organizer_events': organizer_events,
        'my_event_requests': my_event_requests,
        'registration_status_counts': registration_status_counts,
        'category_counts': category_counts,
        'my_certificates': my_certificates,
    })




@login_required(login_url='login')
def holo_lab(request):
    return render(request, 'portal/holocloth_page.html')


@login_required(login_url='login')
def holocloth_asset(request, asset_name):
    if asset_name not in {'holo-bg-2.jpg', 'bump-scratches.jpg'}:
        raise Http404
    asset_path = settings.BASE_DIR / 'static' / 'holocloth' / asset_name
    try:
        asset = asset_path.open('rb')
    except OSError as error:
        raise Http404 from error
    return FileResponse(asset, content_type='image/jpeg')


@login_required(login_url='login')
def events_list(request):
    query = (request.GET.get('q') or '').strip()
    category = (request.GET.get('category') or '').strip()
    selected_date = (request.GET.get('date') or '').strip()
    events = Event.objects.filter(is_published=True, event_date__gte=date.today()).order_by('event_date')

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    if category:
        events = events.filter(category__icontains=category)
    if selected_date:
        events = events.filter(event_date=selected_date)

    categories = Event.objects.filter(is_published=True, event_date__gte=date.today()).values_list('category', flat=True).distinct().order_by('category')

    return render(request, 'portal/events.html', {
        'events': events,
        'query': query,
        'category': category,
        'selected_date': selected_date,
        'categories': categories,
    })


@login_required(login_url='login')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.is_published and request.user != event.organizer:
        raise Http404

    registrations = EventRegistration.objects.filter(event=event).select_related('user').order_by('-registered_at')
    shortlisted = registrations.filter(status='selected')
    waitlisted = registrations.filter(status='waitlist')
    user_registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    return render(request, 'portal/event_detail.html', {
        'event': event,
        'registrations': registrations,
        'shortlisted': shortlisted,
        'waitlisted': waitlisted,
        'user_registration': user_registration,
    })


@login_required(login_url='login')
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    existing = EventRegistration.objects.filter(user=request.user, event=event).first()

    if existing and existing.status != 'cancelled':
        messages.info(request, 'You are already registered for this event.')
        return redirect('event_detail', event_id=event.id)

    if existing and existing.status == 'cancelled':
        existing.delete()

    shortlisted_count = EventRegistration.objects.filter(event=event, status='selected').count()
    status = 'selected' if shortlisted_count < event.capacity else 'waitlist'

    EventRegistration.objects.create(user=request.user, event=event, status=status)

    if status == 'selected':
        messages.success(request, 'You have been shortlisted for this event.')
    else:
        messages.info(request, 'The event is full. You have been placed on the waitlist.')

    return redirect('event_detail', event_id=event.id)


@login_required(login_url='login')
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    if registration:
        registration.delete()

        waitlisted_registrations = EventRegistration.objects.filter(event=event, status='waitlist').order_by('registered_at')
        if waitlisted_registrations.exists():
            next_waitlisted = waitlisted_registrations.first()
            next_waitlisted.status = 'selected'
            next_waitlisted.save()
            messages.success(request, 'Your registration was cancelled successfully. The next waitlisted participant was automatically promoted.')
        else:
            messages.success(request, 'Your registration was cancelled successfully. You can register again anytime.')
    else:
        messages.error(request, 'You are not registered for this event.')
    return redirect('dashboard')


@login_required(login_url='login')
@organizer_required
def organizer_dashboard(request):
    organizer_events = Event.objects.filter(organizer=request.user).order_by('event_date')
    total_registrations = sum(
        EventRegistration.objects.filter(event=event, status='selected').count() for event in organizer_events
    )
    waitlist_count = sum(
        EventRegistration.objects.filter(event=event, status='waitlist').count() for event in organizer_events
    )

    event_capacity_data = []
    for event in organizer_events[:6]:
        event_capacity_data.append({
            'name': event.title[:18],
            'count': event.selected_count,
            'capacity': event.capacity,
            'width': round((event.selected_count / event.capacity) * 100) if event.capacity else 0,
        })

    event_requests = EventRequest.objects.filter(status='pending').order_by('-created_at')

    return render(request, 'portal/organizer_dashboard.html', {
        'organizer_events': organizer_events,
        'total_registrations': total_registrations,
        'waitlist_count': waitlist_count,
        'event_capacity_data': event_capacity_data,
        'event_requests': event_requests,
    })


@login_required(login_url='login')
def event_analytics(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.organizer:
        raise Http404

    registrations = EventRegistration.objects.filter(event=event)

    shortlisted_count = registrations.filter(status='selected').count()
    waitlist_count = registrations.filter(status='waitlist').count()
    cancelled_count = registrations.filter(status='cancelled').count()
    total_registrations = registrations.count()
    attendance_rate = round((shortlisted_count / event.capacity) * 100) if event.capacity else 0

    monthly_labels = []
    monthly_values = []
    current_month = date.today().replace(day=1)
    month_sequence = []
    month_cursor = current_month
    for _ in range(6):
        month_sequence.append(month_cursor)
        if month_cursor.month == 1:
            month_cursor = date(month_cursor.year - 1, 12, 1)
        else:
            month_cursor = date(month_cursor.year, month_cursor.month - 1, 1)
    month_sequence.reverse()

    for month_start in month_sequence:
        month_count = sum(
            1
            for registration in registrations
            if registration.registered_at and registration.registered_at.date().year == month_start.year and registration.registered_at.date().month == month_start.month
        )
        monthly_labels.append(month_start.strftime('%b'))
        monthly_values.append(month_count)

    has_registration_data = any(value > 0 for value in monthly_values)
    max_month_value = max(monthly_values) if has_registration_data else 1
    chart_points = []
    x_axis_start = 60
    x_axis_space = 120
    y_axis_top = 30
    y_axis_bottom = 180
    y_axis_range = y_axis_bottom - y_axis_top

    for idx, value in enumerate(monthly_values):
        x = x_axis_start + (idx * x_axis_space)
        if not has_registration_data:
            y = y_axis_bottom
        else:
            scaled_value = max(value, 0)
            y = y_axis_bottom - ((scaled_value / max_month_value) * y_axis_range)
        chart_points.append(f'{x},{y}')

    status_summary = [
        {'label': 'Shortlisted', 'count': shortlisted_count, 'percent': max((shortlisted_count / max(total_registrations, 1)) * 100, 0), 'color': 'primary'},
        {'label': 'Waitlist', 'count': waitlist_count, 'percent': max((waitlist_count / max(total_registrations, 1)) * 100, 0), 'color': 'warning'},
        {'label': 'Cancelled', 'count': cancelled_count, 'percent': max((cancelled_count / max(total_registrations, 1)) * 100, 0), 'color': 'danger'},
    ]

    return render(request, 'portal/event_analytics.html', {
        'event': event,
        'shortlisted_count': shortlisted_count,
        'waitlist_count': waitlist_count,
        'cancelled_count': cancelled_count,
        'total_registrations': total_registrations,
        'attendance_rate': attendance_rate,
        'status_summary': status_summary,
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
        'chart_points': chart_points,
        'capacity_utilization': min(attendance_rate, 100),
        'has_registration_data': has_registration_data,
    })


@login_required(login_url='login')
@organizer_required
def manage_event_certificates(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    registrations = EventRegistration.objects.filter(event=event).select_related('user').order_by('-registered_at')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        uploaded_file = request.FILES.get('certificate_file')

        if not user_id or not uploaded_file:
            messages.error(request, 'Please select a participant and upload a certificate file.')
            return redirect('manage_event_certificates', event_id=event.id)

        target_user = get_object_or_404(User, id=user_id)
        registration = EventRegistration.objects.filter(event=event, user=target_user).first()

        if not registration:
            messages.error(request, 'This user is not registered for the selected event.')
            return redirect('manage_event_certificates', event_id=event.id)

        certificate, _ = EventCertificate.objects.get_or_create(event=event, user=target_user)
        certificate.certificate_file = uploaded_file
        certificate.save()
        messages.success(request, f'Certificate uploaded for {target_user.get_full_name() or target_user.username}.')
        return redirect('manage_event_certificates', event_id=event.id)

    certificate_map = {
        certificate.user_id: certificate for certificate in EventCertificate.objects.filter(event=event)
    }
    for registration in registrations:
        registration.certificate = certificate_map.get(registration.user_id)

    return render(request, 'portal/manage_event_certificates.html', {
        'event': event,
        'registrations': registrations,
    })


@login_required(login_url='login')
def download_certificate(request, certificate_id):
    certificate = get_object_or_404(EventCertificate, id=certificate_id)

    if request.user != certificate.user and request.user != certificate.event.organizer:
        raise Http404

    if not certificate.certificate_file:
        messages.error(request, 'No certificate file is available for this event yet.')
        return redirect('dashboard')

    response = FileResponse(open(certificate.certificate_file.path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_file.name.split("/")[-1]}"'
    return response


@login_required(login_url='login')
@organizer_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('organizer_dashboard')
    else:
        form = EventForm()
    return render(request, 'portal/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required(login_url='login')
@organizer_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('organizer_dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'portal/event_form.html', {'form': form, 'event': event, 'title': 'Edit Event'})


@login_required(login_url='login')
@organizer_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('organizer_dashboard')


@login_required(login_url='login')
def request_event(request):
    if request.method == 'POST':
        form = StudentEventRequestForm(request.POST)
        if form.is_valid():
            event_request = form.save(commit=False)
            event_request.user = request.user
            event_request.save()
            messages.success(request, 'Your event suggestion has been sent to the organizers.')
            return redirect('dashboard')
    else:
        form = StudentEventRequestForm()
    return render(request, 'portal/request_event.html', {'form': form})


@login_required(login_url='login')
@organizer_required
def update_event_request(request, event_request_id, action):
    event_request = get_object_or_404(EventRequest, id=event_request_id)
    action = action.lower()

    if action == 'approve':
        created_date = event_request.preferred_date or date.today() + timedelta(days=7)
        event = Event.objects.create(
            organizer=request.user,
            title=event_request.title,
            description=event_request.description,
            category=event_request.category,
            location=event_request.location or 'Campus Community Venue',
            event_date=created_date,
            start_time='09:00:00',
            end_time='12:00:00',
            capacity=50,
            is_published=True,
        )
        event_request.status = 'approved'
        event_request.response_message = f'Approved by {request.user.username} and published to the public events list.'
        event_request.save()
        messages.success(request, f'Event request for "{event_request.title}" has been approved and published by {request.user.username}.')
        return redirect('edit_event', event_id=event.id)

    if action == 'reject':
        event_request.status = 'rejected'
        event_request.response_message = 'Rejected by organizer. Please contact the event team for more details.'
        event_request.save()
        messages.info(request, f'Event request for "{event_request.title}" has been rejected.')
        return redirect('organizer_dashboard')

    messages.error(request, 'Invalid request action.')
    return redirect('organizer_dashboard')


@login_required(login_url='login')
def profile(request):
    organizer_profile = OrganizerProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        organizer_form = OrganizerProfileForm(request.POST, instance=organizer_profile) if organizer_profile else OrganizerProfileForm(request.POST)
        if user_form.is_valid() and (not organizer_profile or organizer_form.is_valid()):
            user_form.save()
            if organizer_profile:
                organizer_form.save()
            elif request.POST.get('organization_name'):
                OrganizerProfile.objects.create(
                    user=request.user,
                    organization_name=request.POST.get('organization_name'),
                    phone=request.POST.get('phone', ''),
                    bio=request.POST.get('bio', ''),
                )
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        organizer_form = OrganizerProfileForm(instance=organizer_profile) if organizer_profile else OrganizerProfileForm()

    return render(request, 'portal/profile.html', {
        'user_form': user_form,
        'organizer_form': organizer_form,
        'organizer_profile': organizer_profile,
    })


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, 'You have logged out successfully.')
    return redirect('home')
