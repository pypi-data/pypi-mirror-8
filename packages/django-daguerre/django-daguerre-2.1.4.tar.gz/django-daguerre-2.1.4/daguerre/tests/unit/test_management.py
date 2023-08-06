from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import CommandError
from django.test.utils import override_settings
import mock

from daguerre.adjustments import Fit
from daguerre.management.commands._daguerre_clean import Command as Clean
from daguerre.management.commands._daguerre_preadjust import (NO_ADJUSTMENTS,
    BAD_STRUCTURE, Command as Preadjust)
from daguerre.management.commands.daguerre import Command as Daguerre
from daguerre.models import AdjustedImage, Area
from daguerre.tests.base import BaseTestCase


class CleanTestCase(BaseTestCase):
    def test_old_adjustments(self):
        """
        _old_adjustments should return AdjustedImages whose storage_path
        no longer exists.

        """
        nonexistant = 'daguerre/test/nonexistant.png'
        if default_storage.exists(nonexistant):
            default_storage.delete(nonexistant)

        adjusted = self.create_image('100x100.png')
        adjusted1 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=nonexistant,
                                                 adjusted=adjusted)
        adjusted2 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=adjusted,
                                                 adjusted=adjusted)
        clean = Clean()
        self.assertEqual(list(clean._old_adjustments()), [adjusted1])
        default_storage.delete(adjusted)

    def test_old_areas(self):
        """
        _old_areas should return Areas whose storage_path no longer exists.

        """
        nonexistant = 'daguerre/test/nonexistant.png'
        if default_storage.exists(nonexistant):
            default_storage.delete(nonexistant)

        storage_path = self.create_image('100x100.png')
        kwargs = {
            'x1': 0,
            'x2': 10,
            'y1': 0,
            'y2': 10
        }
        area1 = Area.objects.create(storage_path=nonexistant,
                                    **kwargs)
        area2 = Area.objects.create(storage_path=storage_path,
                                    **kwargs)
        clean = Clean()
        self.assertEqual(list(clean._old_areas()), [area1])
        default_storage.delete(storage_path)

    def test_missing_adjustments(self):
        """
        _missing_adjustments should return AdjustedImages whose adjusted
        no longer exists.

        """
        nonexistant = 'daguerre/test/nonexistant.png'
        if default_storage.exists(nonexistant):
            default_storage.delete(nonexistant)

        storage_path = self.create_image('100x100.png')
        adjusted1 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=storage_path,
                                                 adjusted=nonexistant)
        adjusted2 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=storage_path,
                                                 adjusted=storage_path)
        clean = Clean()
        self.assertEqual(list(clean._missing_adjustments()), [adjusted1])
        default_storage.delete(storage_path)

    def test_duplicate_adjustments(self):
        path1 = self.create_image('100x100.png')
        path2 = self.create_image('100x100.png')
        adjusted1 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=path1,
                                                 adjusted=path1)
        adjusted2 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=path1,
                                                 adjusted=path1)
        adjusted3 = AdjustedImage.objects.create(requested='fit|50|50',
                                                 storage_path=path2,
                                                 adjusted=path1)
        clean = Clean()
        duplicates = clean._duplicate_adjustments()
        self.assertNotIn(adjusted3, duplicates)
        self.assertTrue(list(duplicates) == [adjusted1] or
                        list(duplicates) == [adjusted2])

    def test_orphaned_files(self):
        clean = Clean()
        walk_ret = (
            ('daguerre', ['test'], []),
            ('daguerre/test', [], ['fake1.png', 'fake2.png', 'fake3.png'])
        )
        AdjustedImage.objects.create(requested='fit|50|50',
                                     storage_path='whatever.png',
                                     adjusted='daguerre/test/fake2.png')
        with mock.patch.object(clean, '_walk', return_value=walk_ret) as walk:
            self.assertEqual(clean._orphaned_files(),
                             ['daguerre/test/fake1.png',
                              'daguerre/test/fake3.png'])
            walk.assert_called_once_with('daguerre', topdown=False)


class PreadjustTestCase(BaseTestCase):
    @override_settings()
    def test_get_helpers__no_setting(self):
        try:
            del settings.DAGUERRE_PREADJUSTMENTS
        except AttributeError:
            pass
        preadjust = Preadjust()
        self.assertRaisesMessage(CommandError,
                                 NO_ADJUSTMENTS,
                                 preadjust._get_helpers)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(
        ('model', [Fit(width=50)], None),))
    def test_get_helpers__bad_string(self):
        preadjust = Preadjust()
        self.assertRaisesMessage(CommandError,
                                 BAD_STRUCTURE,
                                 preadjust._get_helpers)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(
        ('app.model', [Fit(width=50)], None),))
    def test_get_helpers__bad_model(self):
        preadjust = Preadjust()
        self.assertRaisesMessage(CommandError,
                                 BAD_STRUCTURE,
                                 preadjust._get_helpers)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(1, 2, 3))
    def test_get_helpers__not_tuples(self):
        preadjust = Preadjust()
        self.assertRaisesMessage(CommandError,
                                 BAD_STRUCTURE,
                                 preadjust._get_helpers)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(
        ('daguerre.adjustedimage', [], 'storage_path'),))
    def test_get_helpers__no_adjustments(self):
        preadjust = Preadjust()
        self.assertRaisesMessage(CommandError,
                                 BAD_STRUCTURE,
                                 preadjust._get_helpers)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(
        ('daguerre.adjustedimage', [Fit(width=50)], 'storage_path'),))
    def test_get_helpers__good_string(self):
        preadjust = Preadjust()
        helpers = preadjust._get_helpers()
        self.assertEqual(len(helpers), 1)

    @override_settings(DAGUERRE_PREADJUSTMENTS=(
        (AdjustedImage, [Fit(width=50)], 'storage_path'),))
    def test_get_helpers__model(self):
        preadjust = Preadjust()
        helpers = preadjust._get_helpers()
        self.assertEqual(len(helpers), 1)

    def test_get_helpers__queryset(self):
        preadjust = Preadjust()
        qs = AdjustedImage.objects.all()
        dp = ((qs, [Fit(width=50)], 'storage_path'),)
        with override_settings(DAGUERRE_PREADJUSTMENTS=dp):
            helpers = preadjust._get_helpers()
        self.assertEqual(len(helpers), 1)
        self.assertTrue(qs._result_cache is None)

    def test_get_helpers__iterable(self):
        preadjust = Preadjust()
        storage_path = self.create_image('100x100.png')
        adjusted = AdjustedImage.objects.create(storage_path=storage_path,
                                                adjusted=storage_path)

        def _iter():
            yield adjusted

        dp = ((_iter(), [Fit(width=50)], 'storage_path'),)

        with override_settings(DAGUERRE_PREADJUSTMENTS=dp):
            helpers = preadjust._get_helpers()
        self.assertEqual(len(helpers), 1)


class DaguerreTestCase(BaseTestCase):
    def test_find_commands(self):
        daguerre_command = Daguerre()
        self.assertEqual(daguerre_command._find_commands(), {
            'clean': '_daguerre_clean',
            'preadjust': '_daguerre_preadjust'
        })
