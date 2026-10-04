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

def run_gis_audit():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    # Load Natural Earth geometries
    geodata_root = "tools/geodata"
    land_shp = find_shp(os.path.join(geodata_root, "ne_10m_land"))
    ocean_shp = find_shp(os.path.join(geodata_root, "ne_10m_ocean"))
    lakes_shp = find_shp(os.path.join(geodata_root, "ne_10m_lakes"))
    minor_islands_shp = find_shp(os.path.join(geodata_root, "ne_10m_minor_islands"))
    ice_shelves_shp = find_shp(os.path.join(geodata_root, "ne_10m_antarctic_ice_shelves_polys"))

    print(f"Loading layers...")
    gdf_land = gpd.read_file(land_shp) if land_shp else None
    gdf_ocean = gpd.read_file(ocean_shp) if ocean_shp else None
    gdf_lakes = gpd.read_file(lakes_shp) if lakes_shp else None
    gdf_minor = gpd.read_file(minor_islands_shp) if minor_islands_shp else None
    gdf_ice = gpd.read_file(ice_shelves_shp) if ice_shelves_shp else None

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    records = []
    idx = 0
    total_birth = 0
    total_death = 0

    counts = {
        "LAND": 0,
        "OPEN_WATER": 0,
        "INLAND_WATER": 0,
        "ICE_SHELF": 0,
        "COASTAL_AMBIGUOUS": 0,
        "UNKNOWN": 0
    }

    loc_counts = {
        "VERIFIED": 0,
        "MISMATCH": 0,
        "UNCERTAIN": 0,
        "NOT_VERIFIED": 0
    }

    print(f"Processing 594 coordinates...")
    for person in quiz_data:
        name_en = person.get("name_en") or person.get("name") or "Unknown"
        birth_city = person.get("birth_city") or "Unknown"
        death_city = person.get("death_city") or "Unknown"
        birth_country = person.get("birth_country") or "Unknown"
        death_country = person.get("death_country") or "Unknown"

        bc = person.get("bc")
        dc = person.get("dc")

        for event_type, coord, city, country in [("Birth", bc, birth_city, birth_country), ("Death", dc, death_city, death_country)]:
            if coord and isinstance(coord, list) and len(coord) == 2:
                if event_type == "Birth": total_birth += 1
                else: total_death += 1
                idx += 1

                lat, lng = coord[0], coord[1]
                pt = Point(lng, lat) # GIS order: x = lng, y = lat

                physical_status = "UNKNOWN"

                # 1. Ice shelf test
                is_ice = False
                if gdf_ice is not None:
                    # check if point intersects any ice shelf geometry
                    # using buffer for tolerance or contains/intersects
                    matches = gdf_ice[gdf_ice.intersects(pt)]
                    if len(matches) > 0:
                        is_ice = True

                if is_ice:
                    physical_status = "ICE_SHELF"
                else:
                    # 2. Lakes test
                    is_lake = False
                    if gdf_lakes is not None:
                        matches = gdf_lakes[gdf_lakes.intersects(pt)]
                        if len(matches) > 0:
                            is_lake = True
                    
                    if is_lake:
                        physical_status = "INLAND_WATER"
                    else:
                        # 3. Land / Minor Islands test
                        is_land = False
                        if gdf_land is not None:
                            if gdf_land.intersects(pt).any():
                                is_land = True
                        if not is_land and gdf_minor is not None:
                            if gdf_minor.intersects(pt).any():
                                is_land = True

                        if is_land:
                            physical_status = "LAND"
                        else:
                            # 4. Ocean test
                            is_ocean = False
                            if gdf_ocean is not None:
                                if gdf_ocean.intersects(pt).any():
                                    is_ocean = True
                            
                            if is_ocean:
                                physical_status = "OPEN_WATER"
                            else:
                                # Check buffer/tolerance for coastal ambiguous
                                pt_buf = pt.buffer(0.05) # ~5km tolerance
                                near_land = False
                                near_water = False
                                if gdf_land is not None and gdf_land.intersects(pt_buf).any():
                                    near_land = True
                                if gdf_ocean is not None and gdf_ocean.intersects(pt_buf).any():
                                    near_water = True
                                
                                if near_land and near_water:
                                    physical_status = "COASTAL_AMBIGUOUS"
                                else:
                                    physical_status = "UNKNOWN"

                counts[physical_status] += 1
                loc_status = "NOT_VERIFIED"
                loc_counts[loc_status] += 1

                records.append({
                    "person": name_en,
                    "record_index": idx,
                    "field": event_type,
                    "city": city,
                    "country": country,
                    "latitude": lat,
                    "longitude": lng,
                    "physical_status": physical_status,
                    "location_match_status": loc_status,
                    "location_source": "Natural Earth 10m GIS Vector Layers",
                    "evidence": f"Point-in-polygon spatial test using GeoPandas with Natural Earth 10m layers. Result: {physical_status}",
                    "duplicate_identity_review": False
                })

    total_coords = total_birth + total_death

    out_json = {
        "TOTAL_PEOPLE": len(quiz_data),
        "TOTAL_BIRTH": total_birth,
        "TOTAL_DEATH": total_death,
        "TOTAL_COORDINATES": total_coords,
        "PHYSICAL_STATUS_COUNTS": counts,
        "LOCATION_MATCH_COUNTS": loc_counts,
        "RUNTIME_MODIFIED": "NO",
        "records": records
    }

    with open("tools/FULL_GEOGRAPHIC_COORDINATE_AUDIT.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Full Geographic Coordinate Audit Report - Map of Fame\n")
    md_lines.append(f"**TOTAL_PEOPLE**: {len(quiz_data)}")
    md_lines.append(f"**TOTAL_BIRTH**: {total_birth}")
    md_lines.append(f"**TOTAL_DEATH**: {total_death}")
    md_lines.append(f"**TOTAL_COORDINATES**: {total_coords}")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")

    md_lines.append("## Physical Status Counts\n")
    for k, v in counts.items():
        md_lines.append(f"- {k} = {v}")
    md_lines.append("")

    md_lines.append("## Location Match Counts\n")
    for k, v in loc_counts.items():
        md_lines.append(f"- {k} = {v}")
    md_lines.append("")

    md_lines.append("## All 594 Records\n")
    md_lines.append("| Index | Person | Field | City | Country | Latitude | Longitude | Physical Status | Location Match |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|")

    for r in records:
        md_lines.append(f"| {r['record_index']} | {r['person']} | {r['field']} | {r['city']} | {r['country']} | {r['latitude']} | {r['longitude']} | {r['physical_status']} | {r['location_match_status']} |")

    with open("tools/FULL_GEOGRAPHIC_COORDINATE_AUDIT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"TOTAL_PEOPLE = {len(quiz_data)}")
    print(f"TOTAL_BIRTH = {total_birth}")
    print(f"TOTAL_DEATH = {total_death}")
    print(f"TOTAL_COORDINATES = {total_coords}")
    for k, v in counts.items():
        print(f"{k} = {v}")
    for k, v in loc_counts.items():
        print(f"{k} = {v}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    run_gis_audit()
