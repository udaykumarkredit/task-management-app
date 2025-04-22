import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from tasks.models import Task


class Command(BaseCommand):
    help = "Imports Tasks from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the csv file",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            with open(file_path, newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    created_at = (
                        datetime.fromisoformat(
                            row["created_at"].replace("Z", "+00:00")
                        ),
                    )
                    completed_at = None
                    if row["completed_at"]:
                        completed_at = datetime.fromisoformat(
                            row["completed_at"].replace("Z", "+00:00")
                        )
                    completed = row["completed"].lower() == "true"
                    Task.objects.create(
                        title=row["title"],
                        description=row["description"],
                        created_at=created_at,
                        completed=completed,
                        completed_at=completed_at,
                        priority=row["priority"],
                    )
            self.stdout.write(
                self.style.SUCCESS("Successfully Imported tasks from csv file")
            )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"file {file_path} not found"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error occurred : {str(e)}"))
