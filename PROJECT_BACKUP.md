# Event Portal - Full Progress and Continuation Guide

## 0. Paste-ready continuation note for a new chat
This file is designed to be pasted directly into a fresh chat so the AI can continue from the exact verified state of the project without re-explaining the build or asking repeated setup questions.

This project is a Django-based event registration and certificate portal. It was originally a timetable concept, but the final product is an event system with student dashboards, organizer management, registration logic, waitlist and shortlist assignment, event cover images, and certificate upload/download for each student per event.

The current verified state is stable and ready to continue in a new chat. The event portal uses its existing Bootstrap CDN presentation layer and has a resilient database startup flow: if MySQL is unavailable, Django falls back to local SQLite. The authenticated Holocloth page itself is fully local, including its upstream source, runtime bundle, textures, and fonts.

## 1. Important current behavior
- No demo or seeded events are created automatically.
- Signed-in users can open the original Holocloth cloth studio directly from the dashboard.
- All public events must be published and dated today or later.
- The homepage shows only real published future events.
- The events page supports search by title, keyword, location, category, and date.
- The duplicate Events nav item has been removed.
- The site has a cleaner, more polished UI.
- Organizers can upload event cover images.
- Cover images appear on the home page, events page, and event detail page.
- Organizer can manage each registered student's certificate individually for each event.
- Student dashboard shows registrations and certificates.
- A student can download a certificate only when it has been uploaded.
- If the organizer has not uploaded a certificate yet, the student sees a pending message instead of a broken or missing file.
- Students can cancel and re-register later.
- Cancelled registrations are deleted instead of staying locked.
- Local database reset was performed: all users, organizer profiles, events, registrations, certificates, and requests were deleted.
- The full portal styling was modernized with a stronger visual system, better card layouts, a more premium landing page, and stronger dashboard polish.
- The home page and events pages now use richer image-led layouts for a more premium final look.

## 2. Database reset status
The local database has been cleared completely, so a fresh start is ready.

This means:
- all organizer accounts are removed
- all participant accounts are removed
- all events are removed
- all registrations are removed
- all event certificates are removed
- all organizer event requests are removed

If you want to recreate the platform from scratch, create new organizer and student accounts again from the app or via Django shell.

## 3. Visual modernization summary
The final UI is now more premium and polished with:
- crisp gradients and deeper blue/green accent styling
- better hero section and illustration treatment
- card-based event layouts with images and clearer metadata
- modern pills, badges, and action buttons
- improved dashboard and analytics visual structure
- stronger spacing, typography, and clean surfaces
- local static illustration support to keep the app working offline

## 4. Final verified state
The app remains in a working state after the modern styling update, analytics chart correction, final home-page/waitlist flow changes, and local database resilience fix.

Verified with:
```powershell
cd C:\Users\RANESH\Downloads\finalyearproject
.\.venv\Scripts\python.exe manage.py test portal
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Result:
- 12 tests passed
- system checks clean
- analytics trend chart handles both real registration data and empty-data states correctly
- logged-in users see the profile CTA instead of create account
- the authenticated `/holo-lab/` route is linked directly from the participant dashboard
- the original MIT-licensed Holocloth app runs locally with zero-gravity Verlet cloth, grab/pull, orbit/pan/zoom, viscosity/stiffness/iterations/smoothing/grab-radius controls, all material/image/render panels, presets, versions, and PNG export
- the upstream MIT-licensed source, original production bundle, cloth textures, and Geist Mono font are stored locally; the Holocloth page makes no external requests
- desktop and 390px mobile layouts were checked; no horizontal overflow was found
- waitlisted participants are promoted automatically on cancellation
- app starts successfully locally even when MySQL is not available, by falling back to SQLite
- app is running successfully at http://127.0.0.1:8000/

## 5. Analytics chart status
The monthly registration trend chart is now fixed to:
- display a proper six-month trend when registrations exist
- avoid broken or flat line rendering when there is no registration history
- show a clear empty state message instead of an invalid graph
- continue to respect the organizer-only access rules for event analytics

## 6. Latest user-flow updates
The app now includes the final user experience rules requested:
- logged-in users see a "View Your Profile" button instead of "Create Account" on the home page
- waitlisted participants are automatically promoted to shortlisted status when a selected participant cancels
- the waitlist promotion uses the earliest waitlisted registration first, preserving fair order
- the app remains fully local and works without internet-based dependencies for the core event flow
- project startup is resilient: if MySQL is unreachable, the app automatically switches to SQLite so it can still run locally
- stale local migration state was cleared and the database was rebuilt cleanly to eliminate startup blockers

## 7. Verified current status
The latest flow changes were validated with the Django test suite and a fresh local run.

Result:
- 12 tests passed
- no system check issues
- home-page logged-in state is updated
- waitlist promotion logic is active and covered by verification
- local database fallback works correctly
- Holocloth route, access control, dashboard link, and authenticated local image delivery are covered by tests
- project was migrated cleanly and is running successfully at http://127.0.0.1:8000/
- final app state is ready for continuation in a fresh chat

## 2. Project path
C:\Users\RANESH\Downloads\finalyearproject

## 3. Technical foundation
- Django: 6.1.1
- Python: 3.13.1 inside the project .venv
- Database: MySQL-ready with SQLite fallback
- Frontend: Bootstrap 5 plus custom CSS
- Main app: portal/
- Project config: studentportal/
- Static assets: static/

## 4. Verified runtime commands
These were the commands used successfully during the final verification and clean reset:

```powershell
cd C:\Users\RANESH\Downloads\finalyearproject
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py test portal
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### Verified result
- Django system check: no issues
- 12 tests ran
- all tests passed
- local SQLite fallback is active when MySQL is unavailable
- server is running successfully on http://127.0.0.1:8000/
- status: OK

## 5. What changed in this project history
### A. Event portal foundation
The project was rebuilt around an event registration portal rather than a timetable. This included:
- organizer accounts
- participant accounts
- event creation and editing
- event public listing
- event detail pages
- registration and waitlist logic

### B. Stale data and business rule repair
Many problems were fixed during development:
- hidden events due to bad filters
- leftover demo data
- duplicate navbar links
- missing visibility for pending organizer requests
- broken organizer ownership logic
- no re-registration after cancellation
- DB mismatch after model updates

### C. Design improvement and visual polish
The UI was repeatedly refined to make it look like a production-ready portal. This included:
- improved top nav
- cleaner cards
- better dashboard layout
- styled buttons and badges
- consistent page spacing and typography
- layout cleanups for event listing and forms

### D. Cover images for events
The event model and templates were extended so organizers can upload cover images. The results:
- home page cards show a real event image
- events list cards show the image
- event detail page shows the main cover image
- missing images show a placeholder title block instead of breaking the layout

### E. Certificate workflow
This is the newest feature and is the current final business logic.

The app now supports:
- organizer uploads a certificate file for a specific registered student and event
- each event can have per-user certificates separately
- students see certificate status in the dashboard
- students can download the certificate if it exists
- if no certificate exists yet, the student sees a pending status message

### F. Local resilience and environment recovery
A final project-level fix was added to make the app more robust during local development:
- if MySQL is not running, Django now falls back to SQLite automatically
- stale local database files were cleaned and the migration chain was re-applied from scratch
- the app starts and runs reliably in a local environment without a working MySQL server

### G. Holocloth studio integration
- added an authenticated `/holo-lab/` page reachable directly from the participant dashboard
- vendored the complete MIT-licensed upstream source in `vendor/holocloth/` with its license
- served the original Holocloth production app, fabric textures, and Geist Mono font from local static files
- retained the original zero-gravity Verlet simulation, grab-and-pull interaction, physics/material/image/render controls, presets, versions, and PNG exports
- added authenticated Django routes for its local image assets; the Holocloth page makes no external requests
- the app is already built and served by Django; Node.js/npm are not required to run it
- a WebGL2-capable browser is required for the 3D simulation

## 6. Core files and responsibilities

### portal/models.py
Contains the main models:
- `OrganizerProfile`
- `Event`
- `EventRegistration`
- `EventCertificate`
- `EventRequest`

The important new model is `EventCertificate`, which links:
- the event
- the user
- the uploaded file

### portal/forms.py
Contains forms for:
- registration
- login
- profile update
- organizer profile update
- event creation/editing
- event certificate upload
- event request submission

### portal/views.py
Contains the main app behavior:
- home page
- dashboard logic
- Holocloth page and local texture delivery
- event listing/filtering
- event detail
- registration
- cancellation
- organizer dashboard
- certificate management for each event
- download certificate logic
- event request approval/rejection

### portal/urls.py
Routes include:
- home
- login/register/logout
- dashboard
- Holocloth (`/holo-lab/`) and local source-texture routes
- events list
- event detail
- registration actions
- organizer dashboard
- create/edit/delete event
- certificate management for organizer
- certificate download for student

### portal/templates/portal/
Current templates include:
- base.html
- home.html
- events.html
- event_detail.html
- dashboard.html
- holocloth_page.html
- organizer_dashboard.html
- manage_event_certificates.html
- event_form.html
- request_event.html
- profile.html

## 7. Certificate flow details
### Organizer side
The organizer opens their dashboard, selects an event, and clicks the Certificates button. On that page:
- each registered member is listed
- each member has a certificate status
- the organizer uploads a file for that student individually
- the certificate is saved and linked to that exact event + student

### Student side
The student goes to the dashboard and sees:
- all their event registrations
- certificate status for each one
- a Download button if the certificate has been uploaded
- a “Certificate pending” message if not uploaded yet

### Safety rule
The download route only allows:
- the enrolled student for that certificate
- or the organizer who created the event

This prevents unauthorized file access.

## 8. IMPORTANT route map
- Home: /
- Register: /register/
- Login: /login/
- Logout: /logout/
- Dashboard: /dashboard/
- Holocloth: /holo-lab/
- Events: /events/
- Event detail: /event/<id>/
- Register: /event/<id>/register/
- Cancel registration: /event/<id>/cancel/
- Request event: /request-event/
- Organizer dashboard: /organizer/
- Create event: /organizer/create/
- Edit event: /organizer/edit/<id>/
- Delete event: /organizer/delete/<id>/
- Event certificates: /organizer/event/<id>/certificates/
- Download certificate: /certificate/<id>/download/
- Profile: /profile/

## 9. How to continue in a fresh chat
If you open a new chat and want to continue with the same app, do exactly this:

### Step 1: go to the project folder
```powershell
cd C:\Users\RANESH\Downloads\finalyearproject
```

### Step 2: run the virtual environment
Use either:
```powershell
.\.venv\Scripts\Activate.ps1
```

Or, if activation is blocked:
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### Step 3: if needed, apply migrations
```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Do not delete `db.sqlite3` as part of normal startup; that removes local accounts and event data. Only reset it intentionally when a full local database wipe is wanted.

### Step 4: start the app
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### Step 5: open the app in the browser
- http://127.0.0.1:8000/

### Step 6: test the flows
1. Create participant account
2. Create organizer account
3. Organizer creates event
4. Student registers
5. Organizer uploads certificate for the student from the certificate page
6. Student sees the certificate in their dashboard and downloads it
7. If no certificate exists, student sees pending message

## 10. Important rules to avoid breaking the app
- Do not reintroduce seeded demo events.
- Keep public queries filtered to future published events.
- Keep organizer edit/delete access limited to the creator of the event.
- Do not let cancelled registrations block re-registration.
- Make certificates unique per event + user.
- Always check that certificate download is only for the correct user or organizer.
- If a certificate has not been uploaded yet, do not display a broken link.

## 11. Final status summary
Completed and verified:
- project setup
- event portal functionality
- organizer and participant roles
- event management
- event requests
- registrations and waitlists
- event cover images
- per-event organizer analytics dashboard
- organizer-only access to event analytics by event creator using event ownership rules
- student dashboard with certificate status
- organizer certificate upload per registered member
- certificate download flow
- polished styling
- database migration readiness
- authenticated original Holocloth with fully local source/runtime/assets, free cloth dragging, full physics/material/image/render settings, and PNG export
- 12 portal tests pass, including Holocloth access and local asset checks
- SQLite fallback support when MySQL is unavailable
- clean local database rebuild after migration issues
- verified running app at http://127.0.0.1:8000/

This is the exact state to resume from when continuing work on the project.

### App URL routing
- Holocloth: /holo-lab/
- File: portal/urls.py
- Function: app routes
- Purpose:
  - home page
  - login/register
  - dashboard
  - events listing and filtering
  - event details and registration
  - organizer dashboard and event management
  - request-event flow

## 5. Important files and their roles

### A. portal/models.py
Purpose: database models
Key models:
- OrganizerProfile
  - stores organizer profile data
- Event
  - event information and capacity settings
  - selected_count and waitlist_count properties
  - is_full property
- EventRegistration
  - participant event registration records
  - status can be selected, waitlist, or cancelled
- EventRequest
  - student event suggestion requests
  - status can be pending, approved, or rejected

### B. portal/forms.py
Purpose: form validation and HTML input setup
Key forms:
- UserRegistrationForm
  - registers new users and organizer role selection
- LoginForm
  - login form styling and validation
- UserUpdateForm
  - edits profile information
- OrganizerProfileForm
  - organizer profile data form
- EventForm
  - create and edit events
  - validates event_date so it cannot be in the past
  - defaults to published state when checked
- StudentEventRequestForm
  - student request for missing events

### C. portal/views.py
Purpose: all app logic and page behavior
Key functions:
- organizer_required(view_func)
  - blocks non-organizers from organizer pages
- ensure_demo_data()
  - intentionally does nothing; no seeded demo events are allowed
- home(request)
  - homepage with up to 3 published future events
  - shows View More if more than 3 events exist
- register_view(request)
  - create user account
- login_view(request)
  - login workflow
- dashboard(request)
  - participant dashboard with registration stats and charts
- holo_lab(request)
  - serves the authenticated original Holocloth app
- holocloth_asset(request, asset_name)
  - serves the upstream cloth textures locally to authenticated users
- events_list(request)
  - event list with keyword/category/date filtering
  - category accepts custom text input
- event_detail(request, event_id)
  - event detail page with registration status
  - fixed organizer reference issue
- register_for_event(request, event_id)
  - register participant and auto-assign shortlist/waitlist
- cancel_registration(request, event_id)
  - cancel registration
- organizer_dashboard(request)
  - organizer overview and pending event requests
- create_event(request)
  - add new event
- edit_event(request, event_id)
  - update existing event
- delete_event(request, event_id)
  - remove event
- request_event(request)
  - student sends event suggestion request
- update_event_request(request, event_request_id, action)
  - approve or reject student request and create event if approved
- profile(request)
  - user/profile management
- logout_view(request)
  - logs out current user

### D. portal/urls.py
Purpose: route definitions
Important routes:
- '' -> home
- register/ -> register_view
- login/ -> login_view
- logout/ -> logout_view
- dashboard/ -> dashboard
- holo-lab/ -> holo_lab
- holo-bg-2.jpg and bump-scratches.jpg -> authenticated local Holocloth assets
- events/ -> events_list
- event/<int:event_id>/ -> event_detail
- event/<int:event_id>/register/ -> register_for_event
- event/<int:event_id>/cancel/ -> cancel_registration
- request-event/ -> request_event
- organizer/ -> organizer_dashboard
- organizer/create/ -> create_event
- organizer/edit/<int:event_id>/ -> edit_event
- organizer/delete/<int:event_id>/ -> delete_event
- organizer/request/<int:event_request_id>/<str:action>/ -> update_event_request
- profile/ -> profile

### E. portal/templates/portal/
Purpose: all HTML pages
Important templates:
- base.html
  - shared navbar, footer, Bootstrap, CSS, JS, alerts
- home.html
  - landing page with hero section and upcoming events
  - displays 3 cards max and a View More button if needed
- events.html
  - list page with search/filter interface
  - category field accepts custom input
- event_detail.html
  - individual event registration screen
  - fixed organizer display logic
- dashboard.html
  - participant dashboard with cards and charts
- holocloth_page.html
- organizer_dashboard.html
  - organizer metrics, event list, and pending requests
- request_event.html
  - student form to request a missing event
- profile.html
  - user and organizer profile update form
- event_form.html
  - event create/edit form

### F. static/css/style.css
Purpose: custom visual styles
Contains:
- layout colors and theme variables
- metric cards
- chart styling
- event card hover animations
- search panel styling
- request panel styling
- responsive layout rules
- Holocloth's local host rules and original Geist Mono font declarations are in `static/css/holocloth_local.css`

### G. static/js/app.js
Purpose: front-end JavaScript behaviors
Contains:
- Bootstrap alert initialization
- reveal animation for event cards
- live client-side filtering for the event search box

### Holocloth upstream source and assets
- repository: `https://github.com/dmitrykurash/holocloth`
- the complete source snapshot is in `vendor/holocloth/`; its MIT copyright and permission notice must remain with redistributed copies
- locally served production artifacts: `static/holocloth/index-7o2sso0D.js` and `static/holocloth/index-CE1qk9yk.css`
- local source images: `static/holocloth/holo-bg-2.jpg` and `static/holocloth/bump-scratches.jpg`
- locally hosted Geist Mono weights and `GEIST-MONO-OFL.txt` are in `static/holocloth/`
- the production CSS font import was removed so this authenticated studio makes no external requests
### H. portal/tests.py

Purpose: regression verification tests
Current test:
- EventRequestTests.test_event_request_requires_user_and_title
- EventRequestTests.test_holo_lab_requires_login
- EventRequestTests.test_dashboard_links_to_holo_lab_and_lab_renders
- EventRequestTests.test_holocloth_assets_require_login_and_serve_local_images
- the project suite currently has 12 passing tests

## 6. Database and MySQL access
Database name: studentportal_db
Connection details:
- Host: 127.0.0.1
- Port: 3306
- User: root
- Password: root123

Access command:

```powershell
"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -uroot -proot123
```

Useful queries:

```sql
SHOW DATABASES;
USE studentportal_db;
SHOW TABLES;
SELECT * FROM portal_event;
SELECT * FROM portal_eventregistration;
SELECT * FROM portal_organizerprofile;
SELECT * FROM portal_eventrequest;
```

## 7. How to continue from here
Run this to continue the project later:

```powershell
cd C:\Users\RANESH\Downloads\finalyearproject
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Then open:
- http://127.0.0.1:8000/

If MySQL is not running, the app will automatically use SQLite locally without crashing.

## 8. Main user flow
1. Register or login
2. Create an organizer account if needed
3. Create a future-dated event from the organizer dashboard
4. Publish it if you want it visible to the public
5. Browse events on the events page
6. Search or filter by custom category/date/keyword
7. Register for an event
8. If full, get placed on waitlist automatically
9. Students can request missing events if not found
10. Organizers approve or reject pending event requests
11. Approved requests appear in the public event list

## 9. Summary of current progress
Completed:
- Django app set up and working
- MySQL database connection is optional for local development; SQLite fallback is now active when MySQL is unavailable
- event portal logic implemented
- search and filter included
- custom category search enabled
- organizer portal implemented
- event requests added
- visuals improved with CSS and JS
- original Holocloth is linked from the dashboard, verified in desktop and mobile browsers, and runs with zero external requests
- 12 portal tests pass, including Holocloth access and local image checks
- future-only validation added for event dates
- homepage event summary and View More behavior fixed
- demo events removed completely
- stale local DB issue repaired by resetting migrations and rebuilding the database
- app is running successfully at http://127.0.0.1:8000/
- documentation updated for handoff

## 10. Notes for future work
Possible next improvements:
- attendee export to CSV
- email notifications
- reviewer comments for event requests
- organizer permission management
- richer analytics charts

Important rules now in force:
- there are no demo or seeded events at startup
- the site begins empty until an organizer creates an event
- only the organizer who created an event can edit or delete it
- events appear publicly only if they are published and dated today or later
- past events do not show on the public event list

This file is the main continuation note for the project and should be used whenever the app needs to be resumed or extended. If a new chat is started, this file can be pasted in directly to resume the project from the verified point.
