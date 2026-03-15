'use client';

import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import { alpha, useTheme } from '@mui/material/styles';
import type { SxProps } from '@mui/material/styles';
import Grid from '@mui/material/Unstable_Grid2';
import type { ApexOptions } from 'apexcharts';
import { AuthError, getPlots } from '@/api/api-call';
import { Chart } from '@/components/core/chart';
import { useEffect, useState } from 'react';

export interface PlotProps {
  chartSeries: { seriesName: string; data: { x: any, y: number }[] }[];
  sx?: SxProps;
}

// This is a client component that gets the auth token
export default function RunPlotWrapper() {
  const [isLoading, setIsLoading] = useState(true);
  const [plotData, setPlotData] = useState<any>(null);

  useEffect(() => {
    const loadPlots = async () => {
      try {
        const plots = await getPlots();
        setPlotData(plots);
      } catch (err) {
        if (err instanceof AuthError) {
          // Treat as unauthenticated – server component will show an auth message
          setPlotData(null);
          return;
        }
        console.error('Failed to load plots', err);
        setPlotData(null);
      } finally {
        setIsLoading(false);
      }
    };

    loadPlots();
  }, []);

  if (isLoading) {
    return <div>Loading plots...</div>;
  }

  return <RunPlotGridServer plotData={plotData} />;
}

// This is a server component that uses the token
async function RunPlotGridServer({ plotData }: { plotData: any }) {
  if (!plotData) {
    return <div>Authentication required</div>;
  }

  
  return (
    <Grid container spacing={3}>
      <Grid lg={6} sm={6} xs={12}>
        <RunPlot chartSeries={[{seriesName:"Pace",data:plotData.pace_plot}]}/>
      </Grid>
      <Grid lg={6} sm={6} xs={12}>
        <RunPlot chartSeries={[{seriesName:"HR",data:plotData.hr_plot}]}/>
      </Grid>
    </Grid>
  );
}

function RunPlot({ chartSeries, sx }: PlotProps): React.JSX.Element {
  const chartOptions = useChartOptions();
  console.log({chartSeries});
   return (
    <Card sx={sx}>
      <CardHeader
        title={chartSeries[0].seriesName}
      />
      <CardContent>
        <Chart height={400} options={chartOptions} series={chartSeries} type="line" width="100%" />
      </CardContent>
    </Card>
  );
}

function useChartOptions(): ApexOptions {
  const theme = useTheme();

  return {
    chart: { background: 'transparent', stacked: false, toolbar: { show: false } },
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
