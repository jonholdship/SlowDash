export interface HrZoneBand {
	id: number;
	label: string;
	min_bpm: number;
	max_bpm: number;
}

export interface HrZonesResponse {
	effective_max_hr: number;
	source: 'override' | 'formula' | 'config_default';
	zones: HrZoneBand[];
}
