# Generated by Django 4.2.11 on 2024-05-09 14:25

import django.core.validators
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models
from django.conf import settings
from django.db import migrations, models

import tools.fields


class Migration(migrations.Migration):
    replaces = [
        ("tools", "0001_initial"),
        ("tools", "0002_alter_organization_octopoes_host"),
        ("tools", "0003_change_orgazation_host_to_code"),
        ("tools", "0004_ooiinformation"),
        ("tools", "0005_scanprofile"),
        ("tools", "0006_alter_organization_name"),
        ("tools", "0007_update_job"),
        ("tools", "0008_organizationmember_verified"),
        ("tools", "0009_scanprofile_is_source_ooi"),
        ("tools", "0010_alter_scanprofile_reference"),
        ("tools", "0011_job_input_ooi"),
        ("tools", "0012_rename_module_job_boefje_name"),
        ("tools", "0013_boefjeconfig"),
        ("tools", "0014_drop_dispatches_field"),
        ("tools", "0015_alter_job_input_ooi"),
        ("tools", "0016_organization_signal_fields"),
        ("tools", "0017_alter_organizationmember_foreignkey"),
        ("tools", "0018_alter_boefjeconfig_options"),
        ("tools", "0019_alter_scanprofile_remove_level_and_user"),
        ("tools", "0020_auto_20220524_1324"),
        ("tools", "0021_delete_boefjeconfig"),
        ("tools", "0022_alter_organization_options"),
        ("tools", "0023_delete_scanprofile"),
        ("tools", "0024_auto_20221005_1251"),
        ("tools", "0025_auto_20221027_1233"),
        ("tools", "0026_auto_20221031_1344"),
        ("tools", "0027_auto_20230103_1721"),
        ("tools", "0028_auto_20230117_1242"),
        ("tools", "0029_set_user_full_name"),
        ("tools", "0030_auto_20230227_1458"),
        ("tools", "0029_alter_organizationtag_color"),
        ("tools", "0031_merge_20230301_2012"),
        ("tools", "0032_alter_organizationmember_user"),
        ("tools", "0033_auto_20230407_1113"),
        ("tools", "0034_organizationmember_groups"),
        ("tools", "0035_update_perms_move_and_clear_groups"),
        ("tools", "0034_alter_organization_options"),
        ("tools", "0035_update_ooi_delete_perm"),
        ("tools", "0036_merge_20230504_1629"),
        ("tools", "0033_alter_organization_options"),
        ("tools", "0037_alter_organization_options"),
        ("tools", "0038_delete_job"),
        ("tools", "0038_alter_organization_options"),
        ("tools", "0039_merge_0038_alter_organization_options_0038_delete_job"),
        ("tools", "0039_update_permissions"),
        ("tools", "0040_update_admin_permission"),
        ("tools", "0040_admin_inherits_red_teamer_permissions"),
        ("tools", "0041_merge_20230731_1131"),
    ]

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField()),
                (
                    "count",
                    models.IntegerField(default=0, help_text="Internal counter of how many times this tag is in use"),
                ),
                (
                    "protected",
                    models.BooleanField(default=False, help_text="Will not be deleted when the count reaches 0"),
                ),
                ("path", models.TextField()),
                ("label", models.CharField(help_text="The name of the tag, without ancestors", max_length=255)),
                ("level", models.IntegerField(default=1, help_text="The level of the tag in the tree")),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("color-1-light", "Blue light"),
                            ("color-1-medium", "Blue medium"),
                            ("color-1-dark", "Blue dark"),
                            ("color-2-light", "Green light"),
                            ("color-2-medium", "Green medium"),
                            ("color-2-dark", "Green dark"),
                            ("color-3-light", "Yellow light"),
                            ("color-3-medium", "Yellow medium"),
                            ("color-3-dark", "Yellow dark"),
                            ("color-4-light", "Orange light"),
                            ("color-4-medium", "Orange medium"),
                            ("color-4-dark", "Orange dark"),
                            ("color-5-light", "Red light"),
                            ("color-5-medium", "Red medium"),
                            ("color-5-dark", "Red dark"),
                            ("color-6-light", "Violet light"),
                            ("color-6-medium", "Violet medium"),
                            ("color-6-dark", "Violet dark"),
                        ],
                        default="color-1-light",
                        max_length=20,
                    ),
                ),
                (
                    "border_type",
                    models.CharField(
                        choices=[("plain", "Plain"), ("solid", "Solid"), ("dashed", "Dashed"), ("dotted", "Dotted")],
                        default="plain",
                        max_length=20,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="tools.organizationtag",
                    ),
                ),
            ],
            options={"ordering": ("name",), "abstract": False, "unique_together": {("slug", "parent")}},
            bases=(tagulous.models.models.BaseTagTreeModel, models.Model),
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The name of the organization", max_length=126, unique=True)),
                (
                    "code",
                    tools.fields.LowerCaseSlugField(
                        allow_unicode=True,
                        help_text="A slug containing only lower-case unicode letters, numbers, hyphens or underscores that will be used in URLs and paths",
                        max_length=32,
                        unique=True,
                    ),
                ),
                (
                    "tags",
                    tagulous.models.fields.TagField(
                        _set_tag_meta=True,
                        blank=True,
                        force_lowercase=True,
                        help_text="Enter a comma-separated tag string",
                        protect_all=True,
                        to="tools.organizationtag",
                        tree=True,
                    ),
                ),
            ],
            options={
                "permissions": (
                    ("can_switch_organization", "Can switch organization"),
                    ("can_scan_organization", "Can scan organization"),
                    ("can_enable_disable_boefje", "Can enable or disable boefje"),
                    ("can_set_clearance_level", "Can set clearance level"),
                    ("can_delete_oois", "Can delete oois"),
                    ("can_mute_findings", "Can mute findings"),
                    ("can_view_katalogus_settings", "Can view KAT-alogus settings"),
                    ("can_set_katalogus_settings", "Can set KAT-alogus settings"),
                    ("can_recalculate_bits", "Can recalculate bits"),
                )
            },
        ),
        migrations.CreateModel(
            name="Indemnification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "organization",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="tools.organization"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OOIInformation",
            fields=[
                ("id", models.CharField(max_length=256, primary_key=True, serialize=False)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("data", models.JSONField(null=True)),
                ("consult_api", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(choices=[("active", "active"), ("new", "new")], default="new", max_length=64),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="members", to="tools.organization"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="members", to=settings.AUTH_USER_MODEL
                    ),
                ),
                ("onboarded", models.BooleanField(default=False)),
                (
                    "acknowledged_clearance_level",
                    models.IntegerField(
                        default=-1,
                        validators=[
                            django.core.validators.MinValueValidator(-1),
                            django.core.validators.MaxValueValidator(4),
                        ],
                    ),
                ),
                (
                    "trusted_clearance_level",
                    models.IntegerField(
                        default=-1,
                        validators=[
                            django.core.validators.MinValueValidator(-1),
                            django.core.validators.MaxValueValidator(4),
                        ],
                    ),
                ),
                ("blocked", models.BooleanField(default=False)),
                ("groups", models.ManyToManyField(blank=True, to="auth.group")),
            ],
            options={"unique_together": {("user", "organization")}},
        ),
    ]
