from django.db.models import Q
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from tagger.models import *
from tagger import constants
from tagger.utils import BaseAdmin


@admin.register(Status)
class StatusAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(DeathCause)
class DeathCauseAdmin(BaseAdmin):
    pass


@admin.register(Code)
class CodeAdmin(BaseAdmin):
    list_display = ("description", "category", "created_by", "created_on", "updated_by", "updated_on")
    list_filter = ("category",)


@admin.register(Period)
class PeriodAdmin(BaseAdmin):
    list_display = ("icd_input", "threshold", "icd_below", "icd_equal", "icd_above", "created_by", "created_on", "updated_by", "updated_on")
    search_fields = (
        "icd_input__description__icontains", 
        "icd_below__description__icontains", 
        "icd_equal__description__icontains",  
        "icd_above__description__icontains", 
        "threshold"
    )


@admin.register(Mapping)
class MappingAdmin(BaseAdmin):
    list_display = (
        "description", "code", "is_option", "is_option_updated_by", "is_option_updated_on", 
        "status", "status_updated_by", "status_updated_on",
        "created_by", "created_on", "updated_by", "updated_on"
    )
    list_filter = ("status", "is_option", "code__category")
    search_fields = ("description__description__icontains", "code__description__icontains")
    actions = ('mark_active', 'mark_inactive', 'mark_rejected', 'mark_is_option', 'mark_non_option')
    ordering = ('description', '-updated_on')
    template_message_singular = '%(count)d mapping was %(method)s marked as %(status)s.'
    template_message_plural = '%(count)d mappings were %(method)s marked as %(status)s.'

    def save_model(self, request, obj, form, change):
        offset = int(change)
        if obj.fields_tracker.has_changed('status_id'):
            obj.status_updated_by = request.user

            if obj.status.description == constants.Status.ACTIVE:
                rejected_status = Status.objects.get(description = constants.Status.REJECTED)
                updated_rejected = self.model.objects.filter(
                    Q(description = obj.description) & Q(status__description = constants.Status.PENDING_REVIEW)
                ).update(status = rejected_status) - offset

                self.message_user(request, ngettext(
                    self.template_message_singular,
                    self.template_message_plural,
                    updated_rejected,
                ) % {'count': updated_rejected, 'method': 'automatically', 'status': 'rejected'}, 
                messages.SUCCESS
                )

        if obj.fields_tracker.has_changed('is_option'):
            obj.is_option_updated_by = request.user

            if obj.is_option:
                updated_non_option = self.model.objects.filter(
                    Q(code = obj.code) & Q(is_option = True)
                ).update(is_option = False)

                self.message_user(request, ngettext(
                    self.template_message_singular,
                    self.template_message_plural,
                    updated_non_option,
                ) % {'count': updated_non_option, 'method': 'automatically', 'status': 'non-option'}, 
                messages.SUCCESS
                )

        super().save_model(request, obj, form, change)

    @admin.action(description = 'Mark selected mappings as active')
    def mark_active(self, request, queryset):
        num_selected_mappings = len(queryset)
        unique_descriptions = set(queryset.values_list('description', flat = True))
        num_unique_descriptions = len(unique_descriptions)

        if num_selected_mappings != num_unique_descriptions:
            self.message_user(request,
                'Please ensure that the selected mappings have unique descriptions.',
                level = messages.ERROR
            )
            return

        active_status = Status.objects.get(description = constants.Status.ACTIVE)
        rejected_status = Status.objects.get(description = constants.Status.REJECTED)
        updated_active = queryset.update(status = active_status)
        updated_rejected = self.model.objects.filter(
            Q(description__in = unique_descriptions) & Q(status__description = constants.Status.PENDING_REVIEW)
        ).update(status = rejected_status)

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_active,
        ) % {'count': updated_active, 'method': 'successfully', 'status': 'active'}, 
        messages.SUCCESS
        )

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_rejected,
        ) % {'count': updated_rejected, 'method': 'automatically', 'status': 'rejected'}, 
        messages.SUCCESS
        )

    @admin.action(description = 'Mark selected mappings as inactive')
    def mark_inactive(self, request, queryset):
        inactive_status = Status.objects.get(description = constants.Status.INACTIVE)
        updated_inactive = queryset.update(status = inactive_status)

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_inactive,
        ) % {'count': updated_inactive, 'method': 'successfully', 'status': 'inactive'}, 
        messages.SUCCESS
        )

    @admin.action(description = 'Mark selected mappings as rejected')
    def mark_rejected(self, request, queryset):
        rejected_status = Status.objects.get(description = constants.Status.REJECTED)
        updated_rejected = queryset.update(status = rejected_status)

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_rejected,
        ) % {'count': updated_rejected, 'method': 'successfully', 'status': 'rejected'}, 
        messages.SUCCESS
        )

    @admin.action(description = 'Mark selected mappings as non-option')
    def mark_non_option(self, request, queryset):
        updated_non_option = queryset.update(is_option = False)
        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_non_option,
        ) % {'count': updated_non_option, 'method': 'successfully', 'status': 'non-option'}, 
        messages.SUCCESS
        )

    @admin.action(description = 'Mark selected mappings as option')
    def mark_is_option(self, request, queryset):
        num_selected_codes = len(queryset)
        unique_codes = set(queryset.values_list('code', flat = True))
        num_unique_codes = len(unique_codes)

        if num_selected_codes != num_unique_codes:
            self.message_user(request,
                'Please ensure that the selected mappings have unique codes.',
                level = messages.ERROR
            )
            return

        updated_is_option = queryset.update(is_option = True)
        updated_non_option = self.model.objects.filter(
            Q(code__in = unique_codes) & Q(is_option = True) & ~Q(id__in = queryset.values_list('id', flat = True))
        ).update(is_option = False)

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_is_option,
        ) % {'count': updated_is_option, 'method': 'successfully', 'status': 'option'}, 
        messages.SUCCESS
        )

        self.message_user(request, ngettext(
            self.template_message_singular,
            self.template_message_plural,
            updated_non_option,
        ) % {'count': updated_non_option, 'method': 'automatically', 'status': 'non-option'}, 
        messages.SUCCESS
        )