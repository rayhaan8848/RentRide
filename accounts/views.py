
from functools import wraps

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import User


# ==========================================
# SIGNUP REDIRECT
# ==========================================

def signup_redirect():
    return redirect(f"{reverse('signup')}?tab=signup")


# ==========================================
# ROLE CHECKING FUNCTIONS
# ==========================================

def is_customer(user):
    return user.role == User.Role.CUSTOMER


def is_owner(user):
    return user.role == User.Role.OWNER


def is_admin(user):
    return user.role == User.Role.ADMIN


# ==========================================
# CUSTOM ROLE REQUIRED DECORATOR
# ==========================================

def role_required(role):

    def decorator(view_function):

        @wraps(view_function)
        def protected_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('signup')

            if request.user.role != role:
                raise PermissionDenied

            return view_function(request, *args, **kwargs)

        return protected_view

    return decorator


# ==========================================
# USER REGISTRATION
# ==========================================

def user_register(request):

    if request.method == "POST":

        # Get form data
        fullname = request.POST.get('fullname', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')

        # Get selected account type
        role = request.POST.get('role', User.Role.CUSTOMER)

        # --------------------------------------
        # CHECK REQUIRED FIELDS
        # --------------------------------------

        if not all((fullname, username, email, phone, password, cpassword)):

            messages.error(
                request,
                "Please complete all sign-up fields."
            )

            return signup_redirect()

        # --------------------------------------
        # VALIDATE ACCOUNT TYPE
        # --------------------------------------

        allowed_roles = [
            User.Role.CUSTOMER,
            User.Role.OWNER,
        ]

        if role not in allowed_roles:

            messages.error(
                request,
                "Invalid account type."
            )

            return signup_redirect()

        # --------------------------------------
        # CHECK PASSWORD CONFIRMATION
        # --------------------------------------

        if password != cpassword:

            messages.error(
                request,
                "Passwords do not match."
            )

            return signup_redirect()

        # --------------------------------------
        # CHECK DUPLICATE USERNAME
        # --------------------------------------

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "That username is already in use."
            )

            return signup_redirect()

        # --------------------------------------
        # CHECK DUPLICATE EMAIL
        # --------------------------------------

        if User.objects.filter(email__iexact=email).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return signup_redirect()

        # --------------------------------------
        # CREATE USER
        # --------------------------------------

        try:

            validate_password(password)

            with transaction.atomic():

                User.objects.create_user(
                    fullname=fullname,
                    username=username,
                    email=email,
                    phone=phone,
                    password=password,
                    role=role,
                    profile_image=request.FILES.get('profile_image'),
                )

        except ValidationError as error:

            for message in error.messages:

                messages.error(request, message)

            return signup_redirect()

        except IntegrityError:

            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email__iexact=email).exists()
            ):

                messages.error(
                    request,
                    "That username or email is already in use."
                )

                return signup_redirect()

            raise

        # --------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------

        messages.success(
            request,
            "Your RentRide account is ready. Please log in."
        )

        return redirect('signup')

    # --------------------------------------
    # DISPLAY SIGNUP PAGE
    # --------------------------------------

    return render(
        request,
        'account.html',
        {
            'signup_active': request.GET.get('tab') == 'signup',
        }
    )


# ==========================================
# ROLE-BASED DASHBOARD REDIRECTION
# ==========================================

def redirect_user_dashboard(user):

    if user.role == User.Role.ADMIN:

        return redirect('admin_dashboard')

    elif user.role == User.Role.OWNER:

        return redirect('owner_dashboard')

    elif user.role == User.Role.CUSTOMER:

        return redirect('customer_dashboard')

    return redirect('home')


# ==========================================
# USER LOGIN
# ==========================================

def log_in(request):

    if request.method == "POST":

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Create login session
            login(request, user)

            # Redirect according to role
            return redirect_user_dashboard(user)

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        'account.html',
        {
            'signup_active': False
        }
    )


# ==========================================
# USER LOGOUT
# ==========================================

@require_POST
def log_out(request):

    logout(request)

    return redirect('home')


# ==========================================
# CUSTOMER DASHBOARD
# ==========================================

@login_required
@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):

    return render(
        request,
        'main/home.html'
    )


# ==========================================
# VEHICLE OWNER DASHBOARD
# ==========================================

@login_required
@role_required(User.Role.OWNER)
def owner_dashboard(request):

    return render(
        request,
        'dashboard/owner_dashboard.html'
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@login_required
@role_required(User.Role.ADMIN)
def admin_dashboard(request):

    return render(
        request,
        'dashboard/admin_dashboard.html'
    )
