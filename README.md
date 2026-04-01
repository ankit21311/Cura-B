# Hospital Resource Management System (Cura)

A comprehensive Django-based application designed to manage and track critical hospital resources such as beds and oxygen supplies. The system provides active monitoring and role-based access for Administrators and Patients to ensure efficient resource allocation and transparency.

## 🚀 Features

-   **Role-Based Access Control**:
    -   **Admin Dashboard**: comprehensive tools for hospital staff to manage inventory (beds, oxygen), update statuses, and view analytics.
    -   **Patient Dashboard**: Read-only view for patients and the public to check real-time availability of resources.
-   **Resource Management**:
    -   **Bed Management**: Track bed availability, assign to wards, and update occupancy status.
    -   **Oxygen Management**: Monitor oxygen cylinder stock and flow metrics.
-   **User Authentication**: Secure login and registration flows.
-   **Data Seeding**: Scripts included to populate the database with demo hospitals and resources for testing.
-   **Responsive Design**: Mobile-friendly interface built with HTML5 and CSS3.

## 📦 Modules

The application is structured into several key functional modules, each handling a specific aspect of healthcare resource management:

### 1. User Management & Security
-   **Profiles**: Distinct profiles for Patients, Hospital Admins, Pharmacy Admins, Oxygen Suppliers, and Platform Admins.
-   **Authentication**: Secure login/registration with role-based dashboard redirection.
-   **Notifications**: Real-time alerts for booking statuses, stock updates, and appointment reminders.

### 2. Hospital & Bed Management
-   **Hospital Directory**: Detailed hospital profiles including location, specialties, and contact info.
-   **Bed Tracking**: Real-time inventory of ICU, General, and Emergency beds.
-   **Booking System**: Patients can request beds; Admins can review and approve bookings, automatically updating availability.

### 3. Doctor & Appointment System
-   **Doctor Profiles**: detailed information including qualifications, experience, and consultation fees.
-   **Scheduling**: Appointment booking system with time-slot selection.
-   **Search**: Find doctors by specialty or city.

### 4. Pharmacy & Medicine
-   **Inventory**: Pharmacies can manage medicine stocks, pricing, and details (strength, brand).
-   **E-Commerce**: Full shopping cart experience for patients to order medicines.
-   **Order Fulfillment**: Pharmacy admins can track and update order statuses (Pending -> Dispatched -> Delivered).

### 5. Oxygen Supply Management
-   **Cylinder Stock**: Suppliers manage inventory of oxygen cylinders (various capacities).
-   **Emergency Booking**: Critical path for patients to book oxygen supplies directly from verified suppliers.

### 6. Financial & Support Services
-   **Digital Wallet**: Integrated wallet system for quick payments and refunds.
-   **Insurance Integration**: Verify and utilize insurance policies for cashless bookings.
-   **Support Desk**: Ticketing system for users to report issues or request assistance.

## 🛠️ Technology Stack

-   **Backend**: Python, Django
-   **Database**: SQLite (Default) / Extensible to PostgreSQL or MySQL
-   **Frontend**: HTML, CSS, Django Templates
-   **Styling**: Custom CSS with responsive layouts

## ⚙️ Installation & Setup

Follow these steps to get the project running locally.

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)

### Steps

1.  **Clone the Repository** (if applicable) or navigate to the project directory:
    ```bash
    cd hospital-system
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Seed Demo Data** (Optional but Recommended):
    To populate the database with demo users and hospital data:
    ```bash
    python create_demo_users.py
    # and/or any specific migration scripts in core/migrations if applicable
    ```

6.  **Create a Superuser** (for Admin access):
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

8.  **Access the Application**:
    Open your browser and navigate to:
    -   Home: `http://127.0.0.1:8000/`
    -   Admin Portal: `http://127.0.0.1:8000/admin/`

## 📂 Project Structure

```
hospital-system/
├── core/                   # Main application app
│   ├── models.py           # Database models (Hospital, Bed, Oxygen, etc.)
│   ├── views.py            # View logic for dashboards and forms
│   ├── urls.py             # App-specific routes
│   └── templates/          # HTML Templates
├── cura/                   # Project configuration
│   ├── settings.py         # Global settings
│   └── urls.py             # Global routing
├── templates/              # Base templates
├── analyze_code.py         # Utility script
├── create_demo_users.py    # Data seeding script
├── manage.py               # Django command-line utility
└── requirements.txt        # Project dependencies
```

## ☁️ Deploy On Render

This project is now configured for Render using the included [render.yaml](render.yaml).

### 1. Push To GitHub

Render deploys from your Git repository, so make sure this code is pushed to a branch.

### 2. Create Blueprint Service

1. In Render, click **New +** -> **Blueprint**.
2. Connect your repository.
3. Render auto-detects `render.yaml` and provisions:
    - A Python web service (`curab-web`)
    - A PostgreSQL database (`curab-db`)

### 3. Environment Variables

Configured automatically via `render.yaml`:

- `SECRET_KEY` (auto-generated)
- `DEBUG=False`
- `DATABASE_URL` (from managed Postgres)

Optional (set manually if needed):

- `OPENAI_API_KEY`
- `ALLOWED_HOSTS` (defaults to `*` unless overridden)
- `CSRF_TRUSTED_ORIGINS` (comma-separated, e.g. `https://your-app.onrender.com`)

### 4. Deploy

On each deploy Render will:

1. Install dependencies
2. Run `collectstatic`
3. Run `migrate`
4. Start Gunicorn (`cura.wsgi:application`)

### 5. First Admin User

After deployment, create a superuser from the Render shell:

```bash
python manage.py createsuperuser
```

## 🤝 Contributing

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is open-source and available under the simple [MIT License](LICENSE).
"# Cura-B" 
