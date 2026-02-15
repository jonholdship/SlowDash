export interface Run {
	id: string;
	name: string;
	start_date: Date;
	distance: number;
	pace: string;
	average_hr?: string;
	polyline?: string;
  }