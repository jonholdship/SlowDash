'use client';

import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';
import { alpha, useTheme } from '@mui/material/styles';
import type { SxProps } from '@mui/material/styles';
import type { ApexOptions } from 'apexcharts';
import dynamic from 'next/dynamic';
import Box from '@mui/material/Box';
import { AuthError, getActivity } from '@/api/api-call';
import { Chart } from '@/components/core/chart';
import type { ActivityResponse } from '@/types/activity';

const ActivityMap = dynamic<{ polyline: string | null }>(
  () => import('./activity-map').then((m) => m.ActivityMap),
  { ssr: false, loading: () => <Card sx={{ height: 280, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading map…</Card> }
);

interface RunDetailProps {
  runId: number | null;
}

function streamsToChartData(
  streams: ActivityResponse['streams'],
  xKey: string,
  yKey: string
): { x: number; y: number }[] {
  const xArr = streams[xKey];
  const yArr = streams[yKey];
  if (!xArr || !yArr || xArr.length !== yArr.length) return [];
  return xArr.map((x, i) => ({ x, y: yArr[i] ?? 0 }));
}

export function RunDetail({ runId }: RunDetailProps) {
  const [data, setData] = React.useState<ActivityResponse | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (runId == null) {
      setData(null);
      setError(null);
      return;
    }
    setLoading(true);
    setError(null);
    getActivity(Number(runId))
      .then(setData)
      .catch((err) => {
        if (err instanceof AuthError) {
          setError('Please log in.');
        } else {
          setError(err instanceof Error ? err.message : 'Failed to load activity');
        }
        setData(null);
      })
      .finally(() => setLoading(false));
  }, [runId]);

  if (runId == null) {
    return (
      <Typography color="text.secondary" sx={{ py: 2 }}>
        Select a run to view details.
      </Typography>
    );
  }

  if (loading) {
    return (
      <Typography color="text.secondary" sx={{ py: 2 }}>
        Loading activity…
      </Typography>
    );
  }

  if (error) {
    return (
      <Typography color="error" sx={{ py: 2 }}>
        {error}
      </Typography>
    );
  }

  if (!data) return null;

  const { activity, streams } = data;
  const paceData = streamsToChartData(streams, 'time', 'pace');
  const hrData = streamsToChartData(streams, 'time', 'heartrate');
  const altData = streamsToChartData(streams, 'time', 'altitude');
  const distData = streamsToChartData(streams, 'time', 'distance');

  const dateLabel = activity.start_date
    ? new Date(activity.start_date).toLocaleString(undefined, {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    : '—';

  return (
    <Grid container spacing={3}>
      {/* Top left: map */}
      <Grid xs={12} md={6}>
        <Card sx={{ overflow: 'hidden' }}>
          <Box sx={{ height: 280 }}>
            <ActivityMap polyline={activity.polyline} />
          </Box>
        </Card>
      </Grid>
      {/* Top right: name, description, calories, date */}
      <Grid xs={12} md={6}>
        <Card sx={{ height: 280, display: 'flex', flexDirection: 'column' }}>
          <CardHeader
            title={activity.name ?? 'Unnamed run'}
            subheader={dateLabel}
            titleTypographyProps={{ variant: 'h6' }}
          />
          <CardContent sx={{ flex: 1, overflow: 'auto', pt: 0 }}>
            {activity.description ? (
              <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'pre-wrap', mb: 1 }}>
                {activity.description}
              </Typography>
            ) : null}
            {activity.calories != null ? (
              <Typography variant="body2">
                <strong>Calories:</strong> {Math.round(activity.calories)}
              </Typography>
            ) : null}
          </CardContent>
        </Card>
      </Grid>
      {/* Middle row: pace, heart rate */}
      <Grid xs={12} md={6}>
        <StreamPlot title="Pace (min/km)" seriesName="Pace" data={paceData} />
      </Grid>
      <Grid xs={12} md={6}>
        <StreamPlot title="Heart rate (bpm)" seriesName="HR" data={hrData} />
      </Grid>
      {/* Bottom row: altitude, distance */}
      <Grid xs={12} md={6}>
        <StreamPlot title="Altitude (m)" seriesName="Altitude" data={altData} />
      </Grid>
      <Grid xs={12} md={6}>
        <StreamPlot title="Distance (m)" seriesName="Distance" data={distData} />
      </Grid>
    </Grid>
  );
}

interface StreamPlotProps {
  title: string;
  seriesName: string;
  data: { x: number; y: number }[];
  sx?: SxProps;
}

function StreamPlot({ title, seriesName, data, sx }: StreamPlotProps): React.JSX.Element {
  const chartOptions = useStreamChartOptions();
  const series = [{ name: seriesName, data }];
  return (
    <Card sx={sx}>
      <CardHeader title={title} />
      <CardContent>
        {data.length > 0 ? (
          <Chart height={280} options={chartOptions} series={series} type="line" width="100%" />
        ) : (
          <Typography variant="body2" color="text.secondary">
            No data for this stream.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

function useStreamChartOptions(): ApexOptions {
  const theme = useTheme();
  return {
    chart: { background: 'transparent', toolbar: { show: false } },
    colors: [theme.palette.primary.main, alpha(theme.palette.primary.main, 0.25)],
    dataLabels: { enabled: false },
    fill: { opacity: 1, type: 'solid' },
    grid: {
      borderColor: theme.palette.divider,
      strokeDashArray: 2,
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } },
    },
    legend: { show: false },
    stroke: { colors: [theme.palette.primary.main], show: true, width: 2 },
    theme: { mode: theme.palette.mode },
    xaxis: {
      type: 'numeric',
      title: { text: 'Time (s)' },
      labels: { style: { colors: theme.palette.text.secondary } },
    },
    yaxis: {
      labels: { style: { colors: theme.palette.text.secondary } },
      decimalsInFloat: 1,
    },
  };
}
