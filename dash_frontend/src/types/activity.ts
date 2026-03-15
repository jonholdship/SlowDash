export interface ActivityDetail {
	name: string | null;
	polyline: string | null;
	description: string;
	start_date: string | null;
	calories: number | null;
}

export interface ActivityStreams {
	time?: number[];
	distance?: number[];
	heartrate?: number[];
	pace?: number[];
	altitude?: number[];
	[key: string]: number[] | undefined;
}

export interface ActivityResponse {
	activity: ActivityDetail;
	streams: ActivityStreams;
}