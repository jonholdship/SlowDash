'use client';
import * as React from 'react';
import { authClient } from '@/lib/auth/client';
import Avatar from '@mui/material/Avatar';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import { SxProps } from '@mui/material/styles';
import { ReactJSXElement } from '@emotion/react/types/jsx-namespace';
import Typography from '@mui/material/Typography';
import { ArrowDown as ArrowDownIcon } from '@phosphor-icons/react/dist/ssr/ArrowDown';
import { ArrowUp as ArrowUpIcon } from '@phosphor-icons/react/dist/ssr/ArrowUp';
import {Path as DistIcon} from '@phosphor-icons/react/dist/ssr/Path';
import {PersonSimpleRun as RunIcon} from '@phosphor-icons/react/dist/ssr/PersonSimpleRun';
import {SneakerMove as PaceIcon} from '@phosphor-icons/react/dist/ssr/SneakerMove';
import { getStats } from '@/api/api-call'; 
import Grid from '@mui/material/Unstable_Grid2';
import { Overview } from '@/types/overview';

export interface HeroProps {
  statName: string;
  diff?: string;
  trend: 'up' | 'down';
  sx?: SxProps;
  value: string;
  icon: ReactJSXElement;
}
// This is a client component that gets the auth token
export default function HeroStatsWrapper() {
  const [overview, setOverview] = React.useState<Overview | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    const getToken = async () => {
      const token = await authClient.getToken();
      const overviewData = await getStats(token);
      setOverview(overviewData);
      setIsLoading(false);
    };
    
    getToken();
  }, []);

  if (isLoading) {
    return <div>Loading stats...</div>;
  }

  return <HeroStatsServer overview={overview} />;
}




// This is a server component that uses the token
export async function HeroStatsServer({ overview }: { overview: Overview | null }) {
    if (!overview) {
      return <div>Authentication required</div>;
    }
  
    const distIcon = <DistIcon fontSize="var(--icon-fontSize-lg)" />;
    const runIcon = <RunIcon fontSize="var(--icon-fontSize-lg)" />;
    const paceIcon = <PaceIcon fontSize="var(--icon-fontSize-lg)" />;
  
    return (
      <Grid container spacing={3}>
        <Grid lg={4} sm={6} xs={12}>
          <HeroStat statName="Runs" diff={overview?.runs_change} trend={overview?.runs_trend} sx={{ height: '100%' }} value={overview?.runs} icon={runIcon} />
        </Grid>
        <Grid lg={4} sm={6} xs={12}>
          <HeroStat statName="Pace" diff={overview?.pace_change} trend={overview?.pace_trend} sx={{ height: '100%' }} value={overview?.pace} icon={paceIcon} />
        </Grid>
        <Grid lg={4} sm={6} xs={12}>
          <HeroStat statName="Distance" diff={overview?.distance_change} trend={overview?.distance_trend} sx={{ height: '100%' }} value={overview?.distance.toFixed(1)} icon={distIcon} />
        </Grid>
      </Grid>
    );
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