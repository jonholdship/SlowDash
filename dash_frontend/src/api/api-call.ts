'use strict';
import type { Overview } from '@/types/overview';
import type { Plots } from '@/types/plots';
import type { Run } from '@/types/run';
import type { ActivityResponse } from '@/types/activity';
import type { HrZonesResponse } from '@/types/hr-zones';
import type { UserSettings, UserSettingsUpdate } from '@/types/user-settings';


const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? '';

function ensureApiBaseUrl(): string {
	if (!API_BASE_URL) throw new Error('NEXT_PUBLIC_API_BASE_URL is not set');
	return API_BASE_URL.endsWith('/') ? API_BASE_URL : API_BASE_URL + '/';
}

export class AuthError extends Error {
	constructor(message = 'Unauthenticated') {
		super(message);
		this.name = 'AuthError';
	}
}

export async function apiRequest<T>(
	endpoint: string,
	//options: RequestInit = {}
): Promise<T> {
	const base = ensureApiBaseUrl();
	const url = new URL(endpoint, base);
	const response = await fetch(url, {
		method: 'GET',
		credentials: 'include',
	});

	if (response.status === 401) {
		throw new AuthError();
	}

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	const body = (await response.json()) as unknown;
	return body as T;
}

export async function getStats(): Promise<Overview> {
	return apiRequest<Overview>('activities/hero-stats');
}

export async function getPlots(): Promise<Plots> {
	return apiRequest<Plots>('activities/summary-plots');
}

export async function getActivity(activityId: number): Promise<ActivityResponse> {
	const endpoint = `activities/activity?activity_id=${encodeURIComponent(activityId)}`;
	return apiRequest<ActivityResponse>(endpoint);
}

export async function getUserSettings(): Promise<UserSettings> {
	return apiRequest<UserSettings>('user/user-settings');
}

export async function getHrZones(): Promise<HrZonesResponse> {
	return apiRequest<HrZonesResponse>('user/hr-zones');
}

export async function getRuns(): Promise<Run[]> {
	const data = await apiRequest<Run[]>('activities/runs');
	// Normalize start_date to JS Date objects (backend may return epoch seconds)
	const normalized = (data as unknown as Array<Record<string, unknown>>).map((r) => {
		const sd = (r.start_date as unknown) as number | string | undefined;
		let dateVal: Date | undefined;
		if (typeof sd === 'number') {
			// backend returns epoch seconds
			dateVal = new Date(sd * 1000);
		} else if (typeof sd === 'string') {
			dateVal = new Date(sd);
		}
		return {
			...(r as object),
			start_date: dateVal,
		} as unknown as Run;
	});
	return normalized;
}

export async function syncActivities(): Promise<void> {
	const base = ensureApiBaseUrl();
	const url = new URL('user/sync-activities', base);
	const response = await fetch(url.toString(), {
		method: 'POST',
		credentials: 'include',
	});

	if (response.status === 401) {
		throw new AuthError();
	}

	if (!response.ok) {
		throw new Error(`Sync activities failed: ${response.statusText}`);
	}
}

export async function setUserSettings(userSettings: UserSettingsUpdate): Promise<void> {
	const base = ensureApiBaseUrl();
	const url = new URL('user/user-settings', base);

	const response = await fetch(url.toString(), {
		method: 'POST',
		credentials: 'include',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(userSettings),
	});

	if (!response.ok) {
		throw new Error(`Update settings failed: ${response.statusText}`);
	}

	return;
}
