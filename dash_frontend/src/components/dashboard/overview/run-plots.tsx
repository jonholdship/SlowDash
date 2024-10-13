'use client';

import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Divider from '@mui/material/Divider';
import { alpha, useTheme } from '@mui/material/styles';
import type { SxProps } from '@mui/material/styles';
import Grid from '@mui/material/Unstable_Grid2';
import { authClient } from '@/lib/auth/client';
import { ArrowClockwise as ArrowClockwiseIcon } from '@phosphor-icons/react/dist/ssr/ArrowClockwise';
import { ArrowRight as ArrowRightIcon } from '@phosphor-icons/react/dist/ssr/ArrowRight';
import type { ApexOptions } from 'apexcharts';
import { getPlots } from '@/api/api_call';
import { Chart } from '@/components/core/chart';
import { useEffect,useState } from 'react';

export interface PlotProps {
  chartSeries: { seriesName: string;data:{x:any,y:number}[] }[];
  sx?: SxProps;
}


export default function RunPlotGrid() {
  const [plotData, setPlotData] = useState({});
  useEffect(()=>{
    authClient.getToken()
    .then(token => getPlots(token))
    .then(plotData => setPlotData(plotData));
  });
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
        action={
          <Button color="inherit" size="small" startIcon={<ArrowClockwiseIcon fontSize="var(--icon-fontSize-md)" />}>
            Sync
          </Button>
        }
        title={chartSeries[0].seriesName}
      />
      <CardContent>
        <Chart height={350} options={chartOptions} series={chartSeries} type="line" width="100%" />
      </CardContent>
      <Divider />
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button color="inherit" endIcon={<ArrowRightIcon fontSize="var(--icon-fontSize-md)" />} size="small">
          Overview
        </Button>
      </CardActions>
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
      axisBorder: { color: theme.palette.divider, show: true },
      axisTicks: { color: theme.palette.divider, show: true },
      labels: { offsetY: 5, style: { colors: theme.palette.text.secondary } },
    },
    yaxis: {
      labels: {
        offsetX: -10,
        style: { colors: theme.palette.text.secondary },
      },
    },
  };
}
