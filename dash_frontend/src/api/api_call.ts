'use server'
import {Overview} from '@/types/overview';
import {Plots} from '@/types/plots';
import {Run} from '@/types/run';
const {API_BASE_URL} = process.env;

export async function getTokenFromCode(code: string): Promise<string> {
	let endpoint = new URL("get-hero-stats",API_BASE_URL);
	fetch(endpoint,{body:`access_code:${code}`})
	.then(res => res.json()).then(res => console.log(res))
	return `${code}`
}

export async function getStats(token: string): Promise<Overview> {
	// For now, consider the data is stored on a static `users.json` file
	
	console.log(token)
	let endpoint = new URL("get-hero-stats",API_BASE_URL);
	return fetch(endpoint)
	  // the JSON body is taken from the response
	  .then(res => res.json())
	  .then(res => {
		// The response has an `any` type, so we need to cast
		// it to the `User` type, and return it from the promise
		return res as Overview
	  })
  }

export async function getPlots(token: string): Promise<Plots> {
	// For now, consider the data is stored on a static `users.json` file
	let endpoint = new URL('get-summary-plots' , API_BASE_URL);
	return fetch(endpoint)
	  // the JSON body is taken from the response
	  .then(res => res.json())
	  .then(res => {
		// The response has an `any` type, so we need to cast
		// it to the `User` type, and return it from the promise
		return res as Plots
	  })
  }

export async function getRuns(): Promise<Run[]> {
	let endpoint = new URL('run-list' , API_BASE_URL);
	return fetch(endpoint)
	// the JSON body is taken from the response
	.then(res => res.json())
	.then(res => {
	  // The response has an `any` type, so we need to cast
	  // it to the `User` type, and return it from the promise
	  return res as Run[]
	})
}
