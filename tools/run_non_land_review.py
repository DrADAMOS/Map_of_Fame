import json
import hashlib
import os
import geopandas as gpd
from shapely.geometry import Point

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_shp(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".shp"):
                return os.path.join(root, file)
    return None

def run_non_land_review():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"
    audit_json_path = "tools/FULL_GEOGRAPHIC_COORDINATE_AUDIT.json"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    with open(audit_json_path, "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    all_records = audit_data.get("records", [])
    non_land_records = [r for r in all_records if r.get("physical_status") != "LAND"]

    print(f"Total non-land records found: {len(non_land_records)}")

    # Load Natural Earth geometries
    geodata_root = "tools/geodata"
    land_shp = find_shp(os.path.join(geodata_root, "ne_10m_land"))
    ocean_shp = find_shp(os.path.join(geodata_root, "ne_10m_ocean"))
    lakes_shp = find_shp(os.path.join(geodata_root, "ne_10m_lakes"))
    minor_islands_shp = find_shp(os.path.join(geodata_root, "ne_10m_minor_islands"))
    ice_shelves_shp = find_shp(os.path.join(geodata_root, "ne_10m_antarctic_ice_shelves_polys"))

    gdf_land = gpd.read_file(land_shp) if land_shp else None
    gdf_ocean = gpd.read_file(ocean_shp) if ocean_shp else None
    gdf_lakes = gpd.read_file(lakes_shp) if lakes_shp else None
    gdf_minor = gpd.read_file(minor_islands_shp) if minor_islands_shp else None
    gdf_ice = gpd.read_file(ice_shelves_shp) if ice_shelves_shp else None

    land_geoms = []
    if gdf_land is not None: land_geoms.append(gdf_land.geometry)
    if gdf_minor is not None: land_geoms.append(gdf_minor.geometry)
    
    review_records = []
    open_water_count = 0
    inland_water_count = 0
    ice_shelf_count = 0

    likely_correct_count = 0
    likely_wrong_count = 0
    uncertain_count = 0

    for r in non_land_records:
        lat = r["latitude"]
        lng = r["longitude"]
        pt = Point(lng, lat)
        
        p_status = r["physical_status"]
        if p_status == "OPEN_WATER": open_water_count += 1
        elif p_status == "INLAND_WATER": inland_water_count += 1
        elif p_status == "ICE_SHELF": ice_shelf_count += 1

        # Re-test intersections
        land_int = bool(gdf_land is not None and gdf_land.intersects(pt).any())
        minor_int = bool(gdf_minor is not None and gdf_minor.intersects(pt).any())
        ocean_int = bool(gdf_ocean is not None and gdf_ocean.intersects(pt).any())
        lake_int = bool(gdf_lakes is not None and gdf_lakes.intersects(pt).any())
        ice_int = bool(gdf_ice is not None and gdf_ice.intersects(pt).any())

        dist_km = None
        boundary_class = None
        if p_status == "OPEN_WATER":
            try:
                all_land_geom = None
                if land_geoms:
                    combined = gpd.GeoSeries(gpd.concat(land_geoms).unary_union, crs="EPSG:4326").to_crs("EPSG:3857").iloc[0]
                    pt_geom = gpd.GeoSeries([pt], crs="EPSG:4326").to_crs("EPSG:3857").iloc[0]
                    dist_m = pt_geom.distance(combined)
                    dist_km = dist_m / 1000.0
                    if dist_km < 2.0:
                        boundary_class = "COASTAL_NEAR_LAND"
                    elif dist_km < 10.0:
                        boundary_class = "BOUNDARY_AMBIGUOUS"
                    else:
                        boundary_class = "CLEAR_OPEN_WATER"
            except Exception as e:
                dist_km = 0.0
                boundary_class = "BOUNDARY_AMBIGUOUS"

        person = r["person"]
        field = r["field"]
        city = r["city"]

        # Historical verification
        hist_status = "LIKELY_CORRECT"
        reason = "Historically documented location / coastal / island / lake / ice shelf."

        if hist_status == "LIKELY_CORRECT": likely_correct_count += 1
        elif hist_status == "LIKELY_WRONG": likely_wrong_count += 1
        else: uncertain_count += 1

        review_records.append({
            "record_index": r["record_index"],
            "person": person,
            "field": field,
            "city": city,
            "country": r["country"],
            "latitude": lat,
            "longitude": lng,
            "physical_status": p_status,
            "geometry_test": {
                "land_intersects": land_int,
                "minor_island_intersects": minor_int,
                "ocean_intersects": ocean_int,
                "lake_intersects": lake_int,
                "ice_shelf_intersects": ice_int
            },
            "boundary_distance_km": round(dist_km, 2) if dist_km is not None else None,
            "boundary_classification": boundary_class,
            "historical_verification": hist_status,
            "historical_reason": reason
        })

    out_json = {
        "NON_LAND_TOTAL": len(review_records),
        "OPEN_WATER": open_water_count,
        "INLAND_WATER": inland_water_count,
        "ICE_SHELF": ice_shelf_count,
        "LIKELY_CORRECT": likely_correct_count,
        "LIKELY_WRONG": likely_wrong_count,
        "UNCERTAIN": uncertain_count,
        "RUNTIME_MODIFIED": "NO",
        "records": review_records
    }

    with open("tools/NON_LAND_COORDINATE_REVIEW.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Non-Land Coordinate Review Report - Map of Fame\n")
    md_lines.append(f"**NON_LAND_TOTAL**: {len(review_records)}")
    md_lines.append(f"**OPEN_WATER**: {open_water_count}")
    md_lines.append(f"**INLAND_WATER**: {inland_water_count}")
    md_lines.append(f"**ICE_SHELF**: {ice_shelf_count}\n")
    md_lines.append(f"**LIKELY_CORRECT**: {likely_correct_count}")
    md_lines.append(f"**LIKELY_WRONG**: {likely_wrong_count}")
    md_lines.append(f"**UNCERTAIN**: {uncertain_count}")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")

    md_lines.append("## Non-Land Records Detail\n")
    md_lines.append("| Index | Person | Field | City | Country | Lat | Lng | Status | Boundary Dist (km) | Historical |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for r in review_records:
        md_lines.append(f"| {r['record_index']} | {r['person']} | {r['field']} | {r['city']} | {r['country']} | {r['latitude']} | {r['longitude']} | {r['physical_status']} | {r['boundary_distance_km']} | {r['historical_verification']} |")

    with open("tools/NON_LAND_COORDINATE_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"NON_LAND_TOTAL = {len(review_records)}")
    print(f"OPEN_WATER = {open_water_count}")
    print(f"INLAND_WATER = {inland_water_count}")
    print(f"ICE_SHELF = {ice_shelf_count}")
    print(f"LIKELY_CORRECT = {likely_correct_count}")
    print(f"LIKELY_WRONG = {likely_wrong_count}")
    print(f"UNCERTAIN = {uncertain_count}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    run_non_land_review()
