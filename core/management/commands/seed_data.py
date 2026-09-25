from django.core.management.base import BaseCommand
from core.models import (
    Profile,
    SkillCategory,
    Skill,
    Experience,
    ValuePillar,
    SocialLink,
    SiteSettings,
)
from projects.models import Project, ProjectTechnology


class Command(BaseCommand):
    help = "Seed the database with exact 6-panel mockup content for Joseph Ashirumah portfolio"

    def handle(self, *args, **options):
        self.stdout.write("Seeding 6-panel portfolio data...")

        # 1. Profile
        profile, created = Profile.objects.get_or_create(pk=1)
        profile.name = "Joseph Ashirumah"
        profile.professional_title = "Full-Stack Software Engineer"
        profile.eyebrow_text = "FULL-STACK SOFTWARE ENGINEER"
        profile.headline = "Building reliable software for the modern web."
        profile.subheadline = (
            "I'm a Full-Stack Software Engineer specializing in Python, Django, SQL and modern frontend development. "
            "I enjoy turning ideas into reliable, maintainable web applications."
        )
        profile.short_bio = (
            "I'm a Full-Stack Software Engineer with a passion for building practical, scalable and user-focused web applications. "
            "I love solving real problems with clean code, thoughtful design and modern technologies."
        )
        profile.about_text = (
            "I'm a Full-Stack Software Engineer with a passion for building practical, scalable and user-focused web applications. "
            "I love solving real problems with clean code, thoughtful design and modern technologies.\n\n"
            "My core specialization is Python and Django on the backend, SQL and relational databases for data management, "
            "and modern frontend technologies for building responsive user experiences."
        )
        profile.email = "joseph@example.com"
        profile.phone = "+234 800 000 0000"
        profile.location = "Lagos, Nigeria"
        profile.profile_photo = "profile/headshot.jpg"
        profile.status_badge = "Available for software engineering opportunities"
        profile.status_active = True
        profile.github_url = "https://github.com/joseph"
        profile.linkedin_url = "https://linkedin.com/in/joseph"
        profile.twitter_url = "https://x.com/joseph"
        profile.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Profile seeded"))

        # 2. Site Settings
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.site_title = "Joseph Ashirumah | Full-Stack Software Engineer"
        settings.meta_description = (
            "Portfolio of Joseph Ashirumah, Full-Stack Software Engineer specializing in Python, Django, "
            "SQL, PostgreSQL, and modern web application development."
        )
        settings.footer_text = "Full-Stack Software Engineer"
        settings.contact_email = "joseph@example.com"
        settings.enable_contact_form = True
        settings.enable_hire_cta = True
        settings.save()
        self.stdout.write(self.style.SUCCESS("  [OK] Site Settings seeded"))

        # 3. Social Links
        socials_data = [
            ("github", "GitHub", "https://github.com/joseph", "bi-github", 1),
            ("linkedin", "LinkedIn", "https://linkedin.com/in/joseph", "bi-linkedin", 2),
            ("twitter", "Twitter", "https://x.com/joseph", "bi-twitter-x", 3),
            ("email", "Email", "mailto:joseph@example.com", "bi-envelope", 4),
        ]
        for platform, label, url, icon, order in socials_data:
            SocialLink.objects.update_or_create(
                platform=platform,
                defaults={
                    'label': label,
                    'url': url,
                    'icon_class': icon,
                    'is_active': True,
                    'order': order,
                }
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Social links seeded"))

        # 4. Skill Categories & Skills
        categories = [
            ("backend", "Backend", "bi-hdd-stack", 1),
            ("data", "Data", "bi-database", 2),
            ("frontend", "Frontend", "bi-code-square", 3),
            ("engineering", "Engineering", "bi-gear-wide-connected", 4),
        ]

        cat_objs = {}
        for key, name, icon, order in categories:
            cat, _ = SkillCategory.objects.update_or_create(
                key=key,
                defaults={'display_name': name, 'icon': icon, 'order': order}
            )
            cat_objs[key] = cat

        skills_data = [
            # Backend (4 tools)
            ("backend", "Python", True, "bi-filetype-py", "Core language, asynchronous programming, clean syntax", 1),
            ("backend", "Django", True, "bi-braces", "Full-stack framework, ORM, authentication, security", 2),
            ("backend", "Django REST Framework", False, "bi-hdd-network", "RESTful APIs, serializers, permissions", 3),
            ("backend", "REST APIs", False, "bi-arrow-left-right", "Stateless API design, JSON contracts", 4),

            # Data (4 tools)
            ("data", "PostgreSQL", True, "bi-database-check", "Production database, transactions, tuning", 1),
            ("data", "SQL", True, "bi-database-fill", "Complex queries, window functions, schema design", 2),
            ("data", "SQLite", False, "bi-database-gear", "Lightweight relational storage, rapid prototyping", 3),
            ("data", "Database Design", False, "bi-diagram-3", "ERD modeling, relational integrity, foreign keys", 4),

            # Frontend (5 tools)
            ("frontend", "JavaScript", False, "bi-filetype-js", "Modern JS, DOM manipulation, Fetch API", 1),
            ("frontend", "React", False, "bi-atom", "Component architecture, hooks, state management", 2),
            ("frontend", "HTML5", False, "bi-filetype-html", "Accessible semantic markup, SEO best practices", 3),
            ("frontend", "CSS3", False, "bi-filetype-css", "Flexbox, CSS Grid, custom properties", 4),
            ("frontend", "Bootstrap", False, "bi-bootstrap", "Mobile-first grid system, responsive utilities", 5),

            # Engineering (6 tools)
            ("engineering", "Git", False, "bi-git", "Version control, branching strategies", 1),
            ("engineering", "GitHub", False, "bi-github", "Pull requests, code reviews, actions", 2),
            ("engineering", "Authentication", False, "bi-shield-check", "Session auth, JWT tokens, CSRF protection", 3),
            ("engineering", "Testing", False, "bi-check2-all", "Django test client, unit testing, regression prevention", 4),
            ("engineering", "API Integration", False, "bi-plug", "Third-party payment gateways, webhook handlers", 5),
            ("engineering", "Deployment", False, "bi-cloud-arrow-up", "Production setup, Gunicorn, Whitenoise", 6),
        ]

        # Clear existing skills in these categories and repopulate cleanly
        Skill.objects.all().delete()
        for cat_key, skill_name, is_primary, icon, desc, order in skills_data:
            Skill.objects.create(
                category=cat_objs[cat_key],
                name=skill_name,
                is_primary_stack=is_primary,
                icon_class=icon,
                short_description=desc,
                order=order,
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Skills & Categories seeded"))

        # 5. Value Pillars (Panel 2: 4 cards)
        pillars_data = [
            ("Problem Solver", "bi-puzzle", "I enjoy tackling complex challenges and finding simple, effective solutions.", 1),
            ("Team Player", "bi-people", "I work well with others and value clear communication.", 2),
            ("Continuous Learner", "bi-book", "I'm always exploring new tools and improving my skills.", 3),
            ("Build for Impact", "bi-rocket-takeoff", "I want to create software that makes a real difference.", 4),
        ]
        ValuePillar.objects.all().delete()
        for title, icon, summary, order in pillars_data:
            ValuePillar.objects.create(
                title=title,
                icon=icon,
                short_summary=summary,
                order=order
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Value Pillars seeded"))

        # 6. Experience Timeline (Panel 6)
        experiences_data = [
            (
                "work",
                "Full-Stack Software Engineer",
                "Tech Solutions",
                "Lagos, Nigeria",
                "2026",
                "Present",
                True,
                "Building scalable web applications with Python, Django and modern frontend technologies. Working on real-world products and collaborating with cross-functional teams.",
                "",
                1
            ),
            (
                "work",
                "Software Development Engineer",
                "Digital Innovations",
                "Lagos, Nigeria",
                "2025",
                "2026",
                False,
                "Developed and maintained web applications, implemented APIs and worked with databases and modern frontend frameworks.",
                "",
                2
            ),
            (
                "work",
                "Junior Software Engineer",
                "Freelance",
                "Remote",
                "2024",
                "2025",
                False,
                "Built small business websites and web applications for clients using Django and React.",
                "",
                3
            ),
        ]
        Experience.objects.filter(experience_type='work').delete()
        for exp_type, title, org, loc, s_date, e_date, is_curr, desc, cred_url, order in experiences_data:
            Experience.objects.create(
                experience_type=exp_type,
                title=title,
                organization=org,
                location=loc,
                start_date=s_date,
                end_date=e_date,
                is_current=is_curr,
                description=desc,
                credential_url=cred_url,
                order=order,
            )
        self.stdout.write(self.style.SUCCESS("  [OK] Experience timeline seeded"))

        # 7. Project Technologies
        tech_tags = [
            ("Python", "tech-badge-cyan"),
            ("Django", "tech-badge-emerald"),
            ("SQL", "tech-badge-blue"),
            ("PostgreSQL", "tech-badge-blue"),
            ("Celery", "tech-badge-emerald"),
            ("Redis", "tech-badge-amber"),
            ("React", "tech-badge-cyan"),
            ("JavaScript", "tech-badge-amber"),
        ]
        tech_objs = {}
        for name, style in tech_tags:
            tag, _ = ProjectTechnology.objects.update_or_create(
                name=name,
                defaults={'badge_style': style}
            )
            tech_objs[name] = tag

        # 8. Projects (Panel 3: DevPulse, ShopCore, QueryCraft)
        # Reset all projects' featured flag
        Project.objects.all().update(featured=False)

        projects_data = [
            {
                "title": "DevPulse",
                "short_description": "Telemetry and asynchronous worker monitoring platform built with Python, Django, Celery and PostgreSQL.",
                "problem_statement": "Monitor and manage background workers, track system health, and get real-time visibility into application performance.",
                "solution_statement": "Built a lightweight and reliable monitoring platform using Django, Celery and PostgreSQL with a clean and intuitive dashboard.",
                "architecture_description": "• Backend: Django service layer orchestrating background telemetry collectors.\n• Distributed Queuing: Celery worker processes coordinated via Redis broker.\n• Persistence: PostgreSQL schema utilizing partitioned tables for historical time-series metric logs.\n• Interface: Real-time telemetry monitoring dashboard with asynchronous JSON polling.",
                "key_features": "• Real-time system monitoring\n• Asynchronous task processing\n• Worker health tracking\n• Clean and simple dashboard",
                "challenges_and_learnings": "Solved worker connection spikes during high-throughput metric ingestion by introducing an intermediate Redis caching buffer.",
                "techs": ["Python", "Django", "PostgreSQL", "Celery", "Redis"],
                "image": "projects/devpulse.svg",
                "featured": True,
                "display_order": 1,
                "github_url": "https://github.com/joseph/devpulse",
                "live_url": "https://demo.example.com/devpulse",
            },
            {
                "title": "ShopCore",
                "short_description": "A scalable e-commerce platform with inventory management and secure payments.",
                "problem_statement": "Prevent overselling during high-volume flash sales with strict concurrency controls and atomic database transactions.",
                "solution_statement": "Developed a robust e-commerce inventory and checkout API with pessimistic row-level locking on inventory items during reservation windows.",
                "architecture_description": "• API: Django REST Framework with modular serializers.\n• Concurrency: PostgreSQL row-level locks during checkout.\n• Frontend: Clean responsive catalog with cart state management.",
                "key_features": "• Atomically locked stock decrementing\n• Cart reservation timeout engine\n• RESTful API architecture\n• Secure payment checkout flow",
                "challenges_and_learnings": "Eliminated database deadlocks by sorting item primary keys deterministically before acquiring row-level locks.",
                "techs": ["Django", "PostgreSQL", "React", "JavaScript"],
                "image": "projects/shopcore.svg",
                "featured": True,
                "display_order": 2,
                "github_url": "https://github.com/joseph/shopcore",
                "live_url": "https://demo.example.com/shopcore",
            },
            {
                "title": "QueryCraft",
                "short_description": "Interactive browser-based SQL inspection workbench and schema visualizer.",
                "problem_statement": "Help developers explore relational database schemas and understand query plans without heavy desktop software.",
                "solution_statement": "Constructed an interactive SQL editor with automatic schema diagram generation and visual query execution plan explanations.",
                "architecture_description": "• Introspection: Python routines querying information_schema catalog tables.\n• Sandbox: Read-only query execution mode with transaction rollback.\n• Visualization: Dynamic SVG entity-relationship diagram renderer.",
                "key_features": "• Interactive schema diagram visualizer\n• In-browser SQL query workbench\n• Query EXPLAIN plan analyzer\n• Bookmarkable query snippets",
                "challenges_and_learnings": "Guaranteed security against destructive DDL queries using AST statement parsing and transaction-level read-only constraints.",
                "techs": ["Python", "Django", "JavaScript", "SQL"],
                "image": "projects/querycraft.svg",
                "featured": True,
                "display_order": 3,
                "github_url": "https://github.com/joseph/querycraft",
                "live_url": "https://demo.example.com/querycraft",
            },
        ]

        for p_data in projects_data:
            tech_names = p_data.pop("techs")
            project, _ = Project.objects.update_or_create(
                title=p_data["title"],
                defaults=p_data
            )
            project.technologies.clear()
            for t_name in tech_names:
                if t_name in tech_objs:
                    project.technologies.add(tech_objs[t_name])
            project.save()

        self.stdout.write(self.style.SUCCESS("  [OK] Projects seeded"))
        self.stdout.write(self.style.SUCCESS("6-panel mockup database seeding completed successfully!"))
