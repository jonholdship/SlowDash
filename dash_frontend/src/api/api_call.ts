'use server';
import { Overview } from '@/types/overview';
import { Plots } from '@/types/plots';
import { Run } from '@/types/run';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
console.log({API_BASE_URL});

export async function apiRequest<T>(
	endpoint: string,
	token: string | null,
	options: RequestInit = {}
): Promise<T> {
	if (!token) {
		throw new Error('No authentication token available');
	}

	const url = new URL(endpoint, API_BASE_URL);
	url.searchParams.append("token", token);

	// // Include authorization header with JWT
	// const headers = {
	// 	...options.headers,
	// 	'Authorization': `Bearer ${token}`,
	// 	'Content-Type': 'application/json',
	// };

	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`API request failed: ${response.statusText}`);
	}

	return response.json();
}

export async function getTokenFromCode(code: string): Promise<string> {
	const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

	let endpoint = new URL("login", API_BASE_URL);
	endpoint.searchParams.append("access_code", code);
	const response = await fetch(endpoint);
	console.log(response);
	const data = await response.json();
	console.log(data);
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
