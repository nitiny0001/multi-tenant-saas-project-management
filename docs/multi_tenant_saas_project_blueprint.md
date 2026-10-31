# Multi-Tenant SaaS Project Management Platform

## Project Blueprint and Technical Specification

**Project type:** Backend-focused SaaS application\
**Backend:** Python + FastAPI\
**Frontend:** React + Vite\
**Database:** PostgreSQL\
**Development approach:** Guided, incremental implementation\
**Architecture:** Modular monolith with shared database and shared
schema multi-tenancy

------------------------------------------------------------------------

## 1. Project Overview

The Multi-Tenant SaaS Project Management Platform is a web application
that allows multiple organizations to manage their teams, projects,
tasks, deadlines, and progress from a single platform.

Each organization operates in its own logically isolated workspace.
Organizations share the same application infrastructure and database,
but users can only access data they are authorized to see.

The product will provide functionality inspired by common
project-management tools such as Jira, Trello, and Asana, while
remaining a manageable learning and portfolio project.

### Main objectives

-   Build a complete REST API using FastAPI.
-   Understand how a real backend application is structured.
-   Implement authentication and role-based authorization.
-   Design relational database models and relationships.
-   Learn multi-tenant architecture and tenant data isolation.
-   Build a React frontend that consumes the API.
-   Add testing, deployment, documentation, and production-minded
    practices.

------------------------------------------------------------------------

## 2. Problem Statement

Small and growing organizations often coordinate projects through a
mixture of spreadsheets, chat messages, email threads, and disconnected
task-management tools.

This can lead to:

-   Unclear ownership of tasks and responsibilities.
-   Missed deadlines and poor progress visibility.
-   Difficulty coordinating work across teams.
-   No consistent record of project decisions or task updates.
-   Scattered information across multiple tools.
-   Limited visibility for managers into workloads and project status.

A further challenge appears when a software provider wants to offer
project-management software to multiple companies. It needs to serve
many organizations through one product while ensuring that one company's
users cannot view or modify another company's private information.

------------------------------------------------------------------------

## 3. Proposed Solution

Build a centralized SaaS platform where organizations can create
workspaces, add members, organize projects, assign tasks, monitor
progress, and receive notifications.

The application will use a **shared application and shared database
schema** model. Organization-owned records will be associated with an
organization, directly or through a validated parent record. The backend
will enforce tenant membership and permissions on every relevant
request.

### Example scenario

Three organizations register on the platform:

  Organization     Members Example projects
  -------------- --------- --------------------------
  TechNova              10 Website, Mobile App
  CodeCraft              5 CRM, API
  DevSphere             20 ERP, Analytics Dashboard

All organizations use the same deployed application. However, TechNova
users cannot access CodeCraft's projects, tasks, comments, or other
private records.

------------------------------------------------------------------------

## 4. Why This Project Is Needed

The project addresses two related needs:

### Need for project coordination

-   A single place to organize projects and tasks.
-   Clear task ownership, priorities, and deadlines.
-   Better visibility into progress and workload.
-   A searchable history of project activity.
-   Consistent collaboration between team members and managers.

### Need for multi-tenant SaaS architecture

-   One product can serve multiple customer organizations.
-   New organizations can onboard without a separate application
    deployment.
-   Shared infrastructure can reduce operational complexity.
-   Centralized updates and maintenance are easier to manage.
-   Tenant boundaries provide logical separation of customer data.

**Important:** Multi-tenancy does not automatically make data secure.
Tenant isolation must be enforced by backend authorization, database
constraints, careful query design, and automated security tests.

------------------------------------------------------------------------

## 5. Users and Roles

The platform will support the following roles. The exact permissions
will be defined and tested during implementation.

  Role                 Responsibilities
  -------------------- ------------------------------------------------------
  Platform Admin       Manages platform-level operations and support
  Organization Admin   Manages an organization, members, and settings
  Project Manager      Creates projects and manages project work
  Member               Views permitted projects and works on assigned tasks

A user may belong to more than one organization and may have a different
role in each organization. Organization membership and role therefore
belong in a membership table rather than being stored as a single global
role on the user record.

Project-level membership may further restrict access to individual
projects.

------------------------------------------------------------------------

## 6. Functional Scope and Modules

### Module 1: Authentication and User Management

-   User registration and login.
-   Secure password hashing.
-   JWT-based authentication.
-   Access-token validation.
-   User profile retrieval and updates.
-   Logout/token invalidation strategy, if required.

### Module 2: Organizations and Membership

-   Create an organization.
-   List organizations the current user belongs to.
-   Add or invite members.
-   Accept or reject invitations.
-   Assign and update organization roles.
-   Remove members, subject to ownership and permission rules.
-   Support users who belong to multiple organizations.

### Module 3: Projects

-   Create, view, update, and archive projects.
-   Store project name, description, status, start date, and deadline.
-   Add or remove project members.
-   Restrict project access to authorized organization members.
-   Filter and paginate project lists.

### Module 4: Tasks

-   Create, view, update, and delete tasks.
-   Assign tasks to eligible project members.
-   Set task status, priority, and due date.
-   Add descriptions and labels.
-   Filter tasks by status, priority, assignee, and deadline.
-   Maintain task activity history.

### Module 5: Comments and Activity Logs

-   Add comments to tasks.
-   Record important actions such as project creation, task assignment,
    and status changes.
-   Track who performed an action and when.
-   Enforce access checks before reading or creating comments.

### Module 6: Notifications

-   Notify users when tasks are assigned.
-   Notify users about comments or relevant changes.
-   Send deadline reminders.
-   Track read/unread status.
-   Retry failed notification delivery where appropriate.

### Module 7: Dashboard and Analytics

-   Show project counts and statuses.
-   Show pending, overdue, and completed tasks.
-   Summarize task assignments and workload.
-   Show project progress.
-   Provide organization-scoped dashboard data.

------------------------------------------------------------------------

## 7. Technology Stack

The stack is divided into core technologies and technologies introduced
as the project becomes more advanced.

### Core stack

  -----------------------------------------------------------------------
  Technology              Purpose                 When used
  ----------------------- ----------------------- -----------------------
  Python                  Backend programming     From the beginning
                          language                

  FastAPI                 REST API framework      From the beginning

  React                   Frontend user interface After initial backend
                                                  APIs

  Vite                    React development and   Frontend setup
                          build tooling           

  JavaScript              Frontend programming    Frontend development
                          language                

  PostgreSQL              Relational database     Phase 1

  SQLAlchemy 2.x          Python ORM and database Phase 1
                          access                  

  Pydantic                Request and response    From the beginning
                          validation              

  Alembic                 Database schema         Database setup
                          migrations              

  Uvicorn                 ASGI application server Local development

  Git and GitHub          Version control and     From the beginning
                          source hosting          

  Swagger UI / OpenAPI    API exploration and     From the beginning
                          documentation           
  -----------------------------------------------------------------------

### Authentication and security

  -----------------------------------------------------------------------
  Technology / concept                Purpose
  ----------------------------------- -----------------------------------
  OAuth2 password-bearer flow         Standard pattern for obtaining and
                                      sending access tokens in the
                                      initial learning implementation

  JWT                                 Carry signed authentication claims

  Argon2 or bcrypt password hashing   Store password hashes instead of
                                      plaintext passwords

  Role-Based Access Control (RBAC)    Enforce permissions by role

  CORS configuration                  Control which browser origins can
                                      call the API

  Environment variables               Keep secrets and
                                      environment-specific settings out
                                      of source code

  Database constraints                Protect data integrity

  Tenant-scoped authorization         Prevent cross-organization data
                                      access
  -----------------------------------------------------------------------

For a production deployment, use a suitable OAuth/OIDC identity provider
where appropriate, short-lived access tokens, secure refresh-token
handling, secret rotation, and HTTPS. Do not treat a user-supplied
organization ID as proof of membership.

### Testing and quality

  Technology                 Purpose
  -------------------------- ---------------------------------
  Pytest                     Automated tests
  HTTPX                      Make HTTP requests in API tests
  Ruff                       Python linting and formatting
  Coverage.py / pytest-cov   Measure test coverage

### Advanced technologies

  -----------------------------------------------------------------------
  Technology              Purpose                 Introduce when
  ----------------------- ----------------------- -----------------------
  Redis                   Caching, temporary      After core APIs work
                          data, and coordination  

  Celery                  Background job          When notifications and
                          processing              scheduled jobs are
                                                  added

  RabbitMQ                Message broker for      If the queue
                          asynchronous workloads  architecture needs it

  Docker                  Consistent application  After local application
                          environments            setup

  Docker Compose          Run backend, database,  During integration
                          and supporting services 
                          together                

  AWS S3                  Store uploaded files    When attachments are
                                                  implemented

  AWS / another cloud     Host the application    Deployment phase
  provider                and managed services    

  Nginx / managed ingress Reverse proxy and       Deployment, if needed
                          traffic routing         
  -----------------------------------------------------------------------

Do not install every advanced tool at the beginning. Add each technology
when a project requirement gives it a clear purpose.

------------------------------------------------------------------------

## 8. High-Level Architecture

The initial system will use a **modular monolith**. This means the
backend is one deployable FastAPI application, organized into separate
modules. It is simpler to develop, test, and deploy than starting with
microservices.

``` text
                         USERS
                           |
                           v
                    REACT FRONTEND
                    (Vite + JavaScript)
                           |
                      HTTPS / JSON
                           |
                           v
                    FASTAPI BACKEND
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        AUTH MODULE   ORGANIZATION   PROJECT / TASK
                        MODULE          MODULE
             |             |             |
             +-------------+-------------+
                           |
                  AUTHORIZATION LAYER
             (membership, role, tenant scope)
                           |
                           v
                     SQLALCHEMY
                           |
                           v
                     POSTGRESQL
                           |
             +-------------+-------------+
             |                           |
             v                           v
       ALEMBIC MIGRATIONS           AUDIT / LOG DATA

       Later additions:
       Redis | Celery | Message Broker | Object Storage
```

### Request lifecycle

1.  A user performs an action in React.
2.  React sends an HTTP request to the FastAPI backend.
3.  FastAPI validates the request using Pydantic.
4.  Authentication identifies the current user.
5.  Authorization checks the user's organization membership and role.
6.  The service layer applies business rules.
7.  SQLAlchemy reads or updates PostgreSQL.
8.  FastAPI returns a structured response.
9.  React updates the interface.

------------------------------------------------------------------------

## 9. Multi-Tenancy Strategy

### Chosen approach: Shared database, shared schema

All organizations use the same database tables. Organization-owned
records are scoped to a tenant.

For example:

``` text
organizations
-------------
id
name
slug
created_at

organization_members
--------------------
id
organization_id
user_id
role

projects
--------
id
organization_id
name
description
status

tasks
-----
id
project_id
title
assigned_to
status
priority
```

### Important design rules

-   A user can belong to multiple organizations.
-   Membership is represented through `organization_members`.
-   A project belongs to exactly one organization.
-   A task belongs to a project and inherits its organization scope
    through that project.
-   A task assignee must be eligible to work on that project.
-   Every endpoint must verify authorization and tenant scope.
-   Database foreign keys and appropriate uniqueness constraints must
    preserve relationships.
-   Sensitive operations must be covered by automated cross-tenant
    access tests.

### Tenant isolation example

If a user from Organization A requests a project belonging to
Organization B, the backend must deny access even if the user knows the
project's ID.

Tenant isolation must be applied to reads, updates, deletes, nested
resources, background jobs, exports, and dashboard queries.

For stronger defense in depth, PostgreSQL Row-Level Security (RLS) can
be evaluated later. It requires careful transaction-scoped tenant
context and connection-pooling design.

------------------------------------------------------------------------

## 10. Initial Database Design

Planned tables:

  Table                  Main purpose
  ---------------------- ------------------------------------------
  users                  User identity and authentication details
  organizations          Customer organizations
  organization_members   User-to-organization membership and role
  invitations            Pending organization invitations
  projects               Organization projects
  project_members        Project-specific membership
  tasks                  Work items within projects
  comments               Task discussion
  notifications          User notifications
  activity_logs          Record of important actions

### Important relationships

-   Users and organizations: many-to-many through
    `organization_members`.
-   Organizations and projects: one-to-many.
-   Projects and tasks: one-to-many.
-   Projects and users: many-to-many through `project_members`.
-   Tasks and comments: one-to-many.
-   Users and notifications: one-to-many.

The final schema will be refined during implementation. It should
include primary keys, foreign keys, uniqueness constraints, indexes,
timestamps, and appropriate deletion behavior.

------------------------------------------------------------------------

## 11. API Design

The backend will expose REST-style endpoints.

  Method   Endpoint                            Purpose
  -------- ----------------------------------- ------------------------------------
  POST     `/auth/register`                    Register a user
  POST     `/auth/login`                       Authenticate a user
  GET      `/users/me`                         Retrieve current user
  POST     `/organizations`                    Create organization
  GET      `/organizations`                    List user's organizations
  GET      `/organizations/{id}/members`       List organization members
  POST     `/organizations/{id}/invitations`   Invite a member
  POST     `/projects`                         Create a project
  GET      `/projects`                         List accessible projects
  GET      `/projects/{id}`                    Get project details
  PATCH    `/projects/{id}`                    Update a project
  POST     `/projects/{id}/tasks`              Create a task
  GET      `/projects/{id}/tasks`              List project tasks
  PATCH    `/tasks/{id}`                       Update a task
  DELETE   `/tasks/{id}`                       Delete a task
  POST     `/tasks/{id}/comments`              Add a comment
  GET      `/dashboard`                        Retrieve authorized dashboard data

The exact API contract may evolve. Responses should use consistent
status codes, validation errors, and pagination conventions.

------------------------------------------------------------------------

## 12. Frontend Scope

The frontend will use React and Vite. It will be developed after the
initial backend foundation and API contracts are established.

### Planned screens

1.  Login and registration.
2.  Organization selection.
3.  Organization dashboard.
4.  Team and member management.
5.  Project listing.
6.  Project details.
7.  Kanban task board.
8.  Task details and comments.
9.  Notifications.
10. User profile and settings.

### Frontend concepts to learn

-   React components and props.
-   State and event handling.
-   React Router.
-   Forms and validation.
-   API calls using Fetch or Axios.
-   Loading and error states.
-   Authentication state.
-   Protected routes.
-   Environment variables for API URLs.

The frontend must never be trusted to enforce security. All
authorization and tenant isolation must be enforced by the backend.

------------------------------------------------------------------------

## 13. Development Workflow and Roadmap

The project will be developed incrementally. Each phase should produce a
working result before the next phase begins.

  -----------------------------------------------------------------------
  Phase                   Work                    Expected outcome
  ----------------------- ----------------------- -----------------------
  1\. Foundation          Python environment,     Running backend
                          FastAPI, PostgreSQL,    connected to database
                          SQLAlchemy, Alembic     

  2\. Authentication      Registration, password  Securely authenticated
                          hashing, login, JWT,    users
                          protected routes        

  3\. Multi-tenancy       Organizations,          Isolated organization
                          memberships, tenant     workspaces
                          scoping, RBAC           

  4\. Projects            Project CRUD, project   Organization-scoped
                          membership, validation  projects

  5\. Tasks               Task CRUD, assignments, Working project task
                          statuses, comments      management

  6\. React frontend      React setup, routing,   Usable web interface
                          forms, API integration  

  7\. Collaboration       Notifications, activity Better team
                          history, background     collaboration
                          jobs                    

  8\. Quality and         Tests, indexing,        More reliable and
  performance             pagination, caching     efficient application

  9\. Deployment          Docker, production      Publicly accessible
                          configuration, cloud    application
                          deployment              

  10\. Documentation      README, architecture    Portfolio-ready
                          diagram, API examples,  repository
                          screenshots             
  -----------------------------------------------------------------------

### Phase 1: Foundation tasks

-   Create the project directory.
-   Create and activate a Python virtual environment.
-   Install FastAPI.
-   Create `main.py`.
-   Run Uvicorn.
-   Verify the root, health, and Swagger endpoints.
-   Install and configure PostgreSQL.
-   Connect PostgreSQL using SQLAlchemy.
-   Create the first database model.
-   Configure Alembic and run an initial migration.

### Definition of done for each phase

A phase is complete only when:

-   The feature works locally.
-   The relevant API endpoints are documented.
-   Important success and failure cases are tested.
-   Authorization checks are in place where required.
-   Code is committed to Git.
-   Setup or usage instructions are updated.

------------------------------------------------------------------------

## 14. Security and Reliability Requirements

Security is a core part of the project, not a final add-on.

-   Hash passwords using a suitable password-hashing algorithm.
-   Never store plaintext passwords or secrets in Git.
-   Validate all incoming data.
-   Authenticate protected endpoints.
-   Verify organization membership and role for each protected
    operation.
-   Scope database queries to the authorized tenant.
-   Prevent users from assigning tasks to unauthorized people.
-   Use foreign keys and database constraints.
-   Avoid exposing sensitive information in error responses.
-   Configure CORS for known frontend origins.
-   Use HTTPS in production.
-   Add rate limiting to sensitive endpoints such as login.
-   Test cross-tenant access attempts.
-   Log important security and administrative events without logging
    secrets.

### Critical security test

Given:

-   User A belongs only to Organization A.
-   Project B belongs to Organization B.

When User A requests Project B by its known ID, the API must deny access
and must not reveal the private project data.

This behavior must be tested for reading, updating, and deleting
resources, as well as nested tasks and comments.

------------------------------------------------------------------------

## 15. Testing Strategy

Testing will be introduced throughout development.

### Unit tests

Test individual functions and business rules, such as:

-   Password verification.
-   Role permission checks.
-   Task status transitions.
-   Project validation.

### Integration tests

Test interactions between API endpoints and the database:

-   User registration and login.
-   Organization creation.
-   Adding and removing members.
-   Creating projects and tasks.
-   Updating task status.

### Security tests

Test:

-   Unauthenticated access to protected routes.
-   Access by non-members.
-   Cross-tenant project access.
-   Unauthorized role actions.
-   Cross-tenant task and comment access.
-   Invalid task assignees.

### Performance tests

Later, measure:

-   Response times.
-   Database query performance.
-   Pagination behavior.
-   Cache effectiveness.
-   Behavior under concurrent requests.

------------------------------------------------------------------------

## 16. Deployment Plan

The first version will run locally:

``` text
React:      http://localhost:5173
FastAPI:    http://localhost:8000
Swagger:    http://localhost:8000/docs
PostgreSQL: localhost:5432
```

The deployment phase will include:

-   Dockerizing the backend.
-   Running services with Docker Compose during development.
-   Configuring production environment variables.
-   Using a managed PostgreSQL service or securely hosted database.
-   Hosting the React frontend and FastAPI backend.
-   Enabling HTTPS.
-   Configuring database migrations and backups.
-   Adding health checks and application logging.

A cloud provider such as AWS can be used as a later learning objective.
Cloud deployment should follow a working and tested local application.

------------------------------------------------------------------------

## 17. Future Scope

Once the core product is stable, the following features can extend it.

### Product features

-   Kanban and calendar views.
-   Gantt charts and project timelines.
-   File attachments and document management.
-   Real-time collaboration using WebSockets.
-   Team chat and project discussions.
-   Recurring tasks.
-   Custom workflows and task fields.
-   Advanced reports and exports.
-   Mobile-friendly interface.

### SaaS business features

-   Free and paid subscription plans.
-   Organization-level usage limits.
-   Billing integration.
-   Subscription lifecycle management.
-   Trial periods and plan upgrades.
-   Usage analytics.
-   Custom organization branding.
-   Custom domains.

### Technical enhancements

-   PostgreSQL Row-Level Security.
-   Redis caching.
-   Celery workers and message queues.
-   Object storage for attachments.
-   Search using PostgreSQL full-text search.
-   Observability with structured logs, metrics, and tracing.
-   Automated CI/CD pipelines.
-   Horizontal scaling.
-   Read replicas where justified.
-   Separate services only when actual scale or operational needs
    justify them.

### Optional AI features

-   Generate task descriptions from short notes.
-   Summarize project activity.
-   Suggest task priorities.
-   Search project documentation using natural language.

AI functionality is optional and should not delay the core backend.

------------------------------------------------------------------------

## 18. Expected Learning Outcomes

By completing this project, the developer should gain practical
experience with:

-   Building REST APIs using FastAPI.
-   Structuring a maintainable Python backend.
-   Designing relational databases.
-   Using SQLAlchemy and Alembic.
-   Implementing JWT authentication.
-   Understanding authorization and RBAC.
-   Designing multi-tenant applications.
-   Preventing cross-tenant data leaks.
-   Building a React frontend that consumes APIs.
-   Writing unit and integration tests.
-   Handling background jobs and caching.
-   Containerizing and deploying an application.
-   Documenting and explaining architectural decisions.

------------------------------------------------------------------------

## 19. Portfolio and Resume Value

The completed project can demonstrate more than basic CRUD knowledge.

### Suggested resume title

**Multi-Tenant SaaS Project Management Platform \| FastAPI, React,
PostgreSQL**

### Suggested resume description (update only after implementation)

-   Developed a multi-tenant project management platform using FastAPI,
    React, and PostgreSQL, supporting organization workspaces, project
    tracking, and task assignment.
-   Implemented JWT authentication, role-based access control, and
    tenant-scoped authorization to protect organization data.
-   Designed relational database models using SQLAlchemy and managed
    schema changes with Alembic.
-   Added automated API and security tests, including cross-tenant
    access prevention.

Do not claim features, performance metrics, user counts, or deployment
results until they have actually been implemented and verified.

### GitHub repository should include

-   Clear README.
-   Architecture diagram.
-   Technology stack.
-   Setup instructions.
-   Environment variable example file without real secrets.
-   Database schema or ER diagram.
-   API endpoint documentation.
-   Automated tests.
-   Screenshots of the React application.
-   Deployment URL, once available.

------------------------------------------------------------------------

## 20. Project Success Criteria

The project will be considered portfolio-ready when:

-   A user can register and authenticate.
-   A user can create or join an organization.
-   A user can belong to multiple organizations.
-   Organization roles are enforced by the backend.
-   Organizations can create and manage projects.
-   Projects can contain tasks and comments.
-   Users can only access resources they are authorized to access.
-   Cross-tenant access tests pass.
-   The React frontend can use the backend successfully.
-   Database migrations and automated tests work.
-   The application can be deployed using documented instructions.

------------------------------------------------------------------------

## 21. Immediate Next Steps

The first implementation milestone is deliberately small.

1.  Create the `saas-project/backend` directory.
2.  Create a Python virtual environment.
3.  Install FastAPI.
4.  Create `main.py`.
5.  Add `/`, `/health`, and `/info` endpoints.
6.  Run the application using Uvicorn.
7.  Verify the endpoints through Swagger UI at `/docs`.

After this, proceed to PostgreSQL installation and database integration.

**Development principle:** Understand each concept, implement it, test
it, and then move forward. The goal is not merely to finish a project,
but to be able to explain its architecture, security decisions, database
design, and trade-offs in a backend developer interview.
