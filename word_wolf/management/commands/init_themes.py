from django.core.management.base import BaseCommand
from word_wolf.models import Theme
from word_wolf.theme_words import all_pairs


class Command(BaseCommand):
    help = "テーマデータを初期化"

    def handle(self, *args, **options):
        themes_data = all_pairs()

        Theme.objects.all().delete()

        for category, normal, wolf in themes_data:
            Theme.objects.create(
                category=category, normal_theme=normal, wolf_theme=wolf
            )

        self.stdout.write(
            self.style.SUCCESS(f"{len(themes_data)}個のテーマを作成しました")
        )
