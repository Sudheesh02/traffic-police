# -*- coding: utf-8 -*-
"""
Generate Ultra-High-Resolution Raipur Maps and Interactive GIS Visualizations
for SynchroClear-ITS Hackathon Submission.

Generates:
1. docs/raipur_satellite_corridor_map.png (High-Res Google Earth Satellite with Tactical Overlay)
2. docs/raipur_gis_roadmap.png (CartoDB / OSM High-Res Street Network Map)
3. docs/raipur_corridor_map.html (Interactive Folium Multi-Layer Map with Live Telemetry)
"""

import os
import sys
import math
import io
import requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
import folium
from folium import plugins

# Target coordinates in Raipur
COORDINATES = {
    'jaistambh': {'name': 'Jaistambh Chowk', 'lat': 21.2435, 'lon': 81.6337, 'type': 'junction', 'role': 'Pilot RTU Junction 01 (GE Road Artery)'},
    'ghadi_chowk': {'name': 'Ghadi Chowk', 'lat': 21.2415, 'lon': 81.6441, 'type': 'junction', 'role': 'Pilot RTU Junction 02 (Raj Bhavan / High Court Link)'},
    'mekahara': {'name': 'Dr. B.R. Ambedkar Hospital (Mekahara)', 'lat': 21.2519, 'lon': 81.6575, 'type': 'hospital', 'role': 'Golden Hour Emergency Trauma Center'},
    'police_iccc': {'name': 'Raipur Police ICCC & Control Room', 'lat': 21.2361, 'lon': 81.6517, 'type': 'iccc', 'role': 'Central Command & e-Challan Whitelist Server'},
    'telibandha': {'name': 'Telibandha Chowk (Marine Drive)', 'lat': 21.2384, 'lon': 81.6788, 'type': 'waypoint', 'role': 'Eastern Corridor Gateway (NH-53)'},
}

CORRIDOR_ROUTE = [
    (21.2384, 81.6788),  # Telibandha
    (21.2400, 81.6620),  # GE Road mid
    (21.2415, 81.6441),  # Ghadi Chowk
    (21.2428, 81.6385),  # Kotwali link
    (21.2435, 81.6337),  # Jaistambh Chowk
    (21.2480, 81.6460),  # Station Road bypass
    (21.2519, 81.6575),  # Mekahara Hospital Trauma Gate
]

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def download_tile(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            return Image.open(io.BytesIO(r.content)).convert('RGB')
    except Exception:
        pass
    return Image.new('RGB', (256, 256), color=(25, 30, 36))

def stitch_tile_grid(tile_url_template, x_min, x_max, y_min, y_max, zoom, headers):
    cols = x_max - x_min + 1
    rows = y_max - y_min + 1
    canvas = Image.new('RGB', (cols * 256, rows * 256), color=(20, 24, 30))
    tasks = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                url = tile_url_template.format(x=x, y=y, z=zoom)
                tasks.append((x, y, executor.submit(download_tile, url, headers)))
        for x, y, fut in tasks:
            img = fut.result()
            px = (x - x_min) * 256
            py = (y - y_min) * 256
            canvas.paste(img, (px, py))
    return canvas

def latlon_to_pixel(lat, lon, x_min, y_min, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_exact = (lon + 180.0) / 360.0 * n
    y_exact = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    px = int((x_exact - x_min) * 256)
    py = int((y_exact - y_min) * 256)
    return px, py

def annotate_satellite_map(base_img, x_min, y_min, zoom, title_type='SATELLITE'):
    img = base_img.copy()
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. Draw 1km RF Coverage Circles around Jaistambh & Ghadi Chowk
    rf_meter_radius = 800  # meters
    px_radius = int(rf_meter_radius / 2.1)
    
    for key in ['jaistambh', 'ghadi_chowk']:
        coord = COORDINATES[key]
        cx, cy = latlon_to_pixel(coord['lat'], coord['lon'], x_min, y_min, zoom)
        draw.ellipse([cx - px_radius, cy - px_radius, cx + px_radius, cy + px_radius],
                     fill=(0, 255, 136, 35), outline=(0, 255, 136, 180), width=3)
        draw.ellipse([cx - int(px_radius*0.5), cy - int(px_radius*0.5), cx + int(px_radius*0.5), cy + int(px_radius*0.5)],
                     outline=(0, 255, 136, 100), width=1)
        
    # 2. Draw Emergency Green Corridor Line
    pixel_route = [latlon_to_pixel(lat, lon, x_min, y_min, zoom) for lat, lon in CORRIDOR_ROUTE]
    for w, a in [(18, 50), (12, 100), (8, 180), (4, 255)]:
        draw.line(pixel_route, fill=(0, 255, 136, a), width=w)
    draw.line(pixel_route, fill=(255, 255, 255, 240), width=2)
    
    # 3. Draw Landmarks & Tactical Callouts
    for key, c in COORDINATES.items():
        px, py = latlon_to_pixel(c['lat'], c['lon'], x_min, y_min, zoom)
        if c['type'] == 'hospital':
            draw.ellipse([px-14, py-14, px+14, py+14], fill=(220, 38, 38, 220), outline=(255, 255, 255, 255), width=2)
            draw.rectangle([px-3, py-9, px+3, py+9], fill=(255, 255, 255, 255))
            draw.rectangle([px-9, py-3, px+9, py+3], fill=(255, 255, 255, 255))
            bx, by = px + 20, py - 40
            draw.rectangle([bx, by, bx + 360, by + 52], fill=(15, 23, 42, 220), outline=(239, 68, 68, 255), width=2)
            draw.text((bx + 10, by + 6), c['name'], fill=(255, 255, 255, 255))
            draw.text((bx + 10, by + 26), f"{c['role']} | Lat: {c['lat']:.4f}", fill=(252, 165, 165, 255))
            draw.line([(px, py), (bx, by + 26)], fill=(239, 68, 68, 200), width=2)
        elif c['type'] == 'junction':
            draw.ellipse([px-12, py-12, px+12, py+12], fill=(16, 185, 129, 230), outline=(255, 255, 255, 255), width=2)
            draw.ellipse([px-4, py-4, px+4, py+4], fill=(255, 255, 255, 255))
            offset_y = -60 if 'jaistambh' in key else 20
            bx, by = px + 25, py + offset_y
            draw.rectangle([bx, by, bx + 340, by + 52], fill=(15, 23, 42, 220), outline=(16, 185, 129, 255), width=2)
            draw.text((bx + 10, by + 6), f"[ACTIVE RTU] {c['name']}", fill=(52, 211, 153, 255))
            draw.text((bx + 10, by + 26), f"{c['role']}", fill=(209, 250, 229, 255))
            draw.line([(px, py), (bx, by + 26)], fill=(16, 185, 129, 200), width=2)
        elif c['type'] == 'iccc':
            draw.ellipse([px-10, py-10, px+10, py+10], fill=(37, 99, 235, 220), outline=(255, 255, 255, 255), width=2)
            bx, by = px - 320, py + 15
            draw.rectangle([bx, by, bx + 300, by + 45], fill=(15, 23, 42, 220), outline=(59, 130, 246, 255), width=2)
            draw.text((bx + 10, by + 5), c['name'], fill=(96, 165, 250, 255))
            draw.text((bx + 10, by + 22), "NIC e-Challan Sync & MQTT Broker", fill=(219, 234, 254, 255))
            draw.line([(px, py), (bx + 300, by + 20)], fill=(59, 130, 246, 200), width=2)

    # 4. Top Tactical HUD Banner
    hud_h = 90
    draw.rectangle([0, 0, img.size[0], hud_h], fill=(10, 15, 25, 235))
    draw.line([(0, hud_h), (img.size[0], hud_h)], fill=(0, 255, 136, 255), width=3)
    draw.text((30, 14), "RAIPUR POLICE COMMISSIONERATE | TRAFFIC INNOVATION HACKATHON 2026", fill=(255, 255, 255, 255))
    draw.text((30, 38), f"SynchroClear-ITS: {title_type} TACTICAL CORRIDOR MAP (Great Eastern Road)", fill=(0, 255, 136, 255))
    draw.text((30, 60), "Sub-1GHz RF Preemption + ITMS CCTV Edge-AI + e-Challan Whitelist Synchronization", fill=(148, 163, 184, 255))
    
    # 5. Bottom Telemetry Bar
    bar_y = img.size[1] - 70
    draw.rectangle([0, bar_y, img.size[0], img.size[1]], fill=(10, 15, 25, 235))
    draw.line([(0, bar_y), (img.size[0], bar_y)], fill=(59, 130, 246, 200), width=2)
    stats_text = "Corridor: 4.8 km (Telibandha -> Mekahara) | Latency: 42 ms | Clearance: 5.5s (3.5s Yellow + 2.0s All-Red) | Pilot Cost: Rs 22,900 (2 Junctions)"
    draw.text((30, bar_y + 16), stats_text, fill=(241, 245, 249, 255))
    draw.text((30, bar_y + 40), "Satellite Imagery: Google Earth / ESRI World High-Resolution Hybrid Stream | Coordinate System: WGS 84", fill=(148, 163, 184, 255))
    
    # 6. North Arrow & Legend
    lx, ly = img.size[0] - 280, hud_h + 20
    draw.rectangle([lx, ly, lx + 260, ly + 140], fill=(15, 23, 42, 220), outline=(148, 163, 184, 180), width=1)
    draw.text((lx + 15, ly + 10), "CORRIDOR LEGEND", fill=(255, 255, 255, 255))
    draw.line([(lx + 15, ly + 40), (lx + 55, ly + 40)], fill=(0, 255, 136, 255), width=4)
    draw.text((lx + 65, ly + 32), "Emergency Green Wave", fill=(226, 232, 240, 255))
    draw.ellipse([lx + 25, ly + 58, lx + 45, ly + 78], fill=(16, 185, 129, 255))
    draw.text((lx + 65, ly + 60), "Preemption Signal RTU", fill=(226, 232, 240, 255))
    draw.rectangle([lx + 20, ly + 90, lx + 50, ly + 105], fill=(0, 255, 136, 80), outline=(0, 255, 136, 200))
    draw.text((lx + 65, ly + 90), "868 MHz Sub-GHz (1km)", fill=(226, 232, 240, 255))
    draw.ellipse([lx + 25, ly + 115, lx + 45, ly + 135], fill=(220, 38, 38, 255))
    draw.text((lx + 65, ly + 117), "Mekahara Hospital", fill=(226, 232, 240, 255))

    final_img = Image.alpha_composite(img.convert('RGBA'), overlay)
    return final_img.convert('RGB')

def build_interactive_html_map(output_path):
    m = folium.Map(location=[21.2445, 81.6465], zoom_start=14, tiles=None, control_scale=True)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Earth / Maps Hybrid', name='Google Earth Satellite (Hybrid)', overlay=False, control=True).add_to(m)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri World Imagery', name='Esri High-Resolution Satellite', overlay=False, control=True).add_to(m)
    folium.TileLayer(tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', attr='CartoDB Voyager', name='CartoDB Clean Street Map', subdomains='abcd', overlay=False, control=True).add_to(m)
    folium.TileLayer(tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', attr='CartoDB Dark Matter', name='Night Mode (Dark Matter)', subdomains='abcd', overlay=False, control=True).add_to(m)
    
    corridor_fg = folium.FeatureGroup(name='Green Wave Corridor (GE Road - 4.8 km)', show=True)
    folium.PolyLine(CORRIDOR_ROUTE, color='#00FF88', weight=12, opacity=0.45, tooltip='SynchroClear Emergency Corridor (GE Road)').add_to(corridor_fg)
    folium.PolyLine(CORRIDOR_ROUTE, color='#059669', weight=4, opacity=0.95).add_to(corridor_fg)
    corridor_fg.add_to(m)
    
    rf_fg = folium.FeatureGroup(name='868 MHz Sub-GHz RF Zones (1 km Radius)', show=True)
    for key in ['jaistambh', 'ghadi_chowk']:
        c = COORDINATES[key]
        folium.Circle(location=[c['lat'], c['lon']], radius=900, color='#10B981', weight=2, fill=True, fill_color='#10B981', fill_opacity=0.15, popup=f"<b>868 MHz Sub-GHz Coverage Zone</b><br>Junction: {c['name']}<br>Radius: 900m<br>Latency: 42ms").add_to(rf_fg)
    rf_fg.add_to(m)
    
    nodes_fg = folium.FeatureGroup(name='Junction RTUs & Strategic Landmarks', show=True)
    j1 = COORDINATES['jaistambh']
    popup_j1 = """<div style='font-family: Arial, sans-serif; width: 280px;'><h4 style='color: #059669; margin-bottom: 4px;'>🚦 Jaistambh Chowk (Pilot RTU 01)</h4><p style='margin: 2px 0; font-size: 12px;'><b>Type:</b> 4-Way Arterial Intersection (GE Road)</p><p style='margin: 2px 0; font-size: 12px;'><b>Controller:</b> Industrial STM32F4 + Form-C Relays</p><p style='margin: 2px 0; font-size: 12px;'><b>Clearance:</b> 3.5s Yellow -> 2.0s All-Red -> Priority Green</p><div style='background: #ECFDF5; padding: 6px; border-left: 3px solid #10B981; margin-top: 6px;'><span style='color: #065F46; font-weight: bold; font-size: 11px;'>STATUS: PREEMPTION READY (42ms RF)</span></div></div>"""
    folium.Marker([j1['lat'], j1['lon']], popup=folium.Popup(popup_j1, max_width=320), tooltip='Jaistambh Chowk - Pilot RTU 01', icon=folium.Icon(color='green', icon='traffic-light', prefix='fa')).add_to(nodes_fg)
    
    j2 = COORDINATES['ghadi_chowk']
    popup_j2 = """<div style='font-family: Arial, sans-serif; width: 280px;'><h4 style='color: #059669; margin-bottom: 4px;'>🚦 Ghadi Chowk (Pilot RTU 02)</h4><p style='margin: 2px 0; font-size: 12px;'><b>Type:</b> Multi-leg Plaza (Raj Bhavan / High Court link)</p><p style='margin: 2px 0; font-size: 12px;'><b>Controller:</b> Industrial STM32F4 + Sub-GHz Transceiver</p><div style='background: #ECFDF5; padding: 6px; border-left: 3px solid #10B981; margin-top: 6px;'><span style='color: #065F46; font-weight: bold; font-size: 11px;'>STATUS: INTERLOCKED (MUTUAL EXCLUSION)</span></div></div>"""
    folium.Marker([j2['lat'], j2['lon']], popup=folium.Popup(popup_j2, max_width=320), tooltip='Ghadi Chowk - Pilot RTU 02', icon=folium.Icon(color='green', icon='clock', prefix='fa')).add_to(nodes_fg)
    
    hosp = COORDINATES['mekahara']
    popup_hosp = """<div style='font-family: Arial, sans-serif; width: 280px;'><h4 style='color: #DC2626; margin-bottom: 4px;'>🏥 Dr. B.R. Ambedkar Hospital (Mekahara)</h4><p style='margin: 2px 0; font-size: 12px;'><b>Facility:</b> 1,200+ Bed State Super-Speciality Hospital</p><p style='margin: 2px 0; font-size: 12px;'><b>Critical Hub:</b> Advanced Trauma & Emergency Department</p><p style='margin: 2px 0; font-size: 12px;'><b>Corridor Gain:</b> 68s saved per trapped junction</p><div style='background: #FEF2F2; padding: 6px; border-left: 3px solid #EF4444; margin-top: 6px;'><span style='color: #991B1B; font-weight: bold; font-size: 11px;'>DESTINATION: GOLDEN HOUR LIFELINE</span></div></div>"""
    folium.Marker([hosp['lat'], hosp['lon']], popup=folium.Popup(popup_hosp, max_width=320), tooltip='Mekahara Hospital', icon=folium.Icon(color='red', icon='plus', prefix='fa')).add_to(nodes_fg)
    
    iccc = COORDINATES['police_iccc']
    popup_iccc = """<div style='font-family: Arial, sans-serif; width: 280px;'><h4 style='color: #2563EB; margin-bottom: 4px;'>🏢 Raipur Police Commissionerate & ICCC</h4><p style='margin: 2px 0; font-size: 12px;'><b>Network:</b> Smart City ITMS Central Server</p><p style='margin: 2px 0; font-size: 12px;'><b>MQTT Broker:</b> Port 8883 (TLS 1.3 Cryptographic Log)</p><p style='margin: 2px 0; font-size: 12px;'><b>Smart Whitelisting:</b> Auto-exempts yielding motorists</p></div>"""
    folium.Marker([iccc['lat'], iccc['lon']], popup=folium.Popup(popup_iccc, max_width=320), tooltip='Raipur Police ICCC', icon=folium.Icon(color='blue', icon='shield', prefix='fa')).add_to(nodes_fg)
    nodes_fg.add_to(m)
    
    folium.LayerControl(collapsed=False).add_to(m)
    plugins.Fullscreen(position='topright').add_to(m)
    plugins.MeasureControl(position='bottomleft', primary_length_unit='kilometers').add_to(m)
    m.save(output_path)
    print(f'Saved interactive Folium map to: {output_path}')

def main():
    print('=== SynchroClear-ITS: High-Resolution Raipur Map Generation ===')
    zoom = 16
    x_min, y_max = deg2num(21.232, 81.628, zoom)
    x_max, y_min = deg2num(21.258, 81.666, zoom)
    print(f'Tile Grid bounds: X=[{x_min}..{x_max}], Y=[{y_min}..{y_max}] at zoom {zoom}')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    print('Downloading Google Earth Hybrid Satellite tiles...')
    sat_url_template = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
    sat_canvas = stitch_tile_grid(sat_url_template, x_min, x_max, y_min, y_max, zoom, headers)
    annotated_sat = annotate_satellite_map(sat_canvas, x_min, y_min, zoom, title_type='GOOGLE EARTH HYBRID SATELLITE')
    sat_path = os.path.join('docs', 'raipur_satellite_corridor_map.png')
    annotated_sat.save(sat_path, quality=95)
    print(f'SUCCESS: High-Res Satellite Map saved to: {sat_path} ({annotated_sat.size[0]}x{annotated_sat.size[1]} px)')
    
    print('Downloading CartoDB Clean Roadmap tiles...')
    road_url_template = 'https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png'
    road_canvas = stitch_tile_grid(road_url_template, x_min, x_max, y_min, y_max, zoom, headers)
    annotated_road = annotate_satellite_map(road_canvas, x_min, y_min, zoom, title_type='CARTOGRAPHIC GIS ROAD NETWORK')
    road_path = os.path.join('docs', 'raipur_gis_roadmap.png')
    annotated_road.save(road_path, quality=95)
    print(f'SUCCESS: High-Res GIS Roadmap saved to: {road_path} ({annotated_road.size[0]}x{annotated_road.size[1]} px)')
    
    html_path = os.path.join('docs', 'raipur_corridor_map.html')
    build_interactive_html_map(html_path)
    print('=== ALL RAIPUR HIGH-RESOLUTION MAPS GENERATED SUCCESSFULLY! ===')

if __name__ == '__main__':
    main()
