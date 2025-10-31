# HotelEase - Hotel Management System

A comprehensive Django-based hotel management system for booking rooms, managing services, handling customer reviews, and administrative operations.

## Project Overview

HotelEase is a full-featured hotel management web application built with Django 5.2.7. The system provides a complete solution for hotel operations including room booking, customer management, service offerings, review systems, and administrative dashboards. The application is designed for "HotelEase" hotel located in Punjab University Employees Housing Society, Phase 2, Block A.

## Key Features

### 🏨 Room Management
- **6 Room Types**: Single, Master, Meeting, Deluxe, Executive, and Luxury Suites
- **Dynamic Pricing**: Rates from PKR 5,000 to PKR 15,000 per night
- **Real-time Availability**: Automatic room availability tracking
- **Room Gallery**: Multiple images per room (main, washroom, balcony, exterior)
- **Amenities Tracking**: JSON-based amenity storage for each room

### 📅 Booking System
- **Online Reservations**: Complete booking form with validation
- **CNIC Validation**: Pakistani CNIC number validation
- **Flexible Stay Duration**: 1-7 day booking limits
- **Airport Transfer**: Optional airport pick & drop service (PKR 7,000)
- **Unique Reference Numbers**: 12-character booking references
- **Booking Confirmation**: Detailed confirmation pages
- **Status Management**: Pending, Confirmed, Cancelled statuses

### 💰 Pricing & Billing
- **Room Type Rates**:
  - Single Room: PKR 5,000/night
  - Master Room: PKR 9,000/night
  - Deluxe Room: PKR 8,000/night
  - Meeting Room: PKR 10,000/night
  - Executive Room: PKR 12,000/night
  - Luxury Suite: PKR 15,000/night
- **Airport Service**: PKR 7,000 fixed rate
- **Automatic Calculation**: Total pricing with multi-day stays

### 🌟 Guest Services
- **Service Catalog**: Comprehensive hotel services listing
- **Default Services**: Wi-Fi, Breakfast, Housekeeping, Room Service, Gym, Parking, Pool
- **Featured Services**: Admin-configurable featured services
- **Service Pricing**: Optional pricing for premium services

### 📝 Review System
- **Guest Reviews**: 5-star rating system with comments
- **Review Display**: Public review gallery with ratings
- **Average Ratings**: Calculated average ratings with star displays
- **Guest Photos**: Optional photo uploads with reviews

### 📞 Contact Management
- **Contact Forms**: Multiple contact forms throughout the site
- **Message Storage**: Database storage of all customer inquiries
- **Admin Tracking**: Handled/unhandled message tracking
- **Contact Information**: Direct phone and email contact

### 👨‍💼 Administrative Features
- **Staff Dashboard**: Overview of bookings and occupancy
- **Room Status Monitoring**: Real-time room availability tracking
- **Booking Management**: View and manage all reservations
- **Message Management**: Handle customer inquiries
- **Content Management**: Manage services, rooms, and reviews

## Technical Architecture

### Backend Framework
- **Django 5.2.7**: Latest stable Django version
- **SQLite Database**: Default development database
- **Model-View-Template (MVT)**: Django architectural pattern
- **Class-Based & Function-Based Views**: Mixed view approaches

### Frontend Technologies
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library for UI elements
- **Django Templates**: Server-side template rendering
- **Responsive Design**: Mobile-first approach

### Key Django Apps

#### 1. Core App (`core/`)
- **Models**: Room, Service, Review, ContactMessage
- **Views**: Home, rooms, services, reviews, contact, dashboard
- **Forms**: ContactForm, ReviewForm with StyledFormMixin
- **Templates**: Complete UI for all hotel pages

#### 2. Bookings App (`bookings/`)
- **Models**: Booking with complete reservation logic
- **Views**: Booking creation and confirmation
- **Forms**: BookingForm with validation
- **Business Logic**: Room assignment, pricing calculation, availability management

## Project Structure

```
Django SCD/
├── hotel_management/         # Main project directory
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI application
├── core/                     # Core hotel functionality
│   ├── models.py             # Room, Service, Review, ContactMessage models
│   ├── views.py              # Main hotel views
│   ├── forms.py              # Contact and review forms
│   ├── urls.py               # Core app URLs
│   └── admin.py              # Admin interface configuration
├── bookings/                 # Booking management
│   ├── models.py             # Booking model with business logic
│   ├── views.py              # Booking creation and confirmation
│   ├── forms.py              # Booking form with validation
│   └── urls.py               # Booking URLs
├── templates/                # Django templates
│   ├── index.html            # Main landing page
│   ├── core/                 # Core app templates
│   │   ├── home.html         # Homepage template
│   │   ├── rooms.html        # Rooms gallery
│   │   ├── services.html     # Services listing
│   │   ├── reviews.html      # Reviews display
│   │   ├── contact.html      # Contact page
│   │   └── auth/
│   │       └── login.html    # Admin login
│   ├── bookings/             # Booking templates
│   │   ├── booking_form.html # Reservation form
│   │   └── booking_confirmation.html
│   └── partials/             # Shared template components
│       └── base.html         # Base template
├── static/                   # Static files
│   ├── css/                  # Custom stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Hotel images
├── media/                    # User uploaded files
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/mursaleen6070/Django_SCD
   cd "Django SCD"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv hotel_env
   # Windows
   hotel_env\Scripts\activate
   # macOS/Linux
   source hotel_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations core
   python manage.py makemigrations bookings
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Usage Guide

### For Customers

1. **Browse Rooms**: Visit the homepage to see available room types and pricing
2. **Make Booking**: Fill out the booking form with personal details and preferences
3. **Confirm Reservation**: Receive booking confirmation with reference number
4. **Leave Review**: Submit reviews and ratings after your stay
5. **Contact Hotel**: Use contact forms for inquiries

### For Hotel Staff

1. **Admin Access**: Login to `/admin/` with staff credentials
2. **Dashboard**: View `/dashboard/` for occupancy overview
3. **Manage Bookings**: Monitor and update reservation statuses
4. **Room Management**: Update room availability and pricing
5. **Customer Service**: Respond to contact messages

## API Endpoints

### Public URLs
- `/` - Homepage with hotel overview
- `/rooms/` - Room gallery and information
- `/services/` - Hotel services listing
- `/reviews/` - Guest reviews and ratings
- `/contact/` - Contact form and information
- `/booking/` - Room reservation form
- `/booking/confirm/<reference>/` - Booking confirmation

### Admin URLs
- `/admin/` - Django admin interface
- `/dashboard/` - Staff dashboard (requires login)

## Database Models

### Room Model
- Room number, type, pricing, images, amenities
- Availability tracking and status management

### Booking Model
- Guest information, stay details, pricing calculation
- Automatic room assignment and availability updates
- Unique reference generation and status tracking

### Service Model
- Hotel amenities with descriptions and pricing
- Featured service selection for homepage

### Review Model
- Guest feedback with 5-star ratings
- Optional photo uploads and location information

### ContactMessage Model
- Customer inquiries with admin handling status
- Email and subject categorization

## Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Input Validation**: Server-side validation for all user inputs
- **CNIC Validation**: Pakistani CNIC format validation
- **Staff Authentication**: Admin dashboard requires staff login
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Prevention**: Template auto-escaping enabled

## Support

For technical support or business inquiries:
- **Email**: mursaleenmalik286@gmail.com
- **Phone**: 0307-2034454
- **Address**: Punjab University Employees Housing Society, Phase 2, Block A

---

**HotelEase** - Seamless hospitality management with Django excellence.