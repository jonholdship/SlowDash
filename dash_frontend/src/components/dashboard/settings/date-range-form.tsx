"use client";

import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Unstable_Grid2';
import { authClient } from '@/lib/auth/client';
import { setUserSettings } from '@/api/api-call';

export function DateRangeForm(): React.JSX.Element {
  const [startDate, setStartDate] = React.useState<string>('');
  const [endDate, setEndDate] = React.useState<string>('');
  const [loading, setLoading] = React.useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const token = await authClient.getToken();
      if (!token) throw new Error('Not authenticated');

      await setUserSettings(
        {start_date: startDate, end_date: endDate || null },
        token
      );

      // Minimal feedback
      alert('Settings updated');
    } catch (err) {
      // Minimal error handling
      alert(err instanceof Error ? err.message : 'Update failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card>
        <CardHeader subheader="Set training date range" title="Date Range" />
        <Divider />
        <CardContent>
          <Grid container spacing={3}>
            <Grid xs={12} sm={6}>
              <Stack spacing={1}>
                <TextField
                  label="Start Date"
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  required
                />
              </Stack>
            </Grid>
            <Grid xs={12} sm={6}>
              <Stack spacing={1}>
                <TextField
                  label="End Date"
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  InputLabelProps={{ shrink: true }}
                />
              </Stack>
            </Grid>
          </Grid>
        </CardContent>
        <Divider />
        <CardActions sx={{ justifyContent: 'flex-end' }}>
          <Button type="submit" variant="contained" disabled={loading}>
            Save
          </Button>
        </CardActions>
      </Card>
    </form>
  );
}
