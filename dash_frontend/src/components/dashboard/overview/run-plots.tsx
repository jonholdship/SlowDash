'use client';

import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import { alpha, useTheme } from '@mui/material/styles';
import type { SxProps } from '@mui/material/styles';
import Grid from '@mui/material/Unstable_Grid2';
import type { ApexOptions } from 'apexcharts';
import { AuthError, getHrZones, getPlots, getUserSettings } from '@/api/api-call';
import { Chart } from '@/components/core/chart';
import type { HrZoneBand } from '@/types/hr-zones';
import { useEffect, useState } from 'react';

export interface PlotProps {
  chartSeries: { seriesName: string; data: { x: any, y: number }[] }[];
  /** When set, draws a horizontal band on the y-axis (heart rate plots only). */
  hrZoneBand?: HrZoneBand | null;
  sx?: SxProps;
}

// This is a client component that gets the auth token
export default function RunPlotWrapper() {
  const [isLoading, setIsLoading] = useState(true);
  const [plotData, setPlotData] = useState<any>(null);
  const [hrZoneBand, setHrZoneBand] = useState<HrZoneBand | null>(null);

  useEffect(() => {
    const loadPlots = async () => {
      try {
        const plots = await getPlots();
        setPlotData(plots);
      } catch (err) {
        if (err instanceof AuthError) {
          // Treat as unauthenticated – server component will show an auth message
          setPlotData(null);
          setHrZoneBand(null);
          return;
        }
        console.error('Failed to load plots', err);
        setPlotData(null);
        setHrZoneBand(null);
      } finally {
        setIsLoading(false);
      }
    };

    void loadPlots();
  }, []);

  useEffect(() => {
    if (!plotData) {
      setHrZoneBand(null);
      return;
    }
    let cancelled = false;
    void (async () => {
      try {
        const [settings, zones] = await Promise.all([getUserSettings(), getHrZones()]);
        if (cancelled) return;
        const highlight = settings.hr_zone_highlight ?? 3;
        const zone = zones.zones.find((z) => z.id === highlight) ?? null;
        setHrZoneBand(zone);
      } catch (err) {
        if (err instanceof AuthError) {
          setHrZoneBand(null);
          return;
        }
        console.error('Failed to load HR zone highlight', err);
        setHrZoneBand(null);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [plotData]);

  if (isLoading) {
    return <div>Loading plots...</div>;
  }

  return <RunPlotGridServer hrZoneBand={hrZoneBand} plotData={plotData} />;
}

// This is a server component that uses the token
function RunPlotGridServer({
  plotData,
  hrZoneBand,
}: {
  plotData: any;
  hrZoneBand: HrZoneBand | null;
}) {
  if (!plotData) {
    return <div>Authentication required</div>;
  }

  return (
    <Grid container spacing={3}>
      <Grid lg={12} xl={6} xs={12}>
        <RunPlot chartSeries={[{ seriesName: 'Pace', data: plotData.pace_plot }]} />
      </Grid>
      <Grid lg={12} xl={6} xs={12}>
        <RunPlot chartSeries={[{ seriesName: 'HR', data: plotData.hr_plot }]} hrZoneBand={hrZoneBand} />
      </Grid>
    </Grid>
  );
}

function RunPlot({ chartSeries, hrZoneBand, sx }: PlotProps): React.JSX.Element {
  const chartOptions = useChartOptions(hrZoneBand);
  return (
    <Card sx={{ overflow: 'visible', ...sx }}>
      <CardHeader title={chartSeries[0].seriesName} />
      <CardContent sx={{ overflow: 'visible', '&:last-child': { paddingBottom: '20px' } }}>
        <Chart height={420} options={chartOptions} series={chartSeries} type="line" width="100%" />
      </CardContent>
    </Card>
  );
}

function useChartOptions(hrZoneBand?: HrZoneBand | null): ApexOptions {
  const theme = useTheme();

  // Never set `annotations: undefined` — ApexCharts' merge assigns that onto the config and
  // later code expects `w.config.annotations.images` to exist.
  return {
    ...(hrZoneBand != null
      ? {
          annotations: {
            yaxis: [
              {
                y: hrZoneBand.min_bpm,
                y2: hrZoneBand.max_bpm,
                fillColor: alpha(theme.palette.primary.main, 0.14),
                borderColor: alpha(theme.palette.primary.main, 0.4),
                borderWidth: 1,
                opacity: 1,
              },
            ],
          },
        }
      : {}),
    chart: {
      background: 'transparent',
      redrawOnParentResize: true,
      stacked: false,
      toolbar: { show: false },
    },
    colors: [theme.palette.primary.main, alpha(theme.palette.primary.main, 0.25)],
    dataLabels: { enabled: false },
    fill: { opacity: 1, type: 'solid' },
    grid: {
      borderColor: theme.palette.divider,
      padding: { bottom: 28, left: 8, right: 16, top: 8 },
      strokeDashArray: 2,
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } },
    },
    legend: { show: false },
    plotOptions: { bar: { columnWidth: '40px' } },
    stroke: { colors: [theme.palette.primary.main], show: true, width: 2 },
    theme: { mode: theme.palette.mode },
    xaxis: {
      type: 'datetime',
      axisBorder: { color: theme.palette.divider, show: true },
      axisTicks: { color: theme.palette.divider, show: true },
      labels: { offsetY: 5, style: { colors: theme.palette.text.secondary } },
    },
    yaxis: {
      labels: {
        offsetX: -10,
        style: { colors: theme.palette.text.secondary },
      },
      decimalsInFloat: 1,
    },
  };
}
