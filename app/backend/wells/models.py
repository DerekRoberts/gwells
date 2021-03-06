"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

from gwells.models import AuditModel, ProvinceStateCode, ScreenIntakeMethodCode, ScreenMaterialCode,\
    ScreenOpeningCode, ScreenBottomCode, ScreenTypeCode, ScreenAssemblyTypeCode
from gwells.models.lithology import (
    LithologyDescriptionCode, LithologyColourCode, LithologyHardnessCode,
    LithologyMaterialCode, BedrockMaterialCode, BedrockMaterialDescriptorCode, LithologyStructureCode,
    LithologyMoistureCode, SurficialMaterialCode)
from registries.models import Person, Organization
from submissions.models import WellActivityCode
from aquifers.models import Aquifer


class DecommissionMethodCode(AuditModel):
    decommission_method_code = models.CharField(primary_key=True, max_length=10, editable=False,
                                                verbose_name="Code")
    description = models.CharField(max_length=255, verbose_name="Description")
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'decommission_method_code'
        ordering = ['display_order']

    def __str__(self):
        return self.description


class BCGS_Numbers(AuditModel):
    bcgs_id = models.BigIntegerField(primary_key=True, editable=False)
    bcgs_number = models.CharField(max_length=20, verbose_name="BCGS Mapsheet Number")

    class Meta:
        db_table = 'bcgs_number'

    def __str__(self):
        return self.bcgs_number


class ObsWellStatusCode(AuditModel):
    """
    Observation Well Status.
    """
    obs_well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'obs_well_status_code'
        ordering = ['display_order', 'obs_well_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(WellStatusCode, self).save(*args, **kwargs)


class YieldEstimationMethodCode(AuditModel):
    """
     The method used to estimate the yield of a well, e.g. Air Lifting, Bailing, Pumping.
    """
    yield_estimation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'yield_estimation_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WaterQualityCharacteristic(AuditModel):
    """
     The characteristic of the well water, e.g. Fresh, Salty, Clear.
    """

    code = models.CharField(primary_key=True, max_length=10, db_column='water_quality_characteristic_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    class Meta:
        db_table = 'water_quality_characteristic'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class DevelopmentMethodCode(AuditModel):
    """
     How the well was developed in order to remove the fine sediment and other organic or inorganic material
     that immediately surrounds the well screen, the drill hole or the intake area at the bottom of the well,
     e.g. air lifting, pumping, bailing.
    """
    development_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'development_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class FilterPackMaterialSizeCode(AuditModel):
    """
     The size of material used to pack a well filter, e.g. 1.0 - 2.0 mm, 2.0 - 4.0 mm, 4.0 - 8.0 mm.
    """
    filter_pack_material_size_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'filter_pack_material_size_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class FilterPackMaterialCode(AuditModel):
    """
     The material used to pack a well filter, e.g. Very coarse sand, Very fine gravel, Fine gravel.
    """
    filter_pack_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'filter_pack_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class LinerMaterialCode(AuditModel):
    """
     Liner material installed in a well to protect the well pump or other works in the well from damage.
    """
    code = models.CharField(
        primary_key=True, max_length=10, editable=False, db_column='liner_material_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'liner_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class SurfaceSealMethodCode(AuditModel):
    """
     Method used to install the surface seal in the annular space around the outside of the outermost casing
     and between mulitple casings of a well.
    """
    surface_seal_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'surface_seal_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class SurfaceSealMaterialCode(AuditModel):
    """
     Sealant material used that is installed in the annular space around the outside of the outermost casing
     and between multiple casings of a well.
    """
    surface_seal_material_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'surface_seal_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class DrillingMethodCode(AuditModel):
    """
    The method used to drill a well. For example, air rotary, dual rotary, cable tool, excavating, other.
    """
    drilling_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'drilling_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


# TODO: Remove this class - now using registries.something
# Not a Code table, but a representative sample of data to support search
class DrillingCompany(AuditModel):
    """
    Companies who perform drilling.
    """
    drilling_company_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    drilling_company_code = models.CharField(
        max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'drilling_company'
        verbose_name_plural = 'Drilling Companies'

    def __str__(self):
        return self.name


class LandDistrictCode(AuditModel):
    """
    Lookup of Legal Land Districts.
    """
    land_district_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    name = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'land_district_code'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class LicencedStatusCode(AuditModel):
    """
    LicencedStatusCode of Well.
    """
    licenced_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'licenced_status_code'
        ordering = ['display_order', 'licenced_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(LicencedStatusCode, self).save(*args, **kwargs)


class IntendedWaterUseCode(AuditModel):
    """
    Usage of Wells (water supply).
    """
    intended_water_use_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'intended_water_use_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class GroundElevationMethodCode(AuditModel):
    """
    The method used to determine the ground elevation of a well.
    Some examples of methods to determine ground elevation include:
    GPS, Altimeter, Differential GPS, Level, 1:50,000 map, 1:20,000 map, 1:10,000 map, 1:5,000 map.
    """
    ground_elevation_method_code = models.CharField(primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'ground_elevation_method_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WellClassCode(AuditModel):
    """
    Class of Well type.
    """
    well_class_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_class_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class WellStatusCodeTypeManager(models.Manager):
    """
    Provides additional methods for returning well status codes that correspond
    to activity submissions
    """

    # Construction reports correspond to "NEW" status
    def construction(self):
        return self.get_queryset().get(well_status_code='NEW')

    # Decommission reports trigger a "CLOSURE" status
    def decommission(self):
        return self.get_queryset().get(well_status_code='CLOSURE')

    # Alteration reports trigger an "ALTERATION" status
    def alteration(self):
        return self.get_queryset().get(well_status_code='ALTERATION')

    def other(self):
        return self.get_queryset().get(well_status_code='OTHER')


class WellStatusCode(AuditModel):
    """
    Well Status.
    """
    well_status_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    types = WellStatusCodeTypeManager()

    class Meta:
        db_table = 'well_status_code'
        ordering = ['display_order', 'well_status_code']

    def save(self, *args, **kwargs):
        self.validate()
        super(WellStatusCode, self).save(*args, **kwargs)


class WellPublicationStatusCode(AuditModel):
    """
    Well Publication Status.
    """
    well_publication_status_code = models.CharField(
        primary_key=True, max_length=20, editable=False, null=False)
    description = models.CharField(max_length=255, null=False)
    display_order = models.PositiveIntegerField(null=False)

    effective_date = models.DateTimeField(null=False)
    expiry_date = models.DateTimeField(null=False)

    class Meta:
        db_table = 'well_publication_status_code'
        ordering = ['display_order', 'well_publication_status_code']


class WellSubclassCode(AuditModel):
    """
    Subclass of Well type; we use GUID here as Django doesn't support multi-column PK's
    """
    well_subclass_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.PROTECT, blank=True)
    well_subclass_code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_subclass_code'
        ordering = ['display_order', 'description']

    def validate_unique(self, exclude=None):
        qs = Room.objects.filter(name=self.well_subclass_code)
        if qs.filter(well_class__well_class_code=self.well_class__well_class_code).exists():
            raise ValidationError('Code must be unique per Well Class')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(WellSubclassCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class WellYieldUnitCode(AuditModel):
    """
    Units of Well Yield.
    """
    well_yield_unit_code = models.CharField(
        primary_key=True, max_length=10, editable=False)
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'well_yield_unit_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class CoordinateAcquisitionCode(AuditModel):
    """
    •	A = (10 m accuracy) ICF cadastre and good location sketch
    •	B = (20 m accuracy) Digitized from 1:5,000 mapping
    •	C = (50 m accuracy) Digitized from 1:20,000 mapping
    •	D = (100 m accuracy) Digitized from old Dept. of Lands, Forests and Water Resources maps
    •	E = (200 m accuracy) Digitized from 1:50,000 maps
    •	F = (1 m accuracy) CDGPS
    •	G = (unknown, accuracy based on parcel size) No ICF cadastre, poor or no location sketch; site
        located in center of primary parcel
    •	H = (10 m accuracy) Handheld GPS with accuracy of +/- 10 metres
    •	I = (20 m accuracy) No ICF cadastre but good location sketch or good written description
    •	J = (unknown, accuracy based on parcel size) ICF cadastre, poor or no location sketch, arbitrarily
        located in center of parcel
    """
    code = models.CharField(primary_key=True, max_length=1, editable=False,
                            db_column='coordinate_acquisition_code')
    description = models.CharField(max_length=250)

    effective_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'coordinate_acquisition_code'
        ordering = ['code', ]

    def __str__(self):
        return self.description


# TODO: Consider having Well and Submission extend off a common base class, given that
#   they mostly have the exact same fields!
class Well(AuditModel):
    """
    Well information.
    """
    well_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well_tag_number = models.AutoField(
        primary_key=True, verbose_name='Well Tag Number')
    identification_plate_number = models.PositiveIntegerField(
        unique=True, blank=True, null=True, verbose_name="Well Identification Plate Number")

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name')
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')
    owner_city = models.CharField(max_length=100, verbose_name='Town/City')
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, blank=True,
        verbose_name='Province', null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

    well_class = models.ForeignKey(WellClassCode, null=True, db_column='well_class_code',
                                   on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Intended Water Use')
    well_status = models.ForeignKey(WellStatusCode, db_column='well_status_code',
                                    on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Well Status')
    well_publication_status = models.ForeignKey(WellPublicationStatusCode, db_column='well_publication_status_code',
                                                on_delete=models.CASCADE, verbose_name='Well Publication Status',
                                                default='Published')
    licenced_status = models.ForeignKey(LicencedStatusCode, db_column='licenced_status_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Licenced Status')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, null=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(blank=True, null=True,
                                            verbose_name='Property Identification Description (PID)')
    well_location_description = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Description of Well Location')

    construction_start_date = models.DateField(
        null=True, verbose_name="Construction Start Date")
    construction_end_date = models.DateField(
        null=True, verbose_name="Construction Date")

    alteration_start_date = models.DateField(
        null=True, verbose_name="Alteration Start Date")
    alteration_end_date = models.DateField(
        null=True, verbose_name="Alteration Date")

    decommission_start_date = models.DateField(
        null=True, verbose_name="Decommission Start Date")
    decommission_end_date = models.DateField(
        null=True, verbose_name="Decommission Date")

    drilling_company = models.ForeignKey(DrillingCompany, db_column='drilling_company_guid',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Drilling Company')

    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached')
    id_plate_attached_by = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Well identification plate attached by')

    latitude = models.DecimalField(
        max_digits=8, decimal_places=6, blank=True, null=True, verbose_name='Latitude')
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Longitude')
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_length = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Length')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Thickness')
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')
    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Backfill Material Above Surface Seal")
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Liner Diameter',
                                         validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                          verbose_name='Liner Thickness',
                                          validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                     verbose_name='Liner From',
                                     validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                   verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Intake Method')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Bottom')
    screen_information = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Screen Information"
    )
    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                           verbose_name='Filter Pack From',
                                           validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Filter Pack To',
                                         validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                verbose_name='Filter Pack Thickness',
                                                validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterialCode, db_column='filter_pack_material_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.CASCADE, blank=True, null=True,
                                                  verbose_name='Filter Pack Material Size')
    development_methods = models.ManyToManyField(DevelopmentMethodCode, blank=True,
                                                 verbose_name='Development Methods')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='well_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    water_supply_system_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(
        max_length=80, blank=True, null=True, verbose_name='Water Supply System Well Name')
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    internal_comments = models.CharField(max_length=3000, blank=True, null=True)

    alternative_specs_submitted = \
        models.BooleanField(default=False,
                            verbose_name='Alternative specs submitted (if required)',
                            choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True)

    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT)

    ems = models.CharField(max_length=10, blank=True, null=True,
                           verbose_name="Environmental Monitoring System (EMS) ID")

    utm_zone_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Zone")
    utm_northing = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Northing")
    utm_easting = models.IntegerField(
        blank=True, null=True, verbose_name="UTM Easting")
    coordinate_acquisition_code = models.ForeignKey(
        CoordinateAcquisitionCode, null=True, blank=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT)
    bcgs_id = models.ForeignKey(BCGS_Numbers, db_column='bcgs_id', on_delete=models.PROTECT, blank=True,
                                null=True, verbose_name="BCGS Mapsheet Number")

    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null="True",
        verbose_name="Method of Decommission", on_delete=models.PROTECT)
    decommission_sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Sealant Material")
    decommission_backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Decommission Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")
    ems_id = models.CharField(max_length=30, blank=True, null=True)
    aquifer = models.ForeignKey(Aquifer, db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
                                null=True, verbose_name='Aquifer ID Number')

    person_responsible = models.ForeignKey(Person, db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           null=True, blank=True)
    company_of_person_responsible = models.ForeignKey(
        Organization, db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
        verbose_name='Company of person responsible for drilling', null=True, blank=True)
    driller_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Company')

    # Aquifer related data
    aquifer_vulnerability_index = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')

    # Production data related data
    yield_estimation_method = models.ForeignKey(
        YieldEstimationMethodCode, db_column='yield_estimation_method_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Estimation Method')
    yield_estimation_rate = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Estimation Rate',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    yield_estimation_duration = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Estimation Duration',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    static_level_before_test = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='SWL Before Test',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    drawdown = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    hydro_fracturing_performed = models.BooleanField(
        default=False, verbose_name='Hydro-fracturing Performed?',
        choices=((False, 'No'), (True, 'Yes')))
    hydro_fracturing_yield_increase = models.DecimalField(
        max_digits=7, decimal_places=2,
        verbose_name='Well Yield Increase Due to Hydro-fracturing',
        blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Recommended pump depth',
                                                 validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                verbose_name='Recommended pump rate',
                                                validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'well'

    def __str__(self):
        if self.well_tag_number:
            return '%d %s' % (self.well_tag_number, self.street_address)
        else:
            return 'No well tag number %s' % (self.street_address)

    # Custom JSON serialisation for Wells. Expand as needed.
    def as_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "guid": self.well_guid,
            "identification_plate_number": self.identification_plate_number,
            "street_address": self.street_address,
            "well_tag_number": self.well_tag_number
        }


class Perforation(AuditModel):
    """
    Liner Details
    """
    perforation_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well_tag_number = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    liner_thickness = models.DecimalField(
        max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Liner Thickness')
    liner_diameter = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner Diameter')
    liner_from = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner From')
    liner_to = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Liner To')
    liner_perforation_from = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation From')
    liner_perforation_to = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Perforation To')

    class Meta:
        db_table = 'perforation'
        ordering = ['liner_from', 'liner_to', 'liner_perforation_from',
                    'liner_perforation_to', 'perforation_guid']

    def __str__(self):
        return self.description


class LtsaOwner(AuditModel):
    """
    Well owner information.
    """
    lsts_owner_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number',
                             on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name='Owner Name')
    mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address')

    city = models.CharField(max_length=100, verbose_name='Town/City')
    province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province')
    postal_code = models.CharField(
        max_length=10, blank=True, verbose_name='Postal Code')

    class Meta:
        db_table = 'ltsa_owner'

    def __str__(self):
        return '%s %s' % (self.full_name, self.mailing_address)


class CasingMaterialCode(AuditModel):
    """
     The material used for casing a well, e.g., Cement, Plastic, Steel.
    """
    code = models.CharField(primary_key=True, max_length=10, editable=False, db_column='casing_material_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'casing_material_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class CasingCode(AuditModel):
    """
    Type of Casing used on a well
    """
    code = models.CharField(primary_key=True, max_length=10, editable=False, db_column='casing_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'casing_code'
        ordering = ['display_order', 'description']

    def __str__(self):
        return self.description


class AquiferWell(AuditModel):
    """
    AquiferWell
    """

    aquifer_well_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aquifer_id = models.PositiveIntegerField(verbose_name="Aquifer Number", blank=True, null=True)
    well_tag_number = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number',
                                        on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'aquifer_well'


# TODO: This class needs to be moved to submissions.models (in order to do that, the fk references for a
# number of other models needs to be updated)
class ActivitySubmission(AuditModel):
    """
    Activity information on a Well submitted by a user.
    """
    filing_number = models.AutoField(primary_key=True)
    activity_submission_guid = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True)
    well_activity_type = models.ForeignKey(
        WellActivityCode, db_column='well_activity_code', on_delete=models.CASCADE,
        verbose_name='Type of Work')
    well_status = models.ForeignKey(WellStatusCode, db_column='well_status_code',
                                    on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='Well Status')
    well_publication_status = models.ForeignKey(WellPublicationStatusCode, db_column='well_publication_status_code',
                                                on_delete=models.CASCADE, verbose_name='Well Publication Status',
                                                default='Published')
    well_class = models.ForeignKey(WellClassCode, blank=True, null=True, db_column='well_class_code',
                                   on_delete=models.CASCADE, verbose_name='Well Class')
    well_subclass = models.ForeignKey(WellSubclassCode, db_column='well_subclass_guid',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Well Subclass')
    intended_water_use = models.ForeignKey(IntendedWaterUseCode, db_column='intended_water_use_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Intended Water Use')
    # Driller responsible should be a required field on all submissions, but for legacy well
    # information this may not be available, so we can't enforce this on a database level.
    person_responsible = models.ForeignKey(Person, db_column='person_responsible_guid',
                                           on_delete=models.PROTECT,
                                           verbose_name='Person Responsible for Drilling',
                                           blank=True, null=True)
    company_of_person_responsible = models.ForeignKey(
        Organization, db_column='org_of_person_responsible_guid', on_delete=models.PROTECT,
        verbose_name='Company of person responsible for drilling', null=True, blank=True)
    driller_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Name of Person Who Did the Work')
    consultant_name = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Name')
    consultant_company = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Consultant Company')
    # Work start & end date should be required fields on all submissions, but for legacy well
    # information this may not be available, so we can't enforce this on a database level.
    work_start_date = models.DateField(
        verbose_name='Work Start Date', null=True, blank=True)
    work_end_date = models.DateField(
        verbose_name='Work End Date', null=True, blank=True)

    owner_full_name = models.CharField(
        max_length=200, verbose_name='Owner Name', blank=True, null=True)
    owner_mailing_address = models.CharField(
        max_length=100, verbose_name='Mailing Address', blank=True, null=True)
    owner_city = models.CharField(max_length=100, verbose_name='Town/City', blank=True, null=True)
    owner_province_state = models.ForeignKey(
        ProvinceStateCode, db_column='province_state_code', on_delete=models.CASCADE, verbose_name='Province',
        blank=True, null=True)
    owner_postal_code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Postal Code')
    owner_email = models.EmailField(null=True, blank=True, verbose_name='Email address')
    owner_tel = models.CharField(
        null=True, blank=True, max_length=25, verbose_name='Telephone number')

    street_address = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Street Address')
    city = models.CharField(max_length=50, blank=True, null=True,
                            verbose_name='Town/City')
    legal_lot = models.CharField(max_length=10, blank=True, null=True, verbose_name='Lot')
    legal_plan = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Plan')
    legal_district_lot = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='District Lot')
    legal_block = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Block')
    legal_section = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Section')
    legal_township = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Township')
    legal_range = models.CharField(
        max_length=10, blank=True, null=True, verbose_name='Range')
    land_district = models.ForeignKey(LandDistrictCode, db_column='land_district_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Land District')
    legal_pid = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='PID')
    well_location_description = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Location Description')

    identification_plate_number = models.PositiveIntegerField(
        blank=True, null=True, verbose_name='Identification Plate Number')
    well_identification_plate_attached = models.CharField(
        max_length=500, blank=True, null=True, verbose_name='Well Identification Plate Is Attached')

    id_plate_attached_by = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Well identification plate attached by')

    latitude = models.DecimalField(
        max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    coordinate_acquisition_code = models.ForeignKey(
        CoordinateAcquisitionCode, null=True, blank=True, verbose_name="Location Accuracy Code",
        db_column='coordinate_acquisition_code', on_delete=models.PROTECT)
    ground_elevation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Ground Elevation')
    ground_elevation_method = models.ForeignKey(GroundElevationMethodCode,
                                                db_column='ground_elevation_method_code',
                                                on_delete=models.CASCADE, blank=True, null=True,
                                                verbose_name='Elevation Determined By')
    drilling_methods = models.ManyToManyField(DrillingMethodCode, verbose_name='Drilling Methods',
                                              blank=True)
    well_orientation = models.BooleanField(default=True, verbose_name='Orientation of Well', choices=(
        (True, 'vertical'), (False, 'horizontal')))
    water_supply_system_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Water Supply System Name')
    water_supply_system_well_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Water Supply System Well Name')

    surface_seal_material = models.ForeignKey(SurfaceSealMaterialCode, db_column='surface_seal_material_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name='Surface Seal Material')
    surface_seal_depth = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Surface Seal Depth')
    surface_seal_thickness = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Surface Seal Thickness',
                                                 validators=[MinValueValidator(Decimal('1.00'))])
    surface_seal_method = models.ForeignKey(SurfaceSealMethodCode, db_column='surface_seal_method_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Surface Seal Installation Method')

    backfill_above_surface_seal = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Backfill Material Above Surface Seal')
    backfill_above_surface_seal_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')
    backfill_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Backfill Depth')

    backfill_type = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Backfill Material Above Surface Seal")
    liner_material = models.ForeignKey(LinerMaterialCode, db_column='liner_material_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Liner Material')
    liner_diameter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Liner Diameter',
                                         validators=[MinValueValidator(Decimal('0.00'))])
    liner_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                          verbose_name='Liner Thickness',
                                          validators=[MinValueValidator(Decimal('0.00'))])
    liner_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                     verbose_name='Liner From',
                                     validators=[MinValueValidator(Decimal('0.00'))])
    liner_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                   verbose_name='Liner To', validators=[MinValueValidator(Decimal('0.01'))])

    screen_intake_method = models.ForeignKey(ScreenIntakeMethodCode, db_column='screen_intake_method_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Intake')
    screen_type = models.ForeignKey(ScreenTypeCode, db_column='screen_type_code',
                                    on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type')
    screen_material = models.ForeignKey(ScreenMaterialCode, db_column='screen_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Material')
    other_screen_material = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Material')
    screen_opening = models.ForeignKey(ScreenOpeningCode, db_column='screen_opening_code',
                                       on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Opening')
    screen_bottom = models.ForeignKey(ScreenBottomCode, db_column='screen_bottom_code',
                                      on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='Bottom')
    other_screen_bottom = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Specify Other Screen Bottom')

    screen_information = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="Screen Information"
    )

    filter_pack_from = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                           verbose_name='Filter Pack From',
                                           validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_to = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                         verbose_name='Filter Pack To',
                                         validators=[MinValueValidator(Decimal('0.01'))])
    filter_pack_thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                verbose_name='Filter Pack Thickness',
                                                validators=[MinValueValidator(Decimal('0.00'))])
    filter_pack_material = models.ForeignKey(FilterPackMaterialCode, db_column='filter_pack_material_code',
                                             on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='Filter Pack Material')
    filter_pack_material_size = models.ForeignKey(FilterPackMaterialSizeCode,
                                                  db_column='filter_pack_material_size_code',
                                                  on_delete=models.CASCADE, blank=True, null=True,
                                                  verbose_name='Filter Pack Material Size')
    development_methods = models.ManyToManyField(DevelopmentMethodCode, blank=True,
                                                 verbose_name='Development Methods')
    development_hours = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                            verbose_name='Development Total Duration',
                                            validators=[MinValueValidator(Decimal('0.00'))])
    development_notes = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Development Notes')

    water_quality_characteristics = models.ManyToManyField(
        WaterQualityCharacteristic, db_table='activity_submission_water_quality', blank=True,
        verbose_name='Obvious Water Quality Characteristics')
    water_quality_colour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Colour')
    water_quality_odour = models.CharField(
        max_length=60, blank=True, null=True, verbose_name='Water Quality Odour')

    total_depth_drilled = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Total Depth Drilled')
    finished_well_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Finished Well Depth')
    final_casing_stick_up = models.DecimalField(
        max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Final Casing Stick Up')
    bedrock_depth = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Depth to Bedrock')
    static_water_level = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Static Water Level (BTOC)')
    well_yield = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True, verbose_name='Estimated Well Yield')
    artesian_flow = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, verbose_name='Artesian Flow')
    artesian_pressure = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Artesian Pressure')
    well_cap_type = models.CharField(
        max_length=40, blank=True, null=True, verbose_name='Well Cap Type')
    well_disinfected = models.BooleanField(
        default=False, verbose_name='Well Disinfected?', choices=((False, 'No'), (True, 'Yes')))

    comments = models.CharField(max_length=3000, blank=True, null=True)
    internal_comments = models.CharField(max_length=3000, blank=True, null=True)

    alternative_specs_submitted = models.BooleanField(
        default=False, verbose_name='Alternative specs submitted (if required)', choices=((False, 'No'), (True, 'Yes')))

    well_yield_unit = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True)
    # want to be integer in future
    diameter = models.CharField(max_length=9, blank=True, null=True)
    ems_id = models.CharField(max_length=30, blank=True, null=True)

    # Observation well details
    observation_well_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Observation Well Number")

    observation_well_status = models.ForeignKey(
        ObsWellStatusCode, db_column='obs_well_status_code', blank=True, null=True,
        verbose_name="Observation Well Status", on_delete=models.PROTECT)
    # aquifer association
    aquifer = models.ForeignKey(Aquifer, db_column='aquifer_id', on_delete=models.PROTECT, blank=True,
                                null=True, verbose_name='Aquifer ID Number')

    # Decommission info
    decommission_reason = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Reason for Decommission")
    decommission_method = models.ForeignKey(
        DecommissionMethodCode, db_column='decommission_method_code', blank=True, null=True,
        verbose_name="Method of Decommission", on_delete=models.PROTECT)
    decommission_sealant_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Sealant Material")
    decommission_backfill_material = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Backfill Material")
    decommission_details = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Decommission Details")

    # Aquifer related data
    aquifer_vulnerability_index = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')

    # Production data related data
    yield_estimation_method = models.ForeignKey(
        YieldEstimationMethodCode, db_column='yield_estimation_method_code',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Estimation Method')
    yield_estimation_rate = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Estimation Rate',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    yield_estimation_duration = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Estimation Duration',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    static_level_before_test = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='SWL Before Test',
        blank=True, null=True, validators=[MinValueValidator(Decimal('0.0'))])
    drawdown = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    hydro_fracturing_performed = models.BooleanField(
        default=False, verbose_name='Hydro-fracturing Performed?',
        choices=((False, 'No'), (True, 'Yes')))
    hydro_fracturing_yield_increase = models.DecimalField(
        max_digits=7, decimal_places=2,
        verbose_name='Well Yield Increase Due to Hydro-fracturing',
        blank=True, null=True,
        validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_depth = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                 verbose_name='Recommended pump depth',
                                                 validators=[MinValueValidator(Decimal('0.00'))])
    recommended_pump_rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True,
                                                verbose_name='Recommended pump rate',
                                                validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'activity_submission'

    def __str__(self):
        if self.filing_number:
            return '%s %d %s %s' % (self.activity_submission_guid, self.filing_number,
                                    self.well_activity_type.code, self.street_address)
        else:
            return '%s %s' % (self.activity_submission_guid, self.street_address)


class LithologyDescription(AuditModel):
    """
    Lithology information details
    """
    lithology_description_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(
        ActivitySubmission, db_column='filing_number', on_delete=models.CASCADE, blank=True, null=True,
        related_name='lithologydescription_set')
    well = models.ForeignKey(
        Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True, null=True,
        related_name='lithologydescription_set')
    lithology_from = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='From',
                                         blank=True, null=True,
                                         validators=[MinValueValidator(Decimal('0.00'))])
    lithology_to = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='To',
                                       blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    lithology_raw_data = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Raw Data')

    lithology_description = models.ForeignKey(LithologyDescriptionCode,
                                              db_column='lithology_description_code',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              verbose_name="Description")
    lithology_colour = models.ForeignKey(LithologyColourCode, db_column='lithology_colour_code',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Colour')
    lithology_hardness = models.ForeignKey(LithologyHardnessCode, db_column='lithology_hardness_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Hardness')
    lithology_material = models.ForeignKey(LithologyMaterialCode, db_column='lithology_material_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Material")

    water_bearing_estimated_flow = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True, verbose_name='Water Bearing Estimated Flow')
    water_bearing_estimated_flow_units = models.ForeignKey(
        WellYieldUnitCode, db_column='well_yield_unit_code', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Units')
    lithology_observation = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='Observations')

    bedrock_material = models.ForeignKey(BedrockMaterialCode, db_column='bedrock_material_code',
                                         on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='Bedrock Material')
    bedrock_material_descriptor = models.ForeignKey(
        BedrockMaterialDescriptorCode, db_column='bedrock_material_descriptor_code', on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='Descriptor')
    lithology_structure = models.ForeignKey(LithologyStructureCode, db_column='lithology_structure_code',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='Bedding')
    lithology_moisture = models.ForeignKey(LithologyMoistureCode, db_column='lithology_moisture_code',
                                           on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name='Moisture')
    surficial_material = models.ForeignKey(SurficialMaterialCode, db_column='surficial_material_code',
                                           related_name='surficial_material_set', on_delete=models.CASCADE,
                                           blank=True, null=True, verbose_name='Surficial Material')
    secondary_surficial_material = models.ForeignKey(SurficialMaterialCode,
                                                     db_column='secondary_surficial_material_code',
                                                     related_name='secondary_surficial_material_set',
                                                     on_delete=models.CASCADE, blank=True, null=True,
                                                     verbose_name='Secondary Surficial Material')

    lithology_sequence_number = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lithology_description'
        ordering = ["lithology_sequence_number"]

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.lithology_from,
                                                         self.lithology_to)
        else:
            return 'well {} {} {}'.format(self.well, self.lithology_from, self.lithology_to)


class LinerPerforation(AuditModel):
    """
    Perforation in a well liner
    """
    liner_perforation_guid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                              editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='linerperforation_set')
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
                             null=True, related_name='linerperforation_set')
    start = models.DecimalField(db_column='liner_perforation_from', max_digits=7, decimal_places=2,
                                verbose_name='Perforated From', blank=False,
                                validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='liner_perforation_to', max_digits=7, decimal_places=2,
                              verbose_name='Perforated To', blank=False,
                              validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        ordering = ["start", "end"]
        db_table = 'liner_perforation'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission,
                                                         self.start,
                                                         self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)


class Casing(AuditModel):
    """
    Casing information

    A casing may be associated to a particular submission, or to a well.
    """
    casing_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='casing_set')
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE,
                             blank=True, null=True,
                             related_name='casing_set')
    # 2018/Sep/26 - According to PO (Lindsay), diameter, start and end are required fields.
    # There is however a lot of legacy data that does not have this field.
    start = models.DecimalField(db_column='casing_from', max_digits=7, decimal_places=2, verbose_name='From',
                                null=True, blank=True, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='casing_to', max_digits=7, decimal_places=2, verbose_name='To',
                              null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    # NOTE: Diameter should be pulling from internal_diameter
    diameter = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Diameter', null=True,
                                   blank=True, validators=[MinValueValidator(Decimal('0.5'))])
    casing_code = models.ForeignKey(CasingCode, db_column='casing_code', on_delete=models.CASCADE,
                                    verbose_name='Casing Type Code', null=True)
    casing_material = models.ForeignKey(CasingMaterialCode, db_column='casing_material_code',
                                        on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='Casing Material Code')
    wall_thickness = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='Wall Thickness',
                                         blank=True, null=True,
                                         validators=[MinValueValidator(Decimal('0.01'))])
    drive_shoe = models.NullBooleanField(default=False, null=True, verbose_name='Drive Shoe',
                                         choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        ordering = ["start", "end"]
        db_table = 'casing'

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.start, self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)

    def as_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "casing_guid": self.casing_guid,
            "well_tag_number": self.well_tag_number,
            "diameter": self.diameter,
            "wall_thickness": self.wall_thickness,
            "casing_material": self.casing_material,
            "drive_shoe": self.drive_shoe
        }


class Screen(AuditModel):
    """
    Screen in a well
    """
    screen_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='screen_set')
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
                             null=True, related_name='screen_set')
    start = models.DecimalField(db_column='screen_from', max_digits=7, decimal_places=2, verbose_name='From',
                                blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='screen_to', max_digits=7, decimal_places=2, verbose_name='To',
                              blank=False, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    internal_diameter = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Diameter',
                                            blank=True, null=True,
                                            validators=[MinValueValidator(Decimal('0.0'))])
    assembly_type = models.ForeignKey(
        ScreenAssemblyTypeCode, db_column='screen_assembly_type_code', on_delete=models.CASCADE, blank=True,
        null=True)
    slot_size = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Slot Size',
                                    blank=True, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'screen'
        ordering = ['start', 'end']

    def __str__(self):
        if self.activity_submission:
            return 'activity_submission {} {} {}'.format(self.activity_submission, self.start,
                                                         self.end)
        else:
            return 'well {} {} {}'.format(self.well, self.start, self.end)


class WaterQualityColour(AuditModel):
    """
    Colour choices for describing water quality
    """
    code = models.CharField(primary_key=True, max_length=32, db_column='water_quality_colour_code')
    description = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField()

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'water_quality_colour_code'

    def __str__(self):
        return self.description


class HydraulicProperty(AuditModel):
    """
    Hydraulic properties of the well, usually determined via tests.
    """
    hydraulic_property_guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    well = models.ForeignKey(Well, db_column='well_tag_number', to_field='well_tag_number',
                             on_delete=models.CASCADE, blank=False, null=False)
    avi = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='AVI')
    storativity = models.DecimalField(
        max_digits=8, decimal_places=7, blank=True, null=True, verbose_name='Storativity')
    transmissivity = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True, verbose_name='Transmissivity')
    hydraulic_conductivity = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Hydraulic Conductivity')
    specific_storage = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Specific Storage')
    specific_yield = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Specific Yield')
    testing_method = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Testing Method')
    testing_duration = models.PositiveIntegerField(blank=True, null=True)
    analytic_solution_type = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Analytic Solution Type')
    boundary_effect = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Boundary Effect')

    class Meta:
        db_table = 'hydraulic_property'
        verbose_name_plural = 'Hydraulic Properties'

    def __str__(self):
        return '{} - {}'.format(self.well, self.hydraulic_property_guid)


class DecommissionMaterialCode(AuditModel):
    """Codes for decommission materials"""
    code = models.CharField(primary_key=True, max_length=30, db_column='decommission_material_code')
    description = models.CharField(max_length=100)

    effective_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.description)


class DecommissionDescription(AuditModel):
    """Provides a description of the ground conditions (between specified start and end depth) for
        decommissioning"""

    decommission_description_guid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    activity_submission = models.ForeignKey(ActivitySubmission, db_column='filing_number',
                                            on_delete=models.CASCADE, blank=True, null=True,
                                            related_name='decommission_description_set')
    well = models.ForeignKey(Well, db_column='well_tag_number', on_delete=models.CASCADE, blank=True,
                             null=True, related_name='decommission_description_set')
    start = models.DecimalField(db_column='decommission_description_from', max_digits=7, decimal_places=2,
                                verbose_name='Decommissioned From', blank=False,
                                validators=[MinValueValidator(Decimal('0.00'))])
    end = models.DecimalField(db_column='decommission_description_to', max_digits=7, decimal_places=2,
                              verbose_name='Decommissioned To', blank=False,
                              validators=[MinValueValidator(Decimal('0.01'))])
    material = models.ForeignKey(DecommissionMaterialCode, db_column='decommission_material_code',
                                 on_delete=models.PROTECT)
    observations = models.CharField(max_length=255, null=True, blank=True)
