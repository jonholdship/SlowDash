import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import type { SxProps } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import { ArrowDown as ArrowDownIcon } from '@phosphor-icons/react/dist/ssr/ArrowDown';
import { ArrowUp as ArrowUpIcon } from '@phosphor-icons/react/dist/ssr/ArrowUp';
import {Path as DistIcon} from '@phosphor-icons/react/dist/ssr/Path';
import {PersonSimpleRun as RunIcon} from '@phosphor-icons/react/dist/ssr/PersonSimpleRun';
import {SneakerMove as PaceIcon} from '@phosphor-icons/react/dist/ssr/SneakerMove';
import {getStats} from '@/api/api_call'
import Grid from '@mui/material/Unstable_Grid2';
import { ReactJSXElement } from '@emotion/react/types/jsx-namespace';
export interface HeroProps {
  statName: string;
  diff?: string;
  trend: 'up' | 'down';
  sx?: SxProps;
  value: string;
  icon: ReactJSXElement;
  
}


export default async function HeroStats() {

  const overview = await getStats();
  const distIcon = <DistIcon  fontSize="var(--icon-fontSize-lg)"/>
  const runIcon = <RunIcon   fontSize="var(--icon-fontSize-lg)"/>
  const paceIcon = <PaceIcon   fontSize="var(--icon-fontSize-lg)"/>

  return (
    <Grid container spacing={3}>
      <Grid lg={4} sm={6} xs={12}>
        <HeroStat statName = "Runs" diff = {overview?.runs_change} trend = {overview?.runs_trend} sx={{ height: '100%' }} value={overview?.runs} icon={runIcon}/>
      </Grid>
      <Grid lg={4} sm={6} xs={12}>
        <HeroStat statName = "Pace" diff = {overview?.pace_change} trend = {overview?.pace_trend} sx={{ height: '100%' }} value={overview?.pace} icon={paceIcon} />
      </Grid>
      <Grid lg={4} sm={6} xs={12}>
        <HeroStat statName = "Distance" diff = {overview?.distance_change} trend = {overview?.distance_trend} sx={{ height: '100%' }} value={overview?.distance} icon={distIcon}/>
      </Grid>
    </Grid>)
  ;
}

 function HeroStat({ statName, diff, trend, sx, value, icon }: HeroProps): React.JSX.Element {
  const TrendIcon = trend === 'up' ? ArrowUpIcon : ArrowDownIcon;
  const trendColor = trend === 'up' ? 'var(--mui-palette-success-main)' : 'var(--mui-palette-error-main)';

  return (
    <Card sx={sx}>
      <CardContent>
        <Stack spacing={3}>
          <Stack direction="row" sx={{ alignItems: 'flex-start', justifyContent: 'space-between' }} spacing={3}>
            <Stack spacing={1}>
              <Typography color="text.secondary" variant="overline">
                {statName}
              </Typography>
              <Typography variant="h4">{value}</Typography>
            </Stack>
            <Avatar sx={{ backgroundColor: 'var(--mui-palette-primary-main)', height: '56px', width: '56px' }}>
              {icon}
            </Avatar>
          </Stack>
          {diff ? (
            <Stack sx={{ alignItems: 'center' }} direction="row" spacing={2}>
              <Stack sx={{ alignItems: 'center' }} direction="row" spacing={0.5}>
                <TrendIcon color={trendColor} fontSize="var(--icon-fontSize-md)" />
                <Typography color={trendColor} variant="body2">
                  {diff}
                </Typography>
              </Stack>
              <Typography color="text.secondary" variant="caption">
                Since last month
              </Typography>
            </Stack>
          ) : null}
        </Stack>
      </CardContent>
    </Card>
  );
}
