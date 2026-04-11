#!/usr/bin/env python3
from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / 'data'
DB_PATH = DATA_DIR / 'collected.db'
OUTPUT_PATH = BASE / 'index.html'
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            station_id TEXT NOT NULL,
            station_name TEXT,
            temperature REAL,
            precipitation REAL,
            UNIQUE(timestamp, station_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS train_announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id TEXT NOT NULL,
            location TEXT NOT NULL,
            activity_type TEXT,
            advertised_time TEXT,
            estimated_time TEXT,
            time_deviation_minutes REAL,
            collected_at TEXT NOT NULL,
            UNIQUE(train_id, location, advertised_time, activity_type)
        )
    """)
    conn.commit()
    conn.close()


def collect_weather():
    lat, lon = 57.7210, 12.9401
    url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={lat}&longitude={lon}'
        '&hourly=temperature_2m,precipitation'
        '&forecast_days=2'
        '&timezone=Europe%2FStockholm'
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    hourly = data.get('hourly', {})
    conn = get_db()
    c = conn.cursor()
    for ts, temp, prec in zip(hourly.get('time', []), hourly.get('temperature_2m', []), hourly.get('precipitation', [])):
        c.execute(
            'INSERT OR IGNORE INTO weather (timestamp, station_id, station_name, temperature, precipitation) VALUES (?, ?, ?, ?, ?)',
            (ts, 'open-meteo-boras', 'Borås', temp, prec),
        )
    conn.commit()
    conn.close()


def collect_trains():
    api_key = os.environ.get('TRAFIKVERKET_API_KEY', '').strip()
    if not api_key:
        return
    modified_time = (datetime.utcnow() - timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')
    request = f'''<?xml version="1.0" encoding="UTF-8"?>
<REQUEST>
    <LOGIN authenticationkey="{api_key}"/>
    <QUERY objecttype="TRAINANNOUNCEMENT" schemaversion="1">
        <FILTER>
            <GT name="ModifiedTime" value="{modified_time}"/>
        </FILTER>
    </QUERY>
</REQUEST>'''
    r = requests.post('https://api.trafikinfo.trafikverket.se/v2/data.json', data=request.encode('utf-8'), headers={'Content-Type': 'application/xml'}, timeout=60)
    r.raise_for_status()
    data = r.json()
    conn = get_db()
    c = conn.cursor()
    for result in data.get('RESPONSE', {}).get('RESULT', []):
        for train in result.get('TrainAnnouncement', []):
            train_id = train.get('ActivityId', '')
            location = train.get('LocationSignature', '')
            activity_type = train.get('ActivityType', '')
            advertised = train.get('AdvertisedTimeAtLocation', '')
            estimated = train.get('EstimatedTimeAtLocation', '')
            deviation = 0.0
            if advertised and estimated:
                try:
                    adv = datetime.fromisoformat(advertised.replace('Z', '+00:00'))
                    est = datetime.fromisoformat(estimated.replace('Z', '+00:00'))
                    deviation = (est - adv).total_seconds() / 60.0
                except Exception:
                    pass
            c.execute(
                'INSERT OR IGNORE INTO train_announcements (train_id, location, activity_type, advertised_time, estimated_time, time_deviation_minutes, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (train_id, location, activity_type, advertised, estimated, deviation, datetime.utcnow().isoformat()),
            )
    conn.commit()
    conn.close()


def get_stats():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stats = {}
    c.execute("SELECT COUNT(*) total, MAX(collected_at) latest, COUNT(DISTINCT location) stations, AVG(time_deviation_minutes) avg_delay, MAX(time_deviation_minutes) max_delay, SUM(CASE WHEN time_deviation_minutes > 2 THEN 1 ELSE 0 END) delayed_trains, COUNT(DISTINCT train_id) unique_trains FROM train_announcements")
    train = c.fetchone()
    total = train['total'] or 0
    stats['trains'] = {
        'total': total,
        'latest': train['latest'] or '',
        'stations': train['stations'] or 0,
        'avg_delay': round(train['avg_delay'], 1) if train['avg_delay'] else 0,
        'max_delay': round(train['max_delay'], 1) if train['max_delay'] else 0,
        'delayed_trains': train['delayed_trains'] or 0,
        'unique_trains': train['unique_trains'] or 0,
        'on_time_pct': round(100 - (train['delayed_trains'] or 0) / total * 100, 1) if total > 0 else 100,
    }
    c.execute("SELECT DATE(timestamp) as date, MIN(temperature) min_temp, MAX(temperature) max_temp, AVG(temperature) avg_temp FROM weather WHERE timestamp >= DATE('now', '-7 days') GROUP BY DATE(timestamp) ORDER BY date")
    history = [{'date': row['date'][5:], 'min': round(row['min_temp'],1), 'max': round(row['max_temp'],1), 'avg': round(row['avg_temp'],1)} for row in c.fetchall()]
    c.execute("SELECT COUNT(*) total, MAX(timestamp) latest, AVG(temperature) avg_temp, MAX(temperature) max_temp, MIN(temperature) min_temp FROM weather")
    weather = c.fetchone()
    stats['weather'] = {
        'total': weather['total'] or 0,
        'latest': weather['latest'] or '',
        'avg_temp': round(weather['avg_temp'], 1) if weather['avg_temp'] else 0,
        'max_temp': round(weather['max_temp'], 1) if weather['max_temp'] else 0,
        'min_temp': round(weather['min_temp'], 1) if weather['min_temp'] else 0,
        'history': history,
    }
    conn.close()
    return stats


def render(stats):
    html = f'''<!DOCTYPE html>
<html lang="sv"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Data Dashboard</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;padding:20px}}.container{{max-width:1100px;margin:0 auto}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}.card{{background:#1e293b;border-radius:12px;padding:20px}}.label{{color:#94a3b8;font-size:.85rem}}.value{{font-size:1.6rem;font-weight:700;margin-top:6px}}</style></head>
<body><div class="container"><h1>Data Dashboard</h1><p>Senast uppdaterad: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p><div class="grid">
<div class="card"><h2>Tåg</h2><div class="label">Poster</div><div class="value">{stats['trains']['total']}</div><div class="label">Stationer</div><div class="value">{stats['trains']['stations']}</div><div class="label">Försenade tåg</div><div class="value">{stats['trains']['delayed_trains']}</div><div class="label">I tid</div><div class="value">{stats['trains']['on_time_pct']}%</div></div>
<div class="card"><h2>Väder Borås</h2><div class="label">Medeltemp</div><div class="value">{stats['weather']['avg_temp']}°</div><div class="label">Högsta</div><div class="value">{stats['weather']['max_temp']}°</div><div class="label">Lägsta</div><div class="value">{stats['weather']['min_temp']}°</div><div class="label">Antal mätpunkter</div><div class="value">{stats['weather']['total']}</div></div>
</div></div></body></html>'''
    OUTPUT_PATH.write_text(html, encoding='utf-8')


def main():
    init_db()
    collect_weather()
    collect_trains()
    render(get_stats())


if __name__ == '__main__':
    main()
