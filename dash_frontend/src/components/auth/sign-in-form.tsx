'use client';

import * as React from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

export interface SignInProps {
  stravaAuth: string;
}

export function SignInForm({ stravaAuth }: SignInProps): React.JSX.Element {
  return (
    <Card elevation={1}>
      <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
        <Stack spacing={3}>
          <Stack spacing={1.5}>
            <Typography variant="h5">Sign in</Typography>
            <Typography color="text.secondary" variant="body2">
              SlowDash requires a Strava account. Use the button below sign in with your Strava account.
            </Typography>
            <Typography color="text.secondary" variant="body2">
              You will be asked to allow read-only access so SlowDash can read your activities. Data is stored on our
              servers and can be removed at any time via the Settings page.
            </Typography>
          </Stack>
          <Box sx={{ display: 'flex', justifyContent: 'center', pt: 0.5 }}>
            <Box
              component="a"
              href={stravaAuth}
              rel="noopener noreferrer"
              sx={{
                borderRadius: 1,
                display: 'inline-block',
                lineHeight: 0,
                transition: 'opacity 0.2s ease',
                '&:hover': { opacity: 0.92 },
                '&:focus-visible': {
                  outline: '2px solid',
                  outlineColor: 'primary.main',
                  outlineOffset: 3,
                },
              }}
            >
              <Box
                alt="Connect with Strava"
                component="img"
                src="/assets/btn_connect_strava.png"
                sx={{ display: 'block', height: 'auto', maxWidth: '100%', width: 193 }}
              />
            </Box>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}
