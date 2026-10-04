import json
import hashlib
import os
import zipfile
import geopandas as gpd

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def validate_datasets():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    datasets_spec = [
        {"key": "LAND_DATA", "zip": "ne_10m_land.zip", "dir": "ne_10m_land"},
        {"key": "OCEAN_DATA", "zip": "ne_10m_ocean.zip", "dir": "ne_10m_ocean"},
        {"key": "LAKES_DATA", "zip": "ne_10m_lakes.zip", "dir": "ne_10m_lakes"},
        {"key": "MINOR_ISLANDS_DATA", "zip": "ne_10m_minor_islands.zip", "dir": "ne_10m_minor_islands"},
        {"key": "ICE_SHELF_DATA", "zip": "ne_10m_antarctic_ice_shelves_polys.zip", "dir": "ne_10m_antarctic_ice_shelves_polys"}
    ]

    geodata_dir = "tools/geodata"
    validation_results = {}
    all_pass = True

    for spec in datasets_spec:
        key = spec["key"]
        zip_name = spec["zip"]
        sub_dir = spec["dir"]
        zip_path = os.path.join(geodata_dir, zip_name)
        extract_path = os.path.join(geodata_dir, sub_dir)

        result = {
            "zip_filename": zip_name,
            "zip_exists": os.path.exists(zip_path),
            "zip_size": os.path.getsize(zip_path) if os.path.exists(zip_path) else 0,
            "sha256": compute_sha256(zip_path) if os.path.exists(zip_path) else "",
            "is_valid_zip": False,
            "shp_filename": None,
            "geopandas_success": False,
            "feature_count": 0,
            "geometry_types": [],
            "crs": None,
            "bbox": None,
            "source_url": "https://www.naturalearthdata.com/downloads/10m-physical-vectors/"
        }

        if result["zip_exists"] and zipfile.is_zipfile(zip_path):
            result["is_valid_zip"] = True
            os.makedirs(extract_path, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
            
            # Find .shp file
            shp_file = None
            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    if file.endswith(".shp"):
                        shp_file = os.path.join(root, file)
                        break
                if shp_file:
                    break

            if shp_file:
                result["shp_filename"] = os.path.relpath(shp_file, geodata_dir)
                try:
                    gdf = gpd.read_file(shp_file)
                    result["geopandas_success"] = True
                    result["feature_count"] = len(gdf)
                    result["geometry_types"] = list(gdf.geometry.geom_type.unique())
                    result["crs"] = str(gdf.crs)
                    result["bbox"] = list(gdf.total_bounds)
                except Exception as e:
                    result["geopandas_success"] = False
                    result["error"] = str(e)

        if result["geopandas_success"]:
            validation_results[key] = "PASS"
        else:
            validation_results[key] = "FAIL"
            all_pass = False

        result["validation_status"] = validation_results[key]
        spec["details"] = result

    data_acquisition_status = "PASS" if all_pass else "FAIL"

    # If all pass, delete test.zip
    test_zip_path = os.path.join(geodata_dir, "test.zip")
    if all_pass and os.path.exists(test_zip_path):
        os.remove(test_zip_path)

    # Re-run validation confirmation if all pass
    if all_pass:
        # Confirm reading successfully again
        for spec in datasets_spec:
            sub_dir = spec["dir"]
            extract_path = os.path.join(geodata_dir, sub_dir)
            shp_file = None
            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    if file.endswith(".shp"):
                        shp_file = os.path.join(root, file)
                        break
                if shp_file:
                    break
            if shp_file:
                try:
                    gdf = gpd.read_file(shp_file)
                    assert len(gdf) > 0
                except:
                    data_acquisition_status = "FAIL"

    report = {
        "DATA_ACQUISITION_STATUS": data_acquisition_status,
        "LAND_DATA": validation_results.get("LAND_DATA", "FAIL"),
        "OCEAN_DATA": validation_results.get("OCEAN_DATA", "FAIL"),
        "LAKES_DATA": validation_results.get("LAKES_DATA", "FAIL"),
        "MINOR_ISLANDS_DATA": validation_results.get("MINOR_ISLANDS_DATA", "FAIL"),
        "ICE_SHELF_DATA": validation_results.get("ICE_SHELF_DATA", "FAIL"),
        "datasets_detail": {spec["key"]: spec["details"] for spec in datasets_spec},
        "RUNTIME_MODIFIED": "NO"
    }

    with open("tools/GEODATA_ACQUISITION_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Geodata Acquisition Report - Map of Fame\n")
    md_lines.append(f"**DATA_ACQUISITION_STATUS**: {data_acquisition_status}")
    md_lines.append(f"**LAND_DATA**: {report['LAND_DATA']}")
    md_lines.append(f"**OCEAN_DATA**: {report['OCEAN_DATA']}")
    md_lines.append(f"**LAKES_DATA**: {report['LAKES_DATA']}")
    md_lines.append(f"**MINOR_ISLANDS_DATA**: {report['MINOR_ISLANDS_DATA']}")
    md_lines.append(f"**ICE_SHELF_DATA**: {report['ICE_SHELF_DATA']}")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")
    md_lines.append("## Dataset Validation Details\n")

    for spec in datasets_spec:
        k = spec["key"]
        d = spec["details"]
        md_lines.append(f"### {k} ({d['zip_filename']})")
        md_lines.append(f"- **File Exists**: {d['zip_exists']}")
        md_lines.append(f"- **ZIP Size**: {d['zip_size']} bytes")
        md_lines.append(f"- **SHA-256**: `{d['sha256']}`")
        md_lines.append(f"- **Valid ZIP**: {d['is_valid_zip']}")
        md_lines.append(f"- **SHP Filename**: {d['shp_filename']}")
        md_lines.append(f"- **GeoPandas Read Success**: {d['geopandas_success']}")
        md_lines.append(f"- **Feature Count**: {d['feature_count']}")
        md_lines.append(f"- **Geometry Types**: {d['geometry_types']}")
        md_lines.append(f"- **CRS**: {d['crs']}")
        md_lines.append(f"- **Bounding Box**: {d['bbox']}")
        md_lines.append(f"- **Status**: {d['validation_status']}\n")

    with open("tools/GEODATA_ACQUISITION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"DATA_ACQUISITION_STATUS = {data_acquisition_status}")
    print(f"LAND_DATA = {report['LAND_DATA']}")
    print(f"OCEAN_DATA = {report['OCEAN_DATA']}")
    print(f"LAKES_DATA = {report['LAKES_DATA']}")
    print(f"MINOR_ISLANDS_DATA = {report['MINOR_ISLANDS_DATA']}")
    print(f"ICE_SHELF_DATA = {report['ICE_SHELF_DATA']}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    validate_datasets()
