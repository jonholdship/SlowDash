'use server';
import type { Overview } from '@/types/overview';
import type { Plots } from '@/types/plots';
import type { Run } from '@/types/run';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? '';

function ensureApiBaseUrl(): string {
	if (!API_BASE_URL) throw new Error('NEXT_PUBLIC_API_BASE_URL is not set');
	return API_BASE_URL.endsWith('/') ? API_BASE_URL : API_BASE_URL + '/';
}

export async function apiRequest<T>(
	endpoint: string,
	token: string | Record<string, unknown> | null,
	//options: RequestInit = {}
): Promise<T> {
	if (!token) throw new Error('No authentication token available');

	const base = ensureApiBaseUrl();
	const url = new URL(endpoint, base);
	const tokenValue = JSON.stringify(token);
	url.searchParams.append('token', tokenValue);


	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	const body = (await response.json()) as unknown;
	return body as T;
}

export type AccessInfo = { access_token: string; refresh_token?: string; expires_at?: number };

export async function getTokenFromCode(code: string): Promise<AccessInfo> {
	const base = ensureApiBaseUrl();
	const endpoint = new URL('login', base);
	endpoint.searchParams.append('access_code', code);
	const response = await fetch(endpoint.toString());
	if (!response.ok) throw new Error(`Login request failed: ${response.statusText}`);
	const data = (await response.json()) as AccessInfo;
	return data;
}

export async function getStats(token: AccessInfo  | null): Promise<Overview> {
	return apiRequest<Overview>('hero-stats', token);
}

export async function getPlots(token: AccessInfo | null): Promise<Plots> {
	return apiRequest<Plots>('summary-plots', token);
}

export async function getRuns(token: AccessInfo | null): Promise<Run[]> {
	const data = await apiRequest<Run[]>('runs', token);
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

export async function setUserSettings(
	userSettings: {start_date: string; end_date?: string | null },
	token: AccessInfo | null
): Promise<void> {
	if (!token) throw new Error('No authentication token available');

	const base = ensureApiBaseUrl();
	const url = new URL('user-settings', base);
	const tokenValue = JSON.stringify(token);
	url.searchParams.append('token', tokenValue);

	const response = await fetch(url.toString(), {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(userSettings),
	});

	if (!response.ok) {
		throw new Error(`Update settings failed: ${response.statusText}`);
	}

	return;
}
