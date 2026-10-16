'use client';

import 'leaflet/dist/leaflet.css';

import dynamic from 'next/dynamic';

const ValuePerAcreMap = dynamic(() => import('@/components/ValuePerAcreMap'), {
  ssr: false,
});

const BASE_PATH = process.env.NODE_ENV === 'production' ? '/siler-city-budget' : '';

export default function ValuePerAcrePage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Tax Value per Acre</h1>
        <p className="mt-1 text-lg text-gray-600">
          Siler City · Assessed value density by parcel
        </p>
      </div>
      <div className="mb-6 rounded-xl border border-chatham-blue/20 bg-blue-50 p-4 text-sm text-gray-700">
        Parcel colors show total assessed value divided by parcel acreage. Draw a polygon to total the
        assessed value of parcels completely inside it and compare that amount with the mapped Town total.
        Your zoom and map position are preserved while drawing and analyzing. Double-click the final
        point to close and analyze, or use Analyze polygon after placing at least three points.
        Results replace the sketch with purple shading on the exact parcels counted and estimate
        annual Town and County property taxes using the rates shown in the summary.
        Building square footage is not available from the source parcel data.
      </div>
      <ValuePerAcreMap dataUrl={`${BASE_PATH}/data/value_per_acre.geojson`} />
      <p className="mt-4 text-xs text-gray-400">
        Source: Chatham County CAMA Parcels ArcGIS service.
      </p>
    </div>
  );
}
