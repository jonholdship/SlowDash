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
	token: string | null,
	//options: RequestInit = {}
): Promise<T> {
	if (!token) throw new Error('No authentication token available');

	const base = ensureApiBaseUrl();
	const url = new URL(endpoint, base);
	url.searchParams.append('token', token);

	// const mergedOptions: RequestInit = {
	// 	...options,
	// 	headers: {
	// 		...(options.headers as Record<string, string> | undefined),
	// 	},
	// };

	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	const body = (await response.json()) as unknown;
	return body as T;
}

export async function getTokenFromCode(code: string): Promise<string> {
	const base = ensureApiBaseUrl();
	const endpoint = new URL('login', base);
	endpoint.searchParams.append('access_code', code);
	const response = await fetch(endpoint.toString());
	if (!response.ok) throw new Error(`Login request failed: ${response.statusText}`);
	const data = (await response.json()) as { token: string };
	return data.token;
}

export async function getStats(token: string | null): Promise<Overview> {
	return apiRequest<Overview>('hero-stats', token);
}

export async function getPlots(token: string | null): Promise<Plots> {
	return apiRequest<Plots>('summary-plots', token);
}

export async function getRuns(token: string | null): Promise<Run[]> {
	return apiRequest<Run[]>('runs', token);
}

export async function setUserSettings(
	userSettings: {start_date: string; end_date?: string | null },
	token: string | null
): Promise<void> {
	if (!token) throw new Error('No authentication token available');

	const base = ensureApiBaseUrl();
	const url = new URL('user-settings', base);
	url.searchParams.append('token', token);

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
