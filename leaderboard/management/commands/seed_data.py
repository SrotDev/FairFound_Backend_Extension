import random
from django.core.management.base import BaseCommand
from leaderboard.models import Freelancer

# Realistic data pools
FIRST_NAMES = [
    'Sarah', 'Michael', 'Emily', 'James', 'Lisa', 'David', 'Anna', 'Robert', 'Jessica', 'Daniel',
    'Jennifer', 'Christopher', 'Amanda', 'Matthew', 'Ashley', 'Andrew', 'Stephanie', 'Joshua', 'Nicole', 'Ryan',
    'Elizabeth', 'Brandon', 'Megan', 'Justin', 'Rachel', 'Kevin', 'Lauren', 'Brian', 'Samantha', 'Tyler',
    'Aisha', 'Mohammed', 'Priya', 'Raj', 'Wei', 'Yuki', 'Carlos', 'Maria', 'Ahmed', 'Fatima',
    'Olga', 'Ivan', 'Sofia', 'Lucas', 'Emma', 'Noah', 'Olivia', 'Liam', 'Ava', 'Ethan'
]

LAST_NAMES = [
    'Johnson', 'Chen', 'Davis', 'Wilson', 'Anderson', 'Brown', 'Martinez', 'Taylor', 'Thomas', 'Garcia',
    'Rodriguez', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'King', 'Wright', 'Lopez', 'Hill',
    'Scott', 'Green', 'Adams', 'Baker', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner',
    'Patel', 'Khan', 'Singh', 'Kumar', 'Wang', 'Zhang', 'Tanaka', 'Sato', 'Kim', 'Park',
    'Nguyen', 'Tran', 'Muller', 'Schmidt', 'Silva', 'Santos', 'Ivanov', 'Petrov', 'Ali', 'Hassan'
]

SPECIALTIES = [
    'Full Stack Developer',
    'Frontend Developer', 
    'Backend Developer',
    'Mobile Developer',
    'UI/UX Designer',
    'Data Scientist',
    'DevOps Engineer',
    'Cloud Architect',
    'Machine Learning Engineer',
    'Blockchain Developer',
    'Game Developer',
    'WordPress Developer',
    'Shopify Developer',
    'React Developer',
    'Python Developer'
]

PLATFORMS = ['upwork', 'fiverr', 'toptal', 'freelancer']


class Command(BaseCommand):
    help = 'Seed database with 100 realistic freelancer profiles'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing freelancers...')
        Freelancer.objects.all().delete()

        self.stdout.write('Generating 100 freelancers...')
        freelancers_created = 0
        used_names = set()

        while freelancers_created < 100:
            # Generate unique name
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            
            if name in used_names:
                continue
            used_names.add(name)

            specialty = random.choice(SPECIALTIES)
            platform = random.choice(PLATFORMS)

            # Generate realistic metrics with variation
            # Top performers (10%)
            if freelancers_created < 10:
                rating = round(random.uniform(4.8, 5.0), 2)
                jobs = random.randint(150, 500)
                on_time = random.randint(92, 100)
                response = random.randint(1, 3)
                rehire = random.randint(75, 95)
                marketplace_score = random.randint(90, 99)
            # Good performers (30%)
            elif freelancers_created < 40:
                rating = round(random.uniform(4.5, 4.9), 2)
                jobs = random.randint(80, 200)
                on_time = random.randint(85, 95)
                response = random.randint(2, 6)
                rehire = random.randint(60, 80)
                marketplace_score = random.randint(75, 92)
            # Average performers (40%)
            elif freelancers_created < 80:
                rating = round(random.uniform(4.0, 4.6), 2)
                jobs = random.randint(30, 120)
                on_time = random.randint(75, 90)
                response = random.randint(3, 12)
                rehire = random.randint(45, 70)
                marketplace_score = random.randint(60, 80)
            # New/struggling (20%)
            else:
                rating = round(random.uniform(3.5, 4.3), 2)
                jobs = random.randint(5, 50)
                on_time = random.randint(65, 85)
                response = random.randint(6, 24)
                rehire = random.randint(30, 55)
                marketplace_score = random.randint(40, 65)

            freelancer = Freelancer.objects.create(
                name=name,
                profile_url=f"https://fairfound.com/freelancer/{name.lower().replace(' ', '-')}",
                specialty=specialty,
                platform=platform,
                marketplace_rating=rating,
                marketplace_score=marketplace_score,
                jobs_completed=jobs,
                on_time_percentage=on_time,
                response_time_hours=response,
                rehire_rate=rehire
            )
            freelancer.calculate_fairfound_score()
            freelancer.save()

            freelancers_created += 1
            if freelancers_created % 20 == 0:
                self.stdout.write(f'  Created {freelancers_created} freelancers...')

        # Print summary by specialty
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {freelancers_created} freelancers'))
        self.stdout.write('\nBreakdown by specialty:')
        for spec in SPECIALTIES:
            count = Freelancer.objects.filter(specialty=spec).count()
            if count > 0:
                self.stdout.write(f'  {spec}: {count}')
