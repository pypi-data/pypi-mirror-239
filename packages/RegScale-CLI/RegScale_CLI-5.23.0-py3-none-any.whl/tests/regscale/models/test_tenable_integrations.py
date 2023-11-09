import json
from pathlib import Path
from random import randint
from unittest.mock import MagicMock, patch

import pytest
from lxml import etree

from regscale.core.app.utils.nessus_utils import (
    cpe_xml_to_dict,
    get_cpe_file,
    lookup_cpe_item_by_name,
    lookup_kev,
)
from regscale.integrations.public.cisa import pull_cisa_kev
from regscale.models.integration_models.nessus import NessusReport
from regscale.models.integration_models.tenable import TenableIOAsset


@pytest.fixture
def cpe_items():
    cpe_root = etree.parse(get_cpe_file())
    dat = cpe_xml_to_dict(cpe_root)
    return dat


@pytest.fixture
def new_assets():
    with open("./tests/test_data/ten_assets.json", "r") as f:
        dat = json.load(f)
    assets = [TenableIOAsset(**a) for a in dat]
    return assets


@pytest.fixture
def new_vulns():
    with open("./tests/test_data/ten_vulns.json", "r") as f:
        dat = json.load(f)
    vulns = [NessusReport(**v) for v in dat]
    return vulns


@pytest.mark.skip(reason="Manual test")
def test_nessus_processing():
    folder_path = Path().absolute() / "test_data"
    regscale_ssp_id = 2
    NessusReport.process_nessus_files(
        folder_path=folder_path, regscale_ssp_id=regscale_ssp_id
    )


@patch("regscale.core.app.application.Application")
@patch("regscale.models.integration_models.tenable.TenableIOAsset.sync_to_regscale")
def test_fetch_assets(mock_app, new_assets):
    # Call the fetch_assets function
    assets = new_assets
    app = mock_app
    with patch.object(TenableIOAsset, "sync_to_regscale") as mock_sync:
        mock_sync(app=app, assets=assets, ssp_id=2)

        # Check that the sync_to_regscale method was called with the correct arguments
        mock_sync.assert_called_once_with(app=app, assets=assets, ssp_id=2)


@patch("regscale.models.integration_models.nessus.NessusReport.sync_to_regscale")
def test_sync_nessus_reports(mock_sync):
    # Create some mock NessusReport objects to pass to the sync_nessus_reports function
    report1 = MagicMock(spec=NessusReport)
    report2 = MagicMock(spec=NessusReport)

    # Call the sync_nessus_reports function with the mock objects
    mock_sync([report1, report2], 123)

    # Check that the sync_to_regscale method was called with the expected arguments
    mock_sync.assert_called_once_with([report1, report2], 123)


def test_kev_lookup():
    cve = "CVE-1234-3456"
    data = pull_cisa_kev()
    avail = [dat["cveID"] for dat in data["vulnerabilities"]]
    index = randint(0, len(avail))
    assert lookup_kev(cve)[0] is None
    assert lookup_kev(avail[index])[0]


def test_cpe_lookup(cpe_items):
    name = "cpe:/a:gobalsky:vega:0.49.4"
    lookup_cpe_item_by_name(name, cpe_items)
