'use client';

import * as React from 'react';

import { AuthError, syncActivities } from '@/api/api-call';
import { useUser } from '@/hooks/use-user';
import { logger } from '@/lib/default-logger';

function localCalendarDateString(): string {
  return new Date().toLocaleDateString('en-CA');
}

/** Dedupes overlapping effect runs (e.g. Strict Mode, dependency churn) for the same user+day. */
const dailyAutoSyncInflight = new Map<string, Promise<void>>();

export function DailyActivitiesSync(): null {
  const { user, isLoading } = useUser();
  const userId = user?.id;

  React.useEffect(() => {
    if (isLoading || userId === undefined) {
      return;
    }

    const today = localCalendarDateString();
    const storageKey = `activities_auto_sync_date_${userId}`;

    if (typeof window === 'undefined') {
      return;
    }

    if (window.localStorage.getItem(storageKey) === today) {
      return;
    }

    const dedupeKey = `${userId}:${today}`;
    let run = dailyAutoSyncInflight.get(dedupeKey);
    if (run) {
      return;
    }

    run = (async () => {
      try {
        await syncActivities();
        window.localStorage.setItem(storageKey, today);
      } catch (err) {
        if (err instanceof AuthError) {
          return;
        }
        logger.error(err);
      }
    })().finally(() => {
      if (dailyAutoSyncInflight.get(dedupeKey) === run) {
        dailyAutoSyncInflight.delete(dedupeKey);
      }
    });

    dailyAutoSyncInflight.set(dedupeKey, run);
  }, [userId, isLoading]);

  return null;
}
