"use client";

import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';
import Divider from '@mui/material/Divider';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Unstable_Grid2';
import { AuthError, getHrZones, getUserSettings, setUserSettings } from '@/api/api-call';

function toDateInputValue(iso: string | null | undefined): string {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return d.toISOString().slice(0, 10);
}

export function HeartRateSettingsForm(): React.JSX.Element {
  const [birthday, setBirthday] = React.useState('');
  const [maxHrOverride, setMaxHrOverride] = React.useState('');
  const [highlight, setHighlight] = React.useState<string>('3');
  const [effectiveInfo, setEffectiveInfo] = React.useState<string>('');
  const [loading, setLoading] = React.useState(false);
  const [initialLoad, setInitialLoad] = React.useState(true);

  React.useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const [settings, zones] = await Promise.all([getUserSettings(), getHrZones()]);
        if (cancelled) return;
        setBirthday(toDateInputValue(settings.birthday));
        setMaxHrOverride(
          settings.max_hr_override !== null && settings.max_hr_override !== undefined
            ? String(settings.max_hr_override)
            : ''
        );
        setHighlight(
          settings.hr_zone_highlight !== null && settings.hr_zone_highlight !== undefined
            ? String(settings.hr_zone_highlight)
            : '3'
        );
        setEffectiveInfo(
          `Effective max HR: ${String(zones.effective_max_hr)} bpm (${zones.source}). Zones use this value.`
        );
      } catch (e) {
        if (e instanceof AuthError) return;
        console.error(e);
      } finally {
        if (!cancelled) setInitialLoad(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const trimmed = maxHrOverride.trim();
      let overrideVal: number | null = null;
      if (trimmed !== '') {
        const n = Number.parseFloat(trimmed);
        if (Number.isNaN(n)) {
          alert('Max HR override must be a number');
          return;
        }
        overrideVal = n;
      }
      await setUserSettings({
        birthday: birthday || null,
        max_hr_override: overrideVal,
        hr_zone_highlight: Number.parseInt(highlight || '3', 10),
      });
      const zones = await getHrZones();
      setEffectiveInfo(
        `Effective max HR: ${String(zones.effective_max_hr)} bpm (${zones.source}). Zones use this value.`
      );
      alert('Heart rate settings updated');
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Update failed');
    } finally {
      setLoading(false);
    }
  }

  if (initialLoad) {
    return (
      <Card>
        <CardHeader title="Heart rate zones" subheader="Loading…" />
      </Card>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card>
        <CardHeader
          subheader="Default max HR is 211 − 0.64 × age when birthday is set. Override below if you know your max from testing."
          title="Heart rate zones"
        />
        <Divider />
        <CardContent>
          <Stack spacing={2}>
            {effectiveInfo ? (
              <Typography variant="body2" color="text.secondary">
                {effectiveInfo}
              </Typography>
            ) : null}
            <Grid container spacing={3}>
              <Grid xs={12} sm={6}>
                <TextField
                  label="Birthday"
                  type="date"
                  value={birthday}
                  onChange={(e) => setBirthday(e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  fullWidth
                />
              </Grid>
              <Grid xs={12} sm={6}>
                <TextField
                  label="Max HR override (bpm)"
                  type="number"
                  value={maxHrOverride}
                  onChange={(e) => setMaxHrOverride(e.target.value)}
                  placeholder="Leave empty for formula"
                  fullWidth
                  inputProps={{ min: 120, max: 220, step: 1 }}
                />
              </Grid>
              <Grid xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="hr-zone-highlight-label">Highlight zone on charts</InputLabel>
                  <Select
                    labelId="hr-zone-highlight-label"
                    label="Highlight zone on charts"
                    value={highlight || '3'}
                    onChange={(e) => {
                      setHighlight(e.target.value);
                    }}
                  >
                    {[1, 2, 3, 4, 5].map((z) => (
                      <MenuItem key={z} value={String(z)}>
                        Zone {z}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Stack>
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
