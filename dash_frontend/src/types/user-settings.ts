export interface UserSettings {
	athlete_id: number;
	start_date: string | null;
	end_date: string | null;
	birthday: string | null;
	max_hr_override: number | null;
	hr_zone_highlight: number | null;
}

export type UserSettingsUpdate = Partial<{
	start_date: string;
	end_date: string | null;
	birthday: string | null;
	max_hr_override: number | null;
	hr_zone_highlight: number | null;
}>;
