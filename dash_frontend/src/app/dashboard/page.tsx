import * as React from 'react';
import type { Metadata } from 'next';
import Grid from '@mui/material/Unstable_Grid2';
import { config } from '@/config';
import HeroStats from '@/components/dashboard/overview/hero';
import RunPlotGrid from "@/components/dashboard/overview/run-plots"
import { Suspense } from 'react';
export const metadata = { title: `Overview | Dashboard | ${config.site.name}` } satisfies Metadata;



export default function Page(): React.JSX.Element {

  return (
    <Grid container spacing={3}>
    <Grid lg={12} sm={6} xs={12}>

    <Suspense>
      <HeroStats />
    </Suspense>
    <Suspense>
      <RunPlotGrid />
    </Suspense>
    </Grid>
    </Grid>
  );
}
