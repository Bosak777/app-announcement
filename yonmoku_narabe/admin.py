from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "current_player",
        "winner",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "winner", "created_at")
    readonly_fields = ("board", "created_at", "updated_at")
    fieldsets = (
        (
            "ゲーム情報",
            {
                "fields": (
                    "id",
                    "status",
                    "current_player",
                    "winner",
                    "created_at",
                    "updated_at",
                )
            },
        ),
        ("盤面", {"fields": ("board",)}),
    )

    def has_add_permission(self, request):
        return False
