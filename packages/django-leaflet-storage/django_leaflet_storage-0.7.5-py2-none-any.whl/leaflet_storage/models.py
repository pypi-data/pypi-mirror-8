# -*- coding: utf-8 -*-

import os

from django.contrib.gis.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.signing import Signer
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.core.files.base import File

from .fields import DictField
from .managers import PublicManager


class NamedModel(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("name"))

    class Meta:
        abstract = True
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class Licence(NamedModel):
    """
    The licence one map is published on.
    """
    details = models.URLField(
        verbose_name=_('details'),
        help_text=_('Link to a page where the licence is detailed.')
    )

    @classmethod
    def get_default(cls):
        """
        Returns a default Licence, creates it if it doesn't exist.
        Needed to prevent a licence deletion from deleting all the linked
        maps.
        """
        return cls.objects.get_or_create(
            # can't use ugettext_lazy for database storage, see #13965
            name=getattr(settings, "LEAFLET_STORAGE_DEFAULT_LICENCE_NAME", ugettext('No licence set'))
        )[0]

    @property
    def json(self):
        return {
            'name': self.name,
            'url': self.details
        }


class TileLayer(NamedModel):
    url_template = models.CharField(
        max_length=200,
        help_text=_("URL template using OSM tile format")
    )
    minZoom = models.IntegerField(default=0)
    maxZoom = models.IntegerField(default=18)
    attribution = models.CharField(max_length=300)
    rank = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_('Order of the tilelayers in the edit box')
    )

    @property
    def json(self):
        return dict((field.name, getattr(self, field.name)) for field in self._meta.fields)

    @classmethod
    def get_default(cls):
        """
        Returns the default tile layer (used for a map when no layer is set).
        """
        return cls.objects.order_by('rank')[0]  # FIXME, make it administrable

    @classmethod
    def get_list(cls, selected=None):
        l = []
        for t in cls.objects.all():
            fields = t.json
            if selected and selected.pk == t.pk:
                fields['selected'] = True
            l.append(fields)
        return l

    class Meta:
        ordering = ('rank', 'name', )


class Map(NamedModel):
    """
    A single thematical map.
    """
    ANONYMOUS = 1
    EDITORS = 2
    OWNER = 3
    PUBLIC = 1
    OPEN = 2
    PRIVATE = 3
    EDIT_STATUS = (
        (ANONYMOUS, _('Everyone can edit')),
        (EDITORS, _('Only editors can edit')),
        (OWNER, _('Only owner can edit')),
    )
    SHARE_STATUS = (
        (PUBLIC, _('everyone (public)')),
        (OPEN, _('anyone with link')),
        (PRIVATE, _('editors only')),
    )
    slug = models.SlugField(db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    center = models.PointField(geography=True, verbose_name=_("center"))
    zoom = models.IntegerField(default=7, verbose_name=_("zoom"))
    locate = models.BooleanField(default=False, verbose_name=_("locate"), help_text=_("Locate user on load?"))
    licence = models.ForeignKey(
        Licence,
        help_text=_("Choose the map licence."),
        verbose_name=_('licence'),
        on_delete=models.SET_DEFAULT,
        default=Licence.get_default
    )
    modified_at = models.DateTimeField(auto_now=True)
    tilelayer = models.ForeignKey(TileLayer, blank=True, null=True, related_name="maps",  verbose_name=_("background"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="owned_maps", verbose_name=_("owner"))
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name=_("editors"))
    edit_status = models.SmallIntegerField(choices=EDIT_STATUS, default=OWNER, verbose_name=_("edit status"))
    share_status = models.SmallIntegerField(choices=SHARE_STATUS, default=PUBLIC, verbose_name=_("share status"))
    settings = DictField(blank=True, null=True, verbose_name=_("settings"))

    objects = models.GeoManager()
    public = PublicManager()

    def get_absolute_url(self):
        return reverse("map", kwargs={'slug': self.slug or "map", 'pk': self.pk})

    def get_anonymous_edit_url(self):
        signer = Signer()
        signature = signer.sign(self.pk)
        return reverse('map_anonymous_edit_url', kwargs={'signature': signature})

    def is_anonymous_owner(self, request):
        if self.owner:
            # edit cookies are only valid while map hasn't owner
            return False
        key, value = self.signed_cookie_elements
        try:
            has_anonymous_cookie = int(request.get_signed_cookie(key, False)) == value
        except ValueError:
            has_anonymous_cookie = False
        return has_anonymous_cookie

    def can_edit(self, user=None, request=None):
        """
        Define if a user can edit or not the instance, according to his account
        or the request.
        """
        can = False
        if request and not self.owner:
            if (getattr(settings, "LEAFLET_STORAGE_ALLOW_ANONYMOUS", False)
                    and self.is_anonymous_owner(request)):
                can = True
                if user and user.is_authenticated():
                    # if user is authenticated, attach as owner
                    self.owner = user
                    self.save()
                    msg = _("Your anonymous map has been attached to your account %s" % user)
                    messages.info(request, msg)
        if self.edit_status == self.ANONYMOUS:
            can = True
        elif not user.is_authenticated():
            pass
        elif user == self.owner:
            can = True
        elif self.edit_status == self.EDITORS and user in self.editors.all():
            can = True
        return can

    def can_view(self, request):
        if self.owner is None:
            can = True
        elif self.share_status in [self.PUBLIC, self.OPEN]:
            can = True
        elif request.user == self.owner:
            can = True
        else:
            can = not (self.share_status == self.PRIVATE and request.user not in self.editors.all())
        return can

    @property
    def signed_cookie_elements(self):
        return ('anonymous_owner|%s' % self.pk, self.pk)

    def get_tilelayer(self):
        return self.tilelayer or TileLayer.get_default()

    def clone(self, **kwargs):
        new = self.__class__.objects.get(pk=self.pk)
        new.pk = None
        new.name = u"%s %s" % (_("Clone of"), self.name)
        if "owner" in kwargs:
            # can be None in case of anonymous cloning
            new.owner = kwargs["owner"]
        new.save()
        for editor in self.editors.all():
            new.editors.add(editor)
        for datalayer in self.datalayer_set.all():
            datalayer.clone(map_inst=new)
        return new


class Pictogram(NamedModel):
    """
    An image added to an icon of the map.
    """
    attribution = models.CharField(max_length=300)
    pictogram = models.ImageField(upload_to="pictogram")

    @property
    def json(self):
        return {
            "id": self.pk,
            "attribution": self.attribution,
            "name": self.name,
            "src": self.pictogram.url
        }


class DataLayer(NamedModel):
    """
    Layer to store Features in.
    """
    def upload_to(instance, filename):
        path = ["datalayer", str(instance.map.pk)[-1]]
        if len(str(instance.map.pk)) > 1:
            path.append(str(instance.map.pk)[-2])
        path.append(str(instance.map.pk))
        path.append("%s.geojson" % (slugify(instance.name)[:50] or "untitled"))
        return os.path.join(*path)
    map = models.ForeignKey(Map)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("description")
    )
    geojson = models.FileField(upload_to=upload_to, blank=True, null=True)
    display_on_load = models.BooleanField(
        default=False,
        verbose_name=_("display on load"),
        help_text=_("Display this layer on load.")
    )

    @property
    def metadata(self):
        return {
            "name": self.name,
            "id": self.pk,
            "displayOnLoad": self.display_on_load
        }

    def clone(self, map_inst=None):
        new = self.__class__.objects.get(pk=self.pk)
        new.pk = None
        if map_inst:
            new.map = map_inst
        new.geojson = File(new.geojson.file.file)
        new.save()
        return new
