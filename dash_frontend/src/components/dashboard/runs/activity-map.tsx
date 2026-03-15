'use client';

import * as React from 'react';
import { MapContainer, TileLayer, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { decodePolyline } from '@/utils/polyline';

// Fix default marker icons in Leaflet when using bundlers
delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

interface ActivityMapProps {
  polyline: string | null;
}

function FitBounds({ points }: { points: [number, number][] }) {
  const map = useMap();
  React.useEffect(() => {
    if (points.length === 0) return;
    const bounds = L.latLngBounds(points as L.LatLngExpression[]);
    map.fitBounds(bounds, { padding: [24, 24], maxZoom: 14 });
  }, [map, points]);
  return null;
}

export function ActivityMap({ polyline }: ActivityMapProps) {
  const points = React.useMemo(() => {
    if (!polyline || !polyline.trim()) return [];
    return decodePolyline(polyline);
  }, [polyline]);

  if (points.length === 0) {
    return (
      <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f5f5' }}>
        <span style={{ color: '#666' }}>No route data</span>
      </div>
    );
  }

  const latLngs = points as L.LatLngExpression[];

  return (
    <MapContainer
      center={points[0]}
      zoom={12}
      style={{ height: '100%', width: '100%' }}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Polyline positions={latLngs} color="#1976d2" weight={4} />
      <FitBounds points={points} />
    </MapContainer>
  );
}
