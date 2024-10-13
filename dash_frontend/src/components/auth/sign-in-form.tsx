'use client';

import * as React from 'react';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';


export interface SignInProps{
  stravaAuth:string;
}
export function SignInForm({stravaAuth}: SignInProps): React.JSX.Element {
  return (
    <Stack spacing={4}>
      <Stack spacing={1}>
        <Typography variant="h4">Sign in</Typography>
        <Typography color="text.secondary" variant="body2">
          Slow Dash requires a Strava account. Please click below to be taken to Strava for authentication.
        </Typography>
        <Typography color="text.secondary" variant="body2">
          You will be asked to allow read-only permissions for Slow Dash to access your Strava data. A copy will be stored on our servers and can be deleted at any time through the settings page.
        </Typography>
      </Stack>
      <button onClick={() => {
      window.open(stravaAuth, '_self');
    }}
  >login with strava</button>
    </Stack>
  );
}
